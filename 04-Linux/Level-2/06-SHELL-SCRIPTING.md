# Section 10: Shell Scripting -- "Automate Everything"

## Day 20 | Linux OS (Day 2) | Time: ~45 minutes

---

## The Scenario

> "Yesterday you manually ran 8 commands to fix the incident. Today, you write a script so that next time, ONE command does it all. That's the power of shell scripting."

---

## 10.1 -- Your First Script

### Create the file:

```bash
nano ~/hello.sh
```

### Write this:

```bash
#!/bin/bash
# My first shell script
echo "Hello, I am $(whoami) on $(hostname)"
echo "Today is $(date +%Y-%m-%d)"
echo "Current directory: $(pwd)"
```

### Make it executable and run:

```bash
chmod +x ~/hello.sh
./hello.sh
```

| Part | Meaning |
|------|---------|
| `#!/bin/bash` | **Shebang** -- tells Linux which program to use to run this script |
| `#` | Comment -- ignored by the shell, notes for humans |
| `chmod +x` | **ch**ange **mod**e + e**x**ecute -- gives the file permission to run |
| `./hello.sh` | Run the script (`./ ` = current directory) |

---

## 10.2 -- Variables

```bash
#!/bin/bash

# Defining variables (NO spaces around =)
APP_NAME="order-service"
VERSION="2.1.0"
PORT=8080

# Using variables (prefix with $)
echo "Deploying $APP_NAME version $VERSION on port $PORT"

# Curly braces for clarity (when variable is next to other text)
echo "Log file: /var/log/${APP_NAME}.log"
#                        ↑ Without braces, shell looks for $APP_NAME.log (wrong)
```

### Reading user input:

```bash
#!/bin/bash

echo "Enter the service name:"
read SERVICE_NAME
# read = wait for user to type something and press Enter

echo "Enter the port number:"
read PORT

echo "Starting $SERVICE_NAME on port $PORT..."
```

`read` = **read** a line of input from the user. Stores it in the variable.

```bash
read -p "Enter service name: " SERVICE_NAME
```

`-p` = **p**rompt. Shows the message and reads input on the same line.

### Command line arguments:

```bash
#!/bin/bash
# File: deploy.sh
# Usage: ./deploy.sh order-service 2.1.0

APP_NAME=$1    # First argument
VERSION=$2     # Second argument

echo "Deploying $APP_NAME version $VERSION"
```

| Variable | Meaning |
|----------|---------|
| `$0` | Script name itself (`./deploy.sh`) |
| `$1` | First argument |
| `$2` | Second argument |
| `$#` | Number of arguments passed |
| `$@` | All arguments as a list |

---

## 10.3 -- if/else: Make Decisions

### Basic syntax:

```bash
#!/bin/bash

FILE="/var/log/foodexpress/app.log"

if [ -f "$FILE" ]; then
    echo "Log file exists"
    echo "Lines: $(wc -l < "$FILE")"
else
    echo "ERROR: Log file not found!"
    exit 1
fi
```

| Part | Meaning |
|------|---------|
| `if [ condition ]; then` | Start of if block |
| `else` | What to do if condition is false |
| `fi` | End of if block (`if` spelled backwards) |
| `exit 1` | Exit script with error code 1 (0 = success, non-zero = error) |

### Test conditions:

**File tests:**

| Test | Stands For | True When |
|------|-----------|-----------|
| `-f file` | is a **f**ile | File exists and is a regular file |
| `-d dir` | is a **d**irectory | Directory exists |
| `-e path` | **e**xists | File or directory exists |
| `-r file` | is **r**eadable | File exists and you can read it |
| `-w file` | is **w**ritable | File exists and you can write to it |
| `-x file` | is e**x**ecutable | File exists and you can execute it |
| `-s file` | has **s**ize | File exists and is not empty |

**String tests:**

| Test | Meaning | Example |
|------|---------|---------|
| `-z "$VAR"` | Is **z**ero length (empty) | `if [ -z "$APP_NAME" ]; then` |
| `-n "$VAR"` | Is **n**ot empty | `if [ -n "$APP_NAME" ]; then` |
| `"$A" = "$B"` | Strings are equal | `if [ "$ENV" = "production" ]; then` |
| `"$A" != "$B"` | Strings are not equal | `if [ "$ENV" != "staging" ]; then` |

**Number tests:**

| Test | Stands For | Meaning |
|------|-----------|---------|
| `-eq` | **eq**ual | `if [ $COUNT -eq 0 ]; then` |
| `-ne` | **n**ot **e**qual | `if [ $COUNT -ne 0 ]; then` |
| `-gt` | **g**reater **t**han | `if [ $COUNT -gt 10 ]; then` |
| `-lt` | **l**ess **t**han | `if [ $COUNT -lt 5 ]; then` |
| `-ge` | **g**reater or **e**qual | `if [ $COUNT -ge 10 ]; then` |
| `-le` | **l**ess or **e**qual | `if [ $COUNT -le 100 ]; then` |

