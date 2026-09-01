# Step 9: Virtual Hosts -- Name-based

## Objective
Serve multiple websites from a single Apache server using domain names (Host header).

---

## Concept

One Apache server, one IP, multiple websites. Apache reads the `Host` header to decide which site config to use. This is how shared hosting works.

```
Browser sends: GET / HTTP/1.1
               Host: foodexpress.local     <-- Apache reads this
                                            <-- picks matching VirtualHost
```

---

## Plan: Two Websites on One Server

| Site | Domain | Folder |
|------|--------|--------|
| FoodExpress (customer app) | foodexpress.local | /var/www/foodexpress |
| FoodTrack (admin panel) | foodtrack.local | /var/www/foodtrack |

---

## Step 1: Create Directory Structure

```bash
sudo mkdir -p /var/www/foodexpress
sudo mkdir -p /var/www/foodtrack
```

## Step 2: Create Content for Site 1 -- FoodExpress

```bash
sudo nano /var/www/foodexpress/index.html
```

```html
<!DOCTYPE html>
<html>
<head><title>FoodExpress</title></head>
<body style="font-family:Arial; text-align:center; padding:50px;">
    <h1 style="color:#e74c3c;">FoodExpress</h1>
    <p>Customer-facing food delivery app</p>
    <p style="background:#f0f0f0; padding:10px; display:inline-block;">
        Served from: /var/www/foodexpress
    </p>
</body>
</html>
```

## Step 3: Create Content for Site 2 -- FoodTrack

```bash
sudo nano /var/www/foodtrack/index.html
```

```html
<!DOCTYPE html>
<html>
<head><title>FoodTrack Admin</title></head>
<body style="font-family:Arial; text-align:center; padding:50px;">
    <h1 style="color:#2c3e50;">FoodTrack Admin Panel</h1>
    <p>Internal operations dashboard</p>
    <p style="background:#f0f0f0; padding:10px; display:inline-block;">
        Served from: /var/www/foodtrack
    </p>
</body>
</html>
```

## Step 4: Create VirtualHost Config -- FoodExpress

```bash
sudo nano /etc/apache2/sites-available/foodexpress.conf
```

```apache
<VirtualHost *:80>
    ServerName foodexpress.local
    ServerAlias www.foodexpress.local
    DocumentRoot /var/www/foodexpress

    ErrorLog ${APACHE_LOG_DIR}/foodexpress-error.log
    CustomLog ${APACHE_LOG_DIR}/foodexpress-access.log combined
</VirtualHost>
```

## Step 5: Create VirtualHost Config -- FoodTrack

```bash
sudo nano /etc/apache2/sites-available/foodtrack.conf
```

```apache
<VirtualHost *:80>
    ServerName foodtrack.local
    DocumentRoot /var/www/foodtrack

    ErrorLog ${APACHE_LOG_DIR}/foodtrack-error.log
    CustomLog ${APACHE_LOG_DIR}/foodtrack-access.log combined
</VirtualHost>
```

## Step 6: Enable Sites, Disable Default

```bash
sudo a2ensite foodexpress.conf
sudo a2ensite foodtrack.conf
sudo a2dissite 000-default.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

## Step 7: Test with Host Header

Since we don't have real DNS, use `curl -H` to simulate:

```bash
curl -H "Host: foodexpress.local" http://localhost
# Shows FoodExpress page

curl -H "Host: foodtrack.local" http://localhost
# Shows FoodTrack page
```

**Same IP, same port, different websites.** Apache matched the `Host` header to the right `ServerName`.

## What Happens with Unknown Host?

```bash
curl -H "Host: unknown.local" http://localhost
```

Apache picks the **first enabled site** alphabetically as the default.

### Set a Default Fallback

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

```apache
<VirtualHost *:80>
    ServerName _default_
    DocumentRoot /var/www/html

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

```bash
sudo a2ensite 000-default.conf
sudo systemctl reload apache2
curl -H "Host: unknown.local" http://localhost     # Gets default page
```

## Step 8: Verify Separate Log Files

```bash
ls -la /var/log/apache2/
```

Each site has its own logs:

```
foodexpress-access.log
foodexpress-error.log
foodtrack-access.log
foodtrack-error.log
```

Test:

```bash
curl -H "Host: foodexpress.local" http://localhost
curl -H "Host: foodtrack.local" http://localhost
sudo tail -1 /var/log/apache2/foodexpress-access.log
sudo tail -1 /var/log/apache2/foodtrack-access.log
```

Different log files caught different requests.

## Step 9: Test with /etc/hosts (Browser Testing)

On the VM:

```bash
echo "127.0.0.1 foodexpress.local foodtrack.local" | sudo tee -a /etc/hosts
curl http://foodexpress.local
curl http://foodtrack.local
```

## View Virtual Host Map

```bash
apache2ctl -S
```

Shows which `ServerName` points to which config file and `DocumentRoot`.

---

## Summary

```
Name-based Virtual Hosts:

  Request: GET / HTTP/1.1
           Host: foodexpress.local
                 |
  Apache checks: ServerName in each <VirtualHost>
                 |
  Match found -> serves DocumentRoot for that site
                 |
  Logs go to that site's own log files

Commands:
  a2ensite foodexpress.conf    <-- enable site
  a2dissite foodexpress.conf   <-- disable site
  apache2ctl -S                <-- show virtual host map

One server -> many websites -> separate configs, folders, logs
```

---

## Key Takeaway

Name-based virtual hosts let you host multiple websites on a single server. Apache uses the `Host` header to route requests. Each site gets its own DocumentRoot, config, and log files.
