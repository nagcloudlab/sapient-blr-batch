const express = require('express');
const path = require('path');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// --- Helpers ---
const VPA_REGEX = /^[a-zA-Z0-9._]{3,}@[a-zA-Z]{2,}$/;

function validateVpa(vpa) {
  return typeof vpa === 'string' && VPA_REGEX.test(vpa);
}

function validateAmount(amount) {
  if (amount === undefined || amount === null || amount === '') return false;
  const num = Number(amount);
  if (!Number.isFinite(num) || num <= 0 || num > 100000) return false;
  if (Math.round(num * 100) / 100 !== num) return false;
  return true;
}

function generateTxnId() {
  return 'TXN' + Date.now() + String(Math.floor(1000 + Math.random() * 9000));
}

// --- Prepared Statements ---
const stmts = {
  getAccount: db.prepare('SELECT * FROM accounts WHERE vpa = ?'),
  getTxn: db.prepare('SELECT * FROM transactions WHERE txn_id = ?'),
  getRecentTxns: db.prepare('SELECT * FROM transactions ORDER BY created_at DESC LIMIT 20'),
  insertTxn: db.prepare(`INSERT INTO transactions (txn_id, payer_vpa, payee_vpa, amount, note, status, type) VALUES (?, ?, ?, ?, ?, 'PENDING', ?)`),
  getAllAccounts: db.prepare('SELECT * FROM accounts ORDER BY vpa'),
  updateTxnStatus: db.prepare(`UPDATE transactions SET status = ?, updated_at = datetime('now') WHERE txn_id = ?`),
  debit: db.prepare('UPDATE accounts SET balance = balance - ? WHERE vpa = ?'),
  credit: db.prepare('UPDATE accounts SET balance = balance + ? WHERE vpa = ?'),
};

// --- Routes ---

// Dashboard
// --- Page Routes (SSR) ---
const pages = ['home', 'pay', 'balance', 'transactions', 'history'];

function renderPage(res, page) {
  const transactions = stmts.getRecentTxns.all();
  const accounts = stmts.getAllAccounts.all();
  res.render('dashboard', { transactions, accounts, page });
}

app.get('/', (req, res) => renderPage(res, 'home'));
app.get('/pay', (req, res) => renderPage(res, 'pay'));
app.get('/balance', (req, res) => renderPage(res, 'balance'));
app.get('/transactions', (req, res) => renderPage(res, 'transactions'));
app.get('/history', (req, res) => renderPage(res, 'history'));

// POST /api/pay
app.post('/api/pay', (req, res) => {
  const { payer_vpa, payee_vpa, amount, note } = req.body;

  if (!payer_vpa) return res.status(400).json({ error: 'payer_vpa is required' });
  if (!payee_vpa) return res.status(400).json({ error: 'payee_vpa is required' });
  if (amount === undefined || amount === null) return res.status(400).json({ error: 'amount is required' });
  if (!validateVpa(payer_vpa)) return res.status(400).json({ error: 'Invalid payer VPA format (expected: username@bankname)' });
  if (!validateVpa(payee_vpa)) return res.status(400).json({ error: 'Invalid payee VPA format (expected: username@bankname)' });
  if (payer_vpa === payee_vpa) return res.status(400).json({ error: 'Payer and payee cannot be the same' });
  if (!validateAmount(amount)) return res.status(400).json({ error: 'Invalid amount (must be > 0, <= 100000, max 2 decimals)' });

  const payer = stmts.getAccount.get(payer_vpa);
  if (!payer) return res.status(404).json({ error: `Payer VPA not found: ${payer_vpa}` });
  const payee = stmts.getAccount.get(payee_vpa);
  if (!payee) return res.status(404).json({ error: `Payee VPA not found: ${payee_vpa}` });

  const amt = Number(amount);
  const txnId = generateTxnId();

  const initiate = db.transaction(() => {
    const freshPayer = stmts.getAccount.get(payer_vpa);
    if (freshPayer.balance < amt) return null;
    stmts.debit.run(amt, payer_vpa);
    const safeNote = note ? String(note).slice(0, 100) : '';
    stmts.insertTxn.run(txnId, payer_vpa, payee_vpa, amt, safeNote, 'PAYMENT');
    return txnId;
  });

  const result = initiate();
  if (!result) return res.status(400).json({ error: 'Insufficient balance' });

  res.status(201).json({ txn_id: txnId, status: 'PENDING', message: 'Transaction initiated, processing...' });

  // Simulate 2-second bank processing delay
  setTimeout(() => {
    try {
      stmts.updateTxnStatus.run('PROCESSING', txnId);
      const success = Math.random() < 0.8; // 80% success rate

      if (success) {
        db.transaction(() => {
          stmts.credit.run(amt, payee_vpa);
          stmts.updateTxnStatus.run('SUCCESS', txnId);
        })();
      } else {
        db.transaction(() => {
          stmts.credit.run(amt, payer_vpa); // Refund on failure
          stmts.updateTxnStatus.run('FAILED', txnId);
        })();
      }
    } catch (err) {
      console.error(`Error processing txn ${txnId}:`, err);
      try {
        stmts.credit.run(amt, payer_vpa);
        stmts.updateTxnStatus.run('FAILED', txnId);
      } catch (e) { console.error(`Rollback failed for ${txnId}:`, e); }
    }
  }, 2000);
});

