# Section 3: find, diff, cut -- Digging Deeper

## Day 19 | Linux OS | Time: ~40 minutes

---

## The Scenario

You found the errors. Root cause: DB connection pool exhausted. But now you need to answer deeper questions:
- Why is max_connections only 100? Did someone change the config?
- Are there old log files eating disk space?
- Where's that lock file blocking the DB restart?

---

## 3.1 -- find: Locate Files on the Server

`find` searches for files by name, size, type, or age. It's your flashlight in the dark.

**Basic syntax:** `find <where> <criteria> <action>`

### Find by name:

`-name` = match files by their **name** using a pattern (supports wildcards like `*`).

```bash
# Find ALL log files anywhere on the server
find . -name "*.log"
#      │  │
#      │  └── -name "*.log" = files ending in .log (* = any characters)
#      └── . = start searching from current directory

# Find ALL config files
find . -name "*.properties"

# Find the lock file that's blocking DB restart
find . -name "*.lock"
```

**Output of lock file search:**
```
./tmp/db.lock
```

Remember the FATAL log said "Auto-restart failed: lock file exists /tmp/db.lock". You just found it.

### Find by name (case insensitive):

`-iname` = **i**gnore case **name**. Same as `-name` but doesn't care about upper/lower case.

```bash
find . -iname "*.LOG"    # Finds .log, .LOG, .Log
```

---

## 3.2 -- find by Size: Disk Cleanup

The server is at 92% disk. Find the biggest files.

`-size` = filter files by their **size**. `+` means greater than, `-` means less than.

```bash
# Files larger than 1MB
find . -size +1M -exec ls -lh {} \;
#              │         │       │  │
#              │         │       │  └── \; = end of -exec command
#              │         │       └── {} = placeholder for each found file
#              │         └── -exec = run this command on each result
#              └── +1M = larger than 1 Megabyte

# Files larger than 5MB
find . -size +5M -exec ls -lh {} \;
```

**Output:**
```
-rw-r--r--  1 nag  wheel   15M  ./var/log/foodexpress/gc.log
-rw-r--r--  1 nag  wheel  8.0M  ./var/log/foodexpress/access.log.2026-08-20
-rw-r--r--  1 nag  wheel  5.0M  ./var/log/foodexpress/app.log.2026-08-20
```

gc.log is 15MB (Java garbage collection log -- grows forever if not rotated). On a real server, these would be GBs.

### Size suffixes:

| Suffix | Meaning |
|--------|---------|
| `+100M` | Larger than 100 MB |
| `-100M` | Smaller than 100 MB |
| `100M` | Exactly 100 MB (rarely useful) |
| `+1G` | Larger than 1 GB |
| `+100k` | Larger than 100 KB |

---

## 3.3 -- find by Type

```bash
# Only directories
find . -type d

# Only regular files
find . -type f

# Only files in etc/
find ./etc -type f
```

| Type | Meaning |
|------|---------|
| `-type f` | Regular files |
| `-type d` | Directories |
| `-type l` | Symbolic links |

---

## 3.4 -- find with -exec: Take Action on Found Files

`find` alone just FINDS files. `find` with `-exec` DOES something with each one.

```bash
# Find all .properties files and show their first line
find . -name "*.properties" -exec head -1 {} \;

# Find all log files and count lines in each
find . -name "*.log" -exec wc -l {} \;

# Find files larger than 1MB and show their sizes
find . -size +1M -exec ls -lh {} \;
```

**Syntax breakdown:**
```
find . -name "*.log" -exec wc -l {} \;
│     │              │          │  │
│     │              │          │  └── end of -exec command
│     │              │          └── placeholder for each found file
│     │              └── action to take
│     └── search pattern
└── start directory
```

**Common mistake:** Forgetting `\;` at the end of `-exec`. This WILL break. Every student will make this mistake once.

---

## 3.5 -- diff: Compare Files

In sustain engineering, "works in staging, fails in prod" is the most common problem. The answer is almost always in the config diff.

### Basic diff:

```bash
diff etc/foodexpress/config_prod.properties etc/foodexpress/config_staging.properties
```

**Output format:**
- Lines starting with `<` are from the FIRST file (prod)
- Lines starting with `>` are from the SECOND file (staging)
- `3c3` means "line 3 changed"

### Side-by-side diff (much easier to read):

`-y` = side-b**y**-side format. Shows both files next to each other with `|` marking differences.

