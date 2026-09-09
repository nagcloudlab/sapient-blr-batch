# Lab 01 - Setup for Windows (WSL)

## Objective
Install Ansible on Windows using WSL and connect to GCP VMs

---

## Why WSL?
- Ansible **does not run natively on Windows**
- WSL (Windows Subsystem for Linux) gives you a real Linux terminal
- Ansible runs inside WSL, SSH works out of the box

---

## Step 1: Install WSL

```powershell
# Open PowerShell as Administrator and run:
wsl --install

# This installs Ubuntu by default
# Restart your PC when prompted
```

- After restart, Ubuntu terminal opens automatically
- Set a **username** and **password** (this is your Linux user)

```powershell
# Verify WSL is installed
wsl --list --verbose

# If you need a specific Ubuntu version
wsl --install -d Ubuntu-22.04
```

## Step 2: Install Ansible inside WSL

```bash
# Open WSL terminal (search "Ubuntu" in Start menu)

# Update packages
sudo apt update && sudo apt upgrade -y

# Install Ansible
sudo apt install -y ansible

# Verify
ansible --version
```

## Step 3: Install Google Cloud CLI inside WSL

```bash
# Install gcloud CLI
sudo apt install -y apt-transport-https ca-certificates gnupg curl

# Add Google Cloud repo
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

# Install
sudo apt update && sudo apt install -y google-cloud-cli

# Login to GCP
gcloud auth login
gcloud config set project grounded-apogee-503607-h2

# Verify
gcloud config list
```

## Step 4: Create GCP VMs (same as Mac)

```bash
# Create VM1 - NGINX Server
gcloud compute instances create vm1-nginx \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server,https-server

# Create VM2 - Spring Boot Server
gcloud compute instances create vm2-springboot \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server

# Allow HTTP traffic
gcloud compute firewall-rules create allow-http \
  --allow tcp:80,tcp:8080 \
  --target-tags=http-server

# Get external IPs
gcloud compute instances list
```

## Step 5: Setup SSH Access

### Find Your GCP Username

```bash
# Your GCP username = part before @ in your Google account
gcloud config get-value account

# Or check the SSH public key (username is the last field)
cat ~/.ssh/google_compute_engine.pub
```

### How SSH Keys Work (WSL + GCP + Ansible)

```
YOUR WSL (Control Node)
┌─────────────────────────────────────┐
│ ~/.ssh/google_compute_engine        │ ◄── PRIVATE KEY (stays here)
│ ~/.ssh/google_compute_engine.pub    │ ◄── PUBLIC KEY
└─────────────────────────────────────┘
        │
        │  gcloud compute ssh (first time)
        │  auto-generates key pair in WSL
        │  auto-copies PUBLIC key to VMs
        ▼
VM1 & VM2 (Managed Nodes)
┌─────────────────────────────────────┐
│ ~/.ssh/authorized_keys              │ ◄── PUBLIC KEY (copied here)
└─────────────────────────────────────┘
```

| Machine | Holds | Why |
|---------|-------|-----|
| **Your WSL** | Private key + Public key | Proves "I am who I say I am" |
| **VM1 & VM2** | Public key only | Verifies "yes, you're allowed in" |

### Connect to VMs (first time generates keys)

```bash
# First SSH auto-generates keys and pushes public key to VMs
gcloud compute ssh vm1-nginx --zone=us-central1-a --command="echo connected"
gcloud compute ssh vm2-springboot --zone=us-central1-a --command="echo connected"

# Test direct SSH
ssh -i ~/.ssh/google_compute_engine <EXTERNAL_IP_VM1>
ssh -i ~/.ssh/google_compute_engine <EXTERNAL_IP_VM2>
```

## Step 6: Verify Ansible Can Reach VMs

```bash
# Quick ping test (replace IPs)
ansible all -i "<VM1_IP>,<VM2_IP>," -m ping --user=<YOUR_USERNAME> --private-key=~/.ssh/google_compute_engine
```

- If you see **"pong"** — you're ready!

---

## Common WSL Issues & Fixes

### Issue: `gcloud auth login` doesn't open browser
```bash
# Use this flag instead
gcloud auth login --no-launch-browser
# Copy the URL manually into your Windows browser
```

### Issue: SSH permission denied
```bash
# Fix key permissions (WSL sometimes has wrong permissions)
chmod 600 ~/.ssh/google_compute_engine
chmod 644 ~/.ssh/google_compute_engine.pub
```

### Issue: Copy files between Windows and WSL
```bash
# Access Windows files from WSL
ls /mnt/c/Users/<WindowsUsername>/Desktop

# Access WSL files from Windows Explorer
# Type in address bar: \\wsl$\Ubuntu
```

### Issue: WSL clock out of sync
```bash
# This can cause SSL/TLS errors with gcloud
sudo hwclock -s
```

---

## Key Differences: Mac vs WSL

| | Mac | Windows (WSL) |
|---|-----|---------------|
| **Install Ansible** | `brew install ansible` | `sudo apt install ansible` |
| **Terminal** | Built-in Terminal | Ubuntu via WSL |
| **SSH keys location** | `~/.ssh/` | `~/.ssh/` (inside WSL) |
| **gcloud install** | `brew install google-cloud-sdk` | `apt install google-cloud-cli` |
| **Everything else** | Same | Same |

Once inside WSL, all Ansible commands and labs work **exactly the same** as Mac.
