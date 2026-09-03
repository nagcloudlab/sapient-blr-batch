# Apache Web Server -- Submission Checklist
## Module 21 | Day 23

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Virtual Host: ServerAlias for www subdomain | [ ] |
| 2 | Virtual Host: DocumentRoot matches actual path | [ ] |
| 3 | Virtual Host: Directory block path matches DocumentRoot | [ ] |
| 4 | Virtual Host: Options -Indexes (no directory listing) | [ ] |
| 5 | Virtual Host: AllowOverride All (for .htaccess) | [ ] |
| 6 | Virtual Host: ProxyPassReverse for both API endpoints | [ ] |
| 7 | Virtual Host: ErrorLog and CustomLog configured | [ ] |
| 8 | .htaccess: RewriteEngine On present | [ ] |
| 9 | .htaccess: Sensitive file extensions blocked (.env, .git, .sql, .log, .sh, .bak) | [ ] |
| 10 | .htaccess: Cache expiration rules set per content type | [ ] |
| 11 | .htaccess: CORS restricted to FoodExpress domain | [ ] |
| 12 | .htaccess: Security headers configured | [ ] |
| 13 | Logging: Combined format used | [ ] |
| 14 | Logging: LogLevel set to warn for production | [ ] |
| 15 | Performance: KeepAlive enabled | [ ] |
| 16 | Performance: Event MPM or worker MPM configured | [ ] |
| 17 | Performance: Compression enabled for text content | [ ] |
| 18 | Configuration passes `apache2ctl configtest` | [ ] |

---

## Self-Check Questions

1. **What is the difference between `sites-available` and `sites-enabled`?** Available has configs; enabled has symlinks to active ones. Use `a2ensite`/`a2dissite`.
2. **Why should you never set `Options Indexes` in production?** It lets anyone browse your file structure and discover sensitive files.
3. **What does `ProxyPassReverse` do?** It rewrites redirect response headers from the backend to use the proxy URL.
4. **When should you use `reload` vs `restart`?** Reload is graceful (no downtime), use for config changes. Restart stops and starts, use for module changes.
5. **What is the purpose of `AllowOverride All`?** It allows `.htaccess` files to override server configuration for that directory.
6. **Why set `ServerTokens Prod`?** It hides the Apache version from HTTP headers, making it harder for attackers to target known vulnerabilities.
7. **What log format should you use in production?** `combined` -- includes Referer and User-Agent, essential for debugging.
8. **Why restrict CORS origin?** `Access-Control-Allow-Origin: *` lets any website access your resources, enabling data theft.
9. **Should you compress JPEG images?** No -- they're already compressed. Compressing them wastes CPU for no benefit.
10. **How do you check if a module is loaded?** `apache2ctl -M | grep module_name`
