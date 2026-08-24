# Section 9: Remote Access -- SSH, SFTP, rsync

## Day 20 | Linux OS (Day 2) | Time: ~25 minutes

---

## The Scenario

> "You're sitting at your desk in Bangalore. The production server is in Mumbai (GCP asia-south1). You need to: connect to it, copy files to it, and sync logs from it. All remotely."

---

## 9.1 -- SSH: Secure Shell (Connect to a remote server)

You've been using SSH all day. Now understand what it does.

```bash
ssh username@server-ip
```

**Example:**
```bash
ssh pappu@34.47.243.154
```

| Part | Meaning |
|------|---------|
| `ssh` | The command (Secure Shell) |
| `pappu` | Your username on the remote server |
| `@` | Separator |
| `34.47.243.154` | IP address (or hostname) of the server |

### SSH with a specific port:

```bash
ssh -p 2222 pappu@34.47.243.154
```

`-p` = **p**ort. Default SSH port is 22. Some servers use a different port for security.

### Run a single command remotely (without staying logged in):

```bash
ssh pappu@34.47.243.154 'df -h'
```

This connects, runs `df -h`, prints the output, and disconnects. You never see a shell prompt.

```bash
ssh pappu@34.47.243.154 'tail -5 ~/foodexpress-server/var/log/foodexpress/app.log'
```

**Sustain context:** Quick health check without fully logging in.

---

## 9.2 -- SSH Key Authentication (No password needed)

Typing passwords every time is slow and insecure. SSH keys are better.

### Step 1: Generate a key pair (on YOUR machine):

```bash
ssh-keygen -t rsa -b 4096
```

| Flag | Stands For | Meaning |
|------|-----------|---------|
| `-t rsa` | **t**ype | Use RSA algorithm |
| `-b 4096` | **b**its | 4096-bit key (very secure) |

Press Enter 3 times (accept defaults, no passphrase for now).

Creates two files:
- `~/.ssh/id_rsa` -- Private key (NEVER share this)
- `~/.ssh/id_rsa.pub` -- Public key (put this on the server)

### Step 2: Copy public key to the server:

```bash
ssh-copy-id pappu@34.47.243.154
```

Enter your password one last time. After this, you'll never need the password again.

### Step 3: Test passwordless login:

```bash
ssh pappu@34.47.243.154
# No password prompt!
```

---

## 9.3 -- SCP: Secure Copy (Copy files to/from server)

`scp` = **S**ecure **C**o**p**y. Copies files over SSH.

### Copy local file TO server:

```bash
scp /path/to/local/file.txt pappu@34.47.243.154:/home/pappu/
#   └── source (local)       └── destination (remote)
```

### Copy file FROM server to local:

```bash
scp pappu@34.47.243.154:/var/log/app.log /tmp/
#   └── source (remote)                  └── destination (local)
```

### Copy a whole directory (recursive):

```bash
scp -r /path/to/local/folder pappu@34.47.243.154:/home/pappu/
```

`-r` = **r**ecursive (copy folder and everything inside it).

