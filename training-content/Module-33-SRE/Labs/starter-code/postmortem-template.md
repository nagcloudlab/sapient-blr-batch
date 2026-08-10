# Post-Mortem: Delivery Tracking Outage
## STARTER CODE -- Contains issues to fix

---

## Incident Summary

**Title:** Delivery Tracking Service Outage
**Date:** September 5, 2026
**Duration:** 20:15 - 20:52 IST (37 minutes)
**Severity:** SEV-2
**Author:** Sustain Engineering Team

The delivery tracking service became unreachable due to an expired TLS certificate, affecting 12,000 customers who could not view their delivery status.

---

## Impact

- 12,000 customers affected
- Delivery tracking unavailable for 37 minutes
- No orders were lost (order placement unaffected)
- Customer support received 340 calls
- Error budget consumed: TODO (calculate)

---

## Timeline

# BUG 1: Timeline section is empty -- fill in the minute-by-minute details
| Time | Event |
|------|-------|
| TODO | TODO |

---

## Root Cause Analysis

The TLS certificate for delivery-service.foodexpress.in expired at 20:15 IST. The certificate had been valid since March 2026 with a 6-month validity period. A renewal warning email was sent to the platform team 14 days before expiry but was not actioned.

---

## What Went Well

- Alert fired within 3 minutes of impact
- Communication to stakeholders was timely
- No data loss occurred
- Other services (ordering, payment) were unaffected

---

## What Went Wrong

# BUG 2: This section blames an individual -- rewrite to be blameless
- Rajesh forgot to renew the certificate despite receiving the warning email
- Rajesh was at dinner and took 12 minutes to respond to the page
- If Rajesh had set up auto-renewal this would not have happened
- Rajesh should have checked the certificate expiry dashboard

---

## Action Items

# BUG 3: Action items have no owners or deadlines
| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | Implement cert-manager for auto-renewal | TODO | TODO | TODO |
| 2 | Add certificate expiry monitoring alert (30 days before) | TODO | TODO | TODO |
| 3 | Create runbook for certificate renewal | TODO | TODO | TODO |
| 4 | Review all other certificates for upcoming expiry | TODO | TODO | TODO |
| 5 | Improve on-call response time (< 5 min acknowledgment) | TODO | TODO | TODO |

---

## Lessons Learned

TODO: What did we learn from this incident?
