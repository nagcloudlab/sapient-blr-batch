# Apache Web Server -- Lab Exercises
## Module 21 | Day 23

---

## Client Email

```
From: vikram.patel@foodexpress.in
To: sustain-engineering@team.com
Subject: Apache Configuration Issues on Production
Date: 2026-08-01

Team,

Our Apache web server serving the FoodExpress frontend has several
configuration problems:

1. The virtual host config has errors causing 500 errors
2. Security headers are missing or misconfigured
3. Logging is not capturing useful information
4. Performance is poor (no compression or caching)
5. The .htaccess file has bugs

Please review and fix all configuration files.

-- Vikram Patel, Infrastructure Lead, FoodExpress
```

---

## Lab 1: Fix the Virtual Host Configuration (7 bugs)

### Buggy Configuration

```apache
# /etc/apache2/sites-available/foodexpress.conf

<VirtualHost *:80>
    ServerName foodexpress.in
    # Bug 1: Missing ServerAlias for www subdomain

    # Bug 2: DocumentRoot path doesn't exist
    DocumentRoot /var/www/foodexpress-app

    # Bug 3: Directory block doesn't match DocumentRoot
    <Directory /var/www/foodexpress>
        Options Indexes FollowSymLinks    # Bug 4: Indexes should be disabled
        AllowOverride None                # Bug 5: Should be All for .htaccess
        Require all granted
    </Directory>

    # Reverse proxy for API
    # Bug 6: ProxyPassReverse is missing
    ProxyPass /api/orders http://localhost:8080/api/orders
    ProxyPass /api/menu http://localhost:3000/api/menu

    # Bug 7: No error/access log configured
</VirtualHost>
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | `www.foodexpress.in` is not configured as an alias | Users typing `www.` get the default page or 404 |
| 2 | DocumentRoot points to `/var/www/foodexpress-app` but files are in `/var/www/foodexpress` | 403 Forbidden or 404 for all pages |
| 3 | `<Directory>` path doesn't match DocumentRoot | Permission rules don't apply; may get 403 |
| 4 | `Options Indexes` allows directory listing, exposing file structure | Security risk: attackers can browse all files |
| 5 | `AllowOverride None` prevents `.htaccess` from working | Custom error pages, rewrites, and security rules in .htaccess are ignored |
| 6 | `ProxyPassReverse` is missing for both API proxies | Backend redirect URLs won't be rewritten; broken redirects |
| 7 | No `ErrorLog` or `CustomLog` directives | No visibility into errors or traffic for this virtual host |

### Fixed Configuration

```apache
<VirtualHost *:80>
    ServerName foodexpress.in
    ServerAlias www.foodexpress.in

    DocumentRoot /var/www/foodexpress

    <Directory /var/www/foodexpress>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ProxyPass /api/orders http://localhost:8080/api/orders
    ProxyPassReverse /api/orders http://localhost:8080/api/orders

    ProxyPass /api/menu http://localhost:3000/api/menu
    ProxyPassReverse /api/menu http://localhost:3000/api/menu

    ErrorLog ${APACHE_LOG_DIR}/foodexpress-error.log
    CustomLog ${APACHE_LOG_DIR}/foodexpress-access.log combined
</VirtualHost>
```

### Checkpoint
- [ ] `ServerAlias www.foodexpress.in` added
- [ ] DocumentRoot matches actual file path
- [ ] `<Directory>` path matches DocumentRoot
- [ ] `Options -Indexes` disables directory listing
- [ ] `AllowOverride All` enables .htaccess
- [ ] `ProxyPassReverse` added for both API endpoints
- [ ] Error and access logs configured

---

## Lab 2: Fix the .htaccess File (6 bugs)

### Buggy .htaccess

```apache
# /var/www/foodexpress/.htaccess

# Bug 1: Redirect HTTP to HTTPS (RewriteEngine not enabled)
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Bug 2: Custom error pages point to wrong paths
ErrorDocument 404 /errors/not-found.html
ErrorDocument 500 /errors/server-error.html

# Bug 3: Blocking access to sensitive files (incomplete pattern)
<FilesMatch "\.(env)$">
    Require all denied
</FilesMatch>

# Bug 4: Cache headers missing expiration values
<IfModule mod_expires.c>
    ExpiresActive On
</IfModule>

# Bug 5: CORS header too permissive
Header set Access-Control-Allow-Origin "*"

