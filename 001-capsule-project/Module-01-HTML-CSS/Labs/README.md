# Module 01: HTML & CSS -- Lab Setup

## Prerequisites

- Google Chrome (latest)
- Visual Studio Code (or any text editor)
- No build tools required

## Running the Starter Code

1. Open the `Labs/` folder in VS Code.
2. Navigate to `starter-code/frontend/`.
3. Right-click `index.html` and choose "Open with Live Server", or drag the file into Chrome.
4. The FoodExpress menu page loads directly from the filesystem -- no server needed.

## Verifying Your Fixes

1. Press `F12` to open Chrome DevTools.
2. Click the device toolbar icon (or press `Ctrl+Shift+M`) to enable responsive mode.
3. Work through each bug listed in `lab-exercises.md` and reload the page after each fix.
4. Use the Elements panel to inspect HTML structure and the Styles panel to confirm CSS rules.

## Expected Behavior

- Restaurant cards display with image, name, rating, and cuisine tag.
- Cart sidebar is visible on the right side of the page.
- Images load without broken-image icons.
- Page has a visible header and footer.
- No red errors appear in the DevTools Console tab.

## Troubleshooting

**Images not loading:** Check that image `src` paths are relative (e.g., `images/burger.jpg`), not absolute
paths that only work on one machine.

**CSS not applying:** Confirm the `<link>` tag in `<head>` points to the correct stylesheet filename,
including the right extension and capitalisation.
