# ITIL Templates -- FoodExpress

This directory contains four operational templates used throughout the FoodExpress training programme. Each template is filled in by participants during lab exercises and project work.

---

## Templates

### incident-report.md

**When to use:** When a production incident occurs -- any unplanned interruption or degradation of a FoodExpress service.

**Covered in modules:** M34-M37

Fill in this template as soon as an incident is declared. Update it in real time during the response. Complete all sections before closing the incident ticket.

---

### change-request.md

**When to use:** Before making any planned change to a production FoodExpress service, configuration, database, or infrastructure component.

**Covered in modules:** M35-M37

All Normal and Emergency changes require approval before implementation. Standard changes (pre-approved, low-risk) may follow a lighter process as defined by the team lead.

---

### post-mortem.md

**When to use:** After any P1 or P2 incident, or any incident that lasted more than 30 minutes. Conduct the post-mortem within 48 hours of resolution while details are still fresh.

**Covered in modules:** M33-M37

Post-mortems are blameless. The goal is to identify systemic and process failures, not to assign individual fault.

---

### runbook-template.md

**When to use:** When documenting a repeatable operational procedure -- such as restarting a service, investigating a known failure mode, or responding to a specific alert.

**Covered in modules:** M32-M37

Create one runbook per distinct procedure. Link runbooks from alert definitions in Grafana so on-call engineers can find them immediately when an alert fires.

---

## Usage in Training

Participants first encounter these templates in the SRE and ITSM modules. From M32 onwards, all lab incidents and project work require participants to produce at least a completed incident report and, where applicable, a post-mortem or change request. The runbook template is used during the Observability module when participants document the operational procedures they discover while instrumenting FoodExpress services.