// GET /api/txn/:txnId
app.get('/api/txn/:txnId', (req, res) => {
  const txn = stmts.getTxn.get(req.params.txnId);
  if (!txn) return res.status(404).json({ error: 'Transaction not found' });
  res.json(txn);
});

// POST /api/refund/:txnId
app.post('/api/refund/:txnId', (req, res) => {
  const refundTxnId = generateTxnId();

  const processRefund = db.transaction(() => {
    const txn = stmts.getTxn.get(req.params.txnId);
    if (!txn) return { error: 'Transaction not found', status: 404 };
    if (txn.type === 'REFUND') return { error: 'Cannot refund a refund transaction', status: 400 };
    if (txn.status !== 'SUCCESS') return { error: `Cannot refund transaction with status: ${txn.status}`, status: 400 };

    const payee = stmts.getAccount.get(txn.payee_vpa);
    if (!payee || payee.balance < txn.amount) return { error: 'Payee has insufficient balance for refund', status: 400 };

    stmts.credit.run(txn.amount, txn.payer_vpa);
    stmts.debit.run(txn.amount, txn.payee_vpa);
    stmts.updateTxnStatus.run('REFUNDED', txn.txn_id);
    stmts.insertTxn.run(refundTxnId, txn.payee_vpa, txn.payer_vpa, txn.amount, `Refund for ${txn.txn_id}`, 'REFUND');
    stmts.updateTxnStatus.run('SUCCESS', refundTxnId);

    return { data: { refund_txn_id: refundTxnId, original_txn_id: txn.txn_id, amount: txn.amount, status: 'SUCCESS', message: 'Refund processed successfully' } };
  });

  const result = processRefund();
  if (result.error) return res.status(result.status).json({ error: result.error });
  res.status(201).json(result.data);
});

// GET /api/balance/:vpa
app.get('/api/balance/:vpa', (req, res) => {
  const account = stmts.getAccount.get(req.params.vpa);
  if (!account) return res.status(404).json({ error: 'VPA not found' });
  res.json({ vpa: account.vpa, name: account.name, balance: account.balance });
});

// GET /api/transactions
app.get('/api/transactions', (_req, res) => {
  res.json(stmts.getRecentTxns.all());
});

// --- RAG Search (proxied to ChromaDB Python server on port 5100) ---
const http = require('http');

const RAG_SERVER = 'http://localhost:5100';

// RAG search page
app.get('/rag', (_req, res) => {
  res.render('rag');
});

// RAG search API -- proxy to ChromaDB Python server
app.get('/api/rag/search', (req, res) => {
  const q = req.query.q;
  if (!q) return res.status(400).json({ error: 'q parameter required' });

  const url = `${RAG_SERVER}/api/rag/search?q=${encodeURIComponent(q)}`;

  http.get(url, (proxyRes) => {
    let data = '';
    proxyRes.on('data', chunk => { data += chunk; });
    proxyRes.on('end', () => {
      try {
        res.json(JSON.parse(data));
      } catch (e) {
        res.status(500).json({ error: 'RAG server returned invalid response' });
      }
    });
  }).on('error', (err) => {
    console.error('RAG server error:', err.message);
    res.status(503).json({
      error: 'RAG server not available. Start it with: python3 rag-server.py',
      hint: 'The ChromaDB vector database server needs to be running on port 5100',
    });
  });
});

// RAG status
app.get('/api/rag/status', (req, res) => {
  http.get(`${RAG_SERVER}/api/rag/status`, (proxyRes) => {
    let data = '';
    proxyRes.on('data', chunk => { data += chunk; });
    proxyRes.on('end', () => {
      try { res.json(JSON.parse(data)); } catch { res.status(500).json({ error: 'Invalid response' }); }
    });
  }).on('error', () => {
    res.status(503).json({ error: 'RAG server not running' });
  });
});

// Export for testing; only listen when run directly
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`UPI Service running at http://localhost:${PORT}`);
  });
}

module.exports = app;
