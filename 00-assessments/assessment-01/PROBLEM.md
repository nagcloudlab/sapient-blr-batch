# Assessment 1 -- HTML & CSS Coding Assessment

**Duration:** 90 minutes | **Total:** 100 marks | **Domain:** QuickTicket Event Booking
**Files:** `index.html`, `styles.css`

---

## Instructions

- You have joined the QuickTicket sustain engineering team.
- The QA team has filed defect reports against the event listing page.
- Investigate each defect, locate the root cause, and fix it.
- Fix only `index.html` and `styles.css` -- do not create new files.
- Do not remove any existing content or functionality.
- Bootstrap 5 CDN is already included in the page.
- Push your fixed files to your assigned branch before the timer ends.

---

## Question 1 -- Form & Validation Fixes [Simple] (30 marks)

The booking form has three defects reported by the accessibility and QA teams:

**DEF-101:** Clicking the "Search Events" label text does not focus the search input field. All other form labels work correctly.

**DEF-102:** The email field accepts "asdf" as valid input without any browser warning. On mobile devices, the standard keyboard appears instead of the email keyboard.

**DEF-103:** Submitting the form with all fields empty succeeds without any browser validation message. The Name and Email fields should be mandatory.

**Files to fix:** `index.html`

---

## Question 2 -- Responsive Layout Fixes [Medium] (35 marks)

The event card grid and footer have layout defects on mobile devices:

**DEF-201:** On mobile (375px), the three event cards remain side by side and overflow the screen, causing a horizontal scrollbar. Cards should automatically reflow to a single column on narrow screens.

**DEF-202:** Event card images appear squashed -- the aspect ratio is distorted. Images should fill the card width and maintain their natural proportions within the fixed height.

**DEF-203:** On mobile (375px), the three footer columns overflow horizontally instead of stacking vertically.

**Files to fix:** `styles.css`

---

## Question 3 -- Navigation, Accessibility & UX Enhancements [Complex] (35 marks)

The navigation and page layout have accessibility and UX issues:

**DEF-301:** Screen reader testing with NVDA shows no navigation landmark detected on the page. The tester expected the main navigation links to be announced as a navigation region.

**DEF-302:** On mobile viewport (375px), tapping the hamburger menu button does nothing. The navigation links should toggle open and closed.

**DEF-303:** Hovering over an event card shows no visual feedback. Users report that the cards don't feel clickable. Cards should have a subtle lift and shadow effect on hover.

**DEF-304:** On pages with short content (e.g., search returns 1 result), the footer appears in the middle of the viewport with blank space below it. The footer should always be at the bottom of the viewport or below the content, whichever is lower.

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
