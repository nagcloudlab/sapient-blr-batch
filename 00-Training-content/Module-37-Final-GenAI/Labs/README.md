# Module 37: Final Capstone + GenAI -- Lab Setup

## Prerequisites

- All tools from the full programme must be installed and working:
  Node.js 18+, Java 17+, Maven, MySQL, MongoDB, Docker Desktop, kubectl, minikube,
  Ansible, Jenkins, Git, Bash/WSL2, Apache2
- A web browser for GenAI lab exercises (Claude or ChatGPT access provided by trainer)
- ServiceNow PDI from Module 36

## Running the Starter Code

This is the capstone project. There is no single start command. Follow `Project/BRIEF.md` for the
full sequence:

1. Start the FoodExpress full stack (`docker compose up` or individual services per BRIEF.md).
2. Apply the Kubernetes manifests for the deployment scenario.
3. Trigger the simulated incident using the provided war game script.
4. Work through the ITIL records (incident, problem, change, SLA, PIR).
5. Complete the GenAI assisted labs (prompt engineering, RCA generation, runbook generation).
6. Prepare the 15-minute team presentation.

## Verifying Your Fixes

Check each deliverable against `Project/CHECKLIST.md`:

- Incident record: full timeline, impact statement, resolution steps (3-day payment gateway outage).
- Problem record: 5 Whys analysis reaches a systemic root cause, permanent fix proposed.
- Change request: change plan, risk assessment, rollback procedure, CAB sign-off section complete.
- SLA definition: Payment Service availability target, measurement window, breach penalties.
- Post-incident review (PIR): blameless format, action items have owners and due dates.
- AI lab output: prompt log, generated runbook, written critique of AI output accuracy.

## Expected Behavior

- All ITIL records are internally consistent and use correct ITIL 4 terminology.
- GenAI-generated content is reviewed critically -- inaccuracies are identified and corrected.
- All 17 AI lab bugs (6 + 6 + 5) are fixed with explanations.
- Presentation covers the incident lifecycle end-to-end within 15 minutes.
- All CHECKLIST.md items are signed off before the presentation slot.

## Troubleshooting

**Services not starting cleanly:** The capstone depends on all previous module environments. Run
the health check script from Module 23 first to confirm each service layer is functional.

**GenAI output is inaccurate or hallucinated:** This is intentional. Document the inaccuracy,
correct it, and include it in the AI lab critique. Uncritical acceptance of AI output is the
anti-pattern being tested -- demonstrating critical evaluation is part of the deliverable.
