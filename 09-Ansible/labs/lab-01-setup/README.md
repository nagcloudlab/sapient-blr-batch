# Lab 01 - Setup & Installation

## Objective
Install Ansible on Mac and provision 2 GCP VMs

---

## What is Ansible?
- **Configuration management** tool — automates server setup
- **Agentless** — no software needed on target servers (uses SSH)
- **Idempotent** — run it 10 times, same result as running once
- **Written in Python**, uses **YAML** for playbooks
- **Push-based** — you push configs from control node to managed nodes

## Architecture
```
[Your Mac]  ──SSH──►  [VM1: NGINX]
(Control Node)        (Managed Node)
     │
     └────SSH──►  [VM2: Spring Boot]
                  (Managed Node)
```

---

## Step 1: Install Ansible on Mac

```bash
# Install via Homebrew
brew install ansible

# Verify installation
ansible --version

# You should see something like:
# ansible [core 2.x.x]
# python version = 3.x.x
```

## Step 2: Create 2 GCP VMs

```bash
# Login to GCP
gcloud auth login
gcloud config set project grounded-apogee-503607-h2

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

## Step 3: Setup SSH Access

### How SSH Keys Work with GCP + Ansible

```
YOUR MAC (Control Node)
┌─────────────────────────────────────┐
│ ~/.ssh/google_compute_engine        │ ◄── PRIVATE KEY (stays here, never shared)
│ ~/.ssh/google_compute_engine.pub    │ ◄── PUBLIC KEY
└─────────────────────────────────────┘
        │
        │  gcloud compute ssh (first time)
        │  auto-generates key pair on Mac
        │  auto-copies PUBLIC key to VMs
        ▼
VM1 & VM2 (Managed Nodes)
┌─────────────────────────────────────┐
│ ~/.ssh/authorized_keys              │ ◄── PUBLIC KEY (copied here by gcloud)
└─────────────────────────────────────┘

Ansible SSH Flow:
Mac (private key) ──authenticates──► VM (public key) ──► Access Granted
```

| Machine | Holds | Why |
|---------|-------|-----|
| **Your Mac** | Private key + Public key | Proves "I am who I say I am" |
| **VM1 & VM2** | Public key only | Verifies "yes, you're allowed in" |

- Private key **never leaves your Mac** — that's the security model
- This is why Ansible is **agentless** — it just needs SSH access

### Find Your GCP Username

```bash
# Your GCP username = part before @ in your Google account
gcloud config get-value account

# Or check the SSH public key (username is the last field)
cat ~/.ssh/google_compute_engine.pub
```

- This username is what Ansible uses as `ansible_user` in inventory files
- GCP auto-creates this user on the VMs when you first SSH

### Connect to VMs (first time generates keys)

```bash
# gcloud compute ssh auto-generates ~/.ssh/google_compute_engine key pair
# First SSH also pushes your public key to the VM
gcloud compute ssh vm1-nginx --zone=us-central1-a --command="echo connected"
gcloud compute ssh vm2-springboot --zone=us-central1-a --command="echo connected"

# Test direct SSH (uses the auto-generated key)
ssh -i ~/.ssh/google_compute_engine <EXTERNAL_IP_VM1>
ssh -i ~/.ssh/google_compute_engine <EXTERNAL_IP_VM2>
```

## Step 4: Verify Ansible Can Reach VMs

```bash
# Quick ping test (replace IPs)
ansible all -i "<VM1_IP>,<VM2_IP>," -m ping --user=<YOUR_USERNAME> --private-key=~/.ssh/google_compute_engine
```

- If you see **"pong"** — you're ready!

---

## Troubleshooting

### "Permission denied (publickey)"
```bash
# Re-push your SSH key to the VM
gcloud compute ssh vm1-nginx --zone=us-central1-a
# Verify key exists
ls -la ~/.ssh/google_compute_engine
```

### "Host unreachable" or "Connection timed out"
```bash
# Check VM is running
gcloud compute instances list
# Check firewall rules
gcloud compute firewall-rules list
# Note: VM IPs change after stop/start — update inventory!
```

### "Python not found" on remote
- Our inventory already has `ansible_python_interpreter: /usr/bin/python3`
- If error persists: `ansible all -m raw -a "sudo apt install -y python3"`

### Wrong username
```bash
# Your GCP username = part before @ in your Google account
gcloud config get-value account
# This must match ansible_user in inventory.yml AND remote_user in ansible.cfg
```

---

## Files in this lab
This lab has no Ansible files — it focuses on environment setup and SSH verification.

| File | Description |
|------|-------------|
| `README.md` | This guide (Mac setup) |
| `SETUP-WINDOWS-WSL.md` | Windows/WSL setup guide |

## Key Takeaways
- Ansible runs from your Mac (control node) — nothing to install on VMs
- SSH is the transport layer — no agents needed
- GCP VMs are our managed nodes
- Next: We'll organize VMs using an **inventory file**
