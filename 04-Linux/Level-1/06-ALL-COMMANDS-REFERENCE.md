# All Commands -- FoodExpress Incident Investigation

## Complete command reference with outputs, tied to the log files in `foodexpress-server/`

All commands assume you are in the server root:
```bash
cd /path/to/04-Linux/foodexpress-server
```

---

## FILES IN THIS SERVER

```
foodexpress-server/
├── etc/foodexpress/
│   ├── config_prod.properties        # Production config (max_connections=100)
│   ├── config_staging.properties     # Staging config (max_connections=50)
│   └── .env.backup                   # Backup env file
├── opt/foodexpress/order-service/
│   ├── app.jar                       # Application binary
│   └── config.yml                    # App config
├── tmp/
│   └── db.lock                       # Lock file blocking DB restart
└── var/log/foodexpress/
    ├── app.log                       # Application log (35 lines, the main file)
    ├── access.log                    # HTTP access log (28 requests)
    ├── app.log.2026-08-20            # Old rotated log
    ├── app.log.2026-08-21            # Old rotated log
    ├── app.log.2026-08-22            # Old rotated log
    ├── app.log.2026-08-23            # Old rotated log
    ├── access.log.2026-08-20         # Old access log
    ├── gc.log                        # Java garbage collection log
    ├── error.log                     # Empty error log
    └── archived/
        ├── app.log.2026-07-15.gz     # Archived compressed log
        └── app.log.2026-07-20.gz     # Archived compressed log
```

---

## SECTION 1: Navigation & Display

### pwd -- Where am I?
```bash
pwd
```
**Output:** `/path/to/04-Linux/foodexpress-server`

---

### ls -- What's here?

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-l` | **l**ong | Detailed view (permissions, size, date) |
| `-a` | **a**ll | Include hidden files (starting with `.`) |
| `-h` | **h**uman readable | Show sizes in KB/MB/GB instead of bytes |
| `-t` | **t**ime | Sort by modification time (newest first) |
| `-S` | **S**ize | Sort by file size (largest first) |
| `-r` | **r**everse | Reverse the sort order |

```bash
ls
```
**Output:**
```
etc  opt  tmp  var
```

```bash
ls -la var/log/foodexpress/
```
**Output:**
```
-rw-r--r--  app.log
-rw-r--r--  access.log
-rw-r--r--  app.log.2026-08-20
-rw-r--r--  app.log.2026-08-21
-rw-r--r--  gc.log
-rw-r--r--  error.log
drwxr-xr-x  archived/
```

```bash
ls -lhS var/log/foodexpress/
# -l = long format, -h = human readable sizes, -S = sort by Size (largest first)
```

---

### cat -- Show entire file
```bash
cat var/log/foodexpress/app.log
```
**Output:** All 35 lines of the application log.

---

### head -- First N lines

`-5` = show first **5** lines. `-N` = first N lines. Default without flag = 10.

```bash
head -5 var/log/foodexpress/app.log
```
**Output:**
```
2026-08-24 09:00:01 INFO  [order-service] Application started on port 8080
2026-08-24 09:00:05 INFO  [menu-service] Application started on port 3000
2026-08-24 09:00:08 INFO  [payment-service] Application started on port 8081
2026-08-24 09:01:15 INFO  [order-service] Order #1001 created for customer_id=42 total=599.00
2026-08-24 09:01:30 INFO  [order-service] Order #1002 created for customer_id=15 total=299.00
```
**Finding:** All 3 services started cleanly. No errors at boot.

---

### tail -- Last N lines

`-5` = show last **5** lines. `-f` = **f**ollow (live updates, Ctrl+C to stop).

```bash
tail -5 var/log/foodexpress/app.log
```
**Output:**
```
2026-08-24 09:15:15 WARN  [order-service] Response time degraded: avg=4500ms (threshold=1000ms)
2026-08-24 09:15:30 ERROR [order-service] Order #1017 failed: Read timed out
2026-08-24 09:16:00 INFO  [menu-service] Health check: OK
2026-08-24 09:16:15 ERROR [order-service] Health check: FAIL (database unreachable)
2026-08-24 09:16:30 ERROR [payment-service] Health check: FAIL (upstream unavailable)
```
**Finding:** Health checks failing. Database unreachable. This is where the problem is.

---

### tail -f -- Live monitoring
```bash
tail -f var/log/foodexpress/app.log
# Press Ctrl+C to stop
```

---

### wc -- Count lines

`wc` = **W**ord **C**ount. Flags: `-l` = **l**ines, `-w` = **w**ords, `-c` = **c**haracters.

```bash
wc -l var/log/foodexpress/app.log
# -l = count lines. Output: 35

