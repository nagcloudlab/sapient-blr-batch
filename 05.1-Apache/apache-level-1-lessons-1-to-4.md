# Apache HTTP Server Administration — Level 1

## Course roadmap

1. **Level 1 — Foundations**
   - Web-server basics
   - Apache architecture
   - Service management
   - Important directories
   - Hosting a basic website
   - Logs and basic troubleshooting

2. **Level 2 — Configuration**
   - Directives and configuration hierarchy
   - Virtual hosts
   - Modules
   - Directory permissions
   - `.htaccess`

3. **Level 3 — Production Administration**
   - HTTPS/TLS
   - Reverse proxy and load balancing
   - Authentication and security
   - Performance tuning
   - Monitoring and troubleshooting

4. **Level 4 — Advanced Operations**
   - Multi-site production setup
   - Hardening
   - High availability
   - Automation
   - Incident scenarios

---

# Level 1 — Lesson 1: What is Apache?

Apache HTTP Server is software that:

- Listens for HTTP/HTTPS requests
- Receives requests from browsers or API clients
- Processes those requests
- Returns static content or forwards requests to applications

Example:

```text
Browser requests:
http://server-ip/index.html

Apache finds:
index.html

Apache returns:
HTML response
```

For a static website:

```text
Browser → Apache → HTML/CSS/Image files
```

For a Java application:

```text
Browser → Apache → Spring Boot application
```

In the second case, Apache commonly works as a **reverse proxy**. We’ll configure that at a later level.

## Apache naming

The naming differs by Linux distribution:

| Ubuntu/Debian | RHEL/Rocky Linux |
|---|---|
| Package: `apache2` | Package: `httpd` |
| Service: `apache2` | Service: `httpd` |
| Configuration: `/etc/apache2` | Configuration: `/etc/httpd` |
| Command: `apache2ctl` | Command: `apachectl` |

We’ll use **Ubuntu/Debian commands**, matching your current server.

---

# Lesson 2: Understanding your service status

You previously ran:

```bash
sudo systemctl status apache2
```

The important output was:

```text
Loaded: loaded
Active: active (running)
Main PID: 2833
```

Meaning:

| Output | Meaning |
|---|---|
| `loaded` | Linux found the Apache service definition |
| `enabled` | Apache will start automatically during boot |
| `active (running)` | Apache is currently running |
| `Main PID` | ID of Apache’s main process |
| `Tasks` | Number of processes/threads associated with Apache |
| `Memory` | Current approximate memory usage |

## Essential service commands

```bash
sudo systemctl start apache2
```

Starts Apache.

```bash
sudo systemctl stop apache2
```

Stops Apache.

```bash
sudo systemctl restart apache2
```

Stops and starts Apache. Existing connections may be interrupted.

```bash
sudo systemctl reload apache2
```

Reloads configuration more gracefully.

```bash
sudo systemctl enable apache2
```

Configures Apache to start during system boot.

```bash
sudo systemctl disable apache2
```

Prevents automatic startup during boot. It does not immediately stop the running service.

## Production rule

After modifying configuration, first validate it:

```bash
sudo apache2ctl configtest
```

Expected result:

```text
Syntax OK
```

Then reload:

```bash
sudo systemctl reload apache2
```

Avoid restarting unnecessarily.

---

# Lesson 3: Apache processes

Run:

```bash
ps -ef | grep apache2 | grep -v grep
```

You will probably see something similar to:

```text
root      2833  ... /usr/sbin/apache2 -k start
www-data  2834  ... /usr/sbin/apache2 -k start
www-data  2835  ... /usr/sbin/apache2 -k start
```

Apache generally has:

- One main or **parent process**, normally running as `root`
- Multiple **worker processes or threads**, normally running as `www-data`

The parent process needs elevated permissions for activities such as binding to port 80. Workers handle requests using a less-privileged account for improved security.

Apache’s exact process/thread arrangement depends on the selected **MPM — Multi-Processing Module**. We’ll study MPMs later.

Check your active MPM:

```bash
apache2ctl -V | grep -i "Server MPM"
```

You may get:

```text
Server MPM: event
```

---

# Lesson 4: Verify Apache from the command line

Check whether Apache is listening on ports:

```bash
sudo ss -lntp | grep apache2
```

Typical output:

```text
LISTEN 0 511 0.0.0.0:80
```

This means:

- `LISTEN` — waiting for connections
- `0.0.0.0` — accepting connections through all IPv4 interfaces
- `80` — HTTP port

Apache binds to configured addresses and ports and waits for incoming connections. The `Listen` directive controls this behavior. [Apache documentation](https://httpd.apache.org/docs/2.4/bind.html)

Test Apache locally:

```bash
curl -I http://localhost
```

Example response:

```http
HTTP/1.1 200 OK
Server: Apache/2.4.x
Content-Type: text/html
```

`-I` tells `curl` to retrieve only the response headers.

Important status codes:

| Code | Meaning |
|---:|---|
| `200` | Request successful |
| `301` / `302` | Redirect |
| `403` | Access forbidden |
| `404` | Resource not found |
| `500` | Internal server error |
| `502` | Bad gateway |
| `503` | Service unavailable |

---

# Level 1 — First practice

Run these commands one by one:

```bash
apache2ctl -v
```

```bash
apache2ctl -V | grep -i "Server MPM"
```

```bash
ps -ef | grep apache2 | grep -v grep
```

```bash
sudo ss -lntp | grep apache2
```

```bash
curl -I http://localhost
```

Send me the output. I’ll explain each line and then continue with **Level 1, Lesson 5: Apache directories and configuration structure**.

Reference: [Official Apache 2.4 documentation](https://httpd.apache.org/docs/2.4/) and [Ubuntu Apache configuration guide](https://ubuntu.com/server/docs/how-to/web-services/configure-apache2-settings/).
