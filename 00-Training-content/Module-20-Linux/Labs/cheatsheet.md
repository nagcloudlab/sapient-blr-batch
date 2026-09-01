# Linux Commands Quick Reference

> Single-page reference for Linux command-line essentials. Run as appropriate user; use `sudo` where elevated privileges are required.

---

## Navigation

| Command | Example | Description |
|---|---|---|
| `pwd` | `pwd` | Print current working directory |
| `cd <dir>` | `cd /var/log/nginx` | Change to directory |
| `cd ..` | `cd ..` | Go up one level |
| `cd -` | `cd -` | Return to previous directory |
| `cd ~` | `cd ~` | Go to home directory |
| `ls` | `ls` | List files in current directory |
| `ls -l` | `ls -l` | Long listing with permissions, size, date |
| `ls -la` | `ls -la` | Long listing including hidden files |
| `ls -lh` | `ls -lh` | Long listing with human-readable sizes |
| `ls -lt` | `ls -lt` | Sort by modification time (newest first) |
| `ls <dir>` | `ls /etc/nginx` | List a specific directory |

---

## File Operations

| Command | Example | Description |
|---|---|---|
| `mkdir <dir>` | `mkdir /opt/foodexpress` | Create directory |
| `mkdir -p <path>` | `mkdir -p /opt/foodexpress/logs/app` | Create nested directories |
| `touch <file>` | `touch app.log` | Create empty file or update timestamp |
| `cp <src> <dst>` | `cp app.conf app.conf.bak` | Copy file |
| `cp -r <src> <dst>` | `cp -r /opt/foodexpress /opt/foodexpress-backup` | Copy directory recursively |
| `mv <src> <dst>` | `mv app.conf /etc/foodexpress/app.conf` | Move or rename file/directory |
| `rm <file>` | `rm old.log` | Remove file |
| `rm -f <file>` | `rm -f stuck.lock` | Force remove (no prompt) |
| `rm -rf <dir>` | `rm -rf /tmp/build` | Remove directory recursively (use with care) |
| `ln -s <target> <link>` | `ln -s /opt/foodexpress/current /opt/foodexpress/app` | Create symbolic link |
| `find <path> -name "pattern"` | `find /var/log -name "*.log"` | Find files by name |
| `find <path> -mtime -n` | `find /var/log -mtime -1` | Files modified in last n days |
| `find <path> -size +nM` | `find /var -size +100M` | Files larger than n megabytes |

---

## Viewing Files

| Command | Example | Description |
|---|---|---|
| `cat <file>` | `cat /etc/hosts` | Print entire file to stdout |
| `cat -n <file>` | `cat -n app.log` | Print with line numbers |
| `less <file>` | `less /var/log/syslog` | Paginated view (`q` to quit, `/` to search) |
| `head <file>` | `head /var/log/nginx/access.log` | First 10 lines |
| `head -n N <file>` | `head -n 50 app.log` | First N lines |
| `tail <file>` | `tail /var/log/app.log` | Last 10 lines |
| `tail -n N <file>` | `tail -n 100 app.log` | Last N lines |
| `tail -f <file>` | `tail -f /var/log/foodexpress/app.log` | Follow file live (Ctrl+C to stop) |
| `grep "pattern" <file>` | `grep "ERROR" /var/log/app.log` | Search for pattern in file |
| `grep -i "pattern" <file>` | `grep -i "timeout" app.log` | Case-insensitive search |
| `grep -r "pattern" <dir>` | `grep -r "database" /etc/foodexpress/` | Recursive search in directory |
| `grep -n "pattern" <file>` | `grep -n "500" access.log` | Show line numbers |
| `grep -v "pattern" <file>` | `grep -v "DEBUG" app.log` | Lines that do NOT match |
| `grep -c "pattern" <file>` | `grep -c "ERROR" app.log` | Count matching lines |

---

## Permissions

