# Step 13: Performance & Troubleshooting

## Objective
Tune Apache for performance, monitor server health, and troubleshoot common issues.

---

## Part 1: MPM -- Multi-Processing Modules

Apache's process/thread model. Check which MPM is active:

```bash
apache2ctl -V | grep MPM
```

Check the config:

```bash
cat /etc/apache2/mods-enabled/mpm_*.conf
```

### Three MPMs

| MPM | Model | Best For |
|-----|-------|----------|
| `prefork` | 1 process per connection | Stability, PHP compatibility |
| `worker` | Threads within processes | Better memory, moderate traffic |
| `event` | Async event-driven | High concurrency, modern default |

### Key Tuning Parameters

```bash
grep -A 10 "<IfModule mpm_" /etc/apache2/mods-available/mpm_event.conf
```

| Directive | What It Controls |
|-----------|-----------------|
| `StartServers` | Processes started on boot |
| `MinSpareThreads` | Minimum idle threads ready |
| `MaxSpareThreads` | Maximum idle threads |
| `ThreadsPerChild` | Threads per process |
| `MaxRequestWorkers` | **Total concurrent connections -- most important** |
| `MaxConnectionsPerChild` | Requests before process recycles (prevents memory leaks) |

Check current processes:

```bash
ps aux | grep apache2 | grep -v grep | wc -l
```

---

## Part 2: mod_status -- Server Monitoring

```bash
sudo a2enmod status
sudo systemctl reload apache2
```

### Create Status Endpoint

```bash
sudo nano /etc/apache2/mods-enabled/status.conf
```

```apache
<Location "/server-status">
    SetHandler server-status
    Require local
</Location>
```

```bash
sudo systemctl reload apache2
curl http://localhost/server-status
```

### Machine-readable Version

```bash
curl http://localhost/server-status?auto
```

### Key Metrics

```bash
curl -s http://localhost/server-status?auto | grep -E "Total Accesses|Total kBytes|Uptime|BusyWorkers|IdleWorkers|ReqPerSec"
```

| Metric | What It Tells You |
|--------|------------------|
| `Total Accesses` | Total requests since start |
| `ReqPerSec` | Requests per second |
| `BusyWorkers` | Threads handling requests now |
| `IdleWorkers` | Threads waiting for requests |
| `Uptime` | Seconds since last restart |

**In production:** If `BusyWorkers` is near `MaxRequestWorkers`, your server is at capacity.

---

## Part 3: Compression -- mod_deflate

### Before Compression

```bash
curl -s -o /dev/null -w "Size: %{size_download} bytes\n" http://localhost/
```

### Enable

```bash
sudo a2enmod deflate
sudo systemctl reload apache2
```

### Test

```bash
curl -s -o /dev/null -w "Size: %{size_download} bytes\n" -H "Accept-Encoding: gzip" http://localhost/
```

Smaller. Check header:

```bash
curl -I -H "Accept-Encoding: gzip" http://localhost/
```

`Content-Encoding: gzip` -- compression working.

### What Gets Compressed

```bash
cat /etc/apache2/mods-enabled/deflate.conf
```

Default: HTML, CSS, JS, XML, text. Binary files (images, PDFs) are skipped.

---

## Part 4: Caching Headers -- mod_expires

```bash
sudo a2enmod expires
sudo systemctl reload apache2
```

Add to FoodExpress `.htaccess`:

```apache
# Browser caching
ExpiresActive On
ExpiresByType text/css "access plus 1 week"
ExpiresByType application/javascript "access plus 1 week"
ExpiresByType image/png "access plus 1 month"
ExpiresByType image/jpeg "access plus 1 month"
ExpiresByType text/html "access plus 0 seconds"
```

```bash
curl -I http://localhost/style.css
```

`Expires` and `Cache-Control` headers appear. HTML = no cache (always fresh), CSS = 1 week.

---

## Part 5: Troubleshooting Common Issues

### Issue 1: Apache Won't Start

```bash
sudo systemctl stop apache2
sudo systemctl start apache2 2>&1
```

If it fails:

```bash
sudo journalctl -u apache2 --no-pager -n 20
sudo apache2ctl configtest
```

Common causes:
- Syntax error --> `configtest` shows it
- Port already in use --> `sudo ss -tlnp | grep :80`
- Missing module --> error log names the module

#### Simulate Port Conflict

