# Observability -- Submission Checklist
## Module 32 | Day 36

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Prometheus: order-service metrics_path is `/actuator/prometheus` | [ ] |
| 2 | Prometheus: payment-service target is `payment-service:8080` | [ ] |
| 3 | Prometheus: menu-service job_name added with correct target | [ ] |
| 4 | Grafana: Error Rate panel uses `rate()` for percentage calculation | [ ] |
| 5 | Grafana: Orders/min panel multiplies by 60 (not divides) | [ ] |
| 6 | Grafana: P99 Latency uses `histogram_quantile(0.99, ...)` | [ ] |
| 7 | Alerts: HighErrorRate threshold is 0.01 (1%) | [ ] |
| 8 | Alerts: HighLatency `for` duration is 5m (not 0m) | [ ] |
| 9 | Alerts: HighCPU threshold is 90% (not 50%) | [ ] |
| 10 | PromQL: Three golden signal queries written | [ ] |
| 11 | Runbook: HighErrorRate runbook with specific steps | [ ] |

---

## Self-Check Questions

1. **Why use `rate()` with counters?** Counters only go up. Without `rate()`, you see ever-increasing numbers. `rate()` calculates the per-second change.
2. **Why is `for: 0m` dangerous?** A single spike triggers the alert immediately. With `for: 5m`, the condition must persist for 5 minutes, filtering out transient spikes.
3. **Why is p99 more useful than average?** Average hides outliers. If 99% of requests take 100ms and 1% take 10s, the average is ~200ms but the user experience for that 1% is terrible.
4. **Why set CPU alert at 90% not 50%?** CPU at 60% is normal during peak hours. Alerting at 50% causes constant noise. 90% indicates real saturation that needs attention.
