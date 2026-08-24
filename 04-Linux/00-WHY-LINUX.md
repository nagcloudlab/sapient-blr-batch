# Why Linux? -- Introduction for Sustain Engineers

## Day 19 | Linux OS | Time: ~10 minutes (opening talk)

---

## The Question Every Student Asks

> "I've been using Windows my whole life. Why do I need to learn Linux?"

---

## The Short Answer

**Because every production server you'll ever touch runs Linux.**

| What | Runs On |
|------|---------|
| AWS EC2 instances | Linux |
| Google Cloud VMs | Linux |
| Azure Virtual Machines | Linux (majority) |
| Docker containers | Linux |
| Kubernetes pods | Linux |
| Jenkins CI/CD agents | Linux |
| Nginx / Apache web servers | Linux |
| MySQL / PostgreSQL databases | Linux |
| FoodExpress production servers | Ubuntu 22.04 LTS (Linux) |

When something breaks in production at 2 AM, you SSH into a Linux server. There is no GUI. No mouse. No VS Code. Just a blinking cursor. If you can't use Linux, you can't fix production.

---

## Linux Market Share

```
Servers worldwide:    ~80% run Linux
Cloud instances:      ~90% run Linux
Supercomputers:       100% run Linux (all 500 of the top 500)
Android phones:       Linux kernel
Your Windows laptop:  NOT used in production
```

---

## What Sustain Engineers Do on Linux (Daily)

| Task | Linux Commands Used |
|------|-------------------|
| Read application logs | `tail -f app.log`, `grep ERROR app.log` |
| Find out why a service is down | `ps aux \| grep java`, `systemctl status` |
| Check if disk is full | `df -h`, `du -sh /var/log/*` |
| Kill a stuck process | `kill -9 <PID>` |
| Compare configs between environments | `diff config_prod.txt config_staging.txt` |
| Search for a specific error across all logs | `grep -r "NullPointerException" /var/log/` |
| Archive and clean old log files | `tar -czvf`, `find . -mtime +30 -delete` |
| Deploy a new version | Shell scripts, `scp`, `ssh` |
| Set up cron jobs for automation | `crontab -e` |
| Monitor system resources | `top`, `htop`, `free -h` |

---

## Linux vs Windows -- The Difference

| Aspect | Windows | Linux (Production) |
|--------|---------|-------------------|
| Interface | GUI (click buttons) | Terminal (type commands) |
| Servers | ~20% market share | ~80% market share |
| Cost | Licensed ($$$) | Free and open source |
| Remote access | Remote Desktop (GUI) | SSH (terminal only) |
| Package manager | Download .exe from websites | `apt install`, `yum install` |
| File paths | `C:\Users\name\file.txt` | `/home/name/file.txt` |
| Line endings | `\r\n` (CRLF) | `\n` (LF) |
| Case sensitive? | No (`File.txt` = `file.txt`) | Yes (`File.txt` is different from `file.txt`) |

---

## The 2 AM Scenario

> It's 2:00 AM. Your phone buzzes. PagerDuty alert: "FoodExpress Order Service -- P1 -- Orders Failing."
>
> You open your laptop. You SSH into the production server:
> ```
> ssh app@prod-server-01.foodexpress.internal
> ```
>
> You see this:
> ```
> app@prod-server-01:~$
> ```
>
> A blinking cursor. No Start menu. No File Explorer. No Google Chrome.
>
> **What do you type?**
>
> If you know Linux, you type:
> ```bash
> tail -20 /var/log/foodexpress/app.log
> ```
> And in 5 seconds, you see the error. In 10 minutes, you fix it. You go back to sleep.
>
> If you don't know Linux, you stare at the cursor. You call someone. They take 30 minutes to join. The outage lasts an hour. Revenue lost: Rs 1,44,000.
>
> **That's why you learn Linux.**

---

## What We'll Cover Today

We're NOT going to learn Linux by memorizing commands. We're going to **solve a production incident**.

**The incident:** FoodExpress order service is down. 47 customer complaints. Revenue loss Rs 2,400/min.

**Your job:** Find the root cause and fix it. Using ONLY the terminal.

Every command you learn today is because you NEED it to solve this incident:

| Section | Incident Question | Commands You'll Learn |
|---------|------------------|----------------------|
| 1 | "Can I read the logs?" | `pwd`, `ls`, `cat`, `head`, `tail`, `wc` |
| 2 | "What went wrong?" | `grep`, `egrep`, pipes |
| 3 | "Why? Who changed what?" | `find`, `diff`, `cut`, `sort` |
| 4 | "Is the server healthy now?" | `df`, `du`, `top`, `ps`, `kill` |

By the end of today, you'll have solved a real incident using 20 commands. No GUI needed.

---

## Key Linux Concepts (30-second version)

### Everything is a file
In Linux, everything is treated as a file: regular files, directories, devices, network connections. This means the same tools (`cat`, `grep`, `find`) work on everything.

### Directories (not folders)
Linux doesn't call them "folders." They're "directories." The structure:

```
/                    Root (the top of everything)
├── home/            User home directories
├── var/log/         Log files (you'll live here)
├── etc/             Configuration files
├── opt/             Optional/third-party software
├── tmp/             Temporary files
└── usr/bin/         System commands
```

### Permissions
Every file has 3 permission types for 3 user types:

```
-rw-r--r--
 │││ │││ │││
 │││ │││ └── Others: r=read (no write, no execute)
 │││ └──── Group: r=read (no write, no execute)
 └──────── Owner: r=read, w=write (no execute)
```

- `r` = **r**ead (view the file)
- `w` = **w**rite (modify the file)
- `x` = e**x**ecute (run the file as a program)

### Case sensitive
`App.log`, `app.log`, and `APP.LOG` are THREE DIFFERENT FILES in Linux. Be careful with casing.

### No "undo"
Linux has no recycle bin. `rm file` deletes it permanently. There is no Ctrl+Z for terminal commands. Be careful with `rm`, especially `rm -rf`.

---

## How to Practice

You don't need a Linux machine to practice. Options:

1. **WSL on Windows:** `wsl --install` in PowerShell (best option)
2. **Git Bash:** Already installed from Git module (works for most commands)
3. **Browser terminal:** https://bellard.org/jslinux/ (zero setup)
4. **Mac terminal:** Already Linux-compatible (macOS is Unix-based)

---

## Let's Go

Open your terminal. Type:

```bash
cd /tmp/foodexpress-server
ls
```

The incident starts now.
