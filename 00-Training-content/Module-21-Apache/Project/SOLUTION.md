# Apache Web Server -- Trainer Solutions & Hints
## Module 21 | Day 23

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Virtual Host | Match DocumentRoot and Directory paths, add ProxyPassReverse, disable Indexes, enable AllowOverride, add logs | Students fix the DocumentRoot but forget the Directory block must match. Also miss ProxyPassReverse | Ask: "What happens if your backend sends a redirect? Without ProxyPassReverse, where does the user end up?" |
| 2 | Fix .htaccess | Add RewriteEngine On, block all sensitive file types, restrict CORS, add security headers | Students add RewriteEngine but forget AllowOverride must be enabled in the virtual host. Also, many only block `.env` and miss `.git` | Ask: "What if someone navigates to `/.git/config`? What sensitive info could they find?" |
| 3 | Fix Logging | Use combined format, set LogLevel to warn, add logrotate, separate proxy logs, add %D | Students don't know about logrotate. Show `/etc/logrotate.d/apache2` and explain rotation | Ask: "How big would your logs be after 1 year with LogLevel debug?" |
| 4 | Fix Performance | Enable KeepAlive, switch to event MPM, enable mod_deflate, increase MaxRequestWorkers | Students enable compression for all content types, including already-compressed ones (JPEG, PNG). Only compress text | Ask: "Should you gzip a JPEG? What about an SVG?" (SVG yes, JPEG no) |
| 5 | Multi-Site | Name-based for main + admin, port-based for docs. Remember ports.conf for port-based | Students create port-based vhosts but forget to add `Listen 8080` to ports.conf | Remind: "Apache won't listen on a port unless you tell it to" |

---

## Key Discussion Points

1. Why is `Options -Indexes` critical for production? (Prevents directory browsing)
2. What is the difference between `reload` and `restart`? (Reload is graceful, no downtime)
3. When would you use .htaccess vs main config? (Main config preferred for performance; .htaccess when you don't have root access)
4. Why use `combined` log format? (Referer and User-Agent are essential for debugging and analytics)
5. What does `ProxyPassReverse` do? (Rewrites redirect headers from backend to use the proxy URL)
