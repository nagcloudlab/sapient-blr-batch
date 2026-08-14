# Module 12: Database SQL -- Lab Setup

## Prerequisites

- MySQL 8.0 or higher (`mysql --version` to confirm)
- MySQL client (CLI) or MySQL Workbench

## Running the Starter Code

```bash
# Load the schema
mysql -u root -p < Labs/starter-code/schema.sql

# Load the seed data
mysql -u root -p < Labs/starter-code/seed-data.sql
```

Both files must succeed before running the report queries. Seed data depends on the schema existing.

## Verifying Your Fixes

Open the MySQL client and run the queries in `starter-code/reports.sql` one by one:

```bash
mysql -u root -p foodexpress
```

Then paste each query from `reports.sql` into the prompt. Compare results against the expected output
table in `lab-exercises.md`. Some queries will return wrong counts or crash -- those are the bugs.

## Expected Behavior

- Schema loads with no errors (no duplicate table or missing FK errors).
- Seed data inserts without constraint violations.
- Report queries return the correct row counts and aggregate values shown in `lab-exercises.md`.
- No queries crash with syntax errors after fixes are applied.
- All JOIN queries return the expected number of rows (no unintended Cartesian products).

## Troubleshooting

**`ERROR 1049 (42000): Unknown database`:** The schema.sql file must create and `USE` the database.
Run it again and check the first few lines contain `CREATE DATABASE IF NOT EXISTS foodexpress;`.

**`ERROR 1292: Incorrect date value`:** Date literals must be in `YYYY-MM-DD` format. Fix any seed
data rows using `DD/MM/YYYY` or other non-standard formats.
