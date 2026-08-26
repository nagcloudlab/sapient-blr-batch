# Step 6: Directory Structure Walkthrough

## Objective
Understand Apache's file layout -- where config, content, logs, and modules live.

---

## See the Full Picture

```bash
sudo apt install -y tree
tree /etc/apache2/
```

## Apache Directory Layout

```
/etc/apache2/
├── apache2.conf            <-- Master config (global settings)
├── ports.conf              <-- Which ports Apache listens on
├── envvars                 <-- Environment variables (user, group, paths)
├── magic                   <-- MIME type detection
├── conf-available/         <-- Extra config snippets (inactive)
│   ├── charset.conf
│   ├── localized-error-pages.conf
│   ├── other-vhosts-access-log.conf
│   ├── security.conf
│   └── serve-cgi-bin.conf
├── conf-enabled/           <-- Symlinks to active snippets
├── mods-available/         <-- All installed modules (inactive)
├── mods-enabled/           <-- Symlinks to active modules
├── sites-available/        <-- All site configs (inactive)
│   ├── 000-default.conf
│   └── default-ssl.conf
└── sites-enabled/          <-- Symlinks to active sites
    └── 000-default.conf -> ../sites-available/000-default.conf
```

---

## 1. Master Config -- `apache2.conf`

```bash
cat -n /etc/apache2/apache2.conf
```

See the non-comment lines:

```bash
grep -n "^[^#]" /etc/apache2/apache2.conf | head -30
```

See what it includes:

```bash
grep -n "IncludeOptional\|Include " /etc/apache2/apache2.conf
```

It pulls in `mods-enabled/`, `conf-enabled/`, `sites-enabled/`. This is Apache's **modular config design**.

---

## 2. ports.conf -- Which Doors Are Open

```bash
cat /etc/apache2/ports.conf
```

```
Listen 80                           <-- Always listen on HTTP

<IfModule ssl_module>
    Listen 443                      <-- Listen on HTTPS only if SSL module loaded
</IfModule>
```

### Experiment: Change the Port

```bash
sudo cp /etc/apache2/ports.conf /etc/apache2/ports.conf.bak
sudo sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf
cat /etc/apache2/ports.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
sudo ss -tlnp | grep apache         # Now on 8080
```

Revert:

```bash
sudo cp /etc/apache2/ports.conf.bak /etc/apache2/ports.conf
sudo systemctl reload apache2
sudo ss -tlnp | grep apache         # Back on 80
```

---

## 3. envvars -- Apache's Identity

```bash
grep -v "^#" /etc/apache2/envvars | grep -v "^$"
```

| Variable | Value | Why It Matters |
|----------|-------|---------------|
| `APACHE_RUN_USER=www-data` | Process runs as this user | Security -- not root |
| `APACHE_RUN_GROUP=www-data` | Process group | File permissions |
| `APACHE_PID_FILE` | `/var/run/apache2/apache2$SUFFIX.pid` | Process tracking |
| `APACHE_LOG_DIR` | `/var/log/apache2$SUFFIX` | Where logs go |

### Verify the Process Model

```bash
ps aux | grep apache2 | grep -v grep
```

- 1 `root` process (parent -- binds to port 80, needs root for ports < 1024)
- Multiple `www-data` processes (children -- handle actual requests)

**Why this matters:** Even if an attacker exploits Apache, they can't modify files because Apache runs as `www-data`, not root.

### Verify File Ownership

```bash
ls -la /var/www/html/
stat /var/www/html/index.html
```

Owner is `root:root`, readable by `www-data` (world-readable). Apache can read but not write. This is intentional.

---

## 4. sites-available vs sites-enabled -- The Symlink Pattern

```bash
ls -la /etc/apache2/sites-available/
ls -la /etc/apache2/sites-enabled/
```

`sites-enabled/` contains **symlinks** pointing to `sites-available/`:

```bash
readlink /etc/apache2/sites-enabled/000-default.conf
# Output: ../sites-available/000-default.conf
```

