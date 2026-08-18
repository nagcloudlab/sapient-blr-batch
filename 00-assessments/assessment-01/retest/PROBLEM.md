# Assessment 1 Re-Test -- HTML & CSS Coding Assessment

**Duration:** 90 minutes | **Total:** 100 marks | **Domain:** QuickTicket Event Booking
**Files:** `index.html`, `styles.css`

---

## Instructions

- You have joined the QuickTicket sustain engineering team.
- The QA team has filed defect reports against the **My Bookings** page.
- Investigate each defect, locate the root cause, and fix it.
- Fix only `index.html` and `styles.css` -- do not create new files.
- Do not remove any existing content or functionality.
- Bootstrap 5 CDN is already included in the page.
- Push your fixed files to your assigned branch before the timer ends.

---

## Question 1 -- Semantic & Form Fixes [Simple] (30 marks)

The bookings page has three defects reported by the accessibility and QA teams:

**DEF-401:** Screen reader testing with NVDA shows the bookings table header row is announced as regular data cells, not column headers. The tester expected each column heading (Event, Date, Venue, etc.) to be announced as a table header.

**DEF-402:** The "Date From" and "Date To" filter fields show a plain text input. Users expect a native date picker (calendar widget) to appear when clicking these fields, especially on mobile devices.

**DEF-403:** The "Status" dropdown has "Confirmed" pre-selected as the default. Users report confusion because they assume their bookings are already filtered. The dropdown should show a neutral placeholder like "All Statuses" that prompts the user to choose.

**Files to fix:** `index.html`

---

## Question 2 -- Responsive & Visual Fixes [Medium] (35 marks)

The bookings table and summary cards have layout defects on mobile devices:

**DEF-501:** On mobile (375px), the bookings table columns get squished and text overlaps. The table should be horizontally scrollable so users can swipe to see all columns without breaking the layout.

**DEF-502:** On mobile (375px), the three summary cards (Total Bookings, Upcoming, Cancelled) remain side by side and overflow the screen. Cards should stack vertically on narrow viewports.

**DEF-503:** All status badges (Confirmed, Pending, Cancelled) appear in the same plain gray colour with no background tint. They should display in distinct colours -- green for Confirmed, yellow for Pending, and red for Cancelled.

**Files to fix:** `styles.css` (DEF-501 may also need `index.html`)

---

## Question 3 -- Accessibility, Navigation & UX Enhancements [Complex] (35 marks)

The page has accessibility and UX issues flagged by the compliance team:

**DEF-601:** The breadcrumb ("Home > My Account > My Bookings") uses plain `<div>` and `<span>` elements. Screen readers do not recognise it as a breadcrumb navigation. The compliance team requires a semantic `<nav>` element with an ordered list structure.

**DEF-602:** The "My Bookings" navigation link in the header has no visual distinction from other links, even though it is the current page. Users cannot tell which page they are on. The active link should be visually highlighted and announced to screen readers as the current page.

**DEF-603:** When scanning the bookings table with many rows, users lose track of which row they are reading. There is no visual feedback when hovering over a table row. Rows should highlight on hover to improve readability.

**DEF-604:** The page title in the browser tab shows "Page" instead of a descriptive title. Additionally, the `<html>` tag is missing the `lang` attribute, which affects screen readers and search engines.

**Files to fix:** `index.html`, `styles.css`

---

## Evaluation Parameters

| Parameter | Weightage |
|-----------|-----------|
| Ability to apply concepts and any additional functionality asked to implement | 20 |
| Coding Standards (Naming Conventions, Comments and Indentation) | 20 |
| Exception Handling | 20 |
| Completeness wrt Timelines as per requirements & Working application | 15 |
| Problem solving ability (think, evaluate and choose among alternates, and innovation/creativity) | 10 |
| Debugging / troubleshooting skills | 15 |
| **Total** | **100** |

---

## Submission

Push your fixed files to your assigned branch before the timer ends.
