# Module 09 Solutions -- TRAINER ONLY

## Bug #1: Missing / Wrong require() Calls

**Root Cause:** `server.js` uses `require('fs')` but the variable is named `filesystem` and never used. `utils/logger.js` uses `require('colours')` instead of `require('chalk')` (wrong package name). Another file uses `require('./config')` but the file is `config.json` (missing extension for JSON).

**Fix:**
```javascript
// server.js
const fs = require('fs');  // consistent variable name

// utils/logger.js
const chalk = require('chalk');  // correct package name

// config loader
const config = require('./config.json');  // include .json extension
```

## Bug #2: Callback Hell in Menu Loader

**Root Cause:** `loadMenu()` nests `fs.readFile` inside `fs.access` inside `fs.readdir` -- three levels deep with duplicated error handling. Errors at inner levels are swallowed.

**Fix:**
```javascript
// Refactor to async/await
async function loadMenu(restaurantId) {
  const menuPath = path.join(__dirname, '..', 'data', 'menus', `${restaurantId}.json`);
  await fs.promises.access(menuPath);
  const data = await fs.promises.readFile(menuPath, 'utf-8');
  return JSON.parse(data);
}
```

## Bug #3: Unhandled Promise Rejection

**Root Cause:** `restaurantService.loadAll()` returns a Promise but the caller does not attach `.catch()`. When the data file is missing, the rejection is unhandled and crashes the process with `UnhandledPromiseRejectionWarning`.

**Fix:**
```javascript
// Option 1: Add .catch()
restaurantService.loadAll()
  .then(data => console.log(`Loaded ${data.length} restaurants`))
  .catch(err => console.error('Failed to load restaurants:', err.message));

// Option 2: wrap in try/catch with async/await
try {
  const data = await restaurantService.loadAll();
} catch (err) {
  console.error('Failed to load restaurants:', err.message);
}
```

## Bug #4: Hardcoded Path Separator

**Root Cause:** File paths use `'data\\menus\\' + id + '.json'` with Windows backslashes. On the Linux deployment server, this resolves to a single directory name instead of nested folders.

**Fix:**
```javascript
// Before
const menuPath = 'data\\menus\\' + id + '.json';

// After
const menuPath = path.join('data', 'menus', `${id}.json`);
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "Read the error message -- which module is not found?" | "Check package name spelling and file extensions" |
| #2 | "Can you rewrite nested callbacks using async/await?" | "Use fs.promises.readFile instead of fs.readFile with callback" |
| #3 | "What happens to a rejected promise with no .catch()?" | "Wrap the call in try/catch or add .catch()" |
| #4 | "Run on Linux or check what path.join() does vs string concat" | "Replace backslash concatenation with path.join()" |
