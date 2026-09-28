const express = require('express');
const path = require('path');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
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
  // Max 2 decimal places — use math instead of string parsing to avoid scientific notation bypass
  if (Math.round(num * 100) / 100 !== num) return false;
  return true;
}

function generateTxnId() {
  const ts = Date.now();
  const rand = String(Math.floor(1000 + Math.random() * 9000));
  return `TXN${ts}${rand}`;
}

// --- Prepared Statements ---

const stmts = {
  getAccount: db.prepare('SELECT * FROM accounts WHERE vpa = ?'),
  getTxn: db.prepare('SELECT * FROM transactions WHERE txn_id = ?'),
  getRecentTxns: db.prepare(
    'SELECT * FROM transactions ORDER BY created_at DESC LIMIT 20'
  ),
  insertTxn: db.prepare(`
    INSERT INTO transactions (txn_id, payer_vpa, payee_vpa, amount, note, status, type)
    VALUES (?, ?, ?, ?, ?, 'PENDING', ?)
  `),
  getAllAccounts: db.prepare('SELECT * FROM accounts ORDER BY vpa'),
  updateTxnStatus: db.prepare(`
    UPDATE transactions SET status = ?, updated_at = datetime('now') WHERE txn_id = ?
  `),
  debit: db.prepare('UPDATE accounts SET balance = balance - ? WHERE vpa = ?'),
  credit: db.prepare('UPDATE accounts SET balance = balance + ? WHERE vpa = ?'),
};

// --- Routes ---

// Dashboard
app.get('/', (_req, res) => {
  const transactions = stmts.getRecentTxns.all();
  const accounts = stmts.getAllAccounts.all();
  res.render('dashboard', { transactions, accounts });
});

// POST /api/pay -- Initiate a UPI transaction
app.post('/api/pay', (req, res) => {
  const { payer_vpa, payee_vpa, amount, note } = req.body;

  // Check required fields
  if (!payer_vpa) return res.status(400).json({ error: 'payer_vpa is required' });
  if (!payee_vpa) return res.status(400).json({ error: 'payee_vpa is required' });
  if (amount === undefined || amount === null) return res.status(400).json({ error: 'amount is required' });

  // Validate VPAs
  if (!validateVpa(payer_vpa)) {
    return res.status(400).json({ error: 'Invalid payer VPA format (expected: username@bankname)' });
  }
  if (!validateVpa(payee_vpa)) {
    return res.status(400).json({ error: 'Invalid payee VPA format (expected: username@bankname)' });
  }
  if (payer_vpa === payee_vpa) {
    return res.status(400).json({ error: 'Payer and payee cannot be the same' });
  }

  // Validate amount
  if (!validateAmount(amount)) {
    return res.status(400).json({ error: 'Invalid amount (must be > 0, <= 100000, max 2 decimals)' });
  }

  // Check accounts exist
  const payer = stmts.getAccount.get(payer_vpa);
  if (!payer) return res.status(404).json({ error: `Payer VPA not found: ${payer_vpa}` });

  const payee = stmts.getAccount.get(payee_vpa);
  if (!payee) return res.status(404).json({ error: `Payee VPA not found: ${payee_vpa}` });

  // Check sufficient balance and debit immediately (atomically) to prevent race condition
  const amt = Number(amount);
  const txnId = generateTxnId();

  const initiate = db.transaction(() => {
    // Re-read balance inside transaction to prevent race condition
    const freshPayer = stmts.getAccount.get(payer_vpa);
    if (freshPayer.balance < amt) return null;
    stmts.debit.run(amt, payer_vpa);
    const safeNote = note ? String(note).slice(0, 100) : '';
    stmts.insertTxn.run(txnId, payer_vpa, payee_vpa, amt, safeNote, 'PAYMENT');
    return txnId;
  });

  const result = initiate();
  if (!result) {
    return res.status(400).json({ error: 'Insufficient balance' });
  }

  // Respond immediately with PENDING
  res.status(201).json({
    txn_id: txnId,
    status: 'PENDING',
    message: 'Transaction initiated, processing...',
  });

  // Simulate bank processing with 2-second delay
  setTimeout(() => {
    try {
      stmts.updateTxnStatus.run('PROCESSING', txnId);

      // 80% success, 20% failure
      const success = Math.random() < 0.8;

      if (success) {
        const settle = db.transaction(() => {
          stmts.credit.run(amt, payee_vpa);
          stmts.updateTxnStatus.run('SUCCESS', txnId);
        });
        settle();
      } else {
        // Refund the debited amount on failure
        const rollback = db.transaction(() => {
          stmts.credit.run(amt, payer_vpa);
          stmts.updateTxnStatus.run('FAILED', txnId);
        });
        rollback();
      }
    } catch (err) {
      console.error(`Error processing txn ${txnId}:`, err);
      // Attempt to refund and mark failed
      try {
        stmts.credit.run(amt, payer_vpa);
        stmts.updateTxnStatus.run('FAILED', txnId);
      } catch (rollbackErr) {
        console.error(`Rollback failed for txn ${txnId}:`, rollbackErr);
      }
    }
  }, 2000);
});

