# Step 7: Configuration File Deep-dive

## Objective
Understand every key directive in Apache's configuration files and how they affect behaviour.

---

## Master Config

```bash
cat -n /etc/apache2/apache2.conf
```

Key directives:

```bash
grep -n "Timeout\|KeepAlive\|HostnameLookups\|ErrorLog\|LogLevel\|IncludeOptional\|Include " /etc/apache2/apache2.conf
```

---

## 1. Timeout & KeepAlive Settings

```bash
grep -n "Timeout\|KeepAlive" /etc/apache2/apache2.conf
```

| Directive | Default | What It Does |
|-----------|---------|-------------|
| `Timeout 300` | 300s | How long Apache waits for a request/response to complete |
| `KeepAlive On` | On | Allow multiple requests per TCP connection |
| `MaxKeepAliveRequests 100` | 100 | Max requests per connection before closing |
| `KeepAliveTimeout 5` | 5s | Wait time for next request on same connection |

### Experiment: Disable KeepAlive

```bash
# Measure with KeepAlive On
curl -w "Total time: %{time_total}s\n" -s -o /dev/null http://localhost

# Disable
sudo sed -i 's/KeepAlive On/KeepAlive Off/' /etc/apache2/apache2.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
curl -w "Total time: %{time_total}s\n" -s -o /dev/null http://localhost

# Revert
sudo sed -i 's/KeepAlive Off/KeepAlive On/' /etc/apache2/apache2.conf
sudo systemctl reload apache2
```

---

## 2. `<Directory>` Blocks -- Access Control

```bash
grep -n -A 5 "^<Directory" /etc/apache2/apache2.conf
```

Three blocks -- Apache evaluates top to bottom:

```apache
<Directory />                        <-- DENY everything by default
    Options FollowSymLinks
    AllowOverride None
    Require all denied
</Directory>

<Directory /usr/share>               <-- Allow shared system files
    AllowOverride None
    Require all granted
</Directory>

<Directory /var/www/>                <-- Allow web content + .htaccess
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
```

### Directive Reference

| Directive | Meaning |
|-----------|---------|
| `Options FollowSymLinks` | Apache follows symbolic links |
| `Options Indexes` | Show directory listing if no index.html |
| `AllowOverride None` | Ignore `.htaccess` files |
| `AllowOverride All` | Allow `.htaccess` to override config |
| `Require all denied` | Block all access |
| `Require all granted` | Allow all access |

### Demo: Directory Listing (Indexes)

```bash
# Create a directory with files but no index.html
sudo mkdir /var/www/html/files
echo "file1" | sudo tee /var/www/html/files/a.txt
echo "file2" | sudo tee /var/www/html/files/b.txt
curl http://localhost/files/           # Shows directory listing
```

Disable it:

```bash
sudo sed -i 's/Options Indexes FollowSymLinks/Options FollowSymLinks/' /etc/apache2/apache2.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
curl http://localhost/files/           # 403 Forbidden -- security best practice
```

Revert:

```bash
sudo sed -i 's/Options FollowSymLinks/Options Indexes FollowSymLinks/' /etc/apache2/apache2.conf
sudo systemctl reload apache2
sudo rm -rf /var/www/html/files       # Clean up
```

**Key teaching point:** Apache denies `/` (root) by default. You must explicitly grant access. This is security by default.

---

## 3. Logging Directives

```bash
grep -n "LogLevel\|ErrorLog\|LogFormat" /etc/apache2/apache2.conf
```

### Log Levels (most to least verbose)

```
trace8 > trace1 > debug > info > notice > warn > error > crit > alert > emerg
```

Default is `warn`.

### Experiment: Change Log Level

```bash
sudo sed -i 's/LogLevel warn/LogLevel info/' /etc/apache2/apache2.conf
sudo systemctl reload apache2
curl http://localhost
sudo tail -5 /var/log/apache2/error.log     # More verbose

# Revert
sudo sed -i 's/LogLevel info/LogLevel warn/' /etc/apache2/apache2.conf
sudo systemctl reload apache2
```

### Log Formats

```bash
grep "LogFormat" /etc/apache2/apache2.conf
```

| Name | What It Logs |
|------|-------------|
| `combined` | IP, time, request, status, size, referer, user-agent |
| `common` | IP, time, request, status, size (no referer/UA) |

---

## 4. Default Site Config

```bash
cat /etc/apache2/sites-available/000-default.conf
```

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost      <-- shown on error pages
    DocumentRoot /var/www/html           <-- where files come from
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

| Directive | Meaning |
|-----------|---------|
| `VirtualHost *:80` | This config applies to all requests on port 80 |
| `ServerAdmin` | Email shown on error pages |
| `DocumentRoot` | Folder Apache serves files from |
| `ErrorLog` | Where errors for THIS site go |
| `CustomLog` | Access log with format "combined" |

### Add a Custom ServerName

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

Add inside the `<VirtualHost>` block:

```
ServerName apache-lab.local
```

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
```

---

## 5. The configtest Habit

**Always test config before reload:**

```bash
# Break it
echo "BROKEN" | sudo tee -a /etc/apache2/apache2.conf
sudo apache2ctl configtest             # Shows error

# Fix it
sudo sed -i '/BROKEN/d' /etc/apache2/apache2.conf
sudo apache2ctl configtest             # Syntax OK
```

---

## Summary

```
apache2.conf controls:
├── Timeouts (Timeout, KeepAlive)
├── Access control (<Directory> blocks)
├── Logging (LogLevel, LogFormat)
└── Includes (modules, sites, conf)

sites-available/*.conf controls:
├── VirtualHost (which port)
├── ServerName (which domain)
├── DocumentRoot (which folder)
└── Logs (per-site error + access)

Golden rule: apache2ctl configtest --> then reload
```

---

## Key Takeaway

Apache's config is modular and layered. The master config sets global rules, site configs set per-site rules, and `.htaccess` sets per-directory rules. Always test before reloading.
