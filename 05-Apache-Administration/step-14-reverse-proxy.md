# Step 14: Apache as Reverse Proxy

## Objective
Configure Apache as a reverse proxy to forward requests to a backend application server -- a critical pattern in sustain engineering.

---

## What is a Reverse Proxy?

**Without reverse proxy:**

```
Browser --> :8080 --> Backend App (exposed directly)
```

**With reverse proxy:**

```
Browser --> :80 --> Apache (reverse proxy) --> :8080 --> Backend App (hidden)
```

The user talks to Apache on port 80. Apache forwards the request to the backend app on port 8080 and returns the response. The user never knows the backend exists.

**Real-world analogy:**

> A receptionist at a company. Visitors (browsers) don't walk directly into the engineering floor (backend). They talk to the receptionist (Apache), who routes them to the right person (backend app) and brings back the response.

---

## Why Use a Reverse Proxy?

| Benefit | How |
|---------|-----|
| **Security** | Backend not exposed to internet; only Apache is public |
| **SSL termination** | Apache handles HTTPS; backend runs plain HTTP |
| **Load balancing** | Apache distributes traffic across multiple backends |
| **Caching** | Apache caches static responses, reduces backend load |
| **URL rewriting** | Clean public URLs mapped to internal service paths |
| **Single entry point** | One domain, multiple backend services behind it |

---

## Step 1: Create a Backend Application

We'll use a simple Node.js app as the backend. Install Node.js first:

```bash
sudo apt install -y nodejs npm
```

Create the app:

```bash
sudo mkdir -p /opt/foodexpress-api
sudo nano /opt/foodexpress-api/server.js
```

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
    const response = {
        status: 'ok',
        service: 'FoodExpress API',
        path: req.url,
        method: req.method,
        timestamp: new Date().toISOString(),
        server: 'backend:8080',
        headers: {
            'x-forwarded-for': req.headers['x-forwarded-for'] || 'direct',
            'x-forwarded-host': req.headers['x-forwarded-host'] || 'none'
        }
    };

    if (req.url === '/api/restaurants') {
        response.data = [
            { id: 1, name: 'Biryani Palace', rating: 4.5, open: true },
            { id: 2, name: 'Dosa Corner', rating: 4.2, open: true },
            { id: 3, name: 'Pizza Express', rating: 3.8, open: false }
        ];
    } else if (req.url === '/api/health') {
        response.data = { uptime: process.uptime(), memory: process.memoryUsage().rss };
    } else if (req.url === '/api/orders') {
        response.data = [
            { id: 101, item: 'Chicken Biryani', status: 'delivered', total: 250 },
            { id: 102, item: 'Masala Dosa', status: 'preparing', total: 120 }
        ];
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(response, null, 2));
});

server.listen(8080, '127.0.0.1', () => {
    console.log('FoodExpress API running on http://127.0.0.1:8080');
});
```

Start it in the background:

```bash
node /opt/foodexpress-api/server.js &
```

Test the backend directly:

```bash
curl http://localhost:8080/api/health
curl http://localhost:8080/api/restaurants
curl http://localhost:8080/api/orders
```

All working. But this is on port 8080 and bound to `127.0.0.1` -- not accessible from outside. That's intentional.

```bash
# From your local machine -- this should FAIL
curl http://<EXTERNAL_IP>:8080/api/health
```

Timeout -- backend is hidden. Only Apache will talk to it.

---

## Step 2: Enable Proxy Modules

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer
sudo a2enmod lbmethod_byrequests
sudo a2enmod headers
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Verify modules loaded:

```bash
apache2ctl -M | grep proxy
```

You should see `proxy_module`, `proxy_http_module`.

---

## Step 3: Configure Apache as Reverse Proxy

### Simple Proxy -- Forward /api to Backend

```bash
sudo nano /etc/apache2/sites-available/foodexpress-proxy.conf
```

```apache
<VirtualHost *:80>
    ServerName foodexpress.local

    # Static files served by Apache directly
    DocumentRoot /var/www/html

    # Proxy /api requests to backend
    ProxyPreserveHost On
    ProxyPass /api http://127.0.0.1:8080/api
    ProxyPassReverse /api http://127.0.0.1:8080/api

    # Pass client IP to backend
    RequestHeader set X-Forwarded-For "%{REMOTE_ADDR}s"
    RequestHeader set X-Forwarded-Proto "http"

    ErrorLog ${APACHE_LOG_DIR}/foodexpress-proxy-error.log
    CustomLog ${APACHE_LOG_DIR}/foodexpress-proxy-access.log combined
</VirtualHost>
```

Enable and reload:

```bash
sudo a2ensite foodexpress-proxy.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

---

## Step 4: Test the Reverse Proxy