// GET /api/txn/:txnId -- Check transaction status
app.get('/api/txn/:txnId', (req, res) => {
  const txn = stmts.getTxn.get(req.params.txnId);
  if (!txn) return res.status(404).json({ error: 'Transaction not found' });
  res.json(txn);
});

// POST /api/refund/:txnId -- Initiate refund
app.post('/api/refund/:txnId', (req, res) => {
  const refundTxnId = generateTxnId();

  const processRefund = db.transaction(() => {
    // Re-read inside transaction to prevent double-refund race condition
    const txn = stmts.getTxn.get(req.params.txnId);
    if (!txn) return { error: 'Transaction not found', status: 404 };

    // Prevent refunding a refund transaction
    if (txn.type === 'REFUND') {
      return { error: 'Cannot refund a refund transaction', status: 400 };
    }

    if (txn.status !== 'SUCCESS') {
      return { error: `Cannot refund transaction with status: ${txn.status}`, status: 400 };
    }

    // Verify both accounts still exist
    const payer = stmts.getAccount.get(txn.payer_vpa);
    if (!payer) return { error: `Payer account no longer exists: ${txn.payer_vpa}`, status: 400 };

    const payee = stmts.getAccount.get(txn.payee_vpa);
    if (!payee) return { error: `Payee account no longer exists: ${txn.payee_vpa}`, status: 400 };

    // Check payee has sufficient balance for refund
    if (payee.balance < txn.amount) {
      return { error: 'Payee has insufficient balance for refund', status: 400 };
    }

    // Reverse the money
    stmts.credit.run(txn.amount, txn.payer_vpa);
    stmts.debit.run(txn.amount, txn.payee_vpa);
    // Mark original as refunded
    stmts.updateTxnStatus.run('REFUNDED', txn.txn_id);
    // Create refund transaction record
    stmts.insertTxn.run(refundTxnId, txn.payee_vpa, txn.payer_vpa, txn.amount, `Refund for ${txn.txn_id}`, 'REFUND');
    stmts.updateTxnStatus.run('SUCCESS', refundTxnId);

    return { data: { refund_txn_id: refundTxnId, original_txn_id: txn.txn_id, amount: txn.amount, status: 'SUCCESS', message: 'Refund processed successfully' } };
  });

  const result = processRefund();

  if (result.error) {
    return res.status(result.status).json({ error: result.error });
  }

  res.status(201).json(result.data);
});

// GET /api/balance/:vpa -- Check mock balance
app.get('/api/balance/:vpa', (req, res) => {
  const account = stmts.getAccount.get(req.params.vpa);
  if (!account) return res.status(404).json({ error: 'VPA not found' });
  res.json({ vpa: account.vpa, name: account.name, balance: account.balance });
});

// Start server
app.listen(PORT, () => {
  console.log(`UPI Service running at http://localhost:${PORT}`);
});
