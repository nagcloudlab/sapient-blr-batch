# Module 09: Node.js (Part 1) -- Fix the Issues

## Lab Overview

The FoodExpress Restaurant Service is being built in Node.js. The previous developer left and the codebase has startup crashes, callback spaghetti, silent failures, and path bugs. Your job is to get it running and serving restaurant data from JSON files.

> "Hi Team, the Restaurant Service won't even start. We get MODULE_NOT_FOUND errors, and when we fix those, it crashes with unhandled promise rejections. The menu loader is impossible to read -- callbacks nested five levels deep. And the paths break when we deploy to our Linux server. Please stabilize this before we add Express routes tomorrow."

---

## Setup

1. Navigate to `starter-code/restaurant-service/`
2. Run `npm install`
3. Run `node server.js` -- notice it crashes immediately
4. Read the error message carefully -- it tells you which module is missing
5. Fix and re-run. You will hit multiple errors in sequence.

---

## Bug List

### Bug #1: Missing / Wrong require() Calls
- **Where:** `server.js`, `utils/logger.js`
- **Symptom:** `Error: Cannot find module 'colours'` on startup
- **Hint:** The package is called `chalk`, not `colours`. Check other require statements too -- one references `./config` but the file is `config.json`.
- **Debug:** Read each error message. Node tells you exactly which module and which file.

### Bug #2: Callback Hell in Menu Loader
- **Where:** `services/menuLoader.js`
- **Symptom:** The `loadMenu()` function has three levels of nested callbacks (`readdir` > `access` > `readFile`). Errors at inner levels are silently swallowed.
- **Hint:** Rewrite using `async/await` with `fs.promises`. Each operation becomes a single line with proper error propagation.
- **Debug:** Add `console.log` at each callback level to see which ones execute.

### Bug #3: Unhandled Promise Rejection
- **Where:** `services/restaurantService.js`, `server.js`
- **Symptom:** When `data/restaurants.json` is missing, the process crashes with `UnhandledPromiseRejectionWarning`
- **Hint:** The `loadAll()` method returns a Promise, but the caller in `server.js` never attaches `.catch()`. Add error handling.
- **Debug:** Delete (or rename) `data/restaurants.json` and run. Watch the crash.

### Bug #4: Hardcoded Windows Path Separator
- **Where:** `services/menuLoader.js`
- **Symptom:** Menu files load on Windows but fail on Linux with "file not found"
- **Hint:** The code uses `'data\\menus\\' + id + '.json'`. Replace with `path.join('data', 'menus', id + '.json')`.
- **Debug:** Log the resolved path and compare with what the filesystem expects.

### Enhancement #5: List All Restaurants
- **Where:** `services/restaurantService.js`
- **Hint:** Read `data/restaurants.json` using `fs.promises.readFile`, parse it, and return the array.

### Enhancement #6: Read Restaurant Menu
- **Where:** `services/menuLoader.js`
- **Hint:** Given a restaurant ID, read `data/menus/{id}.json` and return the parsed menu object.

---

## Checkpoints

1. [ ] `node server.js` starts without any errors
2. [ ] Console shows "Loaded X restaurants" on startup
3. [ ] Menu loader uses async/await (no nested callbacks)
4. [ ] Deleting `restaurants.json` logs a friendly error (no crash)
5. [ ] File paths use `path.join()` (no hardcoded separators)
6. [ ] Restaurant list returns correct data from JSON
7. [ ] Menu for restaurant ID "rest-001" loads correctly

## Bonus Challenges

1. Add a `process.on('unhandledRejection')` global handler in `server.js`
2. Add file-watching with `fs.watch()` to reload restaurant data when JSON changes
3. Create a simple CLI menu: type a restaurant ID, see its menu printed to console
4. Add input validation -- reject IDs that contain `..` or `/` (path traversal prevention)
