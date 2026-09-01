# Linux OS
## Module 20 | Sustain Engineering Training | Days 21-22

---

## Agenda -- Day 21

| # | Topic |
|---|-------|
| 01 | Introduction to Linux |
| 02 | Display Commands: echo, cat, more, less |
| 03 | Display Commands: head, tail |
| 04 | File Comparison: cmp, diff |
| 05 | File Manipulation: cut, paste |
| 06 | File Operations: touch, wc, links |
| 07 | Sorting and Searching: sort |
| 08 | Searching: find |
| 09 | Pattern Matching: grep, egrep |
| 10 | Lab Exercises |
| 11 | Day 21 Wrap-up |

---

## Agenda -- Day 22

| # | Topic |
|---|-------|
| 01 | Archiving: tar |
| 02 | System Resources: df, du, top |
| 03 | Process Management: ps, kill, crontab |
| 04 | Shells & Environment Variables |
| 05 | Remote Access: SSH, SFTP, rsync |
| 06 | Shell Scripting: Variables & Input |
| 07 | Shell Scripting: Control Statements |
| 08 | Shell Scripting: Loops & Functions |
| 09 | Lab Exercises |
| 10 | Day 22 Wrap-up |

---

## Why Linux for Sustain Engineering?

| Fact | Detail |
|------|--------|
| Server market share | ~80% of servers run Linux |
| Cloud native | AWS, GCP, Azure default to Linux |
| Containers | Docker containers are Linux-based |
| DevOps tools | Jenkins, Kubernetes, Ansible -- all Linux-first |
| Cost | Free and open source |

**FoodExpress:** All production servers, Docker containers, and CI/CD agents run Ubuntu 22.04 LTS.

---

## Linux File System Hierarchy

```
/
├── bin/        # Essential binaries (ls, cp, cat)
├── etc/        # Configuration files
├── home/       # User home directories
│   └── foodexpress/
├── var/        # Variable data (logs, databases)
│   └── log/
│       └── foodexpress/
├── tmp/        # Temporary files
├── usr/        # User programs
│   ├── bin/    # Non-essential binaries
│   └── local/  # Locally installed software
├── opt/        # Optional/third-party software
└── root/       # Root user's home
```

---

## Display Commands: echo

```bash
# Basic output
echo "Welcome to FoodExpress"

# With variables
echo "Server: $(hostname)"
echo "Date: $(date)"
echo "User: $USER"

# Escape sequences (-e flag)
echo -e "Menu Items:\n1. Burger\n2. Pizza\n3. Pasta"

# Write to a file
echo "order_id,customer,total" > orders.csv

# Append to a file
echo "1001,Priya,599.00" >> orders.csv

# No newline
echo -n "Processing order..."
```

---

## Display Commands: cat

```bash
# Display file contents
cat orders.csv

# Display with line numbers
cat -n orders.csv

# Display multiple files
cat header.csv data.csv > combined.csv

# Show non-printing characters
cat -A config.txt    # Shows $ for line endings, ^I for tabs

# Create a file with cat (heredoc)
cat > menu.txt << EOF
Burger - 199
Pizza - 299
Pasta - 249
EOF
```

**FoodExpress use:** Quickly view config files, log snippets, and CSV data.

---

## Display Commands: more & less

```bash
# more: Page through a file (forward only)
more /var/log/foodexpress/app.log
# Space = next page, Enter = next line, q = quit

# less: Page through a file (forward AND backward)
less /var/log/foodexpress/app.log
# Space = next page, b = previous page
# /pattern = search forward, ?pattern = search backward
# n = next match, N = previous match
# g = go to start, G = go to end, q = quit
```

| Feature | more | less |
|---------|------|------|
| Forward navigation | Yes | Yes |
| Backward navigation | No | Yes |
| Search | Limited | Full regex |
| Memory usage | Loads entire file | Loads on demand |
| Recommended | Small files | Large log files |

---

## Display Commands: head & tail

```bash
# head: Show first N lines (default 10)
head /var/log/foodexpress/app.log
head -n 5 orders.csv         # First 5 lines
head -c 100 app.log          # First 100 bytes

# tail: Show last N lines (default 10)
tail /var/log/foodexpress/app.log
tail -n 20 orders.csv        # Last 20 lines

# tail -f: Follow a log file in real-time (CRITICAL for sustain eng!)
tail -f /var/log/foodexpress/app.log

# Follow multiple files
tail -f /var/log/foodexpress/app.log /var/log/foodexpress/error.log

# Show lines 15-25 of a file
head -n 25 orders.csv | tail -n 11
```

