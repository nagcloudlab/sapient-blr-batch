# Section 2: grep -- Finding the Problem

## Day 19 | Linux OS | Time: ~45 minutes

---

## The Scenario

You've seen the last 5 lines. Health checks failing. Database unreachable. But HOW did we get here? When did errors start? How many? Which service? You need to SEARCH.

---

## 2.1 -- Basic grep: Find all errors

`grep` searches for a pattern inside a file and shows every matching line.

```bash
grep "ERROR" var/log/foodexpress/app.log
```

**Output (13 lines):**
```
2026-08-24 09:02:30 ERROR [order-service] Order #1003 failed: NullPointerException at OrderService.java:45
2026-08-24 09:05:12 ERROR [payment-service] Payment failed for order #1004: Connection timeout to payment gateway
2026-08-24 09:07:45 ERROR [order-service] Order #1007 failed: NullPointerException at OrderService.java:45
...
2026-08-24 09:16:15 ERROR [order-service] Health check: FAIL (database unreachable)
2026-08-24 09:16:30 ERROR [payment-service] Health check: FAIL (upstream unavailable)
```

**What this tells you:** 13 errors total. Early errors are NullPointerException (a code bug). Then at 09:13, everything collapses with "Database connection unavailable". Two DIFFERENT problems.

---

## 2.2 -- grep -c: Count matches

`-c` = **c**ount. Instead of showing matching lines, just print the NUMBER of matches.

Your manager asks: "How many errors?" Give a number, not a wall of text.

```bash
grep -c "ERROR" var/log/foodexpress/app.log    # 13
grep -c "WARN" var/log/foodexpress/app.log     # 6
grep -c "FATAL" var/log/foodexpress/app.log    # 2
```

**Flag breakdown:** `grep -c "ERROR" file` = search for "ERROR" in file, but instead of printing the matching lines, just print the count.

**13 errors. 6 warnings. 2 FATAL. FATAL is the worst. Let's see what's FATAL.**

---

## 2.3 -- Finding the Root Cause: FATAL

```bash
grep "FATAL" var/log/foodexpress/app.log
```

**Output:**
```
2026-08-24 09:13:15 FATAL [database] Connection pool exhausted: max_connections=100 active=100 waiting=23
2026-08-24 09:14:30 FATAL [database] Auto-restart failed: lock file exists /tmp/db.lock
```

**Root cause found:** Connection pool exhausted -- all 100 connections used up, 23 more waiting. Then the database tried to auto-restart but a lock file blocked it.

---

## 2.4 -- grep -i: Case Insensitive Search

`-i` = **i**gnore case. Treats uppercase and lowercase as the same.

```bash
grep -c "error" var/log/foodexpress/app.log     # 0 (case sensitive -- misses "ERROR")
grep -ci "error" var/log/foodexpress/app.log     # 13 (case insensitive -- catches "ERROR")
```

**Flag breakdown:** `grep -ci "error"` = `-c` (count) + `-i` (ignore case). You can combine multiple flags together.

The log says `ERROR` in uppercase. Searching for lowercase `error` misses everything. `-i` ignores case.

**Rule:** When you're not sure about casing, always use `-i`.

---

## 2.5 -- grep -n: Show Line Numbers

`-n` = line **n**umber. Prefixes each matching line with its line number in the file.

```bash
grep -n "FATAL" var/log/foodexpress/app.log
```

**Output:**
```
22:2026-08-24 09:13:15 FATAL [database] Connection pool exhausted: max_connections=100 active=100 waiting=23
29:2026-08-24 09:14:30 FATAL [database] Auto-restart failed: lock file exists /tmp/db.lock
```

Line 22 and 29. Useful when you need to tell a teammate: "Look at line 22 of app.log."

---

## 2.6 -- grep -B -A -C: Context Around Matches (THIS IS GOLD)

Finding an error is useful. Seeing what happened BEFORE and AFTER the error is where you find the ROOT CAUSE.

```bash
grep -B2 -A2 "FATAL" var/log/foodexpress/app.log
```

| Flag | Meaning | Memory Trick |
|------|---------|-------------|
| `-B2` | 2 lines **B**efore | B = Before |
| `-A2` | 2 lines **A**fter | A = After |
| `-C2` | 2 lines **C**ontext (both sides) | C = Context |

