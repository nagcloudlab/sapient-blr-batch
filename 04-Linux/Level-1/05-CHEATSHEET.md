# Linux Cheat Sheet -- The Sustain Engineer's Top 20

## Quick Reference Card (Print This)

---

## Navigation & Display

| Command | What It Does | When You Need It |
|---------|-------------|-----------------|
| `pwd` | Show current directory | "Where am I?" |
| `ls -lh` | List files with sizes | "What's here?" |
| `ls -lt` | List files by time | "What changed recently?" |
| `cd /path` | Change directory | Move around the server |
| `cat file` | Show entire file | Small files only |
| `head -N file` | First N lines | "How did the app start?" |
| `tail -N file` | Last N lines | "What's happening NOW?" |
| `tail -f file` | Live feed | Watch logs in real time |
| `wc -l file` | Count lines | "How many log entries?" |
| `less file` | Scroll through | Long files, search with `/` |

## Searching

| Command | What It Does | When You Need It |
|---------|-------------|-----------------|
| `grep "ERROR" file` | Find lines with ERROR | "Show me all errors" |
| `grep -c "ERROR" file` | Count matches | "How many errors?" |
| `grep -i "error" file` | Case insensitive | "Find error in any case" |
| `grep -n "ERROR" file` | With line numbers | "Which line is the error?" |
| `grep -v "INFO" file` | Exclude pattern | "Remove the noise" |
| `grep -B3 -A3 "FATAL" file` | Context around match | "What happened before/after?" |
| `grep -r "error" /var/log/` | Search all files | "Search everywhere" |
| `grep -rl "FATAL" /var/log/` | File names only | "Which files have FATAL?" |
| `grep -o "pattern" file` | Only the match | "Extract just this part" |
| `egrep "ERROR\|FATAL" file` | Multiple patterns | "Find ERROR or FATAL" |

## Finding Files

| Command | What It Does | When You Need It |
|---------|-------------|-----------------|
| `find . -name "*.log"` | Find by name | "Where are all log files?" |
| `find . -size +100M` | Find by size | "What's eating disk?" |
| `find . -type d` | Find directories | "Show folder structure" |
| `find . -name "*.lock"` | Find lock files | "What's blocking restart?" |
| `find . -name "*.log" -exec wc -l {} \;` | Find + action | "Count lines in all logs" |

## Comparing & Extracting

| Command | What It Does | When You Need It |
|---------|-------------|-----------------|
| `diff file1 file2` | Show differences | "What changed?" |
| `diff -y file1 file2` | Side-by-side | "Compare configs" |
| `cut -d'=' -f2 file` | Extract column | "Get config values" |
| `awk '{print $4}' file` | Extract field | "Get service name from log" |
| `sort \| uniq -c \| sort -rn` | Count + rank | "What's most common?" |

## System Resources

| Command | What It Does | When You Need It |
|---------|-------------|-----------------|
| `df -h` | Disk space | "Is disk full?" |
| `du -sh * \| sort -hr` | Folder sizes | "Which folder is biggest?" |
| `top` | Live process monitor | "What's eating CPU?" |
| `ps aux \| grep java` | Find process | "Is my service running?" |
| `ps aux \| sort -k3 -rn \| head` | Top CPU users | "What's using most CPU?" |
| `kill PID` | Stop process (polite) | "Stop this process" |
| `kill -9 PID` | Force stop | "Kill it immediately" |

## Redirection & Pipes

| Symbol | What It Does | Example |
|--------|-------------|---------|
| `>` | Write to file (overwrite) | `grep ERROR log > errors.txt` |
| `>>` | Append to file | `echo "done" >> report.txt` |
| `\|` | Pipe to next command | `grep ERROR log \| wc -l` |

## Archiving

| Command | What It Does |
|---------|-------------|
| `tar -czvf backup.tar.gz folder/` | Create compressed archive |
| `tar -xzvf backup.tar.gz` | Extract archive |
| `tar -tzvf backup.tar.gz` | List contents without extracting |

---

## The 10 Commands You'll Use Every Day

```
1.  tail -f app.log              (watch logs live)
2.  grep -r "ERROR" /var/log/    (search everything)
3.  grep -B3 -A3 "FATAL" log    (context around errors)
4.  find . -name "*.log"         (locate files)
5.  ps aux | grep java           (is my service running?)
6.  df -h                        (check disk)
7.  du -sh * | sort -hr          (folder sizes)
8.  kill -9 <PID>                (force stop)
9.  diff config1 config2         (compare configs)
10. cmd1 | cmd2 | cmd3           (pipe -- chain anything)
```

---

## Incident Response Cheat Sheet

```
STEP 1: What's broken?
  $ tail -20 /var/log/app.log

STEP 2: How bad is it?
  $ grep -c "ERROR" /var/log/app.log
  $ grep "FATAL" /var/log/app.log

STEP 3: What caused it?
  $ grep -B5 "FATAL" /var/log/app.log
  $ diff config_prod config_staging

STEP 4: Is disk full?
  $ df -h
  $ du -sh /var/log/* | sort -hr

STEP 5: Is something eating CPU?
  $ top (or ps aux | sort -k3 -rn | head)

STEP 6: Kill the bad process
  $ kill <PID>
  $ kill -9 <PID>  (if polite kill didn't work)

STEP 7: Fix and restart
  $ rm /tmp/bad.lock
  $ systemctl restart service-name

STEP 8: Verify recovery
  $ tail -f /var/log/app.log
  $ curl localhost:8080/health
```