### Common flags:

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-r` | **r**ecursive | Copy directories (not just files) |
| `-P 2222` | **P**ort | Use a specific SSH port |
| `-C` | **C**ompress | Compress data during transfer (faster for large files) |

**Sustain context:** Deploying a JAR file to the server:
```bash
scp backend-app-0.0.1-SNAPSHOT.jar pappu@34.47.243.154:/opt/foodexpress/
```

---

## 9.4 -- SFTP: Interactive File Transfer

`sftp` = **S**ecure **F**ile **T**ransfer **P**rotocol. Like SCP but interactive (you get a prompt).

```bash
sftp pappu@34.47.243.154
```

You get an `sftp>` prompt. Commands:

| Command | What It Does |
|---------|-------------|
| `ls` | List files on remote server |
| `lls` | List files on **l**ocal machine |
| `cd /var/log` | Change directory on remote |
| `lcd /tmp` | Change directory on **l**ocal |
| `get app.log` | Download file from remote to local |
| `put deploy.jar` | Upload file from local to remote |
| `mget *.log` | Download **m**ultiple files |
| `mput *.conf` | Upload **m**ultiple files |
| `exit` | Disconnect |

### Example session:

```bash
sftp pappu@34.47.243.154
sftp> cd /var/log/foodexpress
sftp> ls
app.log    access.log    error.log
sftp> get app.log
Fetching /var/log/foodexpress/app.log to app.log
sftp> exit
```

**SCP vs SFTP:**

| Feature | SCP | SFTP |
|---------|-----|------|
| Style | One command, one transfer | Interactive session |
| Use case | Quick copy of known files | Browse remote files, then decide what to copy |
| Resume transfer | No | Yes |

---

## 9.5 -- rsync: Smart Sync (Only copy what changed)

`rsync` = **r**emote **sync**. Like SCP but smarter -- it only transfers files that CHANGED.

```bash
rsync -avz /local/folder/ pappu@34.47.243.154:/remote/folder/
```

| Flag | Stands For | What It Does |
|------|-----------|-------------|
| `-a` | **a**rchive | Preserves permissions, timestamps, symlinks (use this always) |
| `-v` | **v**erbose | Show files being transferred |
| `-z` | compress (g**z**ip) | Compress during transfer |
| `--delete` | -- | Delete files on destination that don't exist in source |
| `--dry-run` | -- | Show what WOULD happen without actually doing it |
| `-P` | **P**rogress | Show transfer progress |

### Common rsync patterns:

```bash
# Sync local logs to a backup server
rsync -avz /var/log/foodexpress/ backup@backup-server:/backups/foodexpress/

# Sync from server to local (download)
rsync -avz pappu@34.47.243.154:/var/log/foodexpress/ /tmp/logs/

# Dry run first (see what would be copied without actually copying)
rsync -avz --dry-run /local/ remote:/dest/
```

**rsync vs scp:**

| Feature | SCP | rsync |
|---------|-----|-------|
| Copies | Everything, every time | Only changed files |
| Speed (repeated) | Slow (re-copies all) | Fast (skips unchanged) |
| Resume interrupted transfer | No | Yes |
| Delete extra files on dest | No | Yes (`--delete`) |
| Use case | One-time copy | Regular backups/syncs |

**Sustain context:** You sync production logs to a backup server every night with rsync. First run copies everything (maybe 10GB). Every night after that, only new/changed files are copied (maybe 200MB). Much faster.

---

## 9.6 -- FTP (Legacy -- Know it exists, don't use it)

| Protocol | Encrypted? | Use It? |
|----------|-----------|---------|
| FTP | No (passwords in plain text!) | Never in production |
| SFTP | Yes (over SSH) | Yes |
| SCP | Yes (over SSH) | Yes |
| rsync | Yes (over SSH) | Yes, for syncing |

> "If someone asks you to use FTP in production, say no. Use SFTP or rsync instead."

---

## Practice Exercises

| # | Task | Command |
|---|------|---------|
| 1 | SSH into the server | `ssh pappu@34.47.243.154` |
| 2 | Run `hostname` remotely without logging in | `ssh pappu@34.47.243.154 'hostname'` |
| 3 | Copy a local file to the server | `scp file.txt pappu@34.47.243.154:/tmp/` |
| 4 | Copy a file FROM the server | `scp pappu@34.47.243.154:/tmp/file.txt .` |
| 5 | Copy a whole directory to the server | `scp -r myfolder pappu@34.47.243.154:/tmp/` |
| 6 | Start an SFTP session | `sftp pappu@34.47.243.154` |
| 7 | In SFTP: list remote files | `ls` |
| 8 | In SFTP: download a file | `get app.log` |
| 9 | Sync a folder with rsync | `rsync -avz /tmp/logs/ pappu@34.47.243.154:/tmp/backup/` |
| 10 | Dry run rsync (preview only) | `rsync -avz --dry-run /tmp/logs/ pappu@34.47.243.154:/tmp/backup/` |
