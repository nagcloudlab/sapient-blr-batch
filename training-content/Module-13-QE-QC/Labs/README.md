# Module 13: QE/QC -- Lab Setup

## Prerequisites

- No software installation required.
- Pen and paper or a text editor for drafting deliverables.
- Access to `Labs/starter-code/` folder (contains buggy test artefacts to review).

## Running the Starter Code

This is a document-based lab. There is no application to run.

1. Read `Project/BRIEF.md` for the full exercise instructions.
2. Open the files in `Labs/starter-code/` -- they contain test cases, bug reports, and a test
   strategy document with deliberate errors.
3. Work through each issue listed in `lab-exercises.md`.

## Verifying Your Fixes

Compare each deliverable you produce against the criteria in `Project/CHECKLIST.md`:

- Test cases: correct format, cover happy path and edge cases, have clear pass/fail criteria.
- Bug triage table: each bug has severity, priority, root cause category, and reproduction steps.
- Test strategy: includes scope, approach, entry/exit criteria, and risk assessment.
- Automation matrix: categorises scenarios by feasibility and ROI of automation.

## Expected Behavior

- All test cases follow the standard template (ID, title, steps, expected result, actual result).
- Bug severity and priority are assigned consistently with the definitions in `BRIEF.md`.
- Test strategy document references the FoodExpress architecture components correctly.
- Automation matrix identifies at least three high-value candidates for automated regression.

## Troubleshooting

**Unclear severity vs. priority distinction:** Severity = impact on the system; priority = urgency of
fix for the business. A cosmetic bug on the checkout page can be high priority even if low severity.

**Test case steps too vague:** Each step must be actionable by someone who has never used the app.
Include the exact data to enter and the exact UI element to click.
