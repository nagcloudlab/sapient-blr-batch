# Linux Day 2 -- Cheat Sheet

## Quick Reference Card (Print This)

---

## System Info

| Command | What It Does | Memory Trick |
|---------|-------------|-------------|
| `who` | Who's logged in right now | "Who's here?" |
| `whoami` | Your username | "Who am I?" |
| `w` | Who's logged in + what they're doing | `who` with more detail |
| `last -5` | Last 5 logins | Login history |
| `which java` | Where is `java` installed | "Which java?" |
| `whereis bash` | Find binary + manual + source | More than `which` |
| `hostname` | Server name | "What server am I on?" |
| `hostname -I` | Server IP address | `-I` = IP |
| `date` | Current date/time | |
| `date +%Y-%m-%d` | Formatted date | `%Y`=year `%m`=month `%d`=day |
| `uname -a` | OS, kernel, architecture | `-a` = all |

---

## Job Control

| Command | What It Does |
|---------|-------------|
| `command &` | Run in background |
| `jobs` | List background jobs |
| `Ctrl+Z` | Pause current command |
| `bg` | Resume paused command in background |
| `fg` | Bring background command to foreground |
| `fg %2` | Bring job #2 to foreground |
| `kill %1` | Kill job #1 |
| `nohup cmd &` | Run command that survives logout |

---

## Scheduling

### Cron syntax:
```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0=Sun, 1=Mon, ..., 6=Sat)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

### Common patterns:
| Schedule | Expression |
|----------|-----------|
| Every minute | `* * * * *` |
| Every 5 min | `*/5 * * * *` |
| Every hour | `0 * * * *` |
| Daily 2 AM | `0 2 * * *` |
| Monday 9 AM | `0 9 * * 1` |
| Weekdays 8 AM | `0 8 * * 1-5` |
| Sunday 3 AM | `0 3 * * 0` |

### Commands:
| Command | What It Does |
|---------|-------------|
| `crontab -l` | List cron jobs |
| `crontab -e` | Edit cron jobs |
| `crontab -r` | Remove all cron jobs |
| `echo "cmd" \| at 3pm` | One-time scheduled task |
| `atq` | List pending at jobs |

---

## Environment Variables

| Command | What It Does |
|---------|-------------|
| `echo $PATH` | Show PATH variable |
| `echo $HOME` | Show home directory |
| `export VAR=value` | Set variable (available to child processes) |
| `unset VAR` | Remove a variable |
| `env` | Show all environment variables |
| `source ~/.bashrc` | Reload bashrc without logout |
| `alias ll='ls -lah'` | Create command shortcut |

---

## Remote Access

| Command | What It Does |
|---------|-------------|
| `ssh user@host` | Connect to remote server |
| `ssh user@host 'cmd'` | Run single command remotely |
| `ssh-keygen -t rsa -b 4096` | Generate SSH key pair |
| `ssh-copy-id user@host` | Copy public key to server |
| `scp file user@host:/path/` | Copy file TO server |
| `scp user@host:/path/file .` | Copy file FROM server |
| `scp -r folder user@host:/path/` | Copy directory (`-r` = recursive) |
| `sftp user@host` | Interactive file transfer |
| `rsync -avz src/ user@host:dest/` | Smart sync (only changed files) |

---

## Shell Scripting

### Basics:
```bash
#!/bin/bash          # Shebang (first line)
chmod +x script.sh   # Make executable
./script.sh          # Run it
bash -x script.sh    # Run with debug output
```

### Variables:
```bash
VAR="value"          # Set (NO spaces around =)
echo $VAR            # Read
$1 $2 $3             # Arguments
read VAR             # User input
export VAR           # Available to child processes
```

### if/else:
```bash
if [ -f "file" ]; then    # File exists?
    echo "yes"
elif [ -d "dir" ]; then   # Directory exists?
    echo "dir"
else
    echo "no"
fi
```

### Tests:
```
Files:   -f (file) -d (dir) -e (exists) -s (not empty) -r (readable) -w (writable) -x (executable)
Strings: -z (empty) -n (not empty) = (equal) != (not equal)
Numbers: -eq -ne -gt -lt -ge -le
```

### Loops:
```bash
for X in a b c; do echo $X; done          # List loop
for F in *.log; do wc -l "$F"; done        # File loop
while [ $N -lt 10 ]; do echo $N; N=$((N+1)); done  # While loop
```

### Functions:
```bash
greet() {
    local NAME=$1
    echo "Hello $NAME"
}
greet "Pappu"
```

### Arithmetic:
```bash
echo $((5 + 3))          # 8
COUNT=$((COUNT + 1))     # Increment
```

---

## The Day 2 Story

| Section | What You Learned | Real-World Use |
|---------|-----------------|----------------|
| **System Info** | who, which, hostname, date | "Who was on the server during the outage?" |
| **Job Control** | &, bg, fg, nohup | "Run backup while I fix the bug" |
| **Scheduling** | crontab, at | "Clean logs every Sunday at 3 AM" |
| **Environment** | PATH, export, .bashrc | "Why does 'java: command not found' happen?" |
| **Remote Access** | ssh, scp, rsync | "Deploy the jar to production" |
| **Scripting** | if/else, loops, functions | "Automate the incident response" |

> "Day 1: You fixed the incident manually with 8 commands. Day 2: You wrote a script so it never happens again. That's the difference between a reactive engineer and a proactive one."