```bash
diff -y etc/foodexpress/config_prod.properties etc/foodexpress/config_staging.properties
```

**Output (partial):**
```
app.env=production                  |  app.env=staging
db.max_connections=100              |  db.max_connections=50
db.connection_timeout=5000          |  db.connection_timeout=10000
payment.gateway.url=https://api...  |  payment.gateway.url=https://sandbox...
log.level=INFO                      |  log.level=DEBUG
```

Lines with `|` are different. Lines without `|` are the same.

**Key finding:** Prod has `max_connections=100`, staging has only `50`. If customer_id=42's slow queries hold connections for 4 seconds each, 100 runs out fast.

### Count differences:

```bash
diff etc/foodexpress/config_prod.properties etc/foodexpress/config_staging.properties | grep "^[<>]" | wc -l
```

---

## 3.6 -- cut: Extract Specific Columns

`cut` splits each line by a delimiter and extracts specific fields. Like `split()` in programming.

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-d' '` | **d**elimiter | Character to split on (space, comma, `=`, `:`, etc.) |
| `-f2` | **f**ield number | Which column to extract after splitting (1-based) |
| `-f1,3` | **f**ields 1 and 3 | Extract multiple specific columns |
| `-f2-5` | **f**ields 2 through 5 | Extract a range of columns |

### Extract time from log:

```bash
cut -d' ' -f2 var/log/foodexpress/app.log | head -5
#    │      │
#    │      └── -f2 = give me field 2 (the time column)
#    └── -d' ' = split each line by SPACE
```

**Output:**
```
09:00:01
09:00:05
09:00:08
09:01:15
09:01:30
```

**How it works:** The log line `2026-08-24 09:00:01 INFO [order-service] ...` gets split by spaces. Field 1 = `2026-08-24` (date), Field 2 = `09:00:01` (time), Field 3 = `INFO` (level), etc.

### Extract config keys and values:

```bash
# Extract just the KEYS
grep -v "^#" etc/foodexpress/config_prod.properties | grep -v "^$" | cut -d'=' -f1

# Extract just the VALUES
grep -v "^#" etc/foodexpress/config_prod.properties | grep -v "^$" | cut -d'=' -f2
```

**How this works (every part explained):**
1. `grep -v "^#"` -- `-v` = exclude. `^#` = lines starting with `#` (the `^` means "start of line"). Removes comment lines.
2. `grep -v "^$"` -- `-v` = exclude. `^$` = lines that start and immediately end (the `$` means "end of line"). Removes empty lines.
3. `cut -d'=' -f1` -- `-d'='` = split by `=`. `-f1` = first field (the key name, left of `=`).

### cut vs awk:

`cut` fails when there are **multiple spaces** between columns (logs often have this). `awk` handles it automatically.

```bash
# This may give wrong results with cut (extra spaces)
cut -d' ' -f4 var/log/foodexpress/app.log

# This always works correctly
awk '{print $4}' var/log/foodexpress/app.log
```

**Rule of thumb:** Use `cut` for structured data with a consistent delimiter (CSV, config files). Use `awk` for logs and messy data.

---

## 3.7 -- paste: Merge Files Side by Side

`paste` combines multiple files column by column.

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-d'|'` | **d**elimiter | Character to place between merged columns (default is tab) |

```bash
# Create key and value files from configs
grep -v "^#" etc/foodexpress/config_prod.properties | grep -v "^$" | cut -d'=' -f1 > /tmp/keys.txt
grep -v "^#" etc/foodexpress/config_prod.properties | grep -v "^$" | cut -d'=' -f2 > /tmp/prod_vals.txt
grep -v "^#" etc/foodexpress/config_staging.properties | grep -v "^$" | cut -d'=' -f2 > /tmp/staging_vals.txt

