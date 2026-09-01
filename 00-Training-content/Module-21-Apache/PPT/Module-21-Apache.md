# Apache Web Server
## Module 21 | Sustain Engineering Training | Day 23

---

## Agenda

| # | Topic |
|---|-------|
| 01 | Introduction to Apache HTTP Server |
| 02 | Installation & Auto-Start Configuration |
| 03 | Firewall Configuration for Apache |
| 04 | Directory Structure & Key Files |
| 05 | Configuration File Deep Dive |
| 06 | Hosting Static & Dynamic Content |
| 07 | Virtual Hosts: Name-Based |
| 08 | Virtual Hosts: Port-Based |
| 09 | Logging: Access & Error Logs |
| 10 | Security: .htaccess & Best Practices |
| 11 | Performance & Troubleshooting |
| 12 | Lab & Wrap-up |

---

## What Is Apache HTTP Server?

- Most popular web server in the world (since 1995)
- Open source, maintained by Apache Software Foundation
- Serves static content (HTML, CSS, JS, images)
- Reverse proxy for dynamic content (Java, Node.js, Python)
- Modular architecture: enable only what you need

### Key Facts

| Fact | Detail |
|------|--------|
| Full name | Apache HTTP Server (httpd) |
| Default port | 80 (HTTP), 443 (HTTPS) |
| Config language | Directive-based (.conf files) |
| Process model | Prefork, Worker, or Event MPM |
| Market share | ~30% of all web servers |

**FoodExpress:** Apache serves the static frontend (HTML/CSS/JS) and reverse-proxies API requests to backend services.

---

## Apache vs Other Web Servers

| Feature | Apache | Nginx | IIS |
|---------|--------|-------|-----|
| Platform | Linux, Windows | Linux, Windows | Windows only |
| Config style | .htaccess (per-dir) | Centralized only | GUI-based |
| Concurrency | Process/Thread | Event-driven | Thread-based |
| Static files | Good | Excellent | Good |
| Reverse proxy | Good (mod_proxy) | Excellent | Good |
| .htaccess | Yes | No | No |
| Modules | Dynamic loading | Compile-time | GUI install |

---

## Installation

### Ubuntu/Debian

```bash
# Install Apache
sudo apt update
sudo apt install apache2 -y

# Verify installation
apache2 -v
# Server version: Apache/2.4.54 (Ubuntu)

# Check if running
sudo systemctl status apache2

# Test: Open http://localhost in browser
# Should see "Apache2 Ubuntu Default Page"
```

### CentOS/RHEL

```bash
# Install Apache
sudo yum install httpd -y

# Note: Package is called "httpd" on RHEL-based systems
# Service is also "httpd" not "apache2"
```

---

## Auto-Start Configuration

```bash
# Enable Apache to start on boot
sudo systemctl enable apache2

# Disable auto-start
sudo systemctl disable apache2

# Start Apache
sudo systemctl start apache2

# Stop Apache
sudo systemctl stop apache2

# Restart Apache (stops and starts)
sudo systemctl restart apache2

# Reload configuration without stopping (graceful)
sudo systemctl reload apache2

# Check status
sudo systemctl status apache2
```

### Start vs Reload vs Restart

| Command | Downtime | Use When |
|---------|----------|----------|
| `start` | N/A | Starting for the first time |
| `reload` | None | Changed config files (graceful) |
| `restart` | Brief | Changed modules, major config changes |
| `stop` | Full | Maintenance or troubleshooting |

---

## Firewall Configuration

```bash
# UFW (Ubuntu Firewall)
# List available application profiles
sudo ufw app list
# Available applications:
#   Apache
#   Apache Full
#   Apache Secure

# Allow HTTP only (port 80)
sudo ufw allow 'Apache'

# Allow HTTP and HTTPS (ports 80 and 443)
sudo ufw allow 'Apache Full'

# Allow HTTPS only (port 443)
sudo ufw allow 'Apache Secure'

# Verify
sudo ufw status
# Status: active
# To                   Action      From
# Apache Full          ALLOW       Anywhere

# For specific port
sudo ufw allow 8080/tcp
```

---

## Firewall: firewalld (RHEL/CentOS)

