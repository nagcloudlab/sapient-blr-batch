# Module 21: Apache -- Lab Setup

## Prerequisites

- Apache 2.4 (`apache2 -v` or `httpd -v` to confirm)
- `sudo` access on a Linux machine or WSL2 instance
- curl for testing

## Running the Starter Code

```bash
# Copy virtual host config to Apache sites directory
sudo cp Labs/starter-code/foodexpress.conf /etc/apache2/sites-available/

# Enable the site and required modules
sudo a2ensite foodexpress
sudo a2enmod rewrite proxy proxy_http headers

# Restart Apache
sudo systemctl restart apache2
```

If Apache fails to restart, `sudo apachectl configtest` will identify syntax errors.

## Verifying Your Fixes

```bash
# Basic connectivity
curl -I http://localhost

# Virtual host routing (add to /etc/hosts if using a custom ServerName)
curl http://foodexpress.local

# Check rewrite rules
curl -I http://localhost/menu     # Should not return 404

# Check proxy (if backend is running)
curl http://localhost/api/orders

# Review error log
sudo tail -f /var/log/apache2/error.log
```

## Expected Behavior

- `curl -I http://localhost` returns `200 OK` or a redirect, not a connection refused.
- `.htaccess` rewrite rules redirect HTTP to HTTPS (or as specified in `lab-exercises.md`).
- Reverse proxy forwards `/api/*` requests to the backend service on the configured port.
- Apache error log shows no configuration warnings after restart.

## Troubleshooting

**`AH00526: Syntax error` on restart:** Run `sudo apachectl configtest` to get the exact file and
line number. Common causes: missing closing `>` on a directive block, wrong module name.

**403 Forbidden on valid paths:** Check `Require all granted` is present in the `<Directory>` block
for the document root, and that file permissions allow Apache's user (`www-data`) to read the files.
