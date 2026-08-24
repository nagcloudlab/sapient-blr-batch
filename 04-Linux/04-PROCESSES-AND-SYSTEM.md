# Section 4: Processes & System Resources -- "Is the Server Healthy NOW?"

## Day 19 | Linux OS | Time: ~40 minutes

---

## The Scenario

You removed the lock file. Database should restart. But the server still feels slow. Is something eating CPU? Is disk actually full? Is the order-service even running? Time to check vital signs.

---

## 4.1 -- df: Disk Space

`df` = **D**isk **F**ree. Shows how much space is available on each disk partition.

```bash
df -h
```

**Output:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   46G  4.0G  92% /
/dev/sda2       200G  112G   88G  56% /var
/dev/sda3       100G   23G   77G  23% /opt
tmpfs           3.9G  428M  3.5G  11% /tmp
```

**Reading the output:**

| Column | Meaning |
|--------|---------|
| `Size` | Total partition size |
| `Used` | Space used |
| `Avail` | Space free |
| `Use%` | Percentage used (THE KEY NUMBER) |
| `Mounted on` | Where this partition is accessible |

**Health rules:**

| Use% | Status | Action |
|------|--------|--------|
| < 70% | Green | No action needed |
| 70-85% | Yellow | Plan cleanup |
| 85-95% | Red | Clean up NOW |
| > 95% | Critical | Services may crash |

Root partition `/` is at **92%**. That's red. Above 90%, things break: temp files can't be written, logs can't rotate, deployments fail.

**Always `-h`:** Without `-h` you get bytes (impossible to read). `-h` = human readable (KB, MB, GB).

**Sustain engineering context:** First thing you check in any incident after reading logs: `df -h`. If disk is full, NOTHING works.

---

## 4.2 -- du: Which Folder Is Using the Space?

`du` = **D**isk **U**sage. Shows how much space each directory uses. `df` tells you the partition is full. `du` tells you WHO is filling it.

```bash
du -sh /var/log/* | sort -hr | head -10
```

**Output:**
```
8.2G   /var/log/foodexpress
3.1G   /var/log/nginx
1.4G   /var/log/mysql
890M   /var/log/syslog
234M   /var/log/auth.log
12K    /var/log/cron.log
```

FoodExpress logs: **8.2GB**. That's the biggest consumer. Now drill deeper:

```bash
du -sh /var/log/foodexpress/* | sort -hr
```

**Key flags:**

| Flag | Meaning |
|------|---------|
| `-s` | Summary (total per directory, not every file inside) |
| `-h` | Human readable (MB, GB) |
| `-sh *` | Summary of each item in the directory |

### df vs du -- When to use which:

| Command | Question It Answers |
|---------|-------------------|
| `df -h` | "How much TOTAL disk space is left?" (partition level) |
| `du -sh *` | "Which FOLDER is using the most?" (drill down) |

Always `df` first (big picture), then `du` to drill into the problem folder.

---

## 4.3 -- top: Live Process Monitor

`top` is like Task Manager for Linux. It shows processes ranked by CPU/memory usage and refreshes every few seconds.

```bash
top
```

**Output:**
```
top - 09:16:30 up 1 day,  0:16,  1 user,  load average: 3.82, 2.45, 1.98
Tasks: 142 total,   2 running, 139 sleeping,   0 stopped,   1 zombie
%Cpu(s): 78.2 us, 12.3 sy,  0.0 ni,  8.5 id,  0.0 wa,  0.5 hi,  0.5 si
MiB Mem :  8192.0 total,   512.4 free,  6234.8 used,  1444.8 buff/cache

  PID USER      %CPU %MEM     TIME+ COMMAND
 2847 app       98.7  0.1   5:43.21 rebuild_index.sh
 1042 app       45.2 22.8  12:34.56 java (order-svc)
 1089 app        8.5  9.2   2:15.33 java (payment-svc)
  891 mysql      2.3 15.4  45:12.89 mysqld
 1102 app        1.2  3.4   0:18.45 node (menu-svc)
```

### How to read the header:

**Line 1: Load Average**
```
load average: 3.82, 2.45, 1.98
               │     │     │
               │     │     └── last 15 min
               │     └── last 5 min
               └── last 1 min
```

Load average = how many processes are waiting for CPU. On a **4-core** server:
- Load < 4 = healthy (CPU has capacity)
- Load = 4 = fully utilized
- Load > 4 = overloaded (processes are queuing)

3.82 and rising (1 min > 15 min average) = getting worse.

**Line 3: CPU**
```
%Cpu(s): 78.2 us, 12.3 sy, 8.5 id
          │         │        │
          │         │        └── idle (only 8.5% idle = almost maxed)
          │         └── system/kernel
          └── user space (our apps)
```

**Line 4: Memory**
```
MiB Mem: 8192.0 total, 512.4 free, 6234.8 used
```
8GB total, only 512MB free. Memory is tight.

### The process list:

| PID | Process | CPU | What's Happening |
|-----|---------|-----|-----------------|
| 2847 | rebuild_index.sh | **98.7%** | A shell script is eating ALL the CPU! |
| 1042 | order-service (Java) | 45.2% | High because it's retrying failed DB connections |
| 1089 | payment-service | 8.5% | Moderate, waiting on upstream |
| 891 | mysqld | 2.3% | Database itself is not CPU-heavy |
| 1102 | menu-service (Node) | 1.2% | Light load, working fine |

**The problem:** `rebuild_index.sh` (PID 2847) is using 98.7% CPU. Someone ran it to fix the slow queries, but it's making everything WORSE. Kill it.

### top keyboard shortcuts:

| Key | Action |
|-----|--------|
| `q` | Quit top |
| `P` | Sort by CPU (default) |
| `M` | Sort by Memory |
| `k` | Kill a process (type PID) |
| `1` | Show per-CPU core breakdown |
| `h` | Help |

**Note:** `top` does NOT work in Git Bash. Use WSL or the browser terminal.

---

## 4.4 -- ps: Process Snapshot

`ps` is a one-time snapshot of all processes. Unlike `top` (which keeps refreshing), `ps` prints once and exits. This makes it perfect for piping.

```bash
ps aux
```

**Flag breakdown:** `ps aux` -- each letter means something:
- `a` = show processes from **a**ll users (not just yours)
- `u` = show **u**ser-oriented format (with USER, %CPU, %MEM columns)
- `x` = include processes with no terminal (background services like Java, MySQL)

Without `aux`, `ps` shows only YOUR processes in the current terminal -- nearly useless.

| Column | Meaning |
|--------|---------|
| `USER` | Who owns the process |
| `PID` | Process ID (you need this to kill it) |
| `%CPU` | CPU usage |
| `%MEM` | Memory usage |
| `VSZ` | Virtual memory size |
| `RSS` | Real memory used |
| `STAT` | State (R=running, S=sleeping, Z=zombie) |
| `COMMAND` | The actual command |

### The essential patterns:

**"Is my service running?"**
```bash
ps aux | grep order-service
ps aux | grep java
ps aux | grep node
```

**"What's eating the most CPU?"**
```bash
ps aux | sort -k3 -rn | head -5
```
**Flag breakdown:**
- `sort -k3` = `-k` means **k**ey (column number). `-k3` = sort by column 3, which is `%CPU`
- `-r` = **r**everse (biggest first)
- `-n` = **n**umeric (treat values as numbers, not text)
- `head -5` = show only the top 5 results

**"What's eating the most memory?"**
```bash
ps aux | sort -k4 -rn | head -5
```
**Flag breakdown:** `-k4` = sort by column 4 (`%MEM`). Rest is the same.

### ps vs top:

| Command | Use When |
|---------|----------|
| `top` | Watch processes LIVE (stays open, refreshes) |
| `ps aux` | One-time snapshot (perfect for piping and scripting) |
| `ps aux \| grep java` | "Is my Java service running?" |

**Sustain engineering context:** `ps aux | grep java` -- you'll type this 10 times a day. "Is my service running?" That's the question. `ps aux | grep` is the answer.

---

## 4.5 -- kill: Stop a Process

### Step 1: Find the process

```bash
ps aux | grep rebuild_index
```

**Output:**
```
app  2847  98.7  0.1  14532  8420  R  09:12  5:43  /bin/bash /opt/foodexpress/scripts/rebuild_index.sh
```

PID is **2847**.

### Step 2: Kill it (polite first)

```bash
kill 2847
```

This sends **SIGTERM** (signal 15). The process gets a chance to clean up (close files, finish writes) and exit gracefully. Like knocking on the door and saying "please leave."

### Step 3: If it doesn't die, force kill

```bash
kill -9 2847
```

This sends **SIGKILL** (signal 9). The process is IMMEDIATELY terminated. No cleanup. No chance to save. Like pulling the power cord.

### Step 4: Verify it's dead

```bash
ps aux | grep rebuild_index
```

No output = it's dead.

### The kill signals:

| Signal | Number | What It Does | Analogy |
|--------|--------|-------------|---------|
| `SIGTERM` | 15 | Polite shutdown (default `kill`) | "Please leave" |
| `SIGKILL` | 9 | Force kill (cannot be ignored) | Pulling the power cord |
| `SIGHUP` | 1 | Reload config (used by nginx, apache) | "Re-read your settings" |

### The rule:

```
1. kill <PID>          # Try polite first
2. Wait 5 seconds
3. ps aux | grep <name> # Check if it's still alive
4. kill -9 <PID>       # Force kill only if needed
```

### Practice with a real process:

```bash
# Start a fake process
sleep 300 &

# Find it
ps aux | grep "sleep 300"

# Note the PID (second column)
# Kill it
kill <PID>

# Verify it's dead
ps aux | grep "sleep 300"
```

---

## 4.6 -- Redirection: Save Your Evidence

### Redirect output to a file:

```bash
# Save (overwrite)
grep "ERROR" var/log/foodexpress/app.log > /tmp/errors.txt

# Append (add to end)
echo "## Incident 4721" > /tmp/report.txt
echo "Total errors: $(grep -c 'ERROR' var/log/foodexpress/app.log)" >> /tmp/report.txt
grep "FATAL" var/log/foodexpress/app.log >> /tmp/report.txt
```

| Symbol | Action | Memory Trick |
|--------|--------|-------------|
| `>` | Write to file (OVERWRITES existing content) | One arrow = one chance, replaces all |
| `>>` | Append to file (ADDS to end) | Two arrows = adds more |
| `\|` | Pipe: send output to next command | Flows to the right |

### Build an incident report:

```bash
echo "# INCIDENT 4721 - Report" > /tmp/incident_4721.txt
echo "# Generated: $(date)" >> /tmp/incident_4721.txt
echo "" >> /tmp/incident_4721.txt
echo "## Error Summary" >> /tmp/incident_4721.txt
echo "Total ERRORs: $(grep -c 'ERROR' var/log/foodexpress/app.log)" >> /tmp/incident_4721.txt
echo "Total FATALs: $(grep -c 'FATAL' var/log/foodexpress/app.log)" >> /tmp/incident_4721.txt
echo "Total WARNs:  $(grep -c 'WARN' var/log/foodexpress/app.log)" >> /tmp/incident_4721.txt
echo "" >> /tmp/incident_4721.txt
echo "## Root Cause" >> /tmp/incident_4721.txt
grep "FATAL" var/log/foodexpress/app.log >> /tmp/incident_4721.txt
echo "" >> /tmp/incident_4721.txt
echo "## Affected Services" >> /tmp/incident_4721.txt
grep "ERROR" var/log/foodexpress/app.log | awk '{print $4}' | sort | uniq -c | sort -rn >> /tmp/incident_4721.txt

# View the report
cat /tmp/incident_4721.txt
```

You just built an incident report using ONLY the terminal.

---

## 4.7 -- The Complete Incident Resolution

Here's the full story, commands and all:

```bash
# STEP 1: Read the logs
tail -20 var/log/foodexpress/app.log
# Finding: Health checks failing, database unreachable

# STEP 2: Find the root cause
grep "FATAL" var/log/foodexpress/app.log
# Finding: Connection pool exhausted, lock file blocking restart

# STEP 3: Find and remove the lock file
find . -name "*.lock"
rm tmp/db.lock
# Finding: Lock file removed

# STEP 4: Check what's eating CPU
# (use top or ps aux | sort -k3 -rn | head -5)
# Finding: rebuild_index.sh at 98.7% CPU

# STEP 5: Kill the runaway process
kill 2847

# STEP 6: Check disk space
df -h
# Finding: Root partition at 92%

# STEP 7: Find large files and archive old logs
find . -size +1M -exec ls -lh {} \;
tar -czvf /tmp/old_logs.tar.gz var/log/foodexpress/app.log.2026-08-2*
# -c=create, -z=gzip, -v=verbose, -f=filename

# STEP 8: Check config
grep max_connections etc/foodexpress/config_prod.properties
# Finding: Only 100 connections -- too low

# STEP 9: Restart services
# systemctl restart mysqld
# systemctl restart order-service

# STEP 10: Watch logs to confirm recovery
# tail -f var/log/foodexpress/app.log
```

**8 commands solved a real incident. No GUI needed.**

---

## Section 4 Summary

```
df -h                              --> Disk space (partition level)
du -sh * | sort -hr | head -10     --> Which folder is biggest?

top                                --> Live process monitor (q to quit)
  P = sort by CPU
  M = sort by memory
  k = kill process
  q = quit

ps aux                             --> Process snapshot
ps aux | grep java                 --> "Is my service running?"
ps aux | sort -k3 -rn | head -5   --> Top 5 CPU consumers
ps aux | sort -k4 -rn | head -5   --> Top 5 memory consumers

kill <PID>                         --> Polite stop (SIGTERM)
kill -9 <PID>                      --> Force stop (SIGKILL)

>  file                            --> Redirect output (overwrite)
>> file                            --> Redirect output (append)
|                                  --> Pipe output to next command
```

---

## Practice Exercises

| # | Question | Command | Expected |
|---|----------|---------|----------|
| 1 | Check disk space on your machine | `df -h` | Shows all partitions |
| 2 | Which folder in /tmp/foodexpress-server uses most space? | `du -sh /tmp/foodexpress-server/* \| sort -hr` | var/ is the biggest |
| 3 | Drill into the log directory | `du -sh /tmp/foodexpress-server/var/log/foodexpress/* \| sort -hr` | gc.log is largest |
| 4 | Start a fake process, find it, kill it | `sleep 300 &` then `ps aux \| grep "sleep 300"` then `kill <PID>` | Process killed |
| 5 | Find all Java processes on your machine | `ps aux \| grep java` | Varies |
| 6 | Top 3 CPU-consuming processes on your machine | `ps aux \| sort -k3 -rn \| head -4` | First line is header |
| 7 | Top 3 memory-consuming processes | `ps aux \| sort -k4 -rn \| head -4` | First line is header |
| 8 | Save all FATAL errors to a file | `grep "FATAL" /tmp/foodexpress-server/var/log/foodexpress/app.log > /tmp/fatals.txt` | 2 lines saved |
| 9 | Append the error count to that file | `echo "Total FATALs: $(grep -c FATAL /tmp/foodexpress-server/var/log/foodexpress/app.log)" >> /tmp/fatals.txt` | Appended |
| 10 | Build a 5-line incident report using redirection | Use `echo` + `>>` + `grep` to build a report | Practice |

---

## The Incident Story -- Complete

| Section | What You Did | Key Finding |
|---------|-------------|-------------|
| **1** | Opened logs, saw health checks failing | `tail` showed DB unreachable |
| **2** | grep investigation | 13 errors, 2 FATALs, customer_id=42 slow queries |
| **3** | find lock file, diff configs, archive logs | Lock file blocking restart, max_connections too low |
| **4** | Check disk, CPU, processes | Disk 92%, rebuild_index.sh at 98.7% CPU, kill it |

**Tomorrow (Day 20):** Shell scripting, cron jobs, SSH. You'll AUTOMATE everything you did manually today.