```bash
# Enable HTTP
sudo firewall-cmd --permanent --add-service=http

# Enable HTTPS
sudo firewall-cmd --permanent --add-service=https

# Enable custom port
sudo firewall-cmd --permanent --add-port=8080/tcp

# Reload firewall
sudo firewall-cmd --reload

# List active rules
sudo firewall-cmd --list-all
```

---

## Directory Structure

```
/etc/apache2/                    # Main configuration directory
├── apache2.conf                 # Main config file
├── ports.conf                   # Port definitions
├── envvars                      # Environment variables
├── sites-available/             # Virtual host configs (available)
│   ├── 000-default.conf         # Default HTTP site
│   └── foodexpress.conf         # FoodExpress config
├── sites-enabled/               # Symlinks to active sites
│   └── 000-default.conf -> ../sites-available/000-default.conf
├── mods-available/              # Available modules
├── mods-enabled/                # Active modules (symlinks)
├── conf-available/              # Extra config snippets
└── conf-enabled/                # Active config snippets

/var/www/                        # Web content root
├── html/                        # Default document root
│   └── index.html               # Default page
└── foodexpress/                 # FoodExpress app
    ├── index.html
    ├── css/
    ├── js/
    └── images/

/var/log/apache2/                # Log files
├── access.log                   # Access log
├── error.log                    # Error log
└── other_vhosts_access.log      # Virtual host logs
```

---

## Main Configuration File: apache2.conf

```apache
# /etc/apache2/apache2.conf

# Server root directory
ServerRoot "/etc/apache2"

# Timeout for requests (seconds)
Timeout 300

# Keep-Alive connections
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 5

# Server identity
ServerTokens Prod          # Hide version details
ServerSignature Off        # Don't show server info in error pages

# Default document root permissions
<Directory /var/www/>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>

# Include other configs
IncludeOptional sites-enabled/*.conf
```

---

## Configuration Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| `ServerRoot` | Base directory for config | `/etc/apache2` |
| `Listen` | Port to listen on | `Listen 80` |
| `ServerName` | Server hostname | `foodexpress.in` |
| `DocumentRoot` | Where web files are served from | `/var/www/foodexpress` |
| `DirectoryIndex` | Default page | `index.html index.php` |
| `ErrorLog` | Error log location | `/var/log/apache2/error.log` |
| `CustomLog` | Access log location | `/var/log/apache2/access.log combined` |
| `ServerTokens` | Info in HTTP headers | `Prod` (minimal) |
| `Timeout` | Request timeout (seconds) | `300` |
| `MaxRequestWorkers` | Max concurrent connections | `150` |

---

## Hosting Static Content

### FoodExpress Static Site Setup

```bash
# Create document root
sudo mkdir -p /var/www/foodexpress
sudo chown -R www-data:www-data /var/www/foodexpress

# Create index.html
sudo cat > /var/www/foodexpress/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>FoodExpress</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>Welcome to FoodExpress</h1>
        <nav>
            <a href="/menu">Menu</a>
            <a href="/orders">My Orders</a>
        </nav>
    </header>
    <main id="app"></main>
    <script src="js/app.js"></script>
</body>
</html>
EOF
```

---

## Hosting: Reverse Proxy for APIs

```apache
# Enable proxy modules
# sudo a2enmod proxy proxy_http proxy_balancer lbmethod_byrequests

# In FoodExpress virtual host config:
<VirtualHost *:80>
    ServerName foodexpress.in
    DocumentRoot /var/www/foodexpress

    # Static files served directly by Apache
    <Directory /var/www/foodexpress>
        Options -Indexes
        AllowOverride None
        Require all granted
    </Directory>

    # Proxy API requests to Java backend
    ProxyPass /api/orders http://localhost:8080/api/orders
    ProxyPassReverse /api/orders http://localhost:8080/api/orders

    # Proxy API requests to Node.js backend
    ProxyPass /api/menu http://localhost:3000/api/menu
    ProxyPassReverse /api/menu http://localhost:3000/api/menu
</VirtualHost>
```

---

## Virtual Hosts: Concept

### What Are Virtual Hosts?

> Run multiple websites on a single Apache server, each with its own domain, content, and configuration.

```
                    Apache Server (Single IP: 192.168.1.100)
                              │
              ┌───────────────┼───────────────┐
              │               │               │
     foodexpress.in    admin.foodexpress.in   api.foodexpress.in
     /var/www/fe/      /var/www/admin/        Proxy to :8080
```

### Two Types

