# Module 09 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: `node server.js` starts without "MODULE_NOT_FOUND" errors
- [ ] Bug #2: Menu loader uses async/await (no nested callbacks)
- [ ] Bug #3: Missing data file logs an error instead of crashing the process
- [ ] Bug #4: File paths work on both Windows and Linux (uses `path.join`)

## Enhancements
- [ ] Restaurant list loads from `data/restaurants.json`
- [ ] Menu data loads from `data/menus/{id}.json` for a given restaurant ID
- [ ] Console output shows restaurant count on startup

## Code Quality
- [ ] No `require()` calls with wrong module names
- [ ] No raw string path concatenation with `\` or `/`
- [ ] All async operations have error handling

## Self-Check Questions
1. What is the difference between `require()` and `import`?
2. Why does Node.js crash on unhandled promise rejections?
3. What does `path.join()` do differently from string concatenation?
4. When would you use `fs.promises` vs callback-based `fs`?
5. What is the event loop and why does blocking it matter?
