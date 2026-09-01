# Mid-Stage Project + ITSM Introduction -- Submission Checklist
## Module 34 | Days 39-40

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Prometheus: Division-by-zero guard on error rate | [ ] |
| 2 | Prometheus: `for` duration set to 5m (not 0s) | [ ] |
| 3 | Prometheus: Correct metric name `up` for PaymentServiceDown | [ ] |
| 4 | Prometheus: HighLatency threshold is 2s (not 0.001s) | [ ] |
| 5 | Prometheus: DiskSpaceLow uses `<` not `>` | [ ] |
| 6 | Prometheus: Correct severity labels (critical/warning) | [ ] |
| 7 | Prometheus: Namespace filter on HighMemoryUsage | [ ] |
| 8 | Prometheus: Production runbook URLs | [ ] |
| 9 | Fault injection: Namespace is `foodexpress` | [ ] |
| 10 | Fault injection: PASS/FAIL comparison is correct (`>=`) | [ ] |
| 11 | Fault injection: Rollback uses `del` not `add` | [ ] |
| 12 | Fault injection: Sleep duration is 180s | [ ] |
| 13 | Fault injection: Correct Prometheus API path (`/api/v1`) | [ ] |
| 14 | Fault injection: Correct jq JSON path (`.data.result[0].value[1]`) | [ ] |
| 15 | Incident: Priority is P1 - Critical | [ ] |
| 16 | Incident: Affected users count is realistic (~5,000) | [ ] |
| 17 | Incident: Timeline is in chronological order | [ ] |
| 18 | Incident: Resolution matches root cause (rollback, not restart) | [ ] |
| 19 | Incident: Escalation path with contacts and timeframes | [ ] |
| 20 | Incident: Prevention actions with owners and deadlines | [ ] |
| 21 | ITSM: Payment under Application category | [ ] |
| 22 | ITSM: High/High priority is P1 | [ ] |
| 23 | ITSM: P1 escalation is 15 minutes | [ ] |
| 24 | ITSM: P1/P5 resolution times corrected | [ ] |
| 25 | ITSM: P1 notifications include PagerDuty and phone | [ ] |

---

## Self-Check Questions

1. **Why add a `> 0` guard to error rate alerts?** When there are zero requests, dividing by zero produces NaN, which can crash alert evaluation or produce unexpected results.
2. **Why is `for: 0s` dangerous?** It fires on any momentary spike, causing alert fatigue. Engineers learn to ignore alerts.
3. **Why must the rollback command use `del` not `add`?** Using `add` adds another netem rule, doubling the latency instead of removing it.
4. **Why is P5 wrong for a complete outage?** P5 is for planning-level issues. A complete outage affecting thousands of users is P1 (Critical).
5. **Why does resolution need to match root cause?** "Restart the server" might temporarily fix symptoms but the bug remains. Rolling back the faulty release actually addresses the root cause.
