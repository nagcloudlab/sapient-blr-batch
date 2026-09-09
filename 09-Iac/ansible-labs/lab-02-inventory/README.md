# Lab 02 - Inventory

## Objective
Define and organize your servers using Ansible inventory files

## Prerequisites
- Lab 01 completed (VMs created, SSH working)

---

## What is Inventory?
- A **list of servers** Ansible manages
- Can be **INI format** or **YAML format**
- Servers can be grouped (e.g., webservers, appservers)
- Default location: `/etc/ansible/hosts` (we'll use local files)

---

## Step 1: Simple Inventory (INI format)

```bash
# Test connectivity
ansible all -i inventory.ini -m ping
```

- `-i inventory.ini` — use our inventory file
- `-m ping` — run the ping module
- `all` — target all hosts

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
- **SUCCESS + pong** = Ansible can reach the server via SSH

## Step 2: YAML Inventory (preferred)

```bash
# Test with YAML inventory
ansible all -i inventory.yml -m ping
```

## Step 3: Test by Groups

```bash
# Ping only web servers
ansible webservers -i inventory.yml -m ping

# Ping only app servers
ansible appservers -i inventory.yml -m ping
```

## Step 4: List Hosts

```bash
# See what hosts Ansible knows about
ansible-inventory -i inventory.yml --list

# Graph view
ansible-inventory -i inventory.yml --graph
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `inventory.ini` | INI format inventory |
| `inventory.yml` | YAML format inventory (preferred) |
| `ansible.cfg` | Local Ansible configuration |

---

## Key Takeaways
- Inventory = your server address book
- Groups let you target specific servers
- `ansible.cfg` saves you from typing flags every time
- YAML inventory is more readable than INI
- Next: Run **ad-hoc commands** against your inventory