wc -l var/log/foodexpress/access.log
# Output: 28
```

---

## SECTION 2: grep -- Searching

### All grep flags at a glance:

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-c` | **c**ount | Print count of matches, not the lines |
| `-i` | **i**gnore case | Match regardless of upper/lower |
| `-n` | line **n**umber | Prefix matches with line numbers |
| `-v` | in**v**ert | Show lines that do NOT match |
| `-o` | **o**nly matching | Show only the matched part |
| `-r` | **r**ecursive | Search all files in subdirectories |
| `-l` | **l**ist files | Show only file names that match |
| `-w` | **w**hole word | Match only complete words |
| `-B N` | **B**efore | Show N lines before each match |
| `-A N` | **A**fter | Show N lines after each match |
| `-C N` | **C**ontext | Show N lines before AND after |

### Basic grep
```bash
grep "ERROR" var/log/foodexpress/app.log
```
**Output:** 13 error lines showing NullPointerException, payment failures, DB connection unavailable, health check failures.

---

### grep -c -- Count (`-c` = **c**ount: print number of matches instead of lines)
```bash
grep -c "ERROR" var/log/foodexpress/app.log
# Output: 13

grep -c "WARN" var/log/foodexpress/app.log
# Output: 6

grep -c "FATAL" var/log/foodexpress/app.log
# Output: 2

grep -c "INFO" var/log/foodexpress/app.log
# Output: 14
```

---

### grep FATAL -- Root cause
```bash
grep "FATAL" var/log/foodexpress/app.log
```
**Output:**
```
2026-08-24 09:13:15 FATAL [database] Connection pool exhausted: max_connections=100 active=100 waiting=23
2026-08-24 09:14:30 FATAL [database] Auto-restart failed: lock file exists /tmp/db.lock
```
**Root cause:** All 100 DB connections used up. Lock file blocked auto-restart.

---

### grep -i -- Case insensitive (`-i` = **i**gnore case)
```bash
grep -c "error" var/log/foodexpress/app.log     # 0 (misses uppercase ERROR)
grep -ci "error" var/log/foodexpress/app.log     # 13 (-c=count + -i=ignore case)
```

---

### grep -n -- Line numbers (`-n` = line **n**umber)
```bash
grep -n "FATAL" var/log/foodexpress/app.log
```
**Output:**
```
22:2026-08-24 09:13:15 FATAL [database] Connection pool exhausted...
29:2026-08-24 09:14:30 FATAL [database] Auto-restart failed...
```

---

### grep -B -A -C -- Context (`-B` = **B**efore, `-A` = **A**fter, `-C` = **C**ontext both sides)
```bash
grep -B2 -A2 "FATAL" var/log/foodexpress/app.log
# -B2 = show 2 lines Before each match, -A2 = show 2 lines After
```
**Output:**
```
2026-08-24 09:12:00 ERROR [order-service] Order #1011 failed: NullPointerException at OrderService.java:45
2026-08-24 09:12:30 WARN  [order-service] Slow query: SELECT * FROM orders WHERE customer_id=42 (query_time=4100ms)
2026-08-24 09:13:15 FATAL [database] Connection pool exhausted: max_connections=100 active=100 waiting=23
2026-08-24 09:13:16 ERROR [order-service] Order #1012 failed: Database connection unavailable
2026-08-24 09:13:17 ERROR [order-service] Order #1013 failed: Database connection unavailable
--
2026-08-24 09:13:30 WARN  [menu-service] Cache miss rate exceeding threshold: 78%
2026-08-24 09:14:00 ERROR [order-service] Order #1015 failed: Database connection unavailable
2026-08-24 09:14:30 FATAL [database] Auto-restart failed: lock file exists /tmp/db.lock
2026-08-24 09:15:00 INFO  [order-service] Order #1016 created for customer_id=33 total=199.00
2026-08-24 09:15:15 WARN  [order-service] Response time degraded: avg=4500ms (threshold=1000ms)
```
**Finding:** Before FATAL: slow query at 4100ms from customer_id=42 was hogging connections.