| Command | Example | Description |
|---|---|---|
| `chmod <mode> <file>` | `chmod 644 app.conf` | Set permissions (owner=rw, group=r, others=r) |
| `chmod +x <file>` | `chmod +x deploy.sh` | Add execute permission for all |
| `chmod -R <mode> <dir>` | `chmod -R 755 /opt/foodexpress` | Recursive permission change |
| `chown <user> <file>` | `chown appuser app.log` | Change file owner |
| `chown <user>:<group> <file>` | `chown appuser:appgroup /opt/foodexpress` | Change owner and group |
| `chown -R <user>:<group> <dir>` | `chown -R deploy:deploy /opt/foodexpress` | Recursive ownership change |
| `ls -l` | `ls -l app.conf` | View current permissions |

**Permission notation:** `rwxrwxrwx` = owner/group/others. `755` = `rwxr-xr-x`. `644` = `rw-r--r--`.

---

## Process Management

| Command | Example | Description |
|---|---|---|
| `ps aux` | `ps aux` | List all running processes |
| `ps aux | grep <name>` | `ps aux | grep node` | Find a specific process |
| `top` | `top` | Interactive process monitor (`q` to quit) |
| `htop` | `htop` | Enhanced interactive monitor (if installed) |
| `kill <PID>` | `kill 1234` | Send SIGTERM to process (graceful stop) |
| `kill -9 <PID>` | `kill -9 1234` | Send SIGKILL (force kill) |
| `killall <name>` | `killall node` | Kill all processes by name |
| `pkill <pattern>` | `pkill -f "foodexpress"` | Kill by pattern match |
| `systemctl status <service>` | `systemctl status nginx` | Show service status |
| `systemctl start <service>` | `sudo systemctl start nginx` | Start a service |
| `systemctl stop <service>` | `sudo systemctl stop nginx` | Stop a service |
| `systemctl restart <service>` | `sudo systemctl restart nginx` | Restart a service |
| `systemctl enable <service>` | `sudo systemctl enable nginx` | Enable service at boot |
| `systemctl disable <service>` | `sudo systemctl disable nginx` | Disable service at boot |
| `journalctl -u <service>` | `journalctl -u foodexpress -n 100` | View service logs |
| `nohup <cmd> &` | `nohup ./server.sh &` | Run process that survives logout |
| `jobs` | `jobs` | List background jobs in current shell |
| `bg / fg` | `fg %1` | Send job to background / foreground |

---

## Disk Usage

| Command | Example | Description |
|---|---|---|
| `df -h` | `df -h` | Disk space for all mounted filesystems (human-readable) |
| `df -h <path>` | `df -h /var` | Disk space for specific path |
| `du -sh <dir>` | `du -sh /var/log` | Total size of directory |
| `du -sh *` | `du -sh /var/log/*` | Size of each item in directory |
| `du -h --max-depth=1 <dir>` | `du -h --max-depth=1 /opt` | One-level breakdown of sizes |
| `lsblk` | `lsblk` | List block devices (disks, partitions) |

---

## Network

| Command | Example | Description |
|---|---|---|
| `ping <host>` | `ping google.com` | Test connectivity (Ctrl+C to stop) |
| `ping -c 4 <host>` | `ping -c 4 8.8.8.8` | Send exactly 4 packets |
| `curl <url>` | `curl http://localhost:3000/api/health` | Fetch URL output to stdout |
| `curl -I <url>` | `curl -I https://foodexpress.com` | Fetch HTTP headers only |
| `curl -X POST -H "Content-Type: application/json" -d '{...}' <url>` | `curl -X POST -H "Content-Type: application/json" -d '{"name":"Biryani"}' http://localhost:3000/api/items` | POST JSON |
| `curl -o <file> <url>` | `curl -o app.tar.gz https://releases.example.com/app.tar.gz` | Download to file |
| `wget <url>` | `wget https://releases.example.com/agent.deb` | Download file |
| `wget -O <file> <url>` | `wget -O agent.deb https://example.com/agent.deb` | Download with custom filename |
| `ss -tlnp` | `ss -tlnp` | Show listening TCP sockets with PID |
| `ss -tulnp` | `ss -tulnp` | Show listening TCP and UDP sockets |
| `netstat -tlnp` | `netstat -tlnp` | Same (older systems; install net-tools) |
| `ip addr` | `ip addr` | Show network interfaces and IP addresses |
| `ip route` | `ip route` | Show routing table |
| `traceroute <host>` | `traceroute 8.8.8.8` | Trace network path to host |
| `nslookup <host>` | `nslookup foodexpress.com` | DNS lookup |
| `dig <host>` | `dig foodexpress.com` | Detailed DNS lookup |

