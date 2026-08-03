# Module 04: UI Frameworks (React) -- Lab Setup

## Prerequisites

- Node.js 18 or higher (`node -v` to confirm)
- npm 9+ (bundled with Node.js)
- Google Chrome

## Running the Starter Code

```bash
cd Labs/starter-code/frontend
npm install
npm start
```

The dev server starts and opens `http://localhost:3000` in your default browser automatically.
Hot-reload is active -- saving a file refreshes the browser instantly.

## Verifying Your Fixes

1. With the app running at `http://localhost:3000`, open DevTools (`F12`) and check the Console for errors.
2. Test component behaviour:
   - Menu cards should render restaurant names, prices, and an "Add" button.
   - Clicking "Add" should update the cart badge count in the header.
   - The cart panel should list items with quantities and a total.
3. After each fix, save the file -- the browser reloads automatically.
4. The React DevTools browser extension (optional) helps inspect component state and props.

## Expected Behavior

- Home page renders a grid of menu item cards without blank or duplicated entries.
- Cart state updates when items are added or removed.
- No prop-type warnings or key-prop warnings in the Console.
- Components do not crash with "cannot read property of undefined" errors.

## Troubleshooting

**`npm install` fails:** Ensure Node.js 18+ is installed. Delete `node_modules/` and `package-lock.json`,
then run `npm install` again.

**Blank white screen:** Open the Console -- a JavaScript runtime error is likely. Fix the reported error
first; the rest of the app will then render.
