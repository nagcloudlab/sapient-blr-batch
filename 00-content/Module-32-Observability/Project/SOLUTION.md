# Observability -- Trainer Solutions & Hints
## Module 32 | Day 36

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Prometheus Config | Correct target `payment-service:8080`, add menu-service job, fix metrics_path to `/actuator/prometheus` | Students fix the target but use the wrong port. Spring Boot typically exposes metrics on the same port as the app (8080), not a separate metrics port | Ask: "How do you verify Prometheus is scraping a target?" (Check `/targets` page or `up{job="..."}` metric) |
| 2 | Fix Grafana Dashboard | Add `rate()` around counters, change `/ 60` to `* 60`, use `histogram_quantile(0.99, ...)` | Students add rate() but forget it needs a time range like `[5m]`. Also confuse average with percentile. Show them a distribution where average is 100ms but p99 is 2s | Ask: "If 99% of orders take 100ms and 1% take 10s, what is the average? What is p99?" (avg ~200ms, p99=10s) |
| 3 | Fix Alert Rules | Threshold 0.01 (1%), `for: 5m`, CPU threshold 90% | Students set the error threshold to 0 (any error triggers alert). Discuss that some errors are normal (client errors, timeouts). 1% is industry standard | Ask: "If you set the error alert to 0%, how many times per day will you get paged?" (Constantly) |
| 4 | Write PromQL | Rate, histogram_quantile, saturation queries | Students write queries that return too many time series. Use `by()` or `sum()` to aggregate | Ask: "What is the difference between `rate()` and `increase()`?" (rate = per-second, increase = total over range) |
| 5 | Design Runbook | Steps: verify alert, check dashboard, review traces, check recent changes, escalate/fix | Students write vague runbooks like "check logs". Be specific: which logs, what to search for, what dashboard to open | Ask: "If a new engineer gets this alert at 3 AM, can they follow your runbook without calling you?" |

---

## Key Discussion Points

1. Why pull-based (Prometheus) vs push-based (StatsD)? (Pull: central control; Push: fire-and-forget)
2. What is the difference between counter and gauge? Why does it matter for `rate()`?
3. Why alert on symptoms (error rate) not causes (CPU)? (CPU high might be fine; errors always matter)
4. What is alert fatigue and why is it dangerous? (Team ignores alerts; real incidents missed)
5. How do the three pillars complement each other during incident investigation?
6. When would you use DataDog vs Prometheus+Grafana? (Cost vs capability vs team size)
