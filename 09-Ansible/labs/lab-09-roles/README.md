# Lab 09 - Roles

## Objective
Refactor playbooks into reusable Ansible roles

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)
- Lab 06 completed (JAR built at `../lab-06-springboot-playbook/app/target/hello-api-1.0.0.jar`)
- Update `<VM2_IP>` in `roles/nginx/defaults/main.yml`
- Run all commands from this lab directory (`cd lab-09-roles`)

---

## What are Roles?
- A **standard directory structure** for organizing Ansible code
- Makes code **reusable, shareable, and testable**
- Like **packages/modules** in programming
- Each role = one responsibility (e.g., nginx, springboot)

## Role Directory Structure
```
roles/
  nginx/
    tasks/main.yml       # Main task list (required)
    handlers/main.yml    # Handlers
    templates/           # Jinja2 templates
    defaults/main.yml    # Default variables (low priority, easy to override)
    # files/             # (optional) Static files
    # vars/main.yml      # (optional) Role variables (high priority, hard to override)
  springboot/
    tasks/main.yml
    handlers/main.yml
    templates/
    defaults/main.yml
  common/
    tasks/main.yml
    defaults/main.yml
```

> **defaults vs vars:** `defaults/main.yml` can be easily overridden by inventory, group_vars, or `-e`.
> `vars/main.yml` has high priority and is hard to override. Use `defaults` when you want flexibility.

## Why Roles?
| Without Roles | With Roles |
|---------------|------------|
| One huge playbook | Organized directories |
| Hard to reuse | Easy to reuse across projects |
| Hard to test | Can test individually |
| Gets messy fast | Clean, scalable structure |

---

## Step 1: Explore the Role Structure

```bash
# See the directory tree
find roles/ -type f | head -20

# Each role has a standardized layout
```

## Step 2: Create Roles from Scratch (optional)

```bash
# Ansible Galaxy can scaffold a role for you
ansible-galaxy init roles/my-custom-role
```

## Step 3: Run the Site Playbook

```bash
# This playbook uses roles instead of inline tasks
ansible-playbook site.yml

# Limit to just NGINX
ansible-playbook site.yml --limit webservers

# Limit to just Spring Boot
ansible-playbook site.yml --limit appservers
```

## Step 4: Use Tags for Selective Execution

```bash
# Run only tasks tagged "config"
ansible-playbook site.yml --tags config

# Run only tasks tagged "install"
ansible-playbook site.yml --tags install

# Skip specific tags
ansible-playbook site.yml --skip-tags config

# List all available tags
ansible-playbook site.yml --list-tags
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `site.yml` | Master playbook using roles |
| `roles/common/` | Common setup (packages, timezone) |
| `roles/nginx/` | NGINX installation and config |
| `roles/springboot/` | Spring Boot deployment |

---

## Key Takeaways
- Roles = standard structure for reusable Ansible code
- `defaults/main.yml` = overridable defaults
- `vars/main.yml` = fixed role variables
- Tags allow selective execution
- `ansible-galaxy init` scaffolds a new role
- Next: Secure secrets with **Ansible Vault**