```bash
# Static file -- served by Apache directly
curl http://localhost/

# API request -- proxied to backend
curl http://localhost/api/health
curl http://localhost/api/restaurants
curl http://localhost/api/orders
```

The API responses come from the backend, but the user only talks to port 80. Notice the response shows:
- `server: "backend:8080"` -- the backend knows it's on 8080
- `x-forwarded-for` -- the backend sees the client's real IP
- `x-forwarded-host` -- the backend knows which host the client requested

**From the user's perspective:** Everything is on port 80 under one domain. They don't know `/api` goes to a different server.

---

## Step 5: Understand the Proxy Directives

| Directive | What It Does |
|-----------|-------------|
| `ProxyPreserveHost On` | Pass the original `Host` header to backend (not `127.0.0.1`) |
| `ProxyPass /api http://127.0.0.1:8080/api` | Forward requests starting with `/api` to the backend |
| `ProxyPassReverse /api http://127.0.0.1:8080/api` | Rewrite `Location` headers in responses (for redirects) |
| `RequestHeader set X-Forwarded-For` | Tell the backend the real client IP |
| `RequestHeader set X-Forwarded-Proto` | Tell the backend whether the original request was HTTP or HTTPS |

### ProxyPass Order Matters

```apache
# WRONG -- /api/health will match /api first
ProxyPass /api http://backend1:8080/api
ProxyPass /api/health http://backend2:8081/health

# CORRECT -- most specific first
ProxyPass /api/health http://backend2:8081/health
ProxyPass /api http://backend1:8080/api
```

---

## Step 6: Proxy to Multiple Backends

Real-world: different services behind one domain.

```bash
sudo nano /etc/apache2/sites-available/foodexpress-proxy.conf
```

```apache
<VirtualHost *:80>
    ServerName foodexpress.local

    DocumentRoot /var/www/html

    ProxyPreserveHost On

    # API service on port 8080
    ProxyPass /api http://127.0.0.1:8080/api
    ProxyPassReverse /api http://127.0.0.1:8080/api

    # Future: Auth service on port 8081
    # ProxyPass /auth http://127.0.0.1:8081/auth
    # ProxyPassReverse /auth http://127.0.0.1:8081/auth

    # Future: Search service on port 8082
    # ProxyPass /search http://127.0.0.1:8082/search
    # ProxyPassReverse /search http://127.0.0.1:8082/search

    # Pass client info to backends
    RequestHeader set X-Forwarded-For "%{REMOTE_ADDR}s"
    RequestHeader set X-Forwarded-Proto "http"

    ErrorLog ${APACHE_LOG_DIR}/foodexpress-proxy-error.log
    CustomLog ${APACHE_LOG_DIR}/foodexpress-proxy-access.log combined
</VirtualHost>
```

```
Browser --> Apache :80
                |
                |--> /api/*     --> API Service :8080
                |--> /auth/*    --> Auth Service :8081
                |--> /search/*  --> Search Service :8082
                |--> /*         --> Static files (DocumentRoot)
```

This is the **API Gateway pattern** -- one entry point routing to multiple microservices.

---

## Step 7: Add Proxy Timeout and Error Handling

```bash
sudo nano /etc/apache2/sites-available/foodexpress-proxy.conf
```

Add inside `<VirtualHost>`:

```apache
    # Timeout settings for proxy
    ProxyTimeout 30

    # What to show when backend is down
    ProxyErrorOverride On
    ErrorDocument 503 /maintenance.html
```

Create a maintenance page:

```bash
sudo nano /var/www/html/maintenance.html
```

```html
<!DOCTYPE html>
<html>
<head><title>FoodExpress - Maintenance</title></head>
<body style="font-family:Arial; text-align:center; padding:80px;">
    <h1 style="color:#e74c3c; font-size:3em;">Under Maintenance</h1>
    <p style="font-size:1.2em;">FoodExpress API is temporarily unavailable.</p>
    <p>Our team is working on it. Please try again in a few minutes.</p>
</body>
</html>
```

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Now stop the backend:

```bash
kill %1     # Stop the Node.js process
curl http://localhost/api/health
```

Instead of an ugly 503 error, users see the maintenance page. Start it again:

```bash
node /opt/foodexpress-api/server.js &
curl http://localhost/api/health
```

Back to normal.

---

## Step 8: Proxy with WebSocket Support

Modern apps use WebSocket for real-time features. Enable it:

```bash
sudo a2enmod proxy_wstunnel
sudo systemctl reload apache2
```

Add to the VirtualHost:

```apache
    # WebSocket proxy
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/ws/(.*) ws://127.0.0.1:8080/ws/$1 [P,L]
```

This forwards WebSocket connections (`ws://`) to the backend transparently.

---

## Step 9: Security -- Block Direct Backend Access

Ensure the backend ONLY accepts connections from Apache:

