# Section 1: Navigation & Display Commands -- "You Just Got Paged"

## Day 19 | Linux OS | Time: ~30 minutes

---

## The Incident

```
======================================
INCIDENT #4721 | SEVERITY: P1
FoodExpress Order Service DOWN
Customer complaints: 47 in last 10 min
Revenue loss: ~Rs 2,400/min
======================================

Your SSH terminal is all you have.
No GUI. No VS Code. No Google.
Fix it.
======================================
```

You just got paged. Production is down. Open your terminal. Everything you learn today, you'll need to fix this.

---

## 1.1 -- Where Am I? (`pwd`)

When you SSH into a server, the first question is: where am I?

```bash
pwd
```

**Output:**
```
/home/app
```

`pwd` = **P**rint **W**orking **D**irectory. It shows your current location on the server.

**Analogy:** You're dropped into a building blindfolded. `pwd` tells you which room you're in.

---

## 1.2 -- What's Around Me? (`ls`)

```bash
ls
```

Shows files and folders in the current directory. But the basic `ls` doesn't show enough. Use these variants:

| Command | Flags Meaning | What You See | When To Use |
|---------|--------------|-------------|-------------|
| `ls` | (none) | Just names | Quick glance |
| `ls -l` | `-l` = **l**ong format | Names + size + date + permissions | Most common |
| `ls -la` | `-l` = long, `-a` = **a**ll (including hidden files starting with `.`) | Long format + hidden files | Always use this |
| `ls -lh` | `-l` = long, `-h` = **h**uman readable sizes (KB, MB, GB instead of bytes) | Long format with readable sizes | When you care about file sizes |
| `ls -lt` | `-l` = long, `-t` = sort by **t**ime (newest first) | Long format sorted by modification time | "What changed recently?" |
| `ls -lhS` | `-l` = long, `-h` = human, `-S` = sort by **S**ize (largest first) | Long format sorted by size | "What's the biggest file?" |

### Try It:

```bash
cd /tmp/foodexpress-server
ls
ls -la
ls -lh var/log/foodexpress/
```

**What to look for in `ls -la` output:**
```
-rw-r--r--  1  nag  wheel  3255  Aug 24 09:23  app.log
│             │            │      │              │
│             │            │      │              └── file name
│             │            │      └── last modified date
│             │            └── file size
│             └── owner
└── permissions (who can read/write/execute)
```

**Sustain engineering context:** When you SSH into a prod server at 2 AM, `ls -lth /var/log/` shows you which log was modified MOST RECENTLY -- that's probably the active log.

---

## 1.3 -- Read the Logs (`cat`)

```bash
cat var/log/foodexpress/app.log
```

`cat` dumps the ENTIRE file to screen. Good for small files. Terrible for large ones.

**When to use cat:**
- File is short (under 100 lines)
- You want to see EVERYTHING at once
- You're piping to another command: `cat file | grep ERROR`

**When NOT to use cat:**
- File is 500,000 lines (production logs are HUGE)
- You only need the beginning or end
- Use `head`, `tail`, `less` instead

---

## 1.4 -- First N Lines (`head`)

```bash
head -5 var/log/foodexpress/app.log
```

**Flag:** `-5` means show the first **5** lines. You can use any number: `head -20`, `head -100`, etc. Default (no flag) is 10 lines.

**Output:**
```
2026-08-24 09:00:01 INFO  [order-service] Application started on port 8080
2026-08-24 09:00:05 INFO  [menu-service] Application started on port 3000
2026-08-24 09:00:08 INFO  [payment-service] Application started on port 8081
2026-08-24 09:01:15 INFO  [order-service] Order #1001 created for customer_id=42 total=599.00
2026-08-24 09:01:30 INFO  [order-service] Order #1002 created for customer_id=15 total=299.00
```

**What this tells you:** Startup was clean. All 3 services (order, menu, payment) started successfully. No errors at boot.

**Sustain engineering context:** `head` answers: "How did the application start? Was there a problem at boot?"

---

## 1.5 -- Last N Lines (`tail`)

```bash
tail -5 var/log/foodexpress/app.log
```