**FoodExpress use:** `tail -f` is the #1 command for debugging live production issues. Watch logs as orders come in.

---

## File Comparison: cmp

```bash
# cmp: Compare two files byte by byte
cmp config.prod.yml config.staging.yml
# Output (if different):
# config.prod.yml config.staging.yml differ: byte 245, line 12

# Silent mode (exit code only)
cmp -s config.prod.yml config.staging.yml
echo $?   # 0 = identical, 1 = different

# Show all differences
cmp -l config.prod.yml config.staging.yml
```

**Use case:** Quickly check if two config files are identical after a deployment.

---

## File Comparison: diff

```bash
# diff: Show line-by-line differences
diff config.prod.yml config.staging.yml

# Output format:
# 12c12        ← line 12 changed
# < db_host: db.prod.foodexpress.in
# ---
# > db_host: db.staging.foodexpress.in

# Unified format (more readable, used in Git)
diff -u old_menu.js new_menu.js

# Side-by-side comparison
diff -y config.prod.yml config.staging.yml

# Ignore whitespace differences
diff -w file1.txt file2.txt

# Compare directories
diff -r dir1/ dir2/
```

| Symbol | Meaning |
|--------|---------|
| `<` | Line exists only in first file |
| `>` | Line exists only in second file |
| `c` | Changed |
| `a` | Added |
| `d` | Deleted |

---

## File Manipulation: cut

```bash
# Sample file: orders.csv
# order_id,customer,item,quantity,price
# 1001,Priya,Burger,2,199.00
# 1002,Amit,Pizza,1,299.00
# 1003,Sara,Pasta,3,249.00

# Cut by field (delimiter = comma)
cut -d',' -f2 orders.csv          # Customer names
cut -d',' -f2,5 orders.csv        # Customer and price
cut -d',' -f2-4 orders.csv        # Fields 2 through 4

# Cut by character position
cut -c1-10 orders.csv             # First 10 characters

# Cut by bytes
cut -b1-5 orders.csv
```

**FoodExpress use:** Extract specific columns from CSV exports (order reports, menu data).

---

## File Manipulation: paste

```bash
# Sample files:
# names.txt:    prices.txt:
# Burger        199
# Pizza         299
# Pasta         249

# Merge files side by side (tab-delimited)
paste names.txt prices.txt
# Burger  199
# Pizza   299
# Pasta   249

# Custom delimiter
paste -d',' names.txt prices.txt
# Burger,199
# Pizza,299
# Pasta,249

# Merge lines from a single file into one line
paste -s -d',' names.txt
# Burger,Pizza,Pasta
```

---

## File Operations: touch

```bash
# Create an empty file
touch menu_backup.txt

# Create multiple files
touch order_1.log order_2.log order_3.log

# Update timestamp of existing file (without modifying content)
touch -t 202607270900 app.log     # Set to specific time

# Check if file exists (using touch + test)
if [ ! -f config.yml ]; then
    touch config.yml
    echo "Created config.yml"
fi
```

---

## File Operations: wc (word count)

```bash
# Count lines, words, and characters
wc orders.csv
#  4  4  156  orders.csv
# lines  words  bytes

# Count lines only
wc -l orders.csv
# 4 orders.csv

# Count words only
wc -w orders.csv

# Count characters only
wc -c orders.csv

# Count lines in multiple files
wc -l *.log

# Count active orders in FoodExpress
grep -c "IN_PROGRESS" orders.csv
```

**FoodExpress use:** `wc -l access.log` to count total requests; `grep -c "ERROR" app.log` to count errors.

---

## File Operations: Links

### Hard Links vs Symbolic (Soft) Links

```bash
# Hard link: Second name for the same file (same inode)
ln orders.csv orders_backup.csv

# Symbolic link: Shortcut/pointer to a file
ln -s /var/log/foodexpress/app.log ~/app.log

# Check link type
ls -l ~/app.log
# lrwxrwxrwx 1 user user 32 Jul 27 app.log -> /var/log/foodexpress/app.log
```

| Feature | Hard Link | Symbolic Link |
|---------|-----------|---------------|
| Same inode | Yes | No |
| Cross filesystem | No | Yes |
| Link to directory | No | Yes |
| Original deleted | File still accessible | Link breaks (dangling) |
| Syntax | `ln source target` | `ln -s source target` |

