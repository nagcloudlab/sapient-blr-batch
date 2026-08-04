# Assessment 2 -- JavaScript Coding Assessment

**Duration:** 90 minutes | **Total:** 100 marks | **Domain:** QuickTicket Event Booking
**Files:** `app.js` (do not modify `index.html`)

---

## Instructions

- The QuickTicket event listing page has a JavaScript module (`app.js`) powering search, cart, and featured events.
- The QA team has reported defects across 3 features. Locate and fix all issues.
- Fix only `app.js` -- do not modify `index.html`
- Use vanilla JavaScript (ES6+) -- no frameworks or libraries
- Use `const`/`let` only -- no `var`
- Do not modify functions in the "DO NOT MODIFY" section at the bottom of the file
- Push your fixed `app.js` to your assigned branch before the timer ends.

---

## Question 1 -- Search & Filter Fixes [Simple] (30 marks)

**DEF-101:** Searching "jazz" returns no results, but searching "Jazz" shows 2 matching events. Search should be case-insensitive.

**DEF-102:** Search results only update after the user clicks away from the search box or presses Tab. Results should update in real-time as the user types each character.

**DEF-103:** After searching for something, clearing the search box (backspacing to empty) shows "No events found" instead of displaying all events.

**Files to fix:** `app.js`

---

## Question 2 -- Cart Fixes [Medium] (35 marks)

**DEF-201:** Adding the same event twice creates two separate entries in the cart instead of incrementing the quantity on the existing entry.

**DEF-202:** The cart total displays "NaN" when items are in the cart. The total should show the correct sum of (price x quantity) for all items.

**DEF-203:** Clicking "Remove" on a cart item does nothing. The item remains in the cart. The remove function receives the event ID but fails to find and remove the matching item.

**Files to fix:** `app.js`

---

## Question 3 -- API Integration Fixes [Complex] (35 marks)

**DEF-301:** The featured events section shows "[object Promise]" instead of actual event data. The browser Network tab confirms the API call succeeds and returns valid JSON.

**DEF-302:** When the API server returns a 500 error, the app displays the error response data in the featured section as if it were valid events. No error message is shown to the user.

**DEF-303:** When any error occurs during featured event loading, the loading spinner keeps spinning forever and never disappears.

**Files to fix:** `app.js`

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

Push your fixed `app.js` to your assigned branch before the timer ends.
