# Step 12: Security (.htaccess)

## Objective
Secure Apache using `.htaccess` -- password protection, access control, blocking sensitive files, URL rewriting, and security headers.

---

## What is .htaccess?

A per-directory config file that overrides Apache settings **without restarting**. Drop it in any folder, Apache reads it on every request.

## Prerequisites

Confirm `AllowOverride All` is set:

```bash
grep -A 3 "Directory /var/www" /etc/apache2/apache2.conf
```

Enable required modules:

```bash
sudo a2enmod rewrite
sudo a2enmod auth_basic
sudo a2enmod headers
sudo systemctl reload apache2
```

---

## Exercise 1: Password-protect the Admin Site

### Create Password File

```bash
sudo apt install -y apache2-utils
sudo htpasswd -c /etc/apache2/.htpasswd admin
# Enter password (e.g., admin123)

sudo htpasswd /etc/apache2/.htpasswd operator
# Add second user
```

Verify:

```bash
cat /etc/apache2/.htpasswd
```

### Create .htaccess

```bash
sudo nano /var/www/foodtrack/.htaccess
```

```apache
AuthType Basic
AuthName "FoodTrack Admin - Authorized Personnel Only"
AuthUserFile /etc/apache2/.htpasswd
Require valid-user
```

### Test

```bash
curl http://localhost:8080                       # 401 Unauthorized
curl -u admin:admin123 http://localhost:8080     # Shows page
curl -u admin:wrongpass http://localhost:8080    # 401 again
```

Open `http://<EXTERNAL_IP>:8080` in browser -- you'll get a login popup.

---

## Exercise 2: Restrict Access by IP

```bash
sudo nano /var/www/foodtrack/.htaccess
```

```apache
AuthType Basic
AuthName "FoodTrack Admin - Authorized Personnel Only"
AuthUserFile /etc/apache2/.htpasswd
Require valid-user

# Also restrict by IP
<RequireAll>
    Require valid-user
    Require ip 10.160.0
</RequireAll>
```

Revert to simple auth after testing.

---

## Exercise 3: Block Directory Listing

```bash
sudo mkdir -p /var/www/foodexpress/uploads
echo "secret1" | sudo tee /var/www/foodexpress/uploads/config.txt
echo "secret2" | sudo tee /var/www/foodexpress/uploads/passwords.txt
curl http://localhost/uploads/           # Shows listing -- BAD!
```

Fix:

```bash
sudo nano /var/www/foodexpress/uploads/.htaccess
```

```apache
Options -Indexes
```

```bash
curl http://localhost/uploads/           # 403 Forbidden
curl http://localhost/uploads/config.txt # Still accessible
```

To block ALL access:

```apache
Options -Indexes
Require all denied
```

```bash
curl http://localhost/uploads/config.txt # 403 Forbidden -- locked
```

---

## Exercise 4: Block Sensitive Files

```bash
sudo nano /var/www/foodexpress/.htaccess
```

```apache
# Block hidden files (.env, .git, .htpasswd)
<FilesMatch "^\.">
    Require all denied
</FilesMatch>

# Block backup files
<FilesMatch "\.(bak|old|backup|sql|log)$">
    Require all denied
</FilesMatch>
```

Test:

```bash
echo "DB_PASS=secret" | sudo tee /var/www/foodexpress/.env
echo "DROP TABLE users;" | sudo tee /var/www/foodexpress/dump.sql

curl http://localhost/.env              # 403 Forbidden
curl http://localhost/dump.sql          # 403 Forbidden
curl -I http://localhost/index.html     # 200 OK -- normal files work
```

Clean up:

```bash
sudo rm /var/www/foodexpress/.env /var/www/foodexpress/dump.sql
```

---

## Exercise 5: URL Rewriting (Clean URLs)

Add to `/var/www/foodexpress/.htaccess`:

```apache
# Clean URLs
RewriteEngine On
RewriteRule ^status$ /status.html [L]
```

```bash
curl http://localhost/status             # Shows status page without .html
```

---

## Exercise 6: Security Headers

Add to top of `/var/www/foodexpress/.htaccess`:

```apache
# Security headers
Header set X-Content-Type-Options "nosniff"
Header set X-Frame-Options "DENY"
Header set X-XSS-Protection "1; mode=block"
Header set Referrer-Policy "strict-origin-when-cross-origin"
```

```bash
curl -I http://localhost/
```

| Header | What It Prevents |
|--------|-----------------|
| `X-Content-Type-Options: nosniff` | Browser MIME-type sniffing attacks |
| `X-Frame-Options: DENY` | Clickjacking (no iframes) |
| `X-XSS-Protection: 1` | Browser XSS filter |
| `Referrer-Policy` | Controls referer header leaking |

---

## Exercise 7: HTTPS Redirect (Concept)

In production, force all HTTP to HTTPS:

```apache
# Would go in .htaccess for production:
# RewriteEngine On
# RewriteCond %{HTTPS} off
# RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

Every sustain engineer will see this rule.

---

## Performance Warning

```
Apache reads .htaccess on EVERY request.
For /var/www/foodexpress/uploads/photo.jpg, Apache checks:
  /.htaccess
  /var/.htaccess
  /var/www/.htaccess
  /var/www/foodexpress/.htaccess
  /var/www/foodexpress/uploads/.htaccess

5 file reads per request!
```

**Production best practice:** Put rules directly in `<Directory>` blocks in the site config and set `AllowOverride None`. Use `.htaccess` only on shared hosting where you can't restart Apache.

---

## Complete .htaccess Example

```apache
# Security headers
Header set X-Content-Type-Options "nosniff"
Header set X-Frame-Options "DENY"
Header set X-XSS-Protection "1; mode=block"
Header set Referrer-Policy "strict-origin-when-cross-origin"

# Block hidden files (.env, .git, .htpasswd)
<FilesMatch "^\.">
    Require all denied
</FilesMatch>

# Block backup files
<FilesMatch "\.(bak|old|backup|sql|log)$">
    Require all denied
</FilesMatch>

# Clean URLs
RewriteEngine On
RewriteRule ^status$ /status.html [L]
```

---

## Summary

```
.htaccess = per-directory config, no restart needed

Common uses:
├── Password protection    --> AuthType Basic + .htpasswd
├── Block directory listing --> Options -Indexes
├── Block sensitive files  --> <FilesMatch "^\.">
├── Clean URLs             --> RewriteRule ^status$ /status.html
├── Security headers       --> Header set X-Frame-Options "DENY"
├── IP restriction         --> Require ip 10.0.0.0/8
└── HTTPS redirect         --> RewriteCond %{HTTPS} off

Key files:
  .htaccess               <-- rules (in web folder)
  .htpasswd               <-- passwords (OUTSIDE web folder!)

Security rule: .htpasswd must NEVER be inside DocumentRoot
We put it in /etc/apache2/.htpasswd -- not /var/www/
```

---

## Key Takeaway

`.htaccess` is powerful for per-directory security without restarts. Always block hidden files and backup files. Never put `.htpasswd` inside the web root. In production, prefer `<Directory>` blocks over `.htaccess` for performance.
