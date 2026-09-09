# Lab 08 - Variables & Facts

## Objective
Master the variable hierarchy and Ansible facts

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)

---

## Variable Precedence (Low to High)
1. `defaults/main.yml` (role defaults) — lowest
2. Inventory file vars
3. `group_vars/` files
4. `host_vars/` files
5. Playbook `vars:`
6. `--extra-vars` / `-e` on CLI — **highest** (always wins)

## Where to Define Variables?
| Location | Use When |
|----------|----------|
| `group_vars/all.yml` | Applies to ALL hosts |
| `group_vars/webservers.yml` | Applies to webservers group |
| `host_vars/vm1-nginx.yml` | Specific to one host |
| Playbook `vars:` | Playbook-specific settings |
| `-e "key=value"` | One-time overrides |

## What are Facts?
- **Auto-collected info** about each server (OS, IP, CPU, RAM, etc.)
- Gathered at the start of every play (`Gathering Facts` task)
- Access via `ansible_*` variables

---

## Step 1: Explore Facts

```bash
# See ALL facts for a host
ansible vm1-nginx -m setup

# Filter specific facts
ansible vm1-nginx -m setup -a "filter=ansible_distribution*"
ansible vm1-nginx -m setup -a "filter=ansible_default_ipv4"
ansible vm1-nginx -m setup -a "filter=ansible_memtotal_mb"
ansible vm1-nginx -m setup -a "filter=ansible_processor_vcpus"
```

## Step 2: Run the Variables Playbook

```bash
ansible-playbook variables-demo.yml
```

## Step 3: Override with Extra Vars

```bash
# Override the environment variable from CLI
ansible-playbook variables-demo.yml -e "env=production"

# Override multiple variables
ansible-playbook variables-demo.yml -e "env=production app_port=9090"
```

## Step 4: Use group_vars and host_vars

```bash
# These are already set up in this lab
ansible-playbook site.yml

# Notice how each host gets different values based on its group/host vars
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `variables-demo.yml` | Demo playbook showing variable types |
| `site.yml` | Playbook using group_vars and host_vars |
| `group_vars/all.yml` | Variables for all hosts |
| `group_vars/webservers.yml` | Variables for webservers |
| `group_vars/appservers.yml` | Variables for appservers |
| `host_vars/vm1-nginx.yml` | Variables specific to VM1 |
| `host_vars/vm2-springboot.yml` | Variables specific to VM2 |

---

## Key Takeaways
- Variable precedence matters — `-e` always wins
- `group_vars/` and `host_vars/` keep playbooks clean
- Facts give you system info without manual effort
- `register` captures task output into a variable
- `debug` module is your best friend for troubleshooting
- Next: Organize everything into **roles**