| Type | Based On | Example |
|------|----------|---------|
| **Name-based** | Domain name (Host header) | foodexpress.in vs admin.foodexpress.in |
| **Port-based** | Different port numbers | :80 vs :8080 vs :8443 |

---

## Virtual Hosts: Name-Based

```apache
# /etc/apache2/sites-available/foodexpress.conf

# Main site
<VirtualHost *:80>
    ServerName foodexpress.in
    ServerAlias www.foodexpress.in
    DocumentRoot /var/www/foodexpress

    ErrorLog ${APACHE_LOG_DIR}/foodexpress-error.log
    CustomLog ${APACHE_LOG_DIR}/foodexpress-access.log combined
</VirtualHost>

# Admin portal
<VirtualHost *:80>
    ServerName admin.foodexpress.in
    DocumentRoot /var/www/foodexpress-admin

    # Restrict access to internal network
    <Directory /var/www/foodexpress-admin>
        Require ip 10.0.0.0/8
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/admin-error.log
    CustomLog ${APACHE_LOG_DIR}/admin-access.log combined
</VirtualHost>
```

---

## Virtual Hosts: Name-Based Setup

```bash
# Create the config file
sudo nano /etc/apache2/sites-available/foodexpress.conf

# Enable the site
sudo a2ensite foodexpress.conf

# Disable the default site
sudo a2dissite 000-default.conf

# Test configuration for syntax errors
sudo apache2ctl configtest
# Syntax OK

# Reload Apache
sudo systemctl reload apache2

# For local testing, add to /etc/hosts:
echo "127.0.0.1 foodexpress.in admin.foodexpress.in" | sudo tee -a /etc/hosts
```

---

## Virtual Hosts: Port-Based

```apache
# /etc/apache2/ports.conf
Listen 80
Listen 8080
Listen 8443

# /etc/apache2/sites-available/foodexpress-ports.conf

# Public site on port 80
<VirtualHost *:80>
    ServerName foodexpress.in
    DocumentRoot /var/www/foodexpress
</VirtualHost>

# API documentation on port 8080
<VirtualHost *:8080>
    ServerName foodexpress.in
    DocumentRoot /var/www/foodexpress-docs

    <Directory /var/www/foodexpress-docs>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>

# Admin portal on port 8443 (HTTPS)
<VirtualHost *:8443>
    ServerName foodexpress.in
    DocumentRoot /var/www/foodexpress-admin
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/foodexpress.pem
    SSLCertificateKeyFile /etc/ssl/private/foodexpress.key
</VirtualHost>
```

---

## Logging: Access Log

```apache
# Log format definitions
LogFormat "%h %l %u %t \"%r\" %>s %b" common
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined

# Use combined format (recommended)
CustomLog /var/log/apache2/foodexpress-access.log combined
```

### Log Format Variables

| Variable | Meaning | Example |
|----------|---------|---------|
| `%h` | Remote host (IP) | `192.168.1.50` |
| `%t` | Time of request | `[27/Jul/2026:09:15:30 +0530]` |
| `%r` | Request line | `GET /api/menu/items HTTP/1.1` |
| `%>s` | Response status | `200` |
| `%b` | Response size (bytes) | `4523` |
| `%{Referer}i` | Referer header | `https://foodexpress.in/menu` |
| `%{User-Agent}i` | User agent | `Mozilla/5.0...` |

---

## Logging: Access Log Analysis

```bash
# Sample access log entry:
# 192.168.1.50 - - [27/Jul/2026:09:15:30 +0530] "GET /api/menu/items HTTP/1.1" 200 4523

# Count total requests
wc -l /var/log/apache2/foodexpress-access.log

# Count 404 errors
grep '" 404 ' /var/log/apache2/foodexpress-access.log | wc -l

# Top 10 requested URLs
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -10

# Top 10 client IPs
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# Requests per hour
awk '{print $4}' access.log | cut -d: -f1-2 | sort | uniq -c

# Find 5xx server errors
egrep '" 5[0-9]{2} ' access.log

# Response time analysis (if %D is in log format)
awk '{print $NF}' access.log | sort -n | tail -10
```

---

## Logging: Error Log

```apache
# Error log configuration
ErrorLog /var/log/apache2/foodexpress-error.log

# Log levels (from most to least verbose):
# trace8, trace7, ..., trace1, debug, info, notice, warn, error, crit, alert, emerg
LogLevel warn
```

