# Module 34: MidStage + ITSM -- Lab Setup

## Prerequisites

- Docker Desktop and kubectl/minikube (for the alert and fault injection exercises)
- All tools from Modules 01-33 should be installed -- this is the mid-stage checkpoint
- curl for API testing during fault injection

## Running the Starter Code

This module has multiple independent exercises. Start each one as directed in `Project/BRIEF.md`:

```bash
# Exercise 1 -- Alert rules (review YAML files in starter-code/)
# No runtime needed; fix the YAML and validate with promtool if Prometheus is running

# Exercise 2 -- Fault injection
minikube start
kubectl apply -f Labs/starter-code/manifests/
bash Labs/starter-code/fault-injection.sh

# Exercise 3 & 4 -- Documents (incident template, ITSM process)
# Text editor only
```

War game cleanup:
```bash
bash Labs/starter-code/fault-injection.sh stop
```

## Verifying Your Fixes

- Alert rules: correct threshold values, severity labels present, runbook URLs populated.
- Fault injection script: runs without errors, simulates the specified failure, has a rollback step.
- Incident template: correct priority assignment, timeline format, escalation path named.
- ITSM process: correct ITIL categories, SLA targets, notification channels.

## Expected Behavior

- Alert YAML loads into Prometheus without parse errors.
- Fault injection script creates and then cleanly removes the simulated fault.
- Incident record uses the priority matrix correctly (P1-P4 with defined response times).
- ITSM flow diagram covers detection, triage, resolution, and review stages.

## Troubleshooting

**Fault injection script permission denied:** Run `chmod +x fault-injection.sh` first.

**Alert rule not appearing in Prometheus:** Confirm the rule file path is listed under `rule_files:`
in `prometheus.yml` and that the Prometheus container has been reloaded (`curl -X POST
http://localhost:9090/-/reload`).