---

## Sorting: sort

```bash
# Sort alphabetically
sort menu.txt

# Sort numerically
sort -n prices.txt

# Sort in reverse
sort -r menu.txt

# Sort by specific field (comma-delimited, field 5 = price)
sort -t',' -k5 -n orders.csv

# Sort and remove duplicates
sort -u categories.txt

# Sort by multiple keys
sort -t',' -k2,2 -k5,5n orders.csv    # By customer, then by price

# FoodExpress: Top 10 most expensive orders
sort -t',' -k5 -n -r orders.csv | head -n 10
```

---

## Searching: find

```bash
# Find by name
find /var/log -name "*.log"

# Find by name (case-insensitive)
find /home -iname "*.config"

# Find by type (f=file, d=directory)
find /opt/foodexpress -type f -name "*.java"
find /opt/foodexpress -type d -name "config"

# Find by size
find /var/log -size +100M                    # Files larger than 100MB
find /tmp -size 0                            # Empty files

# Find by modification time
find /var/log -mtime -1                      # Modified in last 24 hours
find /var/log -mtime +30                     # Modified more than 30 days ago

# Find and execute
find /var/log -name "*.log" -mtime +30 -exec rm {} \;
find /opt/foodexpress -name "*.java" -exec grep -l "TODO" {} \;

# Find with max depth
find /opt/foodexpress -maxdepth 2 -name "*.yml"
```

---

## Pattern Matching: grep

```bash
# Search for a pattern in a file
grep "ERROR" /var/log/foodexpress/app.log

# Case-insensitive search
grep -i "error" app.log

# Show line numbers
grep -n "ERROR" app.log

# Count matches
grep -c "ERROR" app.log

# Search recursively in directories
grep -r "TODO" /opt/foodexpress/src/

# Invert match (lines NOT containing pattern)
grep -v "DEBUG" app.log

# Show context (3 lines before and after)
grep -B3 -A3 "NullPointerException" app.log

# Search for whole words only
grep -w "port" config.yml      # Matches "port", not "export"

# Multiple patterns
grep -e "ERROR" -e "FATAL" app.log
```

---

## Pattern Matching: grep with Regex

```bash
# Match lines starting with "2026"
grep "^2026" app.log

# Match lines ending with "ERROR"
grep "ERROR$" app.log

# Match any single character
grep "order.id" app.log         # order_id, order-id, order.id

# Match zero or more
grep "order.*failed" app.log    # "order 1001 failed", "order processing failed"

# FoodExpress examples:
# Find all 500 errors
grep "HTTP/1.1\" 5[0-9][0-9]" access.log

# Find orders from a specific customer
grep "customer_id=42" app.log

# Find slow queries (over 1 second)
grep "query_time=[1-9]" slow_query.log
```

---

## Extended Grep: egrep

```bash
# egrep = grep -E (extended regex)

# OR pattern
egrep "ERROR|WARN|FATAL" app.log

# One or more occurrences
egrep "order_id=[0-9]+" app.log

# Optional character
egrep "colou?r" file.txt        # color or colour

# Grouping
egrep "(GET|POST|PUT|DELETE) /api/" access.log

# Exact repetition
egrep "[0-9]{3}\.[0-9]{2}" orders.csv    # Prices like 199.00

# FoodExpress: Find all API calls with response time > 500ms
egrep "response_time=([5-9][0-9]{2}|[0-9]{4,})" app.log
```

---

## Archiving: tar

```bash
# Create a tar archive
tar -cvf backup.tar /opt/foodexpress/config/
# c=create, v=verbose, f=filename

# Create compressed archive (gzip)
tar -czvf backup.tar.gz /opt/foodexpress/config/

# Create compressed archive (bzip2)
tar -cjvf backup.tar.bz2 /opt/foodexpress/config/

# List contents of an archive
tar -tvf backup.tar.gz

# Extract an archive
tar -xzvf backup.tar.gz

# Extract to a specific directory
tar -xzvf backup.tar.gz -C /tmp/restore/

# Extract specific files
tar -xzvf backup.tar.gz opt/foodexpress/config/app.yml
```

| Flag | Meaning |
|------|---------|
| `-c` | Create archive |
| `-x` | Extract archive |
| `-t` | List contents |
| `-v` | Verbose output |
| `-f` | Specify filename |
| `-z` | gzip compression |
| `-j` | bzip2 compression |

