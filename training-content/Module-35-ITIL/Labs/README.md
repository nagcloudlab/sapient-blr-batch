# Module 35: ITIL Practices -- Lab Setup

## Prerequisites

- No software installation required.
- A text editor for reviewing and correcting ITIL records.
- Familiarity with ITIL 4 terminology (covered in the module slides).

## Running the Starter Code

This module is document-based. There is no application to start.

1. Read `Project/BRIEF.md` for the full exercise instructions.
2. Open the four records in `Labs/starter-code/`:
   - `incident-record.md` -- 7 bugs to fix
   - `change-request.md` -- 6 bugs to fix
   - `problem-record.md` -- 6 bugs to fix
   - `sla-definition.md` -- 6 bugs to fix
3. Work through each issue listed in `lab-exercises.md`.

## Verifying Your Fixes

Compare each corrected record against `Project/CHECKLIST.md`:

- Incident: priority assigned using the correct impact x urgency matrix, SLA timers started at
  correct event, status transitions follow the defined lifecycle.
- Change: change type appropriate (standard/normal/emergency), risk score calculated, rollback plan
  included, CAB approval required flag set correctly.
- Problem: 5 Whys analysis reaches a systemic root cause, workaround documented, permanent fix
  planned with owner and target date.
- SLA: availability target is realistic, measurement window defined, breach penalties specified.

## Expected Behavior

- All four records are internally consistent (e.g., incident priority matches SLA response time).
- Records use ITIL 4 terminology correctly (not ITIL v3 terms).
- No contradictions between linked records (the problem record references the incident record).
- SLA targets align with the SLOs defined in the Module 33 exercise.

## Troubleshooting

**Unsure which ITIL version to use:** This training uses ITIL 4. Key differences from v3: practices
replace processes, the service value chain replaces the service lifecycle.

**Priority matrix confusion:** Priority = Impact x Urgency. A high-impact, low-urgency issue is P2
(not P1). P1 requires both high impact AND high urgency.