```bash
sudo apt install -y netcat-openbsd
sudo nc -l 8081 &
echo "Listen 8081" | sudo tee -a /etc/apache2/ports.conf
sudo systemctl reload apache2 2>&1
sudo journalctl -u apache2 --no-pager -n 5    # "Address already in use"
```

Fix:

```bash
sudo kill %1
sudo sed -i '/Listen 8081/d' /etc/apache2/ports.conf
sudo systemctl reload apache2
```

### Issue 2: 403 Forbidden

Check in this order:

```bash
# 1. File exists?
ls -la /var/www/foodexpress/index.html

# 2. Permissions -- www-data can read?
sudo -u www-data cat /var/www/foodexpress/index.html

# 3. Directory permissions -- all parents traversable?
namei -l /var/www/foodexpress/index.html

# 4. .htaccess blocking?
cat /var/www/foodexpress/.htaccess

# 5. <Directory> block denying?
grep -A 4 "Directory /var/www" /etc/apache2/apache2.conf
```

#### Simulate and Fix

```bash
sudo chmod 000 /var/www/foodexpress/index.html
curl http://localhost/                          # 403 Forbidden

sudo chmod 644 /var/www/foodexpress/index.html
curl -I http://localhost/                       # 200 OK
```

### Issue 3: 500 Internal Server Error

```bash
sudo tail -20 /var/log/apache2/error.log
```

Common causes: bad `.htaccess` syntax, missing module, CGI script error.

#### Simulate

```bash
echo "InvalidDirective On" | sudo tee /var/www/foodexpress/uploads/.htaccess
curl http://localhost/uploads/                   # 500 error
sudo tail -1 /var/log/apache2/error.log         # Shows the bad directive
```

Fix:

```bash
echo "Options -Indexes
Require all denied" | sudo tee /var/www/foodexpress/uploads/.htaccess
```

### Issue 4: Slow Responses

```bash
# Server load
uptime
free -h
df -h

# Apache workers
curl -s http://localhost/server-status?auto | grep -E "Busy|Idle|ReqPerSec"

# Connection queue
sudo ss -s

# Slow endpoints (if %D enabled in log format)
sudo awk '{print $(NF-1), $7}' /var/log/apache2/foodexpress-access.log | sort -rn | head -5
```

---

## Part 6: Load Testing

```bash
sudo apt install -y apache2-utils
```

### 100 requests, 10 concurrent

```bash
ab -n 100 -c 10 http://localhost/
```

Key output:

| Metric | Meaning |
|--------|---------|
| `Requests per second` | Throughput |
| `Time per request` | Avg response time |
| `Failed requests` | Should be 0 |
| `Percentage of requests served within X ms` | Latency percentiles |

### 1000 requests, 50 concurrent

```bash
ab -n 1000 -c 50 http://localhost/
```

Check server during load (from second terminal):

```bash
curl -s http://localhost/server-status?auto | grep -E "Busy|Idle"
```

---

## Troubleshooting Checklist

```
TROUBLESHOOTING ORDER:
1. sudo systemctl status apache2       <-- is it running?
2. sudo apache2ctl configtest          <-- config valid?
3. sudo tail -20 error.log             <-- what's the error?
4. sudo journalctl -u apache2 -n 20    <-- systemd says what?
5. sudo ss -tlnp | grep :80            <-- port in use?
6. ls -la /var/www/...                  <-- permissions?
7. namei -l /path/to/file              <-- parent dir perms?
8. cat .htaccess                       <-- blocking rules?
```

## Performance Tuning Checklist

```
PERFORMANCE:
├── mod_status    --> live server metrics
├── mod_deflate   --> gzip compression
├── mod_expires   --> browser caching
├── MPM tuning    --> MaxRequestWorkers
├── ab            --> load testing
└── %D in logs    --> response time tracking
```

---

## Summary

```
Golden rule: Check error.log FIRST. It tells you exactly what's wrong.

Performance stack:
  mod_deflate   = compress responses (smaller transfer)
  mod_expires   = cache at browser (fewer requests)
  mod_status    = monitor server health (live metrics)
  MPM tuning    = handle more concurrent users
  ab            = measure before and after changes

Troubleshooting stack:
  systemctl status    = is it alive?
  configtest          = is config valid?
  error.log           = what went wrong?
  ss -tlnp            = who has the port?
  namei -l            = permission chain?
```

---

## Key Takeaway

Performance and troubleshooting are daily tasks in sustain engineering. Know the troubleshooting order by heart: status, configtest, error.log, journalctl, port check, permissions, .htaccess. For performance: compress, cache, monitor, tune, measure.