---

## System Resources: df & du

```bash
# df: Disk free space
df -h                    # Human-readable (GB, MB)
df -h /var/log           # Specific mount point

# Sample output:
# Filesystem  Size  Used  Avail  Use%  Mounted on
# /dev/sda1   100G   65G   35G   65%   /
# /dev/sdb1   500G  320G  180G   64%   /var

# du: Disk usage (directory sizes)
du -sh /var/log/foodexpress/      # Total size of directory
du -h --max-depth=1 /opt/         # Size of each subdirectory
du -sh /var/log/*.log | sort -hr  # Largest log files first

# FoodExpress: Find what's eating disk space
du -sh /var/log/foodexpress/* | sort -hr | head -5
```

**Sustain use:** When disk space alerts fire, use `du` to find the culprit (usually old logs).

---

## System Resources: top

```bash
# Interactive process monitor
top

# Key columns:
# PID    - Process ID
# USER   - Process owner
# %CPU   - CPU usage
# %MEM   - Memory usage
# TIME+  - Total CPU time
# COMMAND - Process name

# Useful keys inside top:
# P - Sort by CPU
# M - Sort by Memory
# k - Kill a process (enter PID)
# q - Quit

# Non-interactive: show top 10 CPU consumers
top -bn1 | head -17

# Alternative: htop (more user-friendly)
htop
```

---

## Process Management: ps

```bash
# Show your processes
ps

# Show all processes (full format)
ps -ef

# Show all processes (BSD format)
ps aux

# Find a specific process
ps aux | grep java
ps aux | grep "foodexpress"

# Show process tree
ps -ef --forest

# Show specific columns
ps -eo pid,user,%cpu,%mem,command | head -20

# FoodExpress: Find the order service process
ps aux | grep "order-service"
# user  12345  2.5  8.3  java -jar order-service.jar
```

---

## Process Management: kill & crontab

```bash
# Send signals to processes
kill <PID>              # Default: SIGTERM (graceful)
kill -9 <PID>           # SIGKILL (force, last resort)
kill -HUP <PID>         # SIGHUP (reload config)

# Kill by name
killall java
pkill -f "order-service"

# Common signals:
# 1  (SIGHUP)  - Reload configuration
# 9  (SIGKILL) - Force kill (cannot be caught)
# 15 (SIGTERM) - Graceful shutdown (default)

# crontab: Schedule recurring tasks
crontab -e              # Edit crontab
crontab -l              # List crontab

# Crontab format: minute hour day month weekday command
# FoodExpress examples:
# Daily log cleanup at 2 AM
0 2 * * * find /var/log/foodexpress -name "*.log" -mtime +30 -delete

# Every 5 minutes: check disk space
*/5 * * * * /opt/foodexpress/scripts/check_disk.sh

# Monday at 6 AM: generate weekly report
0 6 * * 1 /opt/foodexpress/scripts/weekly_report.sh
```

---

## Crontab Schedule Reference

```
┌──────── minute (0-59)
│ ┌────── hour (0-23)
│ │ ┌──── day of month (1-31)
│ │ │ ┌── month (1-12)
│ │ │ │ ┌ day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * * command

Examples:
0 * * * *     Every hour on the hour
*/15 * * * *  Every 15 minutes
0 9 * * 1-5   Weekdays at 9 AM
0 0 1 * *     First day of every month at midnight
30 2 * * 0    Sundays at 2:30 AM
```

---

## Shells & Environment Variables

### Common Shells

| Shell | Path | Description |
|-------|------|-------------|
| bash | `/bin/bash` | Bourne Again Shell (most common) |
| sh | `/bin/sh` | Bourne Shell (POSIX compliant) |
| zsh | `/bin/zsh` | Z Shell (default on macOS) |
| fish | `/usr/bin/fish` | Friendly Interactive Shell |

```bash
# Check current shell
echo $SHELL

# List available shells
cat /etc/shells

# Change default shell
chsh -s /bin/zsh
```

---

## Environment Variables

```bash
# View all environment variables
env
printenv

# View specific variable
echo $HOME
echo $PATH
echo $USER

# Set a variable (current session)
export FOODEXPRESS_ENV=production
export DB_HOST=db.foodexpress.in
export DB_PORT=3306

# Persist variables (add to ~/.bashrc or ~/.bash_profile)
echo 'export FOODEXPRESS_ENV=production' >> ~/.bashrc
source ~/.bashrc    # Reload

# Unset a variable
unset FOODEXPRESS_ENV

# PATH: Where the shell looks for commands
echo $PATH
export PATH=$PATH:/opt/foodexpress/bin
```