**Flag:** `-5` means show the last **5** lines. You can use any number: `tail -20`, `tail -100`, etc. Default is 10 lines.

**Output:**
```
2026-08-24 09:15:15 WARN  [order-service] Response time degraded: avg=4500ms (threshold=1000ms)
2026-08-24 09:15:30 ERROR [order-service] Order #1017 failed: Read timed out
2026-08-24 09:16:00 INFO  [menu-service] Health check: OK
2026-08-24 09:16:15 ERROR [order-service] Health check: FAIL (database unreachable)
2026-08-24 09:16:30 ERROR [payment-service] Health check: FAIL (upstream unavailable)
```

**What this tells you:** The LATEST entries show health checks FAILING. Database unreachable. Response time at 4500ms (threshold is 1000ms). This is where the problem is.

**The rule:** In an incident, you ALWAYS start with `tail`. The latest entries tell you what's broken RIGHT NOW.

### tail -f: The Live Feed

```bash
tail -f var/log/foodexpress/app.log
```

`-f` = **follow**. The terminal stays open and shows NEW lines as they are written to the file. Like watching a live feed.

**How sustain engineers use this:**
1. Open terminal 1: `tail -f app.log` (watch the logs)
2. Open terminal 2: restart the service
3. Watch terminal 1 to see if the service comes back up

Press `Ctrl+C` to stop `tail -f`.

---

## 1.6 -- Count Lines (`wc`)

```bash
wc -l var/log/foodexpress/app.log
```

**Output:**
```
35 var/log/foodexpress/app.log
```

`wc` = **W**ord **C**ount (but it counts more than just words).

| Flag | Stands For | Counts |
|------|-----------|--------|
| `wc -l` | `-l` = **l**ines | Number of lines in the file |
| `wc -w` | `-w` = **w**ords | Number of words |
| `wc -c` | `-c` = **c**haracters | Number of characters (bytes) |

**Sustain engineering context:** "How many log entries today?" `wc -l app.log`. "How many requests hit the server?" `wc -l access.log`.

---

## 1.7 -- Scroll Through Long Files (`more` / `less`)

```bash
less var/log/foodexpress/app.log
```

| Key | Action |
|-----|--------|
| `Space` | Next page |
| `b` | Previous page |
| `/ERROR` | Search for "ERROR" |
| `n` | Next search result |
| `q` | Quit |

**"less is more"** -- `less` is an improved version of `more`. Use `less`.

Note: `less` may not work in Git Bash. Use `cat` with `| head` or `| tail` as alternatives.

---

## Section 1 Summary

```
pwd                    --> "Where am I?"
ls -lh                 --> "What's here? How big are the files?"
ls -lt                 --> "What was modified most recently?"
cat file               --> "Show me everything" (small files only)
head -N file           --> "Show me the first N lines"
tail -N file           --> "Show me the last N lines"
tail -f file           --> "Show me LIVE updates" (Ctrl+C to stop)
wc -l file             --> "How many lines in this file?"
less file              --> "Let me scroll through page by page"
```

**The incident so far:** You found the server, opened the logs, and saw health checks failing. The database is unreachable. Now you need to SEARCH for what went wrong. That's Section 2.

---

## Practice Exercises

All exercises use the simulated server. Run `cd /tmp/foodexpress-server` first.

**Exercise 1:** How many lines are in the access log?
```bash
wc -l var/log/foodexpress/access.log
# Expected: 28
```

**Exercise 2:** What are the first 3 lines of the app log? What services started?
```bash
head -3 var/log/foodexpress/app.log
# Expected: order-service, menu-service, payment-service
```

**Exercise 3:** What are the last 3 lines? What's the current status?
```bash
tail -3 var/log/foodexpress/app.log
# Expected: menu-service OK, order-service FAIL, payment-service FAIL
```

**Exercise 4:** List all files in `var/log/foodexpress/` sorted by size (largest first):
```bash
ls -lhS var/log/foodexpress/
# gc.log should be the largest
```

**Exercise 5:** How many files are in the entire server?
```bash
find . -type f | wc -l
```

**Exercise 6:** What's the total size of the log directory?
```bash
du -sh var/log/foodexpress/
```