---

### grep -v -- Exclude (`-v` = in**v**ert: show lines that do NOT match)
```bash
grep -v "INFO" var/log/foodexpress/app.log
```
**Output:** All non-INFO lines (only ERROR, WARN, FATAL). Removes the noise.

---

### egrep -- Multiple patterns
```bash
egrep "ERROR|FATAL" var/log/foodexpress/app.log
```
**Output:** 15 lines (13 ERROR + 2 FATAL)

```bash
egrep "ERROR|FATAL|WARN" var/log/foodexpress/app.log
```
**Output:** 21 lines (all problems)

---

### grep -r -- Recursive search (`-r` = **r**ecursive: search all files in all subdirectories)
```bash
grep -r "customer_id=42" var/log/
```
**Output:** Matches in BOTH app.log and access.log. customer_id=42 appears with slow queries in app.log and high response times in access.log.

```bash
grep -rl "FATAL" var/log/
# -r = recursive, -l = list file names only (don't show matching lines)
```
**Output:** `var/log/foodexpress/app.log` (only file with FATAL)

---

### grep -o -- Extract only match (`-o` = **o**nly matching: show just the matched part, not the full line)
```bash
grep "failed" var/log/foodexpress/app.log | grep -o "#[0-9]*"
# -o "#[0-9]*" = show only the part matching # followed by digits
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

---

### Piping: Which services have errors?
```bash
grep "ERROR" var/log/foodexpress/app.log | awk '{print $4}' | sort | uniq -c | sort -rn
# grep "ERROR"      = find error lines
# awk '{print $4}'  = extract 4th column ($4 = service name)
# sort              = sort alphabetically (required before uniq)
# uniq -c           = -c = count: remove duplicates and show count
# sort -rn          = -r = reverse, -n = numeric: biggest count first
```
**Output:**
```
   9 [order-service]
   4 [payment-service]
```

---

### Piping: What types of errors?
```bash
grep "failed" var/log/foodexpress/app.log | sed 's/.*failed: //' | sort | uniq -c | sort -rn
# sed 's/.*failed: //' = sed = stream editor. s/old/new/ = substitute
#   .*failed:  = everything up to "failed: " is replaced with nothing
#   This strips the timestamp/service prefix, leaving just the error message
```
**Output:**
```
   4 Database connection unavailable
   3 NullPointerException at OrderService.java:45
   1 Read timed out
   1 Payment processing halted: upstream database unavailable
   1 Payment failed for order #1008: Invalid card number
   1 Payment failed for order #1004: Connection timeout to payment gateway
```

---

### Piping: Which customers placed orders?
```bash
grep "created" var/log/foodexpress/app.log | grep -o "customer_id=[0-9]*" | sort | uniq -c | sort -rn
```
**Output:**
```
   3 customer_id=42
   2 customer_id=33
   1 customer_id=88
   1 customer_id=15
```

---

### Piping: Slow query times
```bash
grep "Slow query" var/log/foodexpress/app.log | grep -o "query_time=[0-9]*ms"
```
**Output:**
```
query_time=2500ms
query_time=3200ms
query_time=4100ms
```

---

### Access log: Status code breakdown
```bash
awk '{print $9}' var/log/foodexpress/access.log | sort | uniq -c | sort -rn
```
**Output:**
```
   9 503
   7 201
   6 200
   4 500
   1 504
   1 400
```

---

### Access log: Requests per IP
```bash
awk '{print $1}' var/log/foodexpress/access.log | sort | uniq -c | sort -rn
```
**Output:**
```
  14 192.168.1.10
   4 192.168.1.33
   2 192.168.1.88
   2 192.168.1.55
   2 192.168.1.45
   2 192.168.1.22
   1 192.168.1.77
   1 192.168.1.108