---

## Remote Access: SSH

```bash
# Connect to a remote server
ssh user@server.foodexpress.in

# Connect on a specific port
ssh -p 2222 user@server.foodexpress.in

# SSH with key authentication
ssh -i ~/.ssh/foodexpress_key.pem user@server.foodexpress.in

# Generate SSH key pair
ssh-keygen -t ed25519 -C "priya@foodexpress.in"
# Creates: ~/.ssh/id_ed25519 (private) and ~/.ssh/id_ed25519.pub (public)

# Copy public key to remote server
ssh-copy-id user@server.foodexpress.in

# SSH config file (~/.ssh/config)
Host foodexpress-prod
    HostName prod.foodexpress.in
    User deploy
    IdentityFile ~/.ssh/foodexpress_key.pem
    Port 22

# Then connect with:
ssh foodexpress-prod
```

---

## Remote File Transfer: SFTP & rsync

```bash
# SFTP: Secure File Transfer
sftp user@server.foodexpress.in
# Commands inside sftp:
# put local_file.txt          Upload file
# get remote_file.txt         Download file
# ls                          List remote files
# lls                         List local files
# cd /var/log                  Change remote directory
# lcd /tmp                    Change local directory
# exit                        Quit

# rsync: Efficient file sync
# Copy local to remote
rsync -avz /opt/foodexpress/config/ user@server:/opt/foodexpress/config/

# Copy remote to local
rsync -avz user@server:/var/log/foodexpress/ /tmp/logs/

# Dry run (show what would be copied)
rsync -avzn /opt/foodexpress/config/ user@server:/opt/foodexpress/config/
```

| Flag | Meaning |
|------|---------|
| `-a` | Archive mode (preserves permissions, timestamps) |
| `-v` | Verbose |
| `-z` | Compress during transfer |
| `-n` | Dry run |

---

## Shell Scripting: Variables

```bash
#!/bin/bash
# FoodExpress deployment script

# Variable assignment (no spaces around =)
APP_NAME="order-service"
VERSION="2.3.1"
DEPLOY_DIR="/opt/foodexpress"
LOG_FILE="/var/log/foodexpress/deploy.log"

# Using variables
echo "Deploying $APP_NAME version $VERSION"
echo "Deploy directory: ${DEPLOY_DIR}/${APP_NAME}"

# Command substitution
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HOSTNAME=$(hostname)

# Read user input
read -p "Enter environment (staging/production): " ENVIRONMENT

# Special variables
echo "Script name: $0"
echo "First argument: $1"
echo "All arguments: $@"
echo "Number of arguments: $#"
echo "Last exit code: $?"
```

---

## Shell Scripting: Control Statements

```bash
#!/bin/bash

# if-else
ENVIRONMENT=$1

if [ "$ENVIRONMENT" = "production" ]; then
    echo "WARNING: Deploying to PRODUCTION"
    DB_HOST="db.prod.foodexpress.in"
elif [ "$ENVIRONMENT" = "staging" ]; then
    echo "Deploying to staging"
    DB_HOST="db.staging.foodexpress.in"
else
    echo "ERROR: Unknown environment: $ENVIRONMENT"
    exit 1
fi

# File test operators
if [ -f "/opt/foodexpress/config.yml" ]; then
    echo "Config file exists"
fi

if [ -d "/var/log/foodexpress" ]; then
    echo "Log directory exists"
fi

# Numeric comparison
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "ALERT: Disk usage is ${DISK_USAGE}%"
fi
```

---

## Shell Scripting: Test Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `-f` | File exists | `[ -f config.yml ]` |
| `-d` | Directory exists | `[ -d /var/log ]` |
| `-r` | File is readable | `[ -r app.log ]` |
| `-w` | File is writable | `[ -w config.yml ]` |
| `-x` | File is executable | `[ -x deploy.sh ]` |
| `-s` | File is non-empty | `[ -s error.log ]` |
| `-z` | String is empty | `[ -z "$VAR" ]` |
| `-n` | String is non-empty | `[ -n "$VAR" ]` |
| `-eq` | Numeric equal | `[ "$a" -eq 5 ]` |
| `-ne` | Numeric not equal | `[ "$a" -ne 0 ]` |
| `-gt` | Greater than | `[ "$a" -gt 10 ]` |
| `-lt` | Less than | `[ "$a" -lt 100 ]` |
| `=` | String equal | `[ "$a" = "yes" ]` |
| `!=` | String not equal | `[ "$a" != "no" ]` |

