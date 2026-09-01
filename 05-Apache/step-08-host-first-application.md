# Step 8: Host Your First Application

## Objective
Deploy a simple multi-page website on Apache and understand how static file serving works.

---

## Remove Default Page

```bash
sudo rm /var/www/html/index.html
```

## Create FoodExpress Landing Page

```bash
sudo nano /var/www/html/index.html
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FoodExpress</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>FoodExpress</h1>
        <p>Delivering happiness to your doorstep</p>
    </header>
    <main>
        <div class="stats">
            <div class="card">
                <h2>2.4M</h2>
                <p>Monthly Users</p>
            </div>
            <div class="card">
                <h2>12</h2>
                <p>Cities</p>
            </div>
            <div class="card">
                <h2>99.9%</h2>
                <p>Uptime SLA</p>
            </div>
        </div>
        <h3>Server Info</h3>
        <ul>
            <li>Hostname: <span id="host"></span></li>
            <li>Served by: Apache on Ubuntu</li>
            <li>Document Root: /var/www/html</li>
        </ul>
    </main>
    <footer>
        <p>Sustain Engineering Training - Day 21</p>
    </footer>
    <script>
        document.getElementById('host').textContent = location.hostname;
    </script>
</body>
</html>
```

## Create the CSS

```bash
sudo nano /var/www/html/style.css
```

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: #f5f5f5; color: #333; }
header { background: #e74c3c; color: white; text-align: center; padding: 40px 20px; }
header h1 { font-size: 2.5em; }
header p { font-size: 1.2em; margin-top: 10px; }
main { max-width: 800px; margin: 30px auto; padding: 0 20px; }
.stats { display: flex; gap: 20px; margin-bottom: 30px; }
.card { flex: 1; background: white; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.card h2 { font-size: 2em; color: #e74c3c; }
h3 { margin-bottom: 10px; }
ul { list-style: none; background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
li { padding: 8px 0; border-bottom: 1px solid #eee; }
li:last-child { border: none; }
footer { text-align: center; padding: 20px; color: #999; margin-top: 30px; }
```

## Test

```bash
# From VM
curl http://localhost

# From browser
# Open http://<EXTERNAL_IP>
```

## Verify in Logs

```bash
sudo tail -3 /var/log/apache2/access.log
```

Two requests -- one for `index.html`, one for `style.css`.

## Check File Ownership

```bash
ls -la /var/www/html/
```

Files owned by `root:root`, world-readable. Apache (`www-data`) can read but not write. Correct.

---

## Add a Custom 404 Error Page

```bash
curl -I http://localhost/does-not-exist     # Default Apache 404
```

Create custom error page:

```bash
sudo nano /var/www/html/404.html
```

```html
<!DOCTYPE html>
<html>
<head><title>404 - Not Found</title></head>
<body style="text-align:center; padding:50px; font-family:Arial;">
    <h1 style="font-size:4em; color:#e74c3c;">404</h1>
    <p>This page doesn't exist on FoodExpress.</p>
    <a href="/">Go Home</a>
</body>
</html>
```

Tell Apache to use it:

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

Add inside `<VirtualHost>`:

```apache
ErrorDocument 404 /404.html
```

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
curl http://localhost/does-not-exist        # Custom 404 page
```

---

## Add a Status Page

```bash
sudo nano /var/www/html/status.html
```

```html
<!DOCTYPE html>
<html>
<head><title>FoodExpress - Status</title></head>
<body style="font-family:Arial; padding:40px; max-width:600px; margin:auto;">
    <h1>System Status</h1>
    <table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
        <tr><td>Web Server</td><td style="color:green;">UP</td></tr>
        <tr><td>Database</td><td style="color:green;">UP</td></tr>
        <tr><td>Payment Gateway</td><td style="color:green;">UP</td></tr>
        <tr><td>Search Service</td><td style="color:orange;">DEGRADED</td></tr>
    </table>
    <p style="margin-top:20px; color:#999;">Last checked: <script>document.write(new Date().toLocaleString())</script></p>
</body>
</html>
```

## Verify Everything

```bash
curl -I http://localhost/              # 200 - home page
curl -I http://localhost/style.css     # 200 - CSS
curl -I http://localhost/status.html   # 200 - status page
curl -I http://localhost/nope          # 404 - custom error
sudo tail -10 /var/log/apache2/access.log
```

---

## Summary

```
/var/www/html/
├── index.html      <-- Home page
├── style.css       <-- Stylesheet
├── status.html     <-- Status page
├── 404.html        <-- Custom error page

Site config added:
  ErrorDocument 404 /404.html
```

---

## Key Takeaway

Apache serves static files from DocumentRoot. Any file you put in `/var/www/html/` is instantly accessible via HTTP. That's why you NEVER put secrets, `.env` files, or `.git` folders in DocumentRoot.
