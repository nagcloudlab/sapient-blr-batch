# Shared SSH Key Setup (For Participants)

## Objective
Use the trainer's shared SSH key to connect to the lab VMs from your WSL machine

---

## Architecture
```
Trainer's Mac ──────────┐
                        │
Participant-1 (WSL) ────┤── Same SSH Key ──► VM1 (NGINX)
Participant-2 (WSL) ────┤                   VM2 (Spring Boot)
Participant-3 (WSL) ────┘
```

All participants share the **same private key** provided by the trainer.
This key is already authorized on both VMs.

---

## Step 1: Clone the Repo and Get the Key

```bash
# Open your WSL terminal (Ubuntu)

# Clone the training repo
git clone https://github.com/nagcloudlab/sapient-blr-batch.git
cd sapient-blr-batch/09-Ansible/labs
```

The private key is already in the repo at `lab-01-setup/keys/google_compute_engine`.

## Step 2: Copy the Key to SSH Directory

```bash
# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh

# Copy the shared key
cp lab-01-setup/keys/google_compute_engine ~/.ssh/google_compute_engine
```

## Step 3: Fix File Permissions (CRITICAL)

```bash
# SSH refuses keys with wrong permissions — this step is mandatory
chmod 600 ~/.ssh/google_compute_engine
chmod 700 ~/.ssh

# Verify permissions
ls -la ~/.ssh/google_compute_engine
# Should show: -rw------- (only owner can read)
```

> **If you skip this step**, you'll get: `WARNING: UNPROTECTED PRIVATE KEY FILE!`
> and SSH will refuse to connect.

## Step 4: Test SSH Connection

```bash
# Replace <VM1_IP> and <VM2_IP> with IPs provided by trainer
# Replace <TRAINER_USERNAME> with the username provided by trainer

ssh -i ~/.ssh/google_compute_engine <TRAINER_USERNAME>@<VM1_IP>
# Type 'exit' after confirming connection

ssh -i ~/.ssh/google_compute_engine <TRAINER_USERNAME>@<VM2_IP>
# Type 'exit' after confirming connection
```

### Expected Output
```
Welcome to Ubuntu 22.04...
====================================
Server: vm1-nginx
Managed by Ansible
====================================
```

## Step 5: Install Ansible in WSL

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Ansible
sudo apt install -y ansible

# Verify
ansible --version
```

## Step 6: Clone the Lab Files

```bash
# Option A: Clone from Git (if trainer shared a repo)
git clone <REPO_URL>
cd 09-Ansible/labs

# Option B: Copy from shared folder
cp -r /mnt/c/Users/<YOUR_WINDOWS_USERNAME>/Desktop/09-Ansible ~/
cd ~/09-Ansible/labs
```

## Step 7: Update Inventory with Trainer's Details

```bash
# Edit the shared inventory file
nano lab-02-inventory/inventory.yml
```

Replace these values (trainer will provide them):

| Placeholder | Replace With | Example |
|-------------|-------------|---------|
| `<VM1_IP>` | VM1 external IP | `34.123.45.67` |
| `<VM2_IP>` | VM2 external IP | `35.234.56.78` |
| `<YOUR_GCP_USERNAME>` | Trainer's GCP username | `trainer` |

Also update `ansible.cfg` in each lab:
```bash
# Quick replace across all ansible.cfg files
# Replace <YOUR_GCP_USERNAME> with the trainer's username
find . -name "ansible.cfg" -exec sed -i 's/<YOUR_GCP_USERNAME>/TRAINER_USERNAME_HERE/g' {} \;
```

## Step 8: Verify Ansible Connectivity

```bash
cd lab-02-inventory

# Ping both VMs
ansible all -m ping
```

### Expected Output
```
vm1-nginx | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
vm2-springboot | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

If you see **pong** — you're ready for the labs!

---

## Troubleshooting

### "WARNING: UNPROTECTED PRIVATE KEY FILE!"
```bash
chmod 600 ~/.ssh/google_compute_engine
```

### "Permission denied (publickey)"
- Check you're using the correct username (trainer's, not yours)
- Check key file is in the right location: `ls ~/.ssh/google_compute_engine`
- Check the key content wasn't corrupted during copy

### "Connection timed out"
- Verify the VM IP is correct (ask trainer)
- Check your internet connection
- VMs may have been stopped — ask trainer to restart them

### "Host key verification failed"
```bash
# Remove old host key and retry
ssh-keygen -R <VM_IP>
```

### nano not familiar? Use vim or VS Code
```bash
# Use VS Code from WSL (if installed on Windows)
code lab-02-inventory/inventory.yml

# Or use vim
vi lab-02-inventory/inventory.yml
```

---

## Important Notes
- **Do NOT share the private key** outside this training session
- **Delete the key** after the training is complete
- All participants connect as the **same user** — be careful not to overwrite each other's work during labs
- The trainer may reset VMs between labs — don't store important data on them
