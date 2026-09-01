# Post-Mortem: Delivery Tracking Outage
## SOLUTION

---

## Incident Summary

**Title:** Delivery Tracking Service Outage -- Expired TLS Certificate
**Date:** September 5, 2026
**Duration:** 20:15 - 20:52 IST (37 minutes)
**Severity:** SEV-2
**Author:** Sustain Engineering Team
**Post-Mortem Date:** September 6, 2026

The delivery tracking service became unreachable due to an expired TLS certificate, affecting 12,000 customers who could not view their delivery status.

---

## Impact

- 12,000 customers affected (unable to track deliveries)
- Delivery tracking unavailable for 37 minutes
- No orders were lost (order placement unaffected)
- Customer support received 340 calls
- Error budget consumed: 37 / 432 = 8.6% of delivery-tracking monthly budget
- Remaining error budget: 91.4% (395 minutes remaining)

---

## Timeline

# FIX 1: Complete minute-by-minute timeline

| Time | Event |
|------|-------|
| 20:15 | TLS certificate for delivery-service.foodexpress.in expires |
| 20:15 | Delivery tracking API begins returning TLS handshake failures |
| 20:18 | Prometheus alert "DeliveryServiceDown" fires |
| 20:18 | PagerDuty pages on-call engineer |
| 20:23 | Customer support begins receiving calls about tracking unavailability |
| 20:25 | Status page updated: "Investigating delivery tracking issues" |
| 20:30 | On-call engineer acknowledges alert (was at dinner, 12 min response) |
| 20:35 | Engineer VPNs in, identifies expired certificate as root cause |
| 20:40 | Status page updated: "Root cause identified, fix in progress" |
| 20:45 | Engineer begins certificate renewal process |
| 20:48 | New certificate issued and deployed |
| 20:50 | Service restarted with new certificate |
| 20:52 | Health checks pass, service confirmed healthy |
| 20:52 | Status page updated: "Resolved" |

---

## Root Cause Analysis

The TLS certificate for delivery-service.foodexpress.in expired at 20:15 IST. The certificate had been issued on March 5, 2026 with a 6-month validity period. A renewal warning email was sent by the certificate authority to the platform team distribution list 14 days before expiry (August 22), but was not actioned due to it being mixed in with other notification emails.

**Contributing factors:**
1. No automated certificate renewal (cert-manager not configured)
2. No monitoring alert for certificate expiry (only email notification)
3. Certificate warning emails went to a shared inbox with low visibility
4. On-call response time was 12 minutes (target: < 5 minutes)

---

## What Went Well

- Prometheus alert fired within 3 minutes of impact
- Communication to stakeholders was timely (status page updated at 20:25)
- No data loss occurred
- Other services (ordering, payment, menu) were completely unaffected
- Root cause was identified quickly once engineer was online
- Certificate renewal process was straightforward

---

## What Went Wrong

# FIX 2: Rewritten to be blameless -- focus on systems, not individuals

| Issue | Systemic Cause |
|-------|---------------|
| Certificate expired without renewal | No automated certificate management system (cert-manager) was in place |
| Warning email was not actioned | Certificate expiry warnings went to a shared inbox with hundreds of other notifications; no dedicated alerting channel |
| On-call response took 12 minutes | On-call policy does not require engineers to carry a dedicated alert device; personal phone notifications were silenced during dinner |
| Manual renewal process took 13 minutes | No runbook existed for certificate renewal; engineer had to look up the process |

---

## Action Items

# FIX 3: All action items have owners and deadlines

| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | Deploy cert-manager for automatic TLS renewal | Platform Team (Vikram) | Sept 12, 2026 | To Do |
| 2 | Add Prometheus alert for certificate expiry (30 days, 7 days, 1 day before) | SRE Team (Arjun) | Sept 8, 2026 | In Progress |
| 3 | Create certificate renewal runbook | Sustain Team (Author) | Sept 9, 2026 | In Progress |
| 4 | Audit all certificates across services for upcoming expiry | Platform Team (Priya) | Sept 10, 2026 | To Do |
| 5 | Configure PagerDuty escalation to backup on-call if primary doesn't ack in 5 min | SRE Team (Arjun) | Sept 10, 2026 | To Do |
| 6 | Move certificate alerts from email to Slack #platform-alerts channel | Platform Team (Vikram) | Sept 8, 2026 | To Do |

---

## Lessons Learned

1. **Automate certificate management:** Manual certificate tracking does not scale. cert-manager eliminates this entire class of outages.
2. **Monitor what matters:** If something can expire and cause an outage, it needs a monitoring alert -- not just an email notification.
3. **Shared inboxes are where alerts go to die:** Critical notifications must go to dedicated, high-visibility channels with on-call routing.
4. **Runbooks reduce MTTR:** Having a step-by-step runbook would have reduced the fix time from 13 minutes to under 5 minutes.
5. **On-call escalation is essential:** If the primary on-call is unavailable, automatic escalation to a secondary ensures timely response.
6. **This was a preventable outage:** The warning was available 14 days in advance. Better processes would have prevented any customer impact.
