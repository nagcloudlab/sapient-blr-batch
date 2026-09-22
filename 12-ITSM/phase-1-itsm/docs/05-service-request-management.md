# Section 5: Service Request Management

## What is a Service Request?

A **formal request from a user** for something to be provided -- NOT a failure or break.

Key distinction:

| | Incident | Service Request |
|---|---|---|
| **Trigger** | Something is BROKEN | I NEED something |
| **Example** | "UPI payments failing" | "Give me access to production logs" |
| **Urgency** | Usually high | Usually planned |
| **Goal** | Restore service | Fulfill a need |

---

## UPI Examples

### Requests from Banks to NPCI

| Request | Type | Approval needed? |
|---|---|---|
| "Onboard our new UPI handle @kotak" | New service setup | Yes -- compliance review |
| "Add 5 new API credentials for our team" | Access provisioning | Yes -- security approval |
| "Share last month's settlement report" | Information request | No -- standard |
| "Increase our TPS (transactions per second) limit from 500 to 2000" | Capacity change | Yes -- infra team review |

### Requests from NPCI Internal Teams

| Request | Type | Approval needed? |
|---|---|---|
| "I need read access to the settlement database" | Access request | Yes -- manager + DBA approval |
| "Set up a new staging environment for v4.2 testing" | Environment provisioning | Yes -- infra team |
| "Reset my VPN credentials" | Password/credential reset | No -- auto-approved |
| "Order a new monitoring license for Grafana" | Procurement | Yes -- budget approval |

---

## Service Request Lifecycle

```
Submit --> Categorize --> Approve (if needed) --> Fulfill --> Close
```

### Example: Bank Requests Higher TPS Limit

```
1. SUBMIT
   REQ-20260921-0031: "Increase HDFC TPS limit 500 -> 2000"
   Requested by: HDFC Bank Integration Team

2. CATEGORIZE
   Category: Capacity Change
   Fulfillment team: NPCI Platform Engineering

3. APPROVE
   Approver: NPCI Capacity Manager
   Check: Do we have headroom? Yes -- current cluster at 40% utilization.
   Decision: APPROVED

4. FULFILL
   - Update rate limiter config for HDFC
   - Deploy config change (Standard Change -- pre-approved)
   - Run load test to verify

5. CLOSE
   REQ closed. HDFC confirmed new limit working.
   Fulfillment time: 4 hours (within 1-business-day SLA)
```

---

## Request Fulfillment vs Incident Resolution

```
User: "I can't log into the UPI dashboard"

Is it an Incident or a Service Request?

  --> "I get an error 500 when I log in"        = INCIDENT (something is broken)
  --> "I don't have an account yet, need access" = SERVICE REQUEST (need something new)
  --> "My password expired, need a reset"        = SERVICE REQUEST (routine fulfillment)
```

This distinction matters because they follow **different processes, different SLAs, different teams**.

---

## Request Models

For frequently asked requests, ITSM defines **pre-built request models** (like templates):

| Request Model | Pre-filled fields | Auto-approval? |
|---|---|---|
| Password Reset | Category, fulfillment team, SLA | Yes |
| New Employee Onboarding | Checklist: laptop, email, VPN, access | Manager approval only |
| New Bank Onboarding | Compliance docs, API credentials, testing | Multi-level approval |
| Report Generation | Report type, date range, format | Yes |

These models speed up fulfillment and reduce errors.

---

## Connection to Previous Sections

```
Service Request: "I need a new staging environment"
        |
        +--> If it's a routine setup --> Standard Change (pre-approved)
        |
        +--> If it needs new infra --> Normal Change (CAB approval)
        |
        +--> Environment details recorded in --> CMDB (Section 7)
        |
        +--> Available as a menu item in --> Service Catalog (Section 6, next)
```

---

## Key Takeaway

> Not everything is an incident. Users also need things -- access, info, environments, reports.
> Service Request Management gives them a **structured, trackable, SLA-driven way** to ask for it.
>
> Rule of thumb:
> - **Broken?** --> Incident
> - **Need something?** --> Service Request
