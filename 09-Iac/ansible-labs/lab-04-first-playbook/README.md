# Lab 04 - First Playbook

## Objective
Write and run your first Ansible playbook

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)

---

## What is a Playbook?
- A **YAML file** with a list of tasks to execute
- **Repeatable** — run it anytime, get the same result
- **Readable** — almost like English
- Think of it as a **recipe** for server configuration

## Playbook Structure
```yaml
---                          # YAML start
- name: Play Name            # A play (targets a group of hosts)
  hosts: all                 # Which servers to target
  become: yes                # Run as root

  tasks:                     # List of tasks
    - name: Task description # Human-readable name
      module_name:           # Ansible module to use
        key: value           # Module parameters
```

---

## Step 1: Run the Basic Playbook

```bash
# Dry run (check mode) — see what WOULD change
ansible-playbook playbook-basic.yml --check

# Actually run it
ansible-playbook playbook-basic.yml

# Run with verbose output
ansible-playbook playbook-basic.yml -v
ansible-playbook playbook-basic.yml -vv   # more verbose
ansible-playbook playbook-basic.yml -vvv  # maximum verbose
```

## Step 2: Understand the Output

```
PLAY [Setup base packages on all servers] ****

TASK [Gathering Facts] ****
ok: [vm1-nginx]
ok: [vm2-springboot]

TASK [Update apt cache] ****
changed: [vm1-nginx]        <-- "changed" means it did something
changed: [vm2-springboot]

TASK [Install common packages] ****
ok: [vm1-nginx]             <-- "ok" means already in desired state
ok: [vm2-springboot]

PLAY RECAP ****
vm1-nginx      : ok=3  changed=1  unreachable=0  failed=0
vm2-springboot : ok=3  changed=1  unreachable=0  failed=0
```

- **ok** — already in desired state (idempotent!)
- **changed** — Ansible made a change
- **failed** — something went wrong
- **unreachable** — can't connect to host

## Step 3: Run Again — See Idempotency

```bash
# Run the same playbook again
ansible-playbook playbook-basic.yml

# Notice: everything shows "ok" now, not "changed"
# This is IDEMPOTENCY — the core principle of Ansible
```

## Step 4: Target Specific Groups

```bash
# Run only on webservers
ansible-playbook playbook-basic.yml --limit webservers

# Run only on a single host
ansible-playbook playbook-basic.yml --limit vm1-nginx
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `playbook-basic.yml` | Basic playbook — install common packages |

---

## Key Takeaways
- Playbooks are YAML files with plays and tasks
- `--check` = dry run (safe preview)
- `--limit` = target specific hosts/groups
- Idempotency = run multiple times, same result
- `-v` to `-vvv` for increasing verbosity
- Next: Install **NGINX** using a playbook