# Bug 6: Missing security headers
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | `RewriteEngine On` is missing before the RewriteCond/RewriteRule | Rewrite rules are silently ignored; HTTP traffic not redirected to HTTPS |
| 2 | Error pages path `/errors/` may not exist; should be `/404.html` and `/500.html` | Users see default Apache error pages instead of branded ones |
| 3 | Only blocks `.env` files; should also block `.git`, `.log`, `.sql`, `.sh`, `.bak` | Sensitive files like `.git/config` or `.sql` dumps are accessible |
| 4 | No actual expiration rules for file types | Browser never caches assets; every page load re-downloads CSS/JS/images |
| 5 | `*` allows any domain to access FoodExpress resources | Cross-origin security risk; other sites can embed FoodExpress content |
| 6 | No X-Frame-Options, X-Content-Type-Options, or other security headers | Vulnerable to clickjacking, MIME sniffing, and XSS attacks |

### Fixed .htaccess

```apache
# Enable mod_rewrite
RewriteEngine On

# Redirect HTTP to HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Custom error pages
ErrorDocument 404 /404.html
ErrorDocument 500 /500.html

# Block access to sensitive files
<FilesMatch "\.(env|git|log|sql|sh|bak|swp)$">
    Require all denied
</FilesMatch>

# Block access to hidden files and directories
<IfModule mod_rewrite.c>
    RewriteRule (^\.|/\.) - [F]
</IfModule>

# Cache headers
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/html "access plus 1 hour"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>

# CORS - restrict to FoodExpress domains
Header set Access-Control-Allow-Origin "https://foodexpress.in"

# Security headers
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

### Checkpoint
- [ ] `RewriteEngine On` is present
- [ ] Error document paths are correct
- [ ] All sensitive file extensions are blocked
- [ ] Cache expiration rules are set for each content type
- [ ] CORS origin is restricted to FoodExpress domain
- [ ] Security headers (X-Frame-Options, etc.) are configured

---

## Lab 3: Fix the Logging Configuration (5 bugs)

### Buggy Log Configuration

```apache
# Bug 1: Using "common" format instead of "combined"
CustomLog /var/log/apache2/foodexpress-access.log common

# Bug 2: Error log level too verbose for production
LogLevel debug

# Bug 3: No log rotation configured
# (logs grow indefinitely)

# Bug 4: Proxy error logs not separated
# All errors go to one file

# Bug 5: No request duration in log format
# Can't identify slow requests
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | `common` format lacks Referer and User-Agent; `combined` provides more useful data | Can't track where traffic comes from or what browsers are used |
| 2 | `debug` level generates massive log volume in production | Disk fills up quickly; important errors buried in noise |
| 3 | No `logrotate` configuration; logs grow forever | Eventually fills disk and crashes the server |
| 4 | Proxy errors mixed with application errors | Hard to debug proxy vs application issues |
| 5 | No `%D` (microseconds) or `%T` (seconds) in log format | Can't identify slow requests or measure performance |

### Checkpoint
- [ ] Log format changed to `combined` (or custom with more fields)
- [ ] Log level set to `warn` for production
- [ ] logrotate configuration created for Apache logs
- [ ] Proxy errors go to a separate log file
- [ ] Request duration (`%D` or `%T`) added to log format

---

## Lab 4: Performance Configuration (4 bugs)

### Buggy Performance Config

```apache
# Bug 1: KeepAlive disabled
KeepAlive Off

# Bug 2: Using prefork MPM (process-per-connection)
# for a high-traffic site

# Bug 3: No compression enabled
# All responses sent uncompressed

# Bug 4: MaxRequestWorkers too low
<IfModule mpm_prefork_module>
    MaxRequestWorkers 25
</IfModule>
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | KeepAlive Off forces a new TCP connection for every request | Slow page loads (CSS, JS, images each need a new connection) |
| 2 | prefork MPM uses one process per connection (high memory) | 100 connections = 100 processes; server runs out of memory |
| 3 | No mod_deflate compression | Bandwidth wasted; pages take longer to load |
| 4 | MaxRequestWorkers 25 means only 25 simultaneous connections | Under load, users get "connection refused" or timeouts |

### Checkpoint
- [ ] KeepAlive enabled with reasonable timeout (5s)
- [ ] Event MPM configured (or worker MPM)
- [ ] gzip compression enabled for text-based content
- [ ] MaxRequestWorkers increased appropriately (150+)

---

## Bonus Challenge: Multi-Site Configuration

Configure Apache to host three FoodExpress services:

1. **Main site** (`foodexpress.in` on port 80) -- Serves static frontend
2. **Admin portal** (`admin.foodexpress.in` on port 80) -- Restricted to IP `10.0.0.0/8`
3. **API docs** (port 8080) -- Port-based virtual host serving Swagger UI

Create all three virtual host configurations, enable them, and verify with `apache2ctl configtest`.
