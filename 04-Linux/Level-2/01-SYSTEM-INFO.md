# Section 5: System Info Commands -- "Who's on this server?"

## Day 20 | Linux OS (Day 2) | Time: ~20 minutes

---

## The Scenario

> "The incident is fixed. But your manager asks: who else was logged into the server during the outage? Who ran that rebuild_index.sh script? Where is the Java binary installed? What's the server's hostname?"

---

## 5.1 -- who: Who's logged in right now?

```bash
who
```

**Output:**
```
pappu    pts/0        2026-08-25 09:00 (192.168.1.10)
surya    pts/1        2026-08-25 09:02 (192.168.1.22)
sridhar  pts/2        2026-08-25 09:05 (192.168.1.33)
```

| Column | Meaning |
|--------|---------|
| `pappu` | Username |
| `pts/0` | Terminal session (pseudo-terminal) |
| `2026-08-25 09:00` | Login time |
| `(192.168.1.10)` | IP address they connected from |

**Related commands:**

| Command | What It Shows |
|---------|--------------|
| `who` | Users currently logged in |
| `whoami` | YOUR username |
| `w` | Who's logged in + what they're running (more detail than `who`) |
| `last` | Login history (who logged in previously) |
| `last -5` | Last 5 logins |

**Sustain context:** During an incident, `who` tells you who else is on the server. `last` tells you who was on the server when the problem started.

---

## 5.2 -- which: Where is a command installed?

`which` = find the full path of a command.

```bash
which java
```
**Output:** `/usr/bin/java`

```bash
which python3
```
**Output:** `/usr/bin/python3`

```bash
which apache2
```
**Output:** `/usr/sbin/apache2`

**Sustain context:** "Which version of Java is this server using?" First find it with `which java`, then check version with `java -version`.

---

## 5.3 -- whereis: Find binary, source, and man page locations

`whereis` gives MORE info than `which` -- it finds the binary, source code, AND manual pages.

```bash
whereis java
```
**Output:** `java: /usr/bin/java /usr/share/man/man1/java.1.gz`

```bash
whereis apache2
```
**Output:** `apache2: /usr/sbin/apache2 /usr/lib/apache2 /etc/apache2 /usr/share/apache2 /usr/share/man/man8/apache2.8.gz`

| Command | What It Finds |
|---------|--------------|
| `which cmd` | Only the executable path |
| `whereis cmd` | Binary + source + man pages |

---

## 5.4 -- hostname: What server am I on?

```bash
hostname
```
**Output:** `linux-lab`

```bash
hostname -I
```
**Output:** `10.160.0.2` (internal IP)

| Flag | Stands For | What It Shows |
|------|-----------|--------------|
| `hostname` | (none) | Server name |
| `hostname -I` | **I**P addresses | All IP addresses of this machine |
| `hostname -f` | **f**ully qualified | Full domain name (e.g., linux-lab.asia-south1-a.c.project.internal) |

**Sustain context:** When you're SSH'd into multiple servers, `hostname` confirms WHICH server you're on. You don't want to restart the wrong one.

---

## 5.5 -- date: Current date and time

```bash
date
```
**Output:** `Mon Aug 25 09:15:30 IST 2026`

### Formatted date:

| Command | Output | Format Codes |
|---------|--------|-------------|
| `date` | Full date and time | Default |
| `date +%Y-%m-%d` | `2026-08-25` | `%Y`=year, `%m`=month, `%d`=day |
| `date +%H:%M:%S` | `09:15:30` | `%H`=hour, `%M`=minute, `%S`=second |
| `date +%Y%m%d_%H%M%S` | `20260825_091530` | Useful for backup filenames |
| `date +%s` | `1787857530` | Unix timestamp (seconds since 1970) |

### Using date in scripts:

```bash
# Create a backup file with today's date
tar -czvf backup_$(date +%Y%m%d).tar.gz /var/log/

# Log with timestamp
echo "$(date +%Y-%m-%d_%H:%M:%S) -- Deployment started" >> deploy.log
```

**Sustain context:** Every log entry, every backup file, every incident report needs a timestamp. `date` is how you generate them.

---

## 5.6 -- uname: System information

```bash
uname -a
```
**Output:** `Linux linux-lab 5.15.0-1068-gcp #76~20.04.1-Ubuntu SMP ... x86_64 GNU/Linux`

| Flag | Stands For | Shows |
|------|-----------|-------|
| `uname` | (none) | Just the OS name (`Linux`) |
| `uname -a` | **a**ll | Everything: OS, hostname, kernel, architecture |
| `uname -r` | kernel **r**elease | Kernel version (e.g., `5.15.0-1068-gcp`) |
| `uname -m` | **m**achine | Architecture (`x86_64` = 64-bit) |

---

## Practice Exercises

| # | Question | Command |
|---|----------|---------|
| 1 | Who is currently logged into the server? | `who` |
| 2 | What is YOUR username? | `whoami` |
| 3 | Where is the `grep` command installed? | `which grep` |
| 4 | Find all locations related to `bash` | `whereis bash` |
| 5 | What is this server's hostname? | `hostname` |
| 6 | What is today's date in YYYY-MM-DD format? | `date +%Y-%m-%d` |
| 7 | Generate a timestamp for a backup filename | `date +%Y%m%d_%H%M%S` |
| 8 | What kernel version is running? | `uname -r` |
| 9 | Who logged in last 5 times? | `last -5` |
| 10 | What's the server's IP address? | `hostname -I` |