**Output:**
```
2026-08-24 09:12:00 ERROR [order-service] Order #1011 failed: NullPointerException at OrderService.java:45
2026-08-24 09:12:30 WARN  [order-service] Slow query: SELECT * FROM orders WHERE customer_id=42 (query_time=4100ms)
2026-08-24 09:13:15 FATAL [database] Connection pool exhausted: max_connections=100 active=100 waiting=23
2026-08-24 09:13:16 ERROR [order-service] Order #1012 failed: Database connection unavailable
2026-08-24 09:13:17 ERROR [order-service] Order #1013 failed: Database connection unavailable
```

**What the context reveals:** Before the FATAL, there was a slow query taking **4100ms** from customer_id=42. That slow query was hogging database connections. After the FATAL, everything cascaded -- orders failing because database was unavailable.

**The lesson:** `grep` without context gives you the symptom. `grep` with `-B` and `-A` gives you the cause.

---

## 2.7 -- grep -v: Exclude Lines

`-v` = in**v**ert match. Shows lines that do NOT match the pattern.

Sometimes you want to REMOVE the noise instead of searching for the signal.

```bash
grep -v "INFO" var/log/foodexpress/app.log
```

**Flag breakdown:** `grep -v "INFO"` = show every line that does NOT contain "INFO". This removes all the "everything is fine" messages, leaving only problems (ERROR, WARN, FATAL).

---

## 2.8 -- egrep: Multiple Patterns (OR Search)

```bash
egrep "ERROR|FATAL" var/log/foodexpress/app.log
```

`egrep` lets you search for multiple patterns using `|` (OR).

- `egrep "ERROR|FATAL"` = lines containing ERROR **or** FATAL
- `egrep "order-service|payment-service"` = lines from either service
- Regular `grep` needs `\|` which is ugly: `grep "ERROR\|FATAL"`

**Use `egrep` when searching for multiple things.**

---

## 2.9 -- grep -r: Search Across ALL Files

`-r` = **r**ecursive. Searches inside ALL files in a directory and its subdirectories.

```bash
grep -r "customer_id=42" var/log/
```

**Output:**
```
var/log/foodexpress/access.log:... "GET /api/orders?customer_id=42 HTTP/1.1" 200 8921 2.501
var/log/foodexpress/access.log:... "GET /api/orders?customer_id=42 HTTP/1.1" 200 8921 4.102
var/log/foodexpress/app.log:... Order #1001 created for customer_id=42 total=599.00
var/log/foodexpress/app.log:... Slow query: SELECT * FROM orders WHERE customer_id=42 (query_time=2500ms)
var/log/foodexpress/app.log:... Slow query: SELECT * FROM orders WHERE customer_id=42 (query_time=4100ms)
```

customer_id=42 shows up in BOTH app.log AND access.log. Their queries are taking 2500ms and 4100ms. One heavy user caused the entire outage.

| Flag | Stands For | Meaning |
|------|-----------|---------|
| `-r` | **r**ecursive | Search all files in all subdirectories, show matching lines |
| `-rl` | **r**ecursive + **l**ist | Search all files, but only show FILE NAMES that contain a match |

---

## 2.10 -- grep -o: Extract Only the Matching Part

`-o` = **o**nly matching. Instead of showing the full line, shows ONLY the part that matched the pattern.

```bash
grep "failed" var/log/foodexpress/app.log | grep -o "#[0-9]*"
```

**Output:**
```
#1003
#1007
#1011
#1012
#1013
#1014
#1015
#1017
```

`-o` shows ONLY the part that matched, not the entire line. Useful for extracting specific data like order numbers, IDs, timestamps.

---

## 2.11 -- Piping: The Power of Chaining Commands

This is where Linux becomes powerful. You chain commands with `|` (pipe). Each command's output becomes the next command's input.

### Build up one step at a time:

**Step 1:** Find all errors
```bash
grep "ERROR" var/log/foodexpress/app.log
```

**Step 2:** Count them
```bash
grep "ERROR" var/log/foodexpress/app.log | wc -l
# Output: 13
```

**Step 3:** Extract which SERVICE has errors
```bash
grep "ERROR" var/log/foodexpress/app.log | awk '{print $4}' | sort | uniq -c | sort -rn
```

**Output:**
```
   9 [order-service]
   4 [payment-service]
```

**Reading the pipe left to right (every flag explained):**
1. `grep "ERROR"` -- find all lines containing "ERROR"
2. `awk '{print $4}'` -- `awk` splits each line by spaces; `$4` = 4th column (service name). `$1` would be date, `$2` time, `$3` level, `$4` service
3. `sort` -- sort lines alphabetically (required before `uniq` because `uniq` only removes CONSECUTIVE duplicates)
4. `uniq -c` -- `-c` = **c**ount. Removes duplicate lines and shows how many times each appeared
5. `sort -rn` -- `-r` = **r**everse (biggest first), `-n` = **n**umeric (sort as numbers, not text). Without `-n`, "9" would come after "10" alphabetically

