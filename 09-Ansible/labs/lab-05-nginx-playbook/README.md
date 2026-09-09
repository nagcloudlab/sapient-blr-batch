# Lab 05 - NGINX Playbook

## Objective
Install and configure NGINX on VM1 using a playbook

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)

---

## What We'll Do
- Install NGINX on vm1-nginx
- Deploy a custom HTML page
- Start and enable the NGINX service
- Use **handlers** to restart NGINX only when config changes

## What are Handlers?
- Special tasks that run **only when notified**
- Triggered by `notify` in a task
- Run **once at the end** of the play (even if notified multiple times)
- Perfect for **service restarts**

---

## Step 1: Run the NGINX Playbook

```bash
# Dry run first
ansible-playbook nginx-setup.yml --check

# Run it
ansible-playbook nginx-setup.yml
```

## Step 2: Verify NGINX is Running

```bash
# Check from your Mac
curl http://<VM1_IP>

# Or use Ansible
ansible webservers -m shell -a "systemctl status nginx"
ansible webservers -m uri -a "url=http://localhost return_content=yes"
```

### Expected Output (curl)
```html
<!DOCTYPE html>
<html>
<head><title>Ansible Lab - NGINX</title>
...
<h1>Hello from Ansible!</h1>
...
```

## Step 3: Modify the HTML and Re-run

```bash
# Edit files/index.html, change some text, then:
ansible-playbook nginx-setup.yml

# Notice: NGINX handler runs because config changed!
```

## Step 4: Understand Handler Behavior

```bash
# Run again WITHOUT changing anything
ansible-playbook nginx-setup.yml

# Notice: handler does NOT run (nothing notified it)
# This is efficient — no unnecessary restarts
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `nginx-setup.yml` | Main playbook |
| `files/index.html` | Custom HTML homepage |
| `files/nginx.conf` | Custom NGINX configuration |

---

## Key Takeaways
- Handlers = conditional tasks (run only when notified)
- `notify` triggers a handler, `handlers` section defines them
- Handlers run once at the end, even if notified multiple times
- `enabled: yes` ensures service starts on boot
- Next: Install **Spring Boot** on VM2
