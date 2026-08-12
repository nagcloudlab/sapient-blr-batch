# Reference Documents -- FoodExpress Training

Quick-reference materials for the Publicis Sapient Sustain Engineering programme, Bangalore 2026.
These documents are designed to be kept and consulted after the training ends.

---

## Documents in this folder

### ITIL-ITSM-Deep-Dive.md
Complete ITIL and ITSM guide with FoodExpress scenarios.

Covers the full incident lifecycle using a real FoodExpress Payment Service outage at 2:17 AM,
all four core ITIL practices (Incident, Problem, Change, Service Level Management), the P1-P4
priority matrix with FoodExpress examples, the three change types (standard, normal, emergency),
blameless post-mortem format, and the 5 Whys technique.

Relevant modules: M35 (ITSM/ITIL), M36 (ServiceNow).

---

### SRE-Terms-Deep-Dive.md
SRE terminology reference with formulas, PromQL queries, and FoodExpress examples.

Covers SRE vs Traditional Ops, SLI (with formula and PromQL for each FoodExpress service),
SLO targets and allowed downtime calculations, SLA vs SLO distinction, error budget calculation
and burn rate policy, toil definition with FoodExpress examples and the 50% rule, blameless
post-mortem template, and the four Golden Signals with Grafana panel specs.

Relevant modules: M31 (Observability), M32 (SRE).

---

### 7Cs-DevOps-Deep-Dive.md
DevOps lifecycle reference with the FoodExpress pipeline as a running example.

Covers all seven C's: Continuous Development (git branching conventions, commit discipline),
Continuous Integration (Jenkins pipeline stages), Continuous Testing (testing pyramid, all test
types), Continuous Delivery (feature flags, always-deployable main), Continuous Deployment
(Jenkins Groovy pipeline, canary/blue-green strategies), Continuous Monitoring (Prometheus,
Grafana, Loki, Jaeger, PagerDuty alert thresholds), and Continuous Feedback (feedback loop
table, example cycle). Includes the DevOps infinity loop diagram.

Relevant modules: M18 (DevOps), M19 (Git/GitHub), M25 (Jenkins), M27 (Kubernetes).

---

## Related materials

The AI prompt library for sustain engineering is in:
`Module-37-Final-GenAI/Labs/ai-prompts-for-sustain.md`

It contains ready-to-use prompts for log analysis, incident communication, post-mortems,
code review, query optimization, runbook generation, and test case generation -- all in
FoodExpress context.