```

---

### Access log: Slowest requests
```bash
awk '{print $NF, $0}' var/log/foodexpress/access.log | sort -rn | head -5 | awk '{$1=""; print $0}'
```
**Output:** Top 5 slowest: payment 30s, customer_id=42 queries at 4.1s and 2.5s.

---

### Access log: Which endpoints?
```bash
awk '{print $7}' var/log/foodexpress/access.log | cut -d'?' -f1 | sort | uniq -c | sort -rn
```
**Output:**
```
  17 /api/orders
   3 /api/health
   3 /api/payments
   3 /api/menu/search
   1 /api/menu
```

---

### Access log: When did 503s start?
```bash
grep "503" var/log/foodexpress/access.log | head -1
```
**Output:** `09:13:15` -- exact same second as the FATAL in app.log.

---

### Save errors to file
```bash
egrep "ERROR|FATAL" var/log/foodexpress/app.log > /tmp/incident_errors.txt
wc -l /tmp/incident_errors.txt
# Output: 15
```

---

## SECTION 3: find, diff, cut

### All find flags:

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-name "*.log"` | file **name** | Match files by name pattern (`*` = any characters) |
| `-iname "*.LOG"` | **i**gnore case name | Same as -name but case insensitive |
| `-size +1M` | file **size** | Filter by size. `+` = greater than, `-` = less than |
| `-type f` | file **type** | `f` = regular files, `d` = directories, `l` = links |
| `-exec cmd {} \;` | **exec**ute | Run a command on each found file. `{}` = filename placeholder |

### find -- All log files
```bash
find . -name "*.log"
```
**Output:**
```
./var/log/foodexpress/error.log
./var/log/foodexpress/gc.log
./var/log/foodexpress/access.log
./var/log/foodexpress/app.log
```

---

### find -- The lock file
```bash
find . -name "*.lock"
```
**Output:** `./tmp/db.lock`

---

### find -- Config files
```bash
find . -name "*.properties"
```
**Output:**
```
./etc/foodexpress/config_staging.properties
./etc/foodexpress/config_prod.properties
```

---

### find -- Large files
```bash
find . -size +1M -exec ls -lh {} \;
# -size +1M = files larger than 1 Megabyte
# -exec ls -lh {} \; = for each found file, run "ls -lh" on it
#   {} = placeholder for the found filename
#   \; = marks end of the -exec command
```
**Output:** gc.log (15M), access.log.old (8M), app.log.old (5M)

---

### find -- Hidden files
```bash
find . -name ".*" -type f
# -name ".*" = files starting with . (hidden files in Linux)
# -type f = only regular files (not directories like .git/)
```
**Output:** `./etc/foodexpress/.env.backup`

---

### find -- Count lines in all logs
```bash
find . -name "*.log" -exec wc -l {} \;
```

---

### diff -- Prod vs staging config
```bash
diff etc/foodexpress/config_prod.properties etc/foodexpress/config_staging.properties
```

---

### diff -y -- Side by side (`-y` = side-b**y**-side view, `|` marks differences)
```bash
diff -y etc/foodexpress/config_prod.properties etc/foodexpress/config_staging.properties
```
**Key differences:**
```
db.max_connections=100              |  db.max_connections=50
db.connection_timeout=5000          |  db.connection_timeout=10000
payment.gateway.url=https://api...  |  payment.gateway.url=https://sandbox...
log.level=INFO                      |  log.level=DEBUG
```

---

### cut -- Extract time from log (`-d` = **d**elimiter, `-f` = **f**ield number)
```bash
cut -d' ' -f2 var/log/foodexpress/app.log | head -5
# -d' ' = split each line by SPACE
# -f2 = extract field 2 (time). Field 1=date, 2=time, etc.
```
**Output:**
```
09:00:01
09:00:05
09:00:08
09:01:15
09:01:30
```

---