### Common Error Log Entries

```
[Mon Jul 27 09:15:30 2026] [error] [pid 1234] [client 192.168.1.50:42380]
  File does not exist: /var/www/foodexpress/favicon.ico

[Mon Jul 27 09:16:45 2026] [error] [pid 1234] [client 192.168.1.50:42381]
  AH01630: client denied by server configuration: /var/www/foodexpress-admin/

[Mon Jul 27 09:17:00 2026] [error] [pid 1234]
  AH00959: ap_proxy_connect_backend disabling worker for (localhost:8080)
```

---

## Security: .htaccess

### What Is .htaccess?

- Per-directory configuration file
- Overrides main config for that directory
- Changes take effect immediately (no restart needed)
- Must be enabled with `AllowOverride`

```apache
# Enable .htaccess in main config
<Directory /var/www/foodexpress>
    AllowOverride All
</Directory>
```

### Common .htaccess Uses

```apache
# /var/www/foodexpress/.htaccess

# Disable directory listing
Options -Indexes

# Custom error pages
ErrorDocument 404 /404.html
ErrorDocument 500 /500.html

# Redirect HTTP to HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Block access to sensitive files
<FilesMatch "\.(env|log|sql|sh)$">
    Require all denied
</FilesMatch>

# Set caching headers for static assets
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

---

## Security Best Practices

| Practice | Configuration | Why |
|----------|--------------|-----|
| Hide version info | `ServerTokens Prod` | Don't reveal Apache version to attackers |
| Disable directory listing | `Options -Indexes` | Prevent browsing file structure |
| Restrict sensitive files | `FilesMatch` + `Require all denied` | Block `.env`, `.git`, backup files |
| Use HTTPS | `SSLEngine on` + certificates | Encrypt data in transit |
| Disable unnecessary modules | `a2dismod` | Reduce attack surface |
| Set security headers | `Header set X-Frame-Options DENY` | Prevent clickjacking, XSS |
| Limit request size | `LimitRequestBody 10485760` | Prevent upload abuse (10MB) |
| IP whitelisting | `Require ip 10.0.0.0/8` | Restrict admin access to internal IPs |

---

## Security Headers Configuration

```apache
# Enable headers module: sudo a2enmod headers

<VirtualHost *:443>
    ServerName foodexpress.in

    # Security headers
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Content-Security-Policy "default-src 'self'"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

    # Remove server version header
    Header unset Server
</VirtualHost>
```

---

## Performance Tuning

### Multi-Processing Modules (MPM)

| MPM | Model | Best For |
|-----|-------|----------|
| **prefork** | Process per connection | Compatibility (mod_php) |
| **worker** | Thread per connection | General purpose, moderate load |
| **event** | Async event-driven | High concurrency, keep-alive |

```apache
# /etc/apache2/mods-available/mpm_event.conf
<IfModule mpm_event_module>
    StartServers             2
    MinSpareThreads         25
    MaxSpareThreads         75
    ThreadLimit             64
    ThreadsPerChild         25
    MaxRequestWorkers      150
    MaxConnectionsPerChild   0
</IfModule>
```

```bash
# Switch MPM
sudo a2dismod mpm_prefork
sudo a2enmod mpm_event
sudo systemctl restart apache2
```

---

## Performance: Caching & Compression

```apache
# Enable compression (mod_deflate)
# sudo a2enmod deflate
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css text/javascript
    AddOutputFilterByType DEFLATE application/javascript application/json
    AddOutputFilterByType DEFLATE image/svg+xml
</IfModule>

# Enable browser caching (mod_expires)
# sudo a2enmod expires
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/html "access plus 1 hour"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
</IfModule>

# Enable HTTP/2
# sudo a2enmod http2
Protocols h2 h2c http/1.1
```

---

## Troubleshooting

### Common Issues & Solutions

| Symptom | Check | Solution |
|---------|-------|---------|
| Apache won't start | `journalctl -u apache2` | Fix config errors: `apache2ctl configtest` |
| Port already in use | `sudo lsof -i :80` | Stop conflicting service or change port |
| 403 Forbidden | File permissions | `sudo chown -R www-data:www-data /var/www/` |
| 404 Not Found | DocumentRoot path | Verify path exists and is correct in config |
| 502 Bad Gateway | Backend service down | Check if backend (Java/Node) is running |
| Slow performance | Access/error logs | Check MaxRequestWorkers, enable compression |

```bash
# Diagnostic commands
apache2ctl configtest     # Syntax check
apache2ctl -S             # Show virtual host config
apache2ctl -M             # List loaded modules
apachectl graceful        # Graceful restart
tail -f /var/log/apache2/error.log   # Watch errors live
```

---

## Troubleshooting: Step-by-Step

```bash
# Step 1: Check if Apache is running
sudo systemctl status apache2

