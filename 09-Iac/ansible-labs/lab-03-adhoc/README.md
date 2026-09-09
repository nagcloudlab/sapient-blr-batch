# Lab 03 - Ad-Hoc Commands

## Objective
Run one-off commands on your servers without writing a playbook

## Prerequisites
- Lab 02 completed (inventory.yml configured with real IPs and username)

---

## What are Ad-Hoc Commands?
- **One-liner commands** — quick tasks without writing YAML
- Great for **troubleshooting**, **quick checks**, **one-time tasks**
- Syntax: `ansible <target> -m <module> -a "<arguments>"`
- Think of it as **SSH on steroids** — runs on multiple servers at once

---

## Step 1: Basic Connectivity

```bash
# Ping all servers
ansible all -m ping

# Ping specific group
ansible webservers -m ping
ansible appservers -m ping
```

## Step 2: Gather System Info

```bash
# Check uptime
ansible all -m command -a "uptime"

# Check disk space
ansible all -m command -a "df -h"

# Check memory
ansible all -m command -a "free -m"

# Check OS version
ansible all -m command -a "cat /etc/os-release"

# Get all facts about a server
ansible vm1-nginx -m setup

# Get only memory facts
ansible vm1-nginx -m setup -a "filter=ansible_memtotal_mb"
```

## Step 3: Package Management

```bash
# Update apt cache (like apt update)
ansible all -m apt -a "update_cache=yes" --become

# Install a package
ansible all -m apt -a "name=curl state=present" --become

# Install multiple packages
ansible all -m apt -a "name=vim,htop,wget state=present" --become

# Remove a package
ansible all -m apt -a "name=htop state=absent" --become
```

## Step 4: File Operations

```bash
# Create a directory
ansible all -m file -a "path=/opt/myapp state=directory mode=0755" --become

# Create a file
ansible all -m file -a "path=/tmp/hello.txt state=touch"

# Copy a file to remote servers
ansible all -m copy -a "src=./test.txt dest=/tmp/test.txt"

# Download a file from URL
ansible all -m get_url -a "url=https://example.com dest=/tmp/example.html"
```

## Step 5: Service Management

```bash
# Check if a service is running
ansible all -m service -a "name=ssh state=started" --become

# Restart a service
ansible all -m service -a "name=ssh state=restarted" --become
```

## Step 6: User Management

```bash
# Create a user
ansible all -m user -a "name=deploy state=present" --become

# Remove a user
ansible all -m user -a "name=deploy state=absent" --become
```

## Step 7: Shell vs Command Module

```bash
# command module — simple, safe (no pipes, redirects)
ansible all -m command -a "ls /tmp"

# shell module — full shell features (pipes, redirects, env vars)
ansible all -m shell -a "echo $HOSTNAME > /tmp/hostname.txt"
ansible all -m shell -a "ps aux | grep ssh | wc -l"
```

---

## Module Cheat Sheet
| Module | Purpose | Example |
|--------|---------|---------|
| `ping` | Test connectivity | `-m ping` |
| `command` | Run simple commands | `-m command -a "uptime"` |
| `shell` | Run shell commands (pipes, etc.) | `-m shell -a "ps aux \| head"` |
| `apt` | Manage packages (Debian/Ubuntu) | `-m apt -a "name=nginx state=present"` |
| `copy` | Copy files to remote | `-m copy -a "src=x dest=y"` |
| `file` | Manage files/directories | `-m file -a "path=x state=directory"` |
| `service` | Manage services | `-m service -a "name=x state=started"` |
| `user` | Manage users | `-m user -a "name=x state=present"` |
| `setup` | Gather system facts | `-m setup` |

---

## Files in this lab
| File | Description |
|------|-------------|
| `ansible.cfg` | Points to shared inventory in lab-02 |
| `test.txt` | Sample file for copy module demo |

This lab uses only ad-hoc commands — no playbooks.

## Key Takeaways
- Ad-hoc = quick one-liner tasks
- `command` is safe, `shell` is powerful (use wisely)
- `--become` = run as root (sudo)
- Great for debugging, but **playbooks** are better for repeatable tasks
- Next: Write your **first playbook**
