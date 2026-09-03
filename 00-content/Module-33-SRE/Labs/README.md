# Module 33: SRE -- Lab Setup

## Prerequisites

- No specific software installation required.
- A spreadsheet application (Excel, Google Sheets) for error budget calculations.
- The Module 32 Observability environment is useful context but not required to be running.

## Running the Starter Code

This module is document-based. There is no application to start.

1. Read `Project/BRIEF.md` for the full exercise instructions.
2. Open the files in `Labs/starter-code/` -- they contain SLO definitions, an error budget
   spreadsheet, a toil assessment, and a post-mortem document with deliberate errors.
3. Work through each issue listed in `lab-exercises.md`.

## Verifying Your Fixes

Compare each corrected document against `Project/CHECKLIST.md`:

- SLO definitions: realistic targets (not 100%), SLIs are measurable, correct time windows.
- Error budget: arithmetic is correct, burn rate thresholds defined, policy actions documented.
- Toil assessment: each toil item is classified, automation candidate identified, ROI estimated.
- Post-mortem: blameless language throughout, full timeline present, action items have owners and
  due dates.

## Expected Behavior

- SLO document covers availability, latency, and error rate for the FoodExpress Order Service.
- Error budget spreadsheet shows monthly burn rate and remaining budget.
- Toil list ranks items by time cost and flags the top candidate for automation.
- Post-mortem follows a standard structure: summary, impact, timeline, root cause, action items.

## Troubleshooting

**SLO target set to 100%:** No system achieves 100% availability. Use 99.9% (43.8 min/month
downtime budget) or 99.5% as a starting point and adjust based on user impact analysis.

**Post-mortem sounds accusatory:** Replace person-focused language ("the engineer forgot to...")
with system-focused language ("the deployment lacked an automated rollback check...").
