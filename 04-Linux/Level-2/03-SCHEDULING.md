# Section 7: Scheduling -- "Automate it with cron"

## Day 20 | Linux OS (Day 2) | Time: ~30 minutes

---

## The Scenario

> "Yesterday you manually cleaned up old logs, killed runaway processes, and checked disk space. Your manager says: I don't want to do this manually every day. Automate it."

---

## 7.1 -- crontab: Schedule recurring tasks

`cron` = a daemon (background service) that runs scheduled commands automatically.
`crontab` = the file where you define WHAT to run and WHEN.

### View your crontab:

```bash
crontab -l
```

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-l` | **l**ist | Show your current cron jobs |
| `-e` | **e**dit | Open the crontab editor to add/change jobs |
| `-r` | **r**emove | Delete ALL your cron jobs (be careful!) |

### Edit your crontab:

```bash
crontab -e
```

This opens an editor. Add one line per scheduled job.

---

## 7.2 -- Cron syntax (THE MOST IMPORTANT PART)

```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0 and 7 = Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

### Examples (memorize these patterns):

| Schedule | Cron Expression | Plain English |
|----------|----------------|--------------|
| Every minute | `* * * * *` | Every single minute (for testing only!) |
| Every hour | `0 * * * *` | At minute 0 of every hour |
| Every day at 2 AM | `0 2 * * *` | At 02:00 every day |
| Every Monday at 9 AM | `0 9 * * 1` | At 09:00 every Monday |
| Every 5 minutes | `*/5 * * * *` | Every 5th minute |
| Every day at midnight | `0 0 * * *` | At 00:00 every day |
| Weekdays at 8 AM | `0 8 * * 1-5` | Mon-Fri at 08:00 |
| 1st of every month | `0 0 1 * *` | At midnight on the 1st |
| Every Sunday at 3 AM | `0 3 * * 0` | At 03:00 every Sunday |

### Special characters:

| Character | Meaning | Example |
|-----------|---------|---------|
| `*` | Every | `* * * * *` = every minute |
| `*/N` | Every Nth | `*/5 * * * *` = every 5 minutes |
| `N-M` | Range | `1-5` = Monday through Friday |
| `N,M` | List | `0,30 * * * *` = at minute 0 and 30 |

---

## 7.3 -- Real Sustain Engineering Cron Jobs

### Delete old logs every Sunday at 3 AM:

```bash
0 3 * * 0 find /var/log/foodexpress -name "*.log" -mtime +30 -delete
```

**Breakdown:**
- `0 3 * * 0` = Sunday at 03:00
- `find ... -mtime +30` = files modified more than 30 days ago (`-mtime` = **m**odification **time**, `+30` = older than 30 days)
- `-delete` = delete them

### Health check every 5 minutes:

```bash
*/5 * * * * curl -s http://localhost:8080/health >> /var/log/healthcheck.log 2>&1
```

**Breakdown:**
- `*/5 * * * *` = every 5 minutes
- `curl -s` = `-s` = **s**ilent (no progress bar)
- `>> /var/log/healthcheck.log` = append result to log file
- `2>&1` = also capture errors to the same file

### Disk space alert every hour:

```bash
0 * * * * df -h / | awk 'NR==2 {if ($5+0 > 90) print "DISK CRITICAL: "$5}' | mail -s "Disk Alert" admin@foodexpress.in
```

### Backup database every night at 1 AM:

```bash
0 1 * * * /opt/scripts/backup_db.sh >> /var/log/backup.log 2>&1
```

---

## 7.4 -- Hands-on: Create a cron job

```bash
# Open crontab editor
crontab -e

# Add this line (logs disk space every minute -- for testing):
* * * * * echo "$(date): $(df -h / | tail -1)" >> /tmp/disk_monitor.log

# Save and exit (:wq in vim, or Ctrl+X in nano)

# Verify it's saved
crontab -l

# Wait 2 minutes, then check the log
cat /tmp/disk_monitor.log

# Remove the test cron job when done
crontab -e
# Delete the line, save
```

---

## 7.5 -- at: Schedule a ONE-TIME task

`cron` = recurring. `at` = run once at a specific time.

```bash
# Run a command at 3 PM today
echo "tar -czvf /tmp/backup.tar.gz /var/log/" | at 15:00

# Run in 10 minutes
echo "/opt/scripts/deploy.sh" | at now + 10 minutes

# Run tomorrow at 2 AM
echo "/opt/scripts/cleanup.sh" | at 2:00 AM tomorrow
```

### View scheduled at jobs:

```bash
atq
```

`atq` = **at** **q**ueue. Shows pending one-time jobs.

### Remove an at job:

```bash
atrm 1
```

`atrm` = **at** **r**e**m**ove. `1` = job number from `atq`.

### Install at (if not available):

```bash
sudo apt install at
sudo systemctl enable atd
sudo systemctl start atd
```

---

## 7.6 -- cron vs at

| Feature | cron | at |
|---------|------|-----|
| **Frequency** | Recurring (every day, every hour, etc.) | One-time only |
| **Use case** | Log cleanup, health checks, backups | "Run this deploy at 2 AM tonight" |
| **Edit** | `crontab -e` | `echo "cmd" \| at TIME` |
| **View** | `crontab -l` | `atq` |
| **Remove** | `crontab -e` (delete the line) | `atrm JOB_NUMBER` |

---

## Practice Exercises

| # | Task | Command/Answer |
|---|------|---------------|
| 1 | List your current cron jobs | `crontab -l` |
| 2 | Write a cron expression: every day at 6 AM | `0 6 * * *` |
| 3 | Write a cron expression: every Monday at 9 AM | `0 9 * * 1` |
| 4 | Write a cron expression: every 15 minutes | `*/15 * * * *` |
| 5 | Write a cron expression: weekdays at midnight | `0 0 * * 1-5` |
| 6 | Create a cron job that logs the date every minute | `crontab -e` then add `* * * * * date >> /tmp/time.log` |
| 7 | Verify your cron job ran | Wait 2 min, then `cat /tmp/time.log` |
| 8 | Remove all your cron jobs | `crontab -r` |
| 9 | Schedule a one-time task in 5 minutes | `echo "echo hello >> /tmp/at_test.log" \| at now + 5 minutes` |
| 10 | View pending at jobs | `atq` |
