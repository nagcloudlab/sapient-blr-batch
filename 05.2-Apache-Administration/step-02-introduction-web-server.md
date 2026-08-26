# Step 2: Introduction to Web Servers & Apache

## Objective
Understand what a web server does, how HTTP works, and why Apache is used in sustain engineering.

---

## What is a Web Server?

**Real-world analogy:**

> Think of a restaurant. The **customer** (browser) walks in and places an **order** (HTTP request). The **waiter** (web server) takes the order, goes to the **kitchen** (filesystem/backend), picks up the **food** (HTML/CSS/JS/images), and brings it back to the customer (HTTP response). Apache is that waiter.

A web server is software that:
- Listens on a port (usually 80 for HTTP, 443 for HTTPS)
- Receives HTTP requests from clients (browsers)
- Sends back HTTP responses (HTML, CSS, JS, images)

Two roles: **hardware** (the machine) and **software** (Apache, Nginx, IIS).

## How HTTP Works

```
Browser (Client)                    Apache (Server)
     |                                    |
     |--- GET /index.html HTTP/1.1 ------>|
     |                                    | looks up /var/www/html/index.html
     |<--- HTTP/1.1 200 OK --------------|
     |     Content-Type: text/html        |
     |     <html>...</html>               |
```

## Key Concepts

| Concept | Explanation |
|---------|-------------|
| **Port 80** | Default HTTP port. Apache listens here. |
| **Port 443** | Default HTTPS port (SSL/TLS encrypted). |
| **Document Root** | The folder Apache serves files from (`/var/www/html/`) |
| **Process Model** | Apache forks a process (or thread) per incoming connection |
| **Modules** | Plugins that extend Apache -- `mod_rewrite`, `mod_ssl`, `mod_proxy` |
| **`.conf` files** | Configuration files that control Apache's behaviour |
| **`.htaccess`** | Per-directory config overrides without restarting Apache |

## Why Apache?

- Most widely used web server since 1995 (~30% of all websites)
- Open source (Apache Software Foundation)
- Module-based architecture -- load only what you need
- `.htaccess` for per-directory config without restarting
- Runs on Linux, Windows, macOS

## Apache vs Others

| Feature | Apache | Nginx | IIS |
|---------|--------|-------|-----|
| OS | Linux, Windows, macOS | Linux, Windows | Windows only |
| Architecture | Process/Thread per connection | Event-driven (async) | Thread pool |
| `.htaccess` | Yes | No | web.config |
| Best for | Dynamic content, flexibility | Static content, reverse proxy | .NET apps |
| Market share | ~30% | ~34% | ~7% |
| Config reload | Graceful restart | Reload without downtime | App pool recycle |

## Why Apache in Sustain Engineering?

- Many legacy enterprise apps still run on Apache
- `.htaccess` allows **per-app config changes without server restart** -- critical in production
- Module system means you can add features (SSL, compression, rewrite rules) without replacing the server
- Logs (`access.log`, `error.log`) are the **first place you look** during an incident

---

## Hands-on: Verify No Web Server Yet

Before installing Apache, confirm the machine is clean:

```bash
# Try to connect -- should fail
curl http://localhost

# Check port 80 -- nothing listening
sudo ss -tlnp | grep :80

# Check installed packages -- no apache
dpkg -l | grep apache
```

All should return empty or errors. Clean machine.

---

## Key Takeaway

A web server is the bridge between users and your application. Apache is the most common web server you'll encounter in sustain engineering, and understanding it is essential for troubleshooting production issues.