This pattern means:
- Create configs in `*-available/`
- Activate by symlinking to `*-enabled/`
- Apache only reads `*-enabled/`

### The Default Site Config

```bash
cat /etc/apache2/sites-available/000-default.conf
```

Key lines:
- `VirtualHost *:80` -- listens on port 80
- `DocumentRoot /var/www/html` -- where files are served from

### Enable / Disable a Site

```bash
sudo a2dissite 000-default            # Disable
sudo systemctl reload apache2
curl http://localhost                  # 403 Forbidden -- no site enabled

sudo a2ensite 000-default             # Re-enable
sudo systemctl reload apache2
curl -I http://localhost              # 200 OK
```

---

## 5. mods-available vs mods-enabled

```bash
ls /etc/apache2/mods-enabled/ | wc -l       # Active modules
ls /etc/apache2/mods-available/ | wc -l      # All available modules
```

See what's active:

```bash
apache2ctl -M
```

### Enable / Disable a Module

```bash
sudo a2enmod rewrite                  # Enable mod_rewrite
sudo apache2ctl configtest
sudo systemctl reload apache2
apache2ctl -M | grep rewrite          # Verify

sudo a2dismod rewrite                 # Disable
sudo systemctl reload apache2
```

### Commonly Used Modules

| Module | Purpose |
|--------|---------|
| `mod_rewrite` | URL rewriting (clean URLs) |
| `mod_ssl` | HTTPS support |
| `mod_headers` | Custom HTTP headers |
| `mod_proxy` | Reverse proxy |
| `mod_deflate` | Gzip compression |
| `mod_security` | Web application firewall |

---

## 6. Document Root -- Where Your Website Lives

```bash
ls -la /var/www/html/
file /var/www/html/index.html
wc -l /var/www/html/index.html
```

Create a simple test file:

```bash
echo "<h1>Hello from Apache</h1>" | sudo tee /var/www/html/test.html
curl http://localhost/test.html
sudo rm /var/www/html/test.html       # Clean up
```

---

## 7. Logs -- Where to Look When Things Break

```bash
ls -la /var/log/apache2/
```

| File | What It Records |
|------|----------------|
| `access.log` | Every request (IP, time, URL, status, size) |
| `error.log` | Errors, warnings, startup messages |
| `other_vhosts_access.log` | Access logs for non-default virtual hosts |

```bash
sudo tail -5 /var/log/apache2/access.log
sudo tail -5 /var/log/apache2/error.log
```

Generate a log entry -- hit a page that doesn't exist:

```bash
curl http://localhost/does-not-exist
sudo tail -1 /var/log/apache2/access.log     # Shows 404
sudo tail -1 /var/log/apache2/error.log      # Shows "File does not exist"
```

---

## Summary Diagram

```
/etc/apache2/                 <-- "How Apache behaves"
├── apache2.conf              <-- "Boss" -- includes everything below
│   ├── ports.conf            <-- "Which doors to open" (80, 443)
│   ├── envvars               <-- "Who am I?" (www-data user)
│   ├── mods-enabled/*.conf   <-- "What can I do?" (modules)
│   ├── conf-enabled/*.conf   <-- "Extra settings"
│   └── sites-enabled/*.conf  <-- "Which websites to serve"

/var/www/html/                <-- "The kitchen" (your files)
│   └── index.html

/var/log/apache2/             <-- "The diary" (what happened)
    ├── access.log            <-- Who visited, when, what
    └── error.log             <-- What went wrong

/usr/sbin/apache2             <-- "The program itself"

Key commands:
  a2ensite / a2dissite        <-- enable/disable sites
  a2enmod / a2dismod          <-- enable/disable modules
  apache2ctl configtest       <-- test before reload
  apache2ctl -M               <-- list active modules
```

---

## Key Takeaway

When you join a project and something is broken, check 3 places: `sites-enabled/` (what's configured), `error.log` (what failed), and `ports.conf` (is it even listening).