---

## Shell Scripting: Loops

```bash
#!/bin/bash

# for loop: Iterate over list
for SERVICE in order-service menu-service payment-service; do
    echo "Checking $SERVICE..."
    systemctl status $SERVICE
done

# for loop: Iterate over files
for LOG in /var/log/foodexpress/*.log; do
    echo "$(wc -l < "$LOG") lines in $LOG"
done

# for loop: C-style
for ((i=1; i<=5; i++)); do
    echo "Attempt $i of 5"
done

# while loop
RETRY=0
MAX_RETRY=5
while [ $RETRY -lt $MAX_RETRY ]; do
    if curl -s http://localhost:8080/health | grep -q "UP"; then
        echo "Service is UP"
        break
    fi
    RETRY=$((RETRY + 1))
    echo "Retry $RETRY/$MAX_RETRY..."
    sleep 5
done

# Read file line by line
while IFS= read -r line; do
    echo "Processing: $line"
done < orders.csv
```

---

## Shell Scripting: Functions

```bash
#!/bin/bash

# Define a function
deploy_service() {
    local SERVICE_NAME=$1
    local VERSION=$2
    local DEPLOY_DIR="/opt/foodexpress/$SERVICE_NAME"

    echo "[$(date)] Deploying $SERVICE_NAME v$VERSION"

    # Check if directory exists
    if [ ! -d "$DEPLOY_DIR" ]; then
        echo "ERROR: Deploy directory not found: $DEPLOY_DIR"
        return 1
    fi

    # Stop the service
    systemctl stop $SERVICE_NAME

    # Copy new JAR
    cp /tmp/${SERVICE_NAME}-${VERSION}.jar ${DEPLOY_DIR}/app.jar

    # Start the service
    systemctl start $SERVICE_NAME

    # Verify
    sleep 5
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo "SUCCESS: $SERVICE_NAME is running"
        return 0
    else
        echo "FAILED: $SERVICE_NAME did not start"
        return 1
    fi
}

# Call the function
deploy_service "order-service" "2.3.1"
if [ $? -ne 0 ]; then
    echo "Deployment failed! Rolling back..."
fi
```

---

## Complete Script Example: Health Check

```bash
#!/bin/bash
# FoodExpress Service Health Check Script

SERVICES=("order-service:8080" "menu-service:3000" "payment-service:8081")
ALERT_EMAIL="oncall@foodexpress.in"
LOG="/var/log/foodexpress/healthcheck.log"

check_service() {
    local name=$(echo $1 | cut -d: -f1)
    local port=$(echo $1 | cut -d: -f2)
    local url="http://localhost:${port}/health"

    if curl -s --max-time 5 "$url" | grep -q "UP"; then
        echo "[$(date)] OK: $name is healthy" >> "$LOG"
        return 0
    else
        echo "[$(date)] ALERT: $name is DOWN!" >> "$LOG"
        return 1
    fi
}

failed_services=""
for svc in "${SERVICES[@]}"; do
    if ! check_service "$svc"; then
        name=$(echo $svc | cut -d: -f1)
        failed_services="$failed_services $name"
    fi
done

if [ -n "$failed_services" ]; then
    echo "ALERT: Services down:$failed_services" | mail -s "FoodExpress Health Alert" "$ALERT_EMAIL"
fi
```

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Display commands | `cat` to view, `less` to page, `tail -f` to follow logs live |
| File comparison | `diff -u` for readable diffs; `cmp` for binary comparison |
| File manipulation | `cut` to extract columns; `paste` to merge; `wc -l` for line count |
| Searching | `find` for files by name/size/date; `grep` for content; `egrep` for regex |
| Archiving | `tar -czvf` to create; `tar -xzvf` to extract |
| System resources | `df -h` for disk; `du -sh` for directory size; `top` for CPU/memory |
| Process management | `ps aux` to list; `kill` to stop; `crontab` to schedule |
| Shell scripting | Variables, if/else, for/while loops, functions |
| Remote access | `ssh` to connect; `rsync` to sync files efficiently |
| Sustain relevance | Every production debugging session starts on a Linux terminal |

> **Next: Module 21 -- Apache Web Server**