# Merge them into a comparison table
paste -d'|' /tmp/keys.txt /tmp/prod_vals.txt /tmp/staging_vals.txt
```

**Output:**
```
app.name|foodexpress|foodexpress
app.env|production|staging
db.max_connections|100|50
db.connection_timeout|5000|10000
```

You just built a config comparison report with three commands.

---

## 3.8 -- sort: Order Data

| Command | Flags Stand For | What It Does |
|---------|----------------|-------------|
| `sort file` | (none) | Alphabetical sort (A-Z) |
| `sort -n file` | `-n` = **n**umeric | Sort as numbers (so 9 comes before 10) |
| `sort -r file` | `-r` = **r**everse | Reverse order (Z-A) |
| `sort -rn file` | `-r` = reverse, `-n` = numeric | Biggest number first (most common combo) |
| `sort -u file` | `-u` = **u**nique | Sort and remove duplicates |
| `sort -t'=' -k2 file` | `-t` = field separa**t**or, `-k` = **k**ey (column) | Split by `=`, sort by 2nd field |
| `sort -hr file` | `-h` = **h**uman numeric, `-r` = reverse | Sort human sizes like 15M, 8G (biggest first) |

### The essential combo: sort | uniq -c | sort -rn

```bash
# Count services with errors, ranked by frequency
grep "ERROR" var/log/foodexpress/app.log | awk '{print $4}' | sort | uniq -c | sort -rn
```

**Output:**
```
   9 [order-service]
   4 [payment-service]
```

**Why `sort` before `uniq`?** `uniq` only removes CONSECUTIVE duplicates. If you don't sort first, it misses non-adjacent duplicates.

---

## 3.9 -- touch: Create Files and Update Timestamps

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| (none) | -- | Create empty file, or update modification time to now |
| `-t YYYYMMDDhhmm` | **t**imestamp | Set a specific date/time instead of now |

```bash
# Create an empty file
touch incident_4721.md

# Create a marker file (used as flags in production)
touch var/log/foodexpress/MAINTENANCE_MODE

# Update the timestamp of an existing file to Aug 24, 2026, 09:13
touch -t 202608240913 var/log/foodexpress/INCIDENT_MARKER
#         │
#         └── -t 202608240913 = Year:2026, Month:08, Day:24, Hour:09, Min:13
```

**Sustain engineering uses:**
- Create lock files: `touch /tmp/deploy.lock`
- Create incident markers: `touch INCIDENT_STARTED`
- Test log rotation by changing file timestamps

---

## Section 3 Summary

```
find . -name "*.log"                    --> Find files by name
find . -size +100M                      --> Find files by size
find . -type d                          --> Find only directories
find . -name "*.log" -exec wc -l {} \;  --> Find + take action
find . -name "*.lock"                   --> Find that one rogue file

diff file1 file2                        --> Show differences
diff -y file1 file2                     --> Side-by-side comparison

cut -d'=' -f1 config.txt                --> Extract column (by delimiter)
cut -d' ' -f2 app.log                   --> Extract time from log
awk '{print $4}' app.log                --> Extract field (handles spaces)

paste -d'|' file1 file2                 --> Merge files side by side

sort -rn                                --> Sort: reverse, numeric
sort | uniq -c | sort -rn               --> Count + rank pattern

touch filename                          --> Create empty file
```

**The incident so far:** Found the lock file blocking DB restart. Compared prod vs staging configs. Identified disk hogs. Ready to check system resources in Section 4.

---

## Practice Exercises

Run `cd /tmp/foodexpress-server` first.

| # | Question | Command | Expected |
|---|----------|---------|----------|
| 1 | Find all `.properties` files | `find . -name "*.properties"` | 2 files |
| 2 | Find the lock file | `find . -name "*.lock"` | ./tmp/db.lock |
| 3 | Find files larger than 2MB | `find . -size +2M -exec ls -lh {} \;` | gc.log, access.log.old, app.log.old |
| 4 | Find all `.gz` files (archives) | `find . -name "*.gz"` | 2 files in archived/ |
| 5 | Count lines in every log file | `find . -name "*.log" -exec wc -l {} \;` | Varies per file |
| 6 | Side-by-side diff of configs | `diff -y etc/foodexpress/config_prod.properties etc/foodexpress/config_staging.properties` | Shows all differences |
| 7 | Extract just db settings from prod config | `grep "^db\." etc/foodexpress/config_prod.properties` | 6 db settings |
| 8 | Extract log levels from app.log | `awk '{print $3}' var/log/foodexpress/app.log \| sort \| uniq -c \| sort -rn` | INFO=14, ERROR=13, WARN=6, FATAL=2 |
| 9 | Extract only the time of FATAL errors | `grep "FATAL" var/log/foodexpress/app.log \| cut -d' ' -f2` | 09:13:15, 09:14:30 |
| 10 | Create an incident marker with specific timestamp | `touch -t 202608240913 /tmp/incident_marker` | File created |
