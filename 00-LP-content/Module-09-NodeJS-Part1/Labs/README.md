# Module 09: Node.js Part 1 -- Lab Setup

## Prerequisites

- Node.js 18 or higher (`node -v` to confirm)
- npm 9+ (bundled with Node.js)
- A terminal / command prompt

## Running the Starter Code

```bash
cd Labs/starter-code
npm install
node server.js
```

Some bugs will crash the process immediately on startup. The error printed to the terminal tells you
which file and line to look at. Fix the bug and re-run.

## Verifying Your Fixes

1. A successful start prints a message such as "FoodExpress server running on port 3000".
2. Test file-read operations by checking terminal output -- menus or config values should be printed.
3. After each fix, re-run `node server.js` and confirm no crash occurs.
4. All bugs fixed = server stays running and does not exit unexpectedly.

## Expected Behavior

- Server starts without crashing and prints a startup confirmation line.
- Menu data is read from the JSON file and logged to the console on startup.
- Basic HTTP requests return a response (even a simple "OK") rather than a connection reset.
- No `UnhandledPromiseRejectionWarning` in the terminal output.

## Troubleshooting

**`MODULE_NOT_FOUND` error:** A `require()` path is wrong or a dependency is missing. Run
`npm install` first, then check the file path in the failing `require()` statement.

**Server crashes after handling one request:** Look for a missing `try/catch` around async file I/O or
a callback that throws instead of calling `next(err)`.
