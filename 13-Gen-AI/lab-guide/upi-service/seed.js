const db = require('./db');

const accounts = [
  { vpa: 'rahul@ybl', name: 'Rahul Sharma' },
  { vpa: 'priya@paytm', name: 'Priya Patel' },
  { vpa: 'amit@okicici', name: 'Amit Singh' },
  { vpa: 'sneha@axl', name: 'Sneha Reddy' },
  { vpa: 'test@upi', name: 'Test User' },
];

const insert = db.prepare(
  'INSERT OR REPLACE INTO accounts (vpa, name, balance) VALUES (?, ?, 10000.00)'
);

const seedAll = db.transaction(() => {
  for (const acc of accounts) {
    insert.run(acc.vpa, acc.name);
  }
});

seedAll();
console.log('Seeded 5 accounts with Rs 10,000 each:');
accounts.forEach((a) => console.log(`  ${a.vpa} - ${a.name}`));