# Step 2: Check error log
sudo tail -50 /var/log/apache2/error.log

# Step 3: Test configuration
sudo apache2ctl configtest

# Step 4: Check which ports Apache is listening on
sudo ss -tlnp | grep apache2

# Step 5: Check file permissions
ls -la /var/www/foodexpress/
# Should be owned by www-data:www-data

# Step 6: Test from command line
curl -I http://localhost
# Check response headers and status code

# Step 7: Check module is loaded
apache2ctl -M | grep proxy
# If missing: sudo a2enmod proxy proxy_http

# Step 8: Check virtual host resolution
apache2ctl -S
```

---

## Apache Modules for FoodExpress

| Module | Purpose | Enable Command |
|--------|---------|---------------|
| `mod_rewrite` | URL rewriting, redirects | `a2enmod rewrite` |
| `mod_proxy` | Reverse proxy | `a2enmod proxy proxy_http` |
| `mod_ssl` | HTTPS support | `a2enmod ssl` |
| `mod_headers` | Custom HTTP headers | `a2enmod headers` |
| `mod_deflate` | Gzip compression | `a2enmod deflate` |
| `mod_expires` | Browser caching | `a2enmod expires` |
| `mod_security` | Web Application Firewall | Install separately |
| `mod_status` | Server status page | `a2enmod status` |

---

## SSL/TLS: HTTPS Configuration

### Setting Up HTTPS for FoodExpress

```bash
# Enable SSL module
sudo a2enmod ssl

# Option 1: Self-signed certificate (development only)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/foodexpress.key \
  -out /etc/ssl/certs/foodexpress.crt \
  -subj "/CN=foodexpress.in"

# Option 2: Let's Encrypt (production -- free, auto-renewing)
sudo apt install certbot python3-certbot-apache -y
sudo certbot --apache -d foodexpress.in -d www.foodexpress.in
```

```apache
# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName foodexpress.in
    DocumentRoot /var/www/foodexpress

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/foodexpress.crt
    SSLCertificateKeyFile /etc/ssl/private/foodexpress.key

    # Modern TLS configuration
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite HIGH:!aNULL:!MD5
</VirtualHost>
```

---

## Apache in the FoodExpress Architecture

### How Apache Fits in Production

```
                Internet
                   │
              ┌────▼────┐
              │  Apache  │ ──── Static files (HTML/CSS/JS/images)
              │  (Port   │
              │   80/443)│ ──── /api/menu ────> Node.js :3000
              │          │
              │  Reverse │ ──── /api/orders ──> Java :8080
              │  Proxy   │
              │          │ ──── /api/payments > Java :8081
              └──────────┘
```

| What Apache Handles | What Backend Handles |
|--------------------|---------------------|
| SSL termination | Business logic |
| Static file serving | API processing |
| Compression (gzip) | Database queries |
| Caching headers | Authentication logic |
| Load balancing | Data validation |
| Security headers | Response generation |
| Access logging | Application logging |

**Sustain insight:** Most production issues start with Apache logs (access patterns, 5xx errors, slow responses) before diving into backend logs.

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Apache basics | Web server serving static files + reverse proxy for APIs |
| Auto-start | `systemctl enable apache2` to start on boot |
| Firewall | `ufw allow 'Apache Full'` for HTTP + HTTPS |
| Directory structure | Config in `/etc/apache2/`, content in `/var/www/`, logs in `/var/log/apache2/` |
| Virtual hosts | Name-based (domain) or port-based; use `a2ensite` to enable |
| Logging | Combined format for access logs; `tail -f` for live monitoring |
| Security | Hide version, disable indexes, use .htaccess, add security headers |
| Performance | Use event MPM, enable compression, set caching headers |
| Troubleshooting | `configtest` first, then error logs, then permissions, then modules |

> **Next: Module 22 -- Microservices & API**