**Step 4:** What TYPES of errors?
```bash
grep "failed" var/log/foodexpress/app.log | sed 's/.*failed: //' | sort | uniq -c | sort -rn
```

**Flag breakdown:** `sed 's/.*failed: //'` -- `sed` = **s**tream **ed**itor. `s/old/new/` = substitute. `.*failed: ` = everything up to and including "failed: ". Replacing it with nothing (`//`) removes it, leaving only the error message.

**Output:**
```
   4 Database connection unavailable
   3 NullPointerException at OrderService.java:45
   1 Read timed out
   1 Payment failed...
```

---

## 2.12 -- Access Log Analysis

The access log uses a different format (Apache/Nginx). Here's how to analyze it:

### Count by HTTP status code:
```bash
awk '{print $9}' var/log/foodexpress/access.log | sort | uniq -c | sort -rn
```

**Flag breakdown:** `awk '{print $9}'` -- in the access log format, `$9` is the 9th column which is the HTTP status code (200, 404, 500, etc.). `$1` is IP address, `$7` is the URL path.

**Output:**
```
   9 503    (Service Unavailable -- the cascade)
   7 201    (Created -- successful orders)
   6 200    (OK -- successful reads)
   4 500    (Internal Server Error -- NullPointerExceptions)
   1 504    (Gateway Timeout -- payment gateway)
   1 400    (Bad Request -- invalid card)
```

### Count by IP address (who's hitting the server most?):
```bash
awk '{print $1}' var/log/foodexpress/access.log | sort | uniq -c | sort -rn
```

**Output:**
```
  14 192.168.1.10    <-- HALF of all traffic!
   4 192.168.1.33
   2 192.168.1.88
   ...
```

192.168.1.10 made 14 out of 28 requests. That's probably customer_id=42.

---

## Section 2 Summary

### All grep Flags Explained

| Flag | Stands For | What It Does | Example |
|------|-----------|-------------|---------|
| (none) | -- | Show matching lines | `grep "ERROR" file` |
| `-c` | **c**ount | Print only the count of matches | `grep -c "ERROR" file` --> `13` |
| `-i` | **i**gnore case | Match regardless of UPPER/lower case | `grep -i "error" file` catches ERROR, error, Error |
| `-n` | line **n**umber | Prefix each match with its line number | `grep -n "FATAL" file` --> `22:FATAL...` |
| `-v` | in**v**ert | Show lines that do NOT match | `grep -v "INFO" file` removes all INFO lines |
| `-o` | **o**nly matching | Show only the matched part, not the full line | `grep -o "#[0-9]*" file` --> `#1003` |
| `-r` | **r**ecursive | Search all files in all subdirectories | `grep -r "error" /var/log/` |
| `-l` | **l**ist files | Show only file names (not the matching lines) | `grep -rl "FATAL" /var/log/` |
| `-B N` | **B**efore | Show N lines before each match | `grep -B3 "FATAL" file` |
| `-A N` | **A**fter | Show N lines after each match | `grep -A3 "FATAL" file` |
| `-C N` | **C**ontext | Show N lines before AND after | `grep -C3 "FATAL" file` |
| `-w` | **w**ord | Match whole words only | `grep -w "ERROR" file` won't match "ERRORS" |

**You can combine flags:** `grep -cin "error" file` = count + ignore case + line numbers.

### All Piping Commands Explained

| Command | Stands For | What It Does |
|---------|-----------|-------------|
| `awk '{print $4}'` | -- | Split line by spaces, print 4th column. `$1`=first, `$NF`=last |
| `sort` | -- | Sort lines alphabetically |
| `sort -n` | **n**umeric | Sort as numbers (so 9 comes before 10) |
| `sort -r` | **r**everse | Reverse order (Z-A or biggest first) |
| `sort -rn` | **r**everse **n**umeric | Sort numbers, biggest first |
| `sort -k3` | **k**ey column 3 | Sort by the 3rd column |
| `sort -t'=' -k2` | field separa**t**or, **k**ey | Split by `=`, sort by 2nd field |
| `sort -u` | **u**nique | Sort and remove duplicates |
| `uniq` | -- | Remove consecutive duplicate lines |
| `uniq -c` | **c**ount | Remove duplicates and show count of each |
| `wc -l` | **l**ines | Count number of lines |
| `head -N` | -- | Show first N lines |
| `tail -N` | -- | Show last N lines |
| `sed 's/old/new/'` | **s**ubstitute | Replace "old" with "new" in each line |
| `cut -d',' -f2` | **d**elimiter, **f**ield | Split by delimiter, extract field number |