### cut -- Extract config keys
```bash
grep -v "^#" etc/foodexpress/config_prod.properties | grep -v "^$" | cut -d'=' -f1
# grep -v "^#" = -v=exclude, ^#=lines starting with # (comments)
# grep -v "^$" = -v=exclude, ^$=empty lines (^ is start, $ is end)
# cut -d'=' -f1 = split by =, take field 1 (key name, left of =)
```

---

### cut -- Extract config values
```bash
grep -v "^#" etc/foodexpress/config_prod.properties | grep -v "^$" | cut -d'=' -f2
```

---

### awk -- Extract service names (handles multiple spaces)
```bash
awk '{print $4}' var/log/foodexpress/app.log | sort | uniq -c | sort -rn
# awk splits each line by whitespace automatically
# $1=date, $2=time, $3=level, $4=service, $NF=last field
# sort = sort alphabetically (required before uniq)
# uniq -c = -c=count: deduplicate and show count
# sort -rn = -r=reverse -n=numeric: highest count first
```
**Output:**
```
  15 [order-service]
   7 [menu-service]
   5 [payment-service]
   2 [database]
```

---

### sort | uniq -c | sort -rn -- Count log levels
```bash
awk '{print $3}' var/log/foodexpress/app.log | sort | uniq -c | sort -rn
```
**Output:**
```
  14 INFO
  13 ERROR
   6 WARN
   2 FATAL
```

---

### touch -- Create marker file
```bash
touch var/log/foodexpress/INCIDENT_4721_STARTED
```

---

### rm -- Remove the lock file (incident fix)
```bash
rm tmp/db.lock
```

---

## SECTION 4: Processes & System

### df -h -- Disk space (`df` = **D**isk **F**ree, `-h` = **h**uman readable: KB/MB/GB)
```bash
df -h
```
**(On real server would show:)**
```
/dev/sda1   50G   46G  4.0G  92% /        <-- CRITICAL
/dev/sda2  200G  112G   88G  56% /var
/dev/sda3  100G   23G   77G  23% /opt
```

---

### du -sh -- Folder sizes (`du` = **D**isk **U**sage, `-s` = **s**ummary, `-h` = **h**uman readable)
```bash
du -sh var/log/foodexpress/* | sort -hr
# du -s = summary total per folder (not every file inside)
# du -h = human readable sizes (MB, GB)
# sort -h = sort by human numeric values (15M > 8M > 2M)
# sort -r = reverse (biggest first)
```
**Output:** gc.log largest, then old access.log, then old app.log.

---

### ps aux | grep -- Is my service running?

`ps aux` flags: `a` = **a**ll users, `u` = **u**ser format (shows USER, %CPU, %MEM), `x` = include background processes (no terminal).

```bash
ps aux | grep java
ps aux | grep node
ps aux | grep mysql
```

---

### ps aux -- Top CPU consumers
```bash
ps aux | sort -k3 -rn | head -5
# sort -k3 = -k=key: sort by column 3 (%CPU)
# -r = reverse (biggest first), -n = numeric
# head -5 = show top 5 only
```

---

### ps aux -- Top memory consumers
```bash
ps aux | sort -k4 -rn | head -5
# sort -k4 = sort by column 4 (%MEM)
```

---

### kill -- Stop a process

| Command | Signal | Meaning |
|---------|--------|---------|
| `kill PID` | SIGTERM (15) | Polite stop -- process can clean up and exit |
| `kill -9 PID` | SIGKILL (9) | Force kill -- immediate termination, no cleanup |

```bash
# Start a fake process for practice
sleep 300 &

# Find its PID
ps aux | grep "sleep 300"

# Kill it (polite)
kill <PID>

# If still alive, force kill
kill -9 <PID>

# Verify
ps aux | grep "sleep 300"
```

---

### Redirection -- Build incident report