**Backend is already bound to `127.0.0.1`** (we did this in server.js):

```javascript
server.listen(8080, '127.0.0.1', () => { ... });
```

This means even if someone discovers port 8080, they can't reach it from outside. Only localhost (Apache) can.

Verify:

```bash
# From the VM -- works (localhost)
curl http://127.0.0.1:8080/api/health

# From outside -- fails (not bound to 0.0.0.0)
# curl http://<EXTERNAL_IP>:8080/api/health --> Connection refused
```

**Additional hardening -- block proxy abuse:**

Add to `<VirtualHost>`:

```apache
    # Prevent Apache from being used as a forward proxy
    ProxyRequests Off

    # Only allow proxy to our backends
    <Proxy *>
        Require all granted
    </Proxy>
```

`ProxyRequests Off` is critical -- without it, Apache could be abused as an open proxy.

---

## Step 10: Monitor Proxy Performance

Check if proxy requests are logged:

```bash
sudo tail -10 /var/log/apache2/foodexpress-proxy-access.log
```

Add response time to see proxy latency:

```bash
sudo nano /etc/apache2/apache2.conf
```

Add the timed format if not already present:

```apache
LogFormat "%h %l %u %t \"%r\" %>s %O %D \"%{User-Agent}i\"" timed
```

Update the proxy site to use it:

```apache
CustomLog ${APACHE_LOG_DIR}/foodexpress-proxy-access.log timed
```

```bash
sudo systemctl reload apache2
curl http://localhost/api/restaurants
sudo tail -1 /var/log/apache2/foodexpress-proxy-access.log
```

The `%D` value (microseconds) now includes proxy round-trip time. High values = slow backend.

---

## Step 11: Clean Up

Stop the backend process:

```bash
kill %1 2>/dev/null
```

Or keep it running for further practice.

---

## Common Reverse Proxy Patterns in Production

```
Pattern 1: Single Backend
  Apache :80 --> App :8080

Pattern 2: API Gateway (multiple backends)
  Apache :80 --> /api     --> API :8080
              --> /auth    --> Auth :8081
              --> /admin   --> Admin :9090

Pattern 3: SSL Termination
  Browser --HTTPS--> Apache :443 --HTTP--> Backend :8080
  Apache handles certificates; backend runs plain HTTP

Pattern 4: Load Balancer
  Apache :80 --> Backend1 :8080
              --> Backend2 :8080
              --> Backend3 :8080
  (round-robin or least-connections)

Pattern 5: Blue-Green Deploy
  Apache :80 --> /api --> Blue :8080  (current)
                     --> Green :8081  (new version, testing)
  Switch ProxyPass to cut over
```

---

## Troubleshooting Proxy Issues

```
TROUBLESHOOTING ORDER:
1. Is backend running?        -->  curl http://127.0.0.1:8080/api/health
2. Proxy modules loaded?      -->  apache2ctl -M | grep proxy
3. Config valid?              -->  apache2ctl configtest
4. Check error log            -->  tail -20 /var/log/apache2/foodexpress-proxy-error.log
5. Check access log           -->  tail -20 /var/log/apache2/foodexpress-proxy-access.log
6. Backend bound correctly?   -->  ss -tlnp | grep 8080
7. Firewall blocking?         -->  ufw status

COMMON ERRORS:
- "503 Service Unavailable"   -->  Backend is down or wrong port
- "502 Bad Gateway"           -->  Backend crashed mid-request
- "504 Gateway Timeout"       -->  Backend too slow, increase ProxyTimeout
- "AH01114: HTTP: failed"    -->  Backend refused connection
```

---

## Summary

```
Reverse Proxy = Apache sits in front of backend apps

Key directives:
├── ProxyPass /api http://backend:8080/api          <-- forward requests
├── ProxyPassReverse /api http://backend:8080/api    <-- fix redirects
├── ProxyPreserveHost On                             <-- keep original Host
├── ProxyRequests Off                                <-- prevent open proxy abuse
├── ProxyTimeout 30                                  <-- backend response timeout
└── RequestHeader set X-Forwarded-For                <-- pass real client IP

Required modules:
  mod_proxy, mod_proxy_http, mod_proxy_balancer, mod_headers

Why it matters in sustain engineering:
├── Backend never exposed to internet
├── SSL handled at one place (Apache)
├── Multiple services behind one domain
├── Maintenance page when backend is down
└── Logs show both frontend and proxy latency
```

---

## Key Takeaway

In production sustain engineering, you will almost never expose backend applications directly to the internet. Apache (or Nginx) sits in front as a reverse proxy -- handling SSL, routing, caching, and error pages. Understanding this pattern is essential for debugging production issues where the problem could be in Apache's proxy config, the network between Apache and the backend, or the backend itself.
