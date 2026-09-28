const Database = require('better-sqlite3');
const path = require('path');

const db = new Database(path.join(__dirname, 'upi.db'));

// Enable WAL mode for better concurrency
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS accounts (
    vpa TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 10000.00
  );

  CREATE TABLE IF NOT EXISTS transactions (
    txn_id TEXT PRIMARY KEY,
    payer_vpa TEXT NOT NULL,
    payee_vpa TEXT NOT NULL,
    amount REAL NOT NULL,
    note TEXT,
    status TEXT NOT NULL DEFAULT 'PENDING',
    type TEXT NOT NULL DEFAULT 'PAYMENT',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (payer_vpa) REFERENCES accounts(vpa),
    FOREIGN KEY (payee_vpa) REFERENCES accounts(vpa)
  );
`);

module.exports = db;