---

## Text Processing

| Command | Example | Description |
|---|---|---|
| `sed 's/old/new/g' <file>` | `sed 's/localhost/prod-db/g' app.conf` | Replace all occurrences |
| `sed -i 's/old/new/g' <file>` | `sed -i 's/8080/3000/g' nginx.conf` | Replace in-place |
| `sed -n '10,20p' <file>` | `sed -n '10,20p' app.log` | Print lines 10 to 20 |
| `awk '{print $1, $3}' <file>` | `awk '{print $1, $3}' access.log` | Print columns 1 and 3 |
| `awk -F: '{print $1}' <file>` | `awk -F: '{print $1}' /etc/passwd` | Use `:` as field separator |
| `awk '/ERROR/{print}' <file>` | `awk '/ERROR/{print}' app.log` | Print lines matching pattern |
| `awk 'NR%2==0' <file>` | `awk 'NR%2==0' data.txt` | Print even-numbered lines |
| `cut -d: -f1 <file>` | `cut -d: -f1 /etc/passwd` | Cut field 1 with `:` delimiter |
| `cut -c1-10 <file>` | `cut -c1-10 app.log` | Cut first 10 characters per line |
| `sort <file>` | `sort names.txt` | Sort lines alphabetically |
| `sort -n <file>` | `sort -n sizes.txt` | Sort numerically |
| `sort -rn <file>` | `sort -rn sizes.txt` | Sort numerically, descending |
| `sort -u <file>` | `sort -u ips.txt` | Sort and remove duplicates |
| `uniq <file>` | `sort errors.txt | uniq` | Remove consecutive duplicate lines |
| `uniq -c <file>` | `sort errors.txt | uniq -c` | Count occurrences of each line |
| `wc -l <file>` | `wc -l app.log` | Count lines |
| `wc -w <file>` | `wc -w report.txt` | Count words |
| `wc -c <file>` | `wc -c binary.dat` | Count bytes |

---

## Compression / Archives

| Command | Example | Description |
|---|---|---|
| `tar -czf <archive> <dir>` | `tar -czf foodexpress-backup.tar.gz /opt/foodexpress` | Create gzip-compressed archive |
| `tar -xzf <archive>` | `tar -xzf foodexpress-backup.tar.gz` | Extract gzip archive |
| `tar -xzf <archive> -C <dir>` | `tar -xzf app.tar.gz -C /opt/` | Extract to specific directory |
| `tar -tzf <archive>` | `tar -tzf backup.tar.gz` | List contents without extracting |
| `tar -cjf <archive> <dir>` | `tar -cjf backup.tar.bz2 /opt/foodexpress` | Create bzip2-compressed archive |
| `gzip <file>` | `gzip app.log` | Compress file (replaces original with `.gz`) |
| `gunzip <file>.gz` | `gunzip app.log.gz` | Decompress `.gz` file |
| `zcat <file>.gz` | `zcat app.log.gz` | View compressed file without extracting |
| `zip -r <archive> <dir>` | `zip -r foodexpress.zip /opt/foodexpress` | Create zip archive |
| `unzip <archive>` | `unzip foodexpress.zip` | Extract zip archive |
| `unzip -l <archive>` | `unzip -l foodexpress.zip` | List zip contents |

---

## Useful Combinations (Pipes)

| Example | Description |
|---|---|
| `cat app.log | grep ERROR | wc -l` | Count error lines in log |
| `ps aux | grep node | awk '{print $2}'` | Get PIDs of node processes |
| `tail -f app.log | grep --line-buffered "ERROR"` | Live stream of error lines |
| `du -sh /var/log/* | sort -rh | head -10` | Top 10 largest log files |
| `ss -tlnp | grep LISTEN` | All listening ports |
| `find /var/log -name "*.log" -mtime -1 | xargs grep -l "ERROR"` | Logs from last 24h containing ERROR |

---

*FoodExpress Training | Module 20: Linux | Publicis Sapient Sustain Eng 2026*
