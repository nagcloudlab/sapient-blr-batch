# Module 02: CSS & Frameworks -- Lab Setup

## Prerequisites

- Google Chrome (latest)
- Visual Studio Code (or any text editor)
- No build tools or local server required

## Running the Starter Code

1. Navigate to `Labs/starter-code/frontend/`.
2. Open `index.html` directly in Chrome (drag-and-drop or File > Open).
3. The page loads Bootstrap and custom CSS from CDN links -- internet access required.

## Verifying Your Fixes

1. Open Chrome DevTools (`F12`).
2. Enable the device toolbar (`Ctrl+Shift+M`) and test these three breakpoints:
   - Mobile: 375 px width
   - Tablet: 768 px width
   - Desktop: 1200 px width
3. After fixing each bug in `lab-exercises.md`, reload the page and re-test all three viewports.
4. Check the Console tab for JavaScript errors related to Bootstrap component initialisation.

## Expected Behavior

- Bootstrap navbar collapses correctly on mobile and expands on desktop.
- Restaurant cards display in a responsive grid (1 col mobile, 2 col tablet, 3 col desktop).
- Modal dialogs open and close without freezing the page.
- Image carousel auto-advances and responds to prev/next controls.
- No layout overflow or horizontal scroll bar at any tested viewport.

## Troubleshooting

**Bootstrap JS not working (modal/carousel broken):** Verify the Bootstrap JS bundle `<script>` tag is
placed just before `</body>`, not in `<head>`, and that the CDN URL is correct.

**Grid not responding:** Check that column classes follow the `col-sm-`, `col-md-`, `col-lg-` pattern and
that the parent element has the `row` class inside a `container` or `container-fluid`.
