# Step 11: Logging Deep-dive

## Objective
Understand Apache's logging system -- access logs, error logs, custom formats, real-time monitoring, and log analysis.

---

## Two Types of Logs

```bash
ls -la /var/log/apache2/
```

| Log | Purpose | When to Check |
|-----|---------|---------------|
| `access.log` | Every request that hits Apache | Traffic analysis, debugging 404s |
| `error.log` | Errors, warnings, startup/shutdown | Something broke |
| `<site>-access.log` | Per-site access (from virtual hosts) | Site-specific debugging |
| `<site>-error.log` | Per-site errors | Site-specific issues |

---

## Access Log Format -- Every Field Explained

```bash
sudo tail -5 /var/log/apache2/foodexpress-access.log
```

A typical line:

```
10.160.0.7 - - [26/Aug/2026:04:30:15 +0000] "GET / HTTP/1.1" 200 512 "-" "curl/7.81.0"
```

| Field | Value | Meaning |
|-------|-------|---------|
| `10.160.0.7` | Client IP | Who made the request |
| `-` | Ident | Always dash (unused) |
| `-` | Auth user | Dash if no auth |
| `[26/Aug/2026:04:30:15 +0000]` | Timestamp | When |
| `"GET / HTTP/1.1"` | Request line | Method, path, protocol |
| `200` | Status code | Success |
| `512` | Response size | Bytes sent |
| `"-"` | Referer | Where user came from |
| `"curl/7.81.0"` | User-Agent | What client/browser |

## Format Definition

```bash
grep "LogFormat" /etc/apache2/apache2.conf
```

```
combined = "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\""
common   = "%h %l %u %t \"%r\" %>s %O"
```

| Code | Meaning |
|------|---------|
| `%h` | Client hostname/IP |
| `%l` | Ident (always -) |
| `%u` | Authenticated user |
| `%t` | Timestamp |
| `%r` | Request line |
| `%>s` | Final status code |
| `%O` | Bytes sent |
| `%{Referer}i` | Referer header |
| `%{User-Agent}i` | User-Agent header |

---

## Generate Different Log Entries

```bash
curl http://localhost/                                         # 200
curl http://localhost/does-not-exist                           # 404
curl -X POST http://localhost/                                 # 200 (POST)
curl -H "Referer: https://google.com" http://localhost/       # with referer
curl -A "Mozilla/5.0 (iPhone)" http://localhost/              # fake mobile UA
```

Check logs:

```bash
sudo tail -5 /var/log/apache2/foodexpress-access.log
```

---

## Error Log

```bash
sudo tail -10 /var/log/apache2/error.log
```

Generate an error:

```bash
curl http://localhost/this/deep/path/missing.html
sudo tail -1 /var/log/apache2/error.log
```

Shows: `File does not exist: /var/www/foodexpress/this`

---

## Real-time Log Monitoring

Open a **second SSH session**:

```bash
gcloud compute ssh apache-lab --zone=asia-south1-a
```

In the second session:

```bash
sudo tail -f /var/log/apache2/foodexpress-access.log
```

In the **first session**, generate traffic:

```bash
for i in $(seq 1 5); do curl -s http://localhost/ > /dev/null; done
curl http://localhost/missing
```

Watch the second terminal -- logs appear in real-time. `Ctrl+C` to stop.

**This is how you monitor a live server during an incident.**

---

## Log Analysis -- Common Questions

### How many requests total?

```bash
sudo wc -l /var/log/apache2/foodexpress-access.log
```

### How many 404s?

```bash
sudo grep '" 404 ' /var/log/apache2/foodexpress-access.log | wc -l
```

### Which pages got 404?

```bash
sudo grep '" 404 ' /var/log/apache2/foodexpress-access.log | awk '{print $7}' | sort | uniq -c | sort -rn
```

### Top IPs hitting the server

```bash
sudo awk '{print $1}' /var/log/apache2/foodexpress-access.log | sort | uniq -c | sort -rn | head -5
```

### Status code breakdown

```bash
sudo awk '{print $9}' /var/log/apache2/foodexpress-access.log | sort | uniq -c | sort -rn
```

### Requests per minute

```bash
sudo awk '{print $4}' /var/log/apache2/foodexpress-access.log | cut -d: -f1-3 | sort | uniq -c
```

---

## Custom Log Format -- Add Response Time

```bash
sudo nano /etc/apache2/apache2.conf
```

Add after existing LogFormat lines:

```apache
LogFormat "%h %l %u %t \"%r\" %>s %O %D \"%{User-Agent}i\"" timed
```

`%D` = response time in **microseconds**.

Use it in FoodExpress:

```bash
sudo nano /etc/apache2/sites-available/foodexpress.conf
```

Change:

```apache
CustomLog ${APACHE_LOG_DIR}/foodexpress-access.log timed
```

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
curl http://localhost
sudo tail -1 /var/log/apache2/foodexpress-access.log
```

The number before user-agent is response time in microseconds. Divide by 1000 for milliseconds.

**Why this matters:** In production, response time in logs lets you spot slow pages before users complain.

---

## Log Rotation

```bash
cat /etc/logrotate.d/apache2
```

Default:

```
weekly          <-- rotate every week
rotate 14       <-- keep 14 old copies
compress        <-- gzip old logs
delaycompress   <-- don't compress most recent rotated file
```

Apache keeps ~3 months of logs automatically.

---

## Summary

```
Access Log:  WHO visited, WHEN, WHAT they requested, STATUS
Error Log:   WHAT went wrong, WHEN, WHY

Real-time:   sudo tail -f /var/log/apache2/access.log
Analysis:    grep, awk, sort, uniq -c, sort -rn

Key analysis commands:
├── Total requests:     wc -l access.log
├── 404 count:          grep '" 404 ' | wc -l
├── Top IPs:            awk '{print $1}' | sort | uniq -c | sort -rn
├── Status breakdown:   awk '{print $9}' | sort | uniq -c
└── Slow pages:         add %D to LogFormat, check microseconds

Custom format with response time:
  LogFormat "%h %l %u %t \"%r\" %>s %O %D \"%{User-Agent}i\"" timed

During an incident: tail -f is your first move.
```

---

## Key Takeaway

Logs are your primary debugging tool. Access logs tell you what happened; error logs tell you what went wrong. Learn to read them quickly -- during an incident, logs are the first place you look.
