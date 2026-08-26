# Level 1 — Lesson 5: Apache Directory Structure

On Ubuntu, Apache configuration is stored under:

```bash
/etc/apache2/
```

View it:

```bash
ls -l /etc/apache2/
```

Typical structure:

```text
/etc/apache2/
├── apache2.conf
├── ports.conf
├── envvars
├── sites-available/
├── sites-enabled/
├── mods-available/
├── mods-enabled/
├── conf-available/
└── conf-enabled/
```

## 1. `apache2.conf`

The main Apache configuration file:

```bash
less /etc/apache2/apache2.conf
```

It contains:

- Global server settings
- Directory access rules
- Included configuration files
- Logging-related configuration

Near the bottom, you’ll find lines similar to:

```apache
IncludeOptional mods-enabled/*.load
IncludeOptional mods-enabled/*.conf
Include ports.conf
IncludeOptional conf-enabled/*.conf
IncludeOptional sites-enabled/*.conf
```

Apache uses these `Include` directives to load additional configuration files.

## 2. `ports.conf`

Controls which ports Apache listens on:

```bash
cat /etc/apache2/ports.conf
```

Typical content:

```apache
Listen 80

<IfModule ssl_module>
    Listen 443
</IfModule>
```

Common ports:

| Port | Protocol | Usage |
|---:|---|---|
| `80` | HTTP | Unencrypted web traffic |
| `443` | HTTPS | TLS-encrypted web traffic |

Important distinction:

```apache
Listen 80
```

This tells Apache to accept connections on port 80. It does not define which website should answer the request.

The website is selected through a **virtual host**.

## 3. `sites-available`

Contains all website configurations:

```bash
ls -l /etc/apache2/sites-available/
```

You may see:

```text
000-default.conf
default-ssl.conf
```

`000-default.conf` is the default HTTP website configuration.

Inspect it:

```bash
cat /etc/apache2/sites-available/000-default.conf
```

Typical configuration:

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Meaning:

| Directive | Purpose |
|---|---|
| `<VirtualHost *:80>` | Handles requests arriving on port 80 |
| `ServerAdmin` | Administrator’s contact address |
| `DocumentRoot` | Directory containing website files |
| `ErrorLog` | Errors and diagnostic messages |
| `CustomLog` | Details of client requests |

## 4. `sites-enabled`

Contains the websites that Apache currently loads:

```bash
ls -l /etc/apache2/sites-enabled/
```

You will probably see:

```text
000-default.conf -> ../sites-available/000-default.conf
```

This is a **symbolic link**.

The actual configuration is stored in:

```text
sites-available/
```

The symbolic link in this directory activates it:

```text
sites-enabled/
```

The standard administration commands are:

```bash
sudo a2ensite 000-default.conf
sudo a2dissite 000-default.conf
```

After changing enabled sites:

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
```

## 5. Module directories

Available Apache modules:

```bash
ls /etc/apache2/mods-available/
```

Currently enabled modules:

```bash
ls /etc/apache2/mods-enabled/
```

List loaded modules:

```bash
apache2ctl -M
```

Enable a module:

```bash
sudo a2enmod rewrite
```

Disable a module:

```bash
sudo a2dismod rewrite
```

Then validate and reload:

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Do not disable an unfamiliar module on a production server.

## 6. General configuration directories

Reusable configurations are stored in:

```text
/etc/apache2/conf-available/
```

Enabled configurations are linked inside:

```text
/etc/apache2/conf-enabled/
```

Commands:

```bash
sudo a2enconf security
sudo a2disconf security
```

---

# Lesson 6: Document Root

The default website directory is:

```text
/var/www/html
```

List its files:

```bash
ls -la /var/www/html
```

You will probably find:

```text
index.html
```

When a browser requests:

```text
http://server-ip/
```

Apache serves:

```text
/var/www/html/index.html
```

The mapping is:

```text
http://server-ip/index.html
                 ↓
/var/www/html/index.html
```

`DocumentRoot` controls this URL-to-filesystem mapping.

## Check the current page

```bash
curl http://localhost
```

To see only the first few lines:

```bash
curl -s http://localhost | head
```

## Create a simple test page

Because this modifies the existing default page, first create a separate file:

```bash
sudo nano /var/www/html/training.html
```

Add:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Apache Training</title>
</head>
<body>
    <h1>Apache is working!</h1>
    <p>This page is served by Apache HTTP Server.</p>
</body>
</html>
```

Save it and test:

```bash
curl http://localhost/training.html
```

Or open:

```text
http://server-ip/training.html
```

## What happens internally?

```text
GET /training.html
        ↓
Apache receives the request on port 80
        ↓
Apache selects the matching virtual host
        ↓
DocumentRoot is /var/www/html
        ↓
Apache reads /var/www/html/training.html
        ↓
HTTP response is returned
```

## Practice

Run these commands:

```bash
ls -l /etc/apache2/
```

```bash
cat /etc/apache2/sites-available/000-default.conf
```

```bash
ls -l /etc/apache2/sites-enabled/
```

```bash
apache2ctl -M
```

```bash
ls -la /var/www/html/
```

Then create and test `training.html`.

Next lesson: **Apache access logs, error logs, and basic troubleshooting**.