| Symbol | What It Does | Example |
|--------|-------------|---------|
| `>` | Write to file (**overwrites** existing content) | `echo "hello" > file.txt` |
| `>>` | **Append** to file (adds to end) | `echo "more" >> file.txt` |
| `\|` | **Pipe**: send output of one command as input to next | `grep ERROR log \| wc -l` |
| `$(...)` | **Command substitution**: run a command inside another | `echo "Count: $(wc -l file)"` |
```bash
echo "# INCIDENT 4721" > /tmp/report.txt
echo "Generated: $(date)" >> /tmp/report.txt
echo "" >> /tmp/report.txt
echo "## Error Count" >> /tmp/report.txt
echo "ERRORs: $(grep -c 'ERROR' var/log/foodexpress/app.log)" >> /tmp/report.txt
echo "FATALs: $(grep -c 'FATAL' var/log/foodexpress/app.log)" >> /tmp/report.txt
echo "WARNs:  $(grep -c 'WARN' var/log/foodexpress/app.log)" >> /tmp/report.txt
echo "" >> /tmp/report.txt
echo "## Root Cause" >> /tmp/report.txt
grep "FATAL" var/log/foodexpress/app.log >> /tmp/report.txt
echo "" >> /tmp/report.txt
echo "## Affected Services" >> /tmp/report.txt
grep "ERROR" var/log/foodexpress/app.log | awk '{print $4}' | sort | uniq -c | sort -rn >> /tmp/report.txt
echo "" >> /tmp/report.txt
echo "## Top Error Types" >> /tmp/report.txt
grep "failed" var/log/foodexpress/app.log | sed 's/.*failed: //' | sort | uniq -c | sort -rn >> /tmp/report.txt

cat /tmp/report.txt
```

---

### tar -- Archive old logs

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-c` | **c**reate | Create a new archive |
| `-x` | e**x**tract | Extract files from an archive |
| `-t` | lis**t** | List contents of an archive (without extracting) |
| `-z` | g**z**ip | Compress/decompress with gzip (makes .tar.gz) |
| `-v` | **v**erbose | Show file names as they are processed |
| `-f` | **f**ilename | The next argument is the archive filename |

**Memory trick:** `-czvf` = **C**reate, g**Z**ip, **V**erbose, **F**ilename. `-xzvf` = e**X**tract, g**Z**ip, **V**erbose, **F**ilename.

```bash
# Create compressed archive
tar -czvf /tmp/old_logs.tar.gz var/log/foodexpress/app.log.2026-08-2*
#    ││││  └── filename of the archive
#    │││└── f = filename follows
#    ││└─── v = verbose (show files being archived)
#    │└──── z = gzip compression
#    └───── c = create new archive

# List archive contents (without extracting)
tar -tzvf /tmp/old_logs.tar.gz
#    └── t = list (instead of c=create or x=extract)

# Extract archive
tar -xzvf /tmp/old_logs.tar.gz
#    └── x = extract
```

---

## COMPLETE INCIDENT TIMELINE

```
09:00  Services start normally (head -5 app.log confirms)
09:02  First NullPointerException (code bug, separate issue)
09:04  Slow query: customer_id=42, 2500ms
09:05  Payment gateway timeout
09:09  Slow query: customer_id=108, 3200ms
09:12  Slow query: customer_id=42, 4100ms (GETTING WORSE)
09:13  FATAL: Connection pool exhausted (100/100 used, 23 waiting)
09:13  CASCADE: All orders fail with "Database connection unavailable"
09:14  FATAL: DB auto-restart blocked by lock file /tmp/db.lock
09:15  Response time degraded to 4500ms avg
09:16  Health checks: order-service FAIL, payment-service FAIL, menu-service OK
```

**Root cause chain:**
```
customer_id=42 slow queries (no index?)
  --> queries hold DB connections for 4+ seconds
    --> 100 connections all used up
      --> connection pool exhausted (FATAL)
        --> all new orders fail
          --> DB tries to auto-restart
            --> lock file blocks restart (FATAL)
              --> services report Health check: FAIL
```

**Resolution:**
```bash
1. grep "FATAL" app.log                    # Found root cause
2. find . -name "*.lock"                   # Found lock file
3. rm tmp/db.lock                          # Removed it
4. ps aux | grep rebuild_index             # Found runaway CPU process
5. kill 2847                               # Killed it
6. tar -czvf old_logs.tar.gz *.old         # Freed disk space
7. systemctl restart mysqld                # Restarted DB
8. tail -f app.log                         # Watched recovery
```