### Real example: Health check script

```bash
#!/bin/bash
# healthcheck.sh -- Check if the service is healthy

URL="http://localhost:8080/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
# -s = silent, -o /dev/null = discard body, -w = write out status code

if [ "$RESPONSE" = "200" ]; then
    echo "$(date): Service is UP"
else
    echo "$(date): Service is DOWN (HTTP $RESPONSE)"
    exit 1
fi
```

---

## 10.4 -- Loops: Repeat Things

### for loop (iterate over a list):

```bash
#!/bin/bash

# Loop over a list of services
for SERVICE in order-service menu-service payment-service; do
    echo "Checking $SERVICE..."
    ps aux | grep "$SERVICE" | grep -v grep
done
```

| Part | Meaning |
|------|---------|
| `for VAR in list; do` | Start of loop |
| `done` | End of loop |

### for loop (iterate over files):

```bash
#!/bin/bash

# Count lines in every log file
for FILE in ~/foodexpress-server/var/log/foodexpress/*.log; do
    LINES=$(wc -l < "$FILE")
    echo "$FILE: $LINES lines"
done
```

### for loop (iterate over numbers):

```bash
#!/bin/bash

# Check ports 8080 to 8085
for PORT in $(seq 8080 8085); do
    curl -s -o /dev/null -w "Port $PORT: HTTP %{http_code}\n" http://localhost:$PORT/health
done
```

`seq 8080 8085` = generate sequence: 8080, 8081, 8082, 8083, 8084, 8085.

### while loop (repeat until condition is false):

```bash
#!/bin/bash

# Wait for service to come up (check every 5 seconds, max 60 seconds)
ATTEMPTS=0
MAX_ATTEMPTS=12

while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)
    if [ "$RESPONSE" = "200" ]; then
        echo "Service is UP after $((ATTEMPTS * 5)) seconds"
        exit 0
    fi
    echo "Waiting... (attempt $((ATTEMPTS + 1))/$MAX_ATTEMPTS)"
    sleep 5
    ATTEMPTS=$((ATTEMPTS + 1))
done

echo "Service did NOT come up in 60 seconds!"
exit 1
```

| Part | Meaning |
|------|---------|
| `while [ condition ]; do` | Loop while condition is true |
| `$((expression))` | Arithmetic: `$((5 + 3))` = 8, `$((ATTEMPTS + 1))` |

---

## 10.5 -- Functions: Reusable Blocks

```bash
#!/bin/bash

# Define a function
check_service() {
    local SERVICE=$1       # local = variable only exists inside this function
    local PORT=$2

    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/health")
    if [ "$RESPONSE" = "200" ]; then
        echo "[OK]   $SERVICE (port $PORT)"
    else
        echo "[FAIL] $SERVICE (port $PORT) -- HTTP $RESPONSE"
    fi
}

# Call the function
check_service "order-service" 8080
check_service "menu-service" 3000
check_service "payment-service" 8081
```

| Part | Meaning |
|------|---------|
| `function_name() { ... }` | Define a function |
| `local VAR=value` | Variable scoped to this function only |
| `$1, $2` | Arguments passed to the function |

---

## 10.6 -- Real Script: Incident Auto-Fix

Combining EVERYTHING from Day 1 and Day 2:

```bash
#!/bin/bash
# incident_autofix.sh -- Automated incident response for FoodExpress
# Usage: ./incident_autofix.sh

set -euo pipefail
# set -e = exit on any error
# set -u = error on undefined variables
# set -o pipefail = catch errors in pipes

LOG_DIR="$HOME/foodexpress-server/var/log/foodexpress"
APP_LOG="$LOG_DIR/app.log"
REPORT="/tmp/incident_report_$(date +%Y%m%d_%H%M%S).txt"

# Function: Log with timestamp
log() {
    echo "$(date +%H:%M:%S) -- $1" | tee -a "$REPORT"
    # tee -a = print to screen AND append to file
}

# Function: Check error count
check_errors() {
    local ERROR_COUNT=$(grep -c "ERROR" "$APP_LOG")
    local FATAL_COUNT=$(grep -c "FATAL" "$APP_LOG")
    local WARN_COUNT=$(grep -c "WARN" "$APP_LOG")

    log "Error Summary: $ERROR_COUNT ERRORs, $FATAL_COUNT FATALs, $WARN_COUNT WARNs"

    if [ "$FATAL_COUNT" -gt 0 ]; then
        log "CRITICAL: FATAL errors found!"
        grep "FATAL" "$APP_LOG" >> "$REPORT"
        return 1
    fi
    return 0
}

# Function: Check disk space
check_disk() {
    local USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    log "Disk usage: ${USAGE}%"

    if [ "$USAGE" -gt 90 ]; then
        log "WARNING: Disk above 90%! Cleaning old logs..."
        local CLEANED=$(find "$LOG_DIR" -name "*.log.*" -mtime +7 | wc -l)
        log "Found $CLEANED old log files to archive"
    fi
}

# Function: Check for lock files
check_locks() {
    local LOCKS=$(find "$HOME/foodexpress-server" -name "*.lock" 2>/dev/null)
    if [ -n "$LOCKS" ]; then
        log "WARNING: Lock files found:"
        echo "$LOCKS" | tee -a "$REPORT"
    else
        log "No lock files found"
    fi
}

# Function: Top error types
error_breakdown() {
    log "--- Error Breakdown ---"
    grep "ERROR" "$APP_LOG" | awk '{print $4}' | sort | uniq -c | sort -rn >> "$REPORT"
}

# Main execution
log "=========================================="
log "INCIDENT AUTO-CHECK STARTED"
log "Server: $(hostname)"
log "User: $(whoami)"
log "=========================================="

check_errors
check_disk
check_locks
error_breakdown

log "=========================================="
log "REPORT SAVED: $REPORT"
log "=========================================="

cat "$REPORT"
```

### Make it executable and run:

```bash
chmod +x incident_autofix.sh
./incident_autofix.sh
```

---

## 10.7 -- Debugging Scripts

| Technique | How | What It Does |
|-----------|-----|-------------|
| `bash -x script.sh` | Run with `-x` flag | Prints every command before executing it |
| `set -x` | Add inside script | Same, but only from that point onward |
| `set +x` | Add inside script | Turn off debug output |
| `echo "DEBUG: $VAR"` | Add print statements | Oldest trick in the book |
| `set -e` | Add at top of script | Exit immediately if any command fails |
| `set -u` | Add at top of script | Error if you use an undefined variable |

```bash
#!/bin/bash
set -x    # Turn on debug mode

APP="order-service"
echo "Deploying $APP"
# Debug output will show:
# + APP=order-service
# + echo 'Deploying order-service'
# Deploying order-service

set +x    # Turn off debug mode
```

---

## Section 10 Summary

```
# Script basics
#!/bin/bash              Shebang (always first line)
chmod +x script.sh       Make executable
./script.sh              Run the script

# Variables
VAR="value"              Set a variable (NO spaces around =)
echo $VAR                Read a variable
$1, $2, $3               Command line arguments
read VAR                 Read user input
export VAR               Make available to child processes

# if/else
if [ condition ]; then
    commands
elif [ condition ]; then
    commands
else
    commands
fi

# Tests
-f file    (file exists)     -d dir    (directory exists)
-z "$VAR"  (empty string)    -n "$VAR" (not empty)
-eq -ne -gt -lt -ge -le     (number comparisons)
=  !=                        (string comparisons)

# Loops
for VAR in list; do          while [ condition ]; do
    commands                     commands
done                         done

# Functions
func_name() {
    local VAR=$1
    commands
}

# Arithmetic
$((5 + 3))                   Result: 8
$((COUNT + 1))               Increment

# Debugging
bash -x script.sh            Show each command as it runs
set -euo pipefail            Exit on error, undefined vars, pipe fails
```

---

## Practice Exercises

| # | Task | What To Do |
|---|------|-----------|
| 1 | Write hello.sh that prints your name and date | `echo "Hello $(whoami), today is $(date +%Y-%m-%d)"` |
| 2 | Write greet.sh that takes a name as argument | `echo "Hello $1"`, run with `./greet.sh Pappu` |
| 3 | Write filecheck.sh that checks if a file exists | Use `if [ -f "$1" ]; then` |
| 4 | Write a loop that counts ERROR, WARN, FATAL in app.log | `for LEVEL in ERROR WARN FATAL; do grep -c $LEVEL app.log; done` |
| 5 | Write a script that loops through all .log files and counts lines | Use `for FILE in *.log; do wc -l "$FILE"; done` |
| 6 | Write a disk check script that warns if usage > 80% | Use `df -h`, `awk`, and `if [ $USAGE -gt 80 ]` |
| 7 | Write a function that checks if a port is open | Use `curl -s -o /dev/null -w "%{http_code}"` |
| 8 | Modify the incident_autofix.sh and run it | Copy from section 10.6, run on the server |
| 9 | Schedule your script to run every hour | `crontab -e`, add `0 * * * * /home/user/incident_autofix.sh` |
| 10 | Debug a script with bash -x | `bash -x ./hello.sh` |
