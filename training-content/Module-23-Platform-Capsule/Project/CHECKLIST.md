# Platform Capsule Project -- Submission Checklist
## Module 23 | Day 26

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Startup script: Java 17 path (not Java 11) | [ ] |
| 2 | Startup script: Heap size >= 512m | [ ] |
| 3 | Startup script: Log directory chmod 755 | [ ] |
| 4 | Startup script: Correct systemd ExecStart path in comments | [ ] |
| 5 | application.yml: Port 8081 (not 8082) | [ ] |
| 6 | application.yml: DB host localhost (not db-server) | [ ] |
| 7 | application.yml: Connection pool >= 10 | [ ] |
| 8 | application.yml: Log level INFO (not DEBUG) | [ ] |
| 9 | application.yml: RestTemplate timeout configured | [ ] |
| 10 | application.yml: Circuit breaker configured | [ ] |
| 11 | logrotate: Path /var/log/ (not /var/logs/) | [ ] |
| 12 | logrotate: compress + delaycompress present | [ ] |
| 13 | cleanup script: find uses -type f and -mtime +30 | [ ] |
| 14 | cleanup script: Correct cron schedule (0 2 * * *) | [ ] |
| 15 | restaurant-service.js: Async file read (not readFileSync) | [ ] |
| 16 | restaurant-service.js: uncaughtException handler | [ ] |
| 17 | restaurant-service.js: unhandledRejection handler | [ ] |
| 18 | Post-mortem: Timeline included | [ ] |
| 19 | Post-mortem: Root cause identified | [ ] |
| 20 | Post-mortem: Prevention measures listed | [ ] |

---

## Self-Check Questions

1. **Why does chmod 644 on a directory prevent file creation inside it?** Without the execute bit (x), the OS cannot traverse into the directory. 755 adds execute for owner, group, and others.
2. **What does `-mtime -30` actually match?** Files modified within the LAST 30 days (i.e., recent files). Using `-mtime +30` matches files OLDER than 30 days.
3. **What is the cron format?** `minute hour day-of-month month day-of-week`. So `0 2 * * *` means "at 2:00 AM every day."
4. **Why is readFileSync dangerous in Node.js?** Node.js is single-threaded. A synchronous read blocks the entire event loop, preventing ALL other requests from being processed.
5. **What is a circuit breaker?** A pattern that monitors failures and "opens" (stops making calls) when failures exceed a threshold, returning a fallback response instead of hanging.
6. **Why set connection pool size > 2?** Each concurrent database query needs a connection. With pool=2, the 3rd concurrent query must wait, creating a bottleneck under any real traffic.
7. **Why is DEBUG logging dangerous in production?** It generates 10-100x more log data than INFO, filling disks and degrading I/O performance.
8. **What should a post-mortem include?** Timeline, impact, root cause, fix applied, and prevention measures to avoid recurrence.
9. **Why does a port conflict cause a service to fail?** Only one process can bind to a port. If Payment Service already uses 8082, Order Service cannot start on the same port.
10. **How does logrotate's `delaycompress` help?** It waits to compress the most recent rotated file, which may still be written to if the process holds an old file handle.