### Quick Reference

```
grep "ERROR" file                  --> Find lines containing ERROR
grep -c "ERROR" file               --> COUNT matching lines
grep -i "error" file               --> Case INSENSITIVE search
grep -n "ERROR" file               --> Show LINE NUMBERS
grep -v "INFO" file                --> EXCLUDE lines (everything EXCEPT)
grep -B3 -A3 "FATAL" file         --> 3 lines BEFORE and AFTER (CONTEXT)
grep -r "error" /var/log/          --> Search RECURSIVELY across all files
grep -rl "FATAL" /var/log/         --> Just show FILE NAMES that match
grep -o "pattern" file             --> Show ONLY the matching part
egrep "ERROR|FATAL" file           --> Search MULTIPLE patterns (OR)

THE POWER COMBO:
grep "ERROR" file | awk '{print $4}' | sort | uniq -c | sort -rn
  Find errors --> extract field --> sort --> count --> rank
```

**The incident so far:** You found 13 errors and 2 FATALs. Root cause: DB connection pool exhaustion caused by customer_id=42's slow queries from IP 192.168.1.10.

---

## Practice Exercises

Run `cd /tmp/foodexpress-server` first.

| # | Question | Command | Expected |
|---|----------|---------|----------|
| 1 | Find all lines containing "payment-service" | `grep "payment-service" var/log/foodexpress/app.log` | 6 lines |
| 2 | How many orders were successfully created? | `grep -c "created" var/log/foodexpress/app.log` | 8 |
| 3 | Search "fail" in any case | `grep -i "fail" var/log/foodexpress/app.log` | Catches failed, FAIL, Failed |
| 4 | Show line numbers for every WARN | `grep -n "WARN" var/log/foodexpress/app.log` | 6 results |
| 5 | Show each ERROR with 1 line before and after | `grep -B1 -A1 "ERROR" var/log/foodexpress/app.log` | Context around each error |
| 6 | Show all lines that are NOT INFO | `grep -v "INFO" var/log/foodexpress/app.log` | Only problems |
| 7 | Find "NullPointerException" OR "Connection timeout" | `egrep "NullPointerException\|Connection timeout" var/log/foodexpress/app.log` | 4 lines |
| 8 | Search for "503" across ALL log files | `grep -r "503" var/log/` | Only in access.log |
| 9 | Which files contain "database"? (file names only) | `grep -ril "database" var/log/` | app.log |
| 10 | Show only the FIRST 3 errors | `grep "ERROR" var/log/foodexpress/app.log \| head -3` | First 3 error lines |
| 11 | Show only the LAST 2 errors | `grep "ERROR" var/log/foodexpress/app.log \| tail -2` | Health check failures |
| 12 | Extract only order numbers from failed orders | `grep "failed" var/log/foodexpress/app.log \| grep -o "#[0-9]*"` | #1003, #1007, etc. |
| 13 | Find slow queries and extract query times | `grep "Slow query" var/log/foodexpress/app.log \| grep -o "[0-9]*ms"` | 2500ms, 3200ms, 4100ms |
| 14 | Which customers placed orders? How many each? | `grep "created" var/log/foodexpress/app.log \| grep -o "customer_id=[0-9]*" \| sort \| uniq -c \| sort -rn` | customer_id=42 has 3 |
| 15 | How many 503 errors in access log? | `awk '{print $9}' var/log/foodexpress/access.log \| grep -c "503"` | 9 |
| 16 | Which API endpoints were called? | `awk '{print $7}' var/log/foodexpress/access.log \| cut -d'?' -f1 \| sort \| uniq -c \| sort -rn` | /api/orders most common |
| 17 | When did 503 errors start? Does it match the FATAL? | `grep "503" var/log/foodexpress/access.log \| head -1` then `grep "FATAL" var/log/foodexpress/app.log \| head -1` | Both at 09:13:15 |
| 18 | Save all ERROR and FATAL to an incident report file | `egrep "ERROR\|FATAL" var/log/foodexpress/app.log > /tmp/incident_report.txt` | 15 lines saved |
| 19 | One-liner: failed orders per error type, sorted | `grep "failed" var/log/foodexpress/app.log \| sed 's/.*failed: //' \| sort \| uniq -c \| sort -rn` | DB connection unavailable tops |
| 20 | Requests per IP address | `awk '{print $1}' var/log/foodexpress/access.log \| sort \| uniq -c \| sort -rn` | 192.168.1.10 = 14 requests |
