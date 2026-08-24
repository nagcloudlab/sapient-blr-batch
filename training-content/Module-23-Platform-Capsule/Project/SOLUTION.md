# Platform Capsule Project -- Trainer Solutions & Hints
## Module 23 | Day 26

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Order Service Startup | Java 11->17, port 8082->8081, db-server->localhost, Xmx 64m->512m, chmod 644->755, systemd path | Students fix the port but forget the DB host. They also often miss the chmod issue | Ask: "What's the difference between chmod 644 and 755 on a directory?" (execute = traverse) |
| 2 | Fix Disk & Log Rotation | /var/logs/ -> /var/log/, -mtime -30 -> +30, add -type f, cron 0 * 2 * * -> 0 2 * * *, add compress | Students confuse -mtime +30 (older than) with -30 (newer than). Draw a timeline | Ask: "What does -mtime -30 mean vs +30?" (-30 = modified within last 30 days = recent files!) |
| 3 | Fix API Timeout Chain | readFileSync->readFile, add timeout: 5000, add circuit breaker config, add process.on handlers, pool 2->15 | Students make getMenuData async but forget to await it in the route handler | Ask: "If readFileSync takes 8 seconds, how many requests can Node handle per 8 seconds?" (One!) |
| 4 | Post-Mortem | Must include: timeline, root cause, fix, prevention measures. Should suggest monitoring alerts for JVM heap | Students write what they did but skip prevention. Push them on "how do we prevent this?" | Ask: "If this happens again in 3 months, would your monitoring catch it before customers notice?" |

---

## Key Discussion Points

1. Why did we have 3 incidents at the same time? (Deployment changed configs + lack of monitoring)
2. How would you prioritize these incidents? (P1 first -- revenue impact)
3. What monitoring would have prevented each incident?
   - Incident 1: JVM memory alert, port conflict check in CI/CD
   - Incident 2: Disk space alert at 80%, logrotate validation
   - Incident 3: Response time SLO alert, circuit breaker dashboard
4. Why is `-mtime -30` dangerous in a cleanup script? (Deletes RECENT files, not old ones)
5. Why does `readFileSync` kill Node.js performance? (Single-threaded event loop)

---

## Incident 1: Complete Fix Summary

| Bug | File | Line/Section | Fix |
|-----|------|-------------|-----|
| Wrong Java version | order-service-start.sh | JAVA_HOME | java-11 -> java-17 |
| Heap too small | order-service-start.sh | JVM_OPTS | -Xmx64m -> -Xmx512m |
| Wrong permissions | order-service-start.sh | chmod | 644 -> 755 |
| Wrong port | application.yml | server.port | 8082 -> 8081 |
| Wrong DB host | application.yml | datasource.url | db-server -> localhost |
| Wrong systemd path | order-service-start.sh | comment | /opt/foodexpress/services/order/ -> /opt/foodexpress/order-service/ |

## Incident 2: Complete Fix Summary

| Bug | File | Line/Section | Fix |
|-----|------|-------------|-----|
| Wrong log path | foodexpress-logrotate.conf | path | /var/logs/ -> /var/log/ |
| Wrong find flags | disk-cleanup.sh | find command | Add -type f, change -mtime -30 to +30 |
| Wrong cron format | disk-cleanup.sh | comment | 0 * 2 * * -> 0 2 * * * |
| Missing compression | foodexpress-logrotate.conf | directives | Add compress + delaycompress |
| DEBUG in production | application.yml | logging.level | DEBUG -> INFO |

## Incident 3: Complete Fix Summary

| Bug | File | Line/Section | Fix |
|-----|------|-------------|-----|
| Sync file read | restaurant-service.js | getMenuData() | readFileSync -> readFile (Promise) |
| No timeout | application.yml | restaurant-service | Add timeout: 5000 |
| No circuit breaker | application.yml | resilience4j | Add circuit breaker config |
| No error handlers | restaurant-service.js | bottom | Add uncaughtException + unhandledRejection handlers |
| Pool too small | application.yml | hikari | maximum-pool-size: 2 -> 15 |
