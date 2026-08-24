# Ansible -- Lab Exercises
## Module 30 | Day 33

---

## Client Email

```
From: priya.mehta@foodexpress.in
To: sustain-engineering@team.com
Subject: Ansible Deployment Playbooks Broken
Date: 2026-09-06

Team,

Our Ansible playbooks for FoodExpress deployment are failing.
The previous engineer left and these playbooks haven't been
maintained. We need them working ASAP for our next release:

1. The main deployment playbook fails with module errors
   and permission denied messages
2. The inventory file has wrong host groupings
3. The nginx template generates invalid configuration

Please fix these playbooks so we can deploy reliably.

-- Priya Mehta, DevOps Lead, FoodExpress
```

---

## Lab 1: Fix the Deployment Playbook (4 bugs)

### File: `starter-code/deploy-foodexpress.yml`

| # | Hint | Impact |
|---|------|--------|
| 1 | The `apt` module is misspelled as `atp` | Ansible fails with "MODULE FAILURE -- module atp not found" |
| 2 | The `become: yes` directive is missing from the play level | All apt/service tasks fail with "Permission denied" because they run as unprivileged user |
| 3 | A variable is referenced using `$app_port` (shell syntax) instead of `{{ app_port }}` (Jinja2 syntax) | Variable is not interpolated; literal string "$app_port" is used in the config |
| 4 | The handler name in `notify` does not match the actual handler name | Handler never triggers; nginx is not restarted after config changes |

### Verification
- `ansible-playbook deploy-foodexpress.yml --syntax-check` -- passes
- `ansible-playbook deploy-foodexpress.yml --check` -- no errors (dry run)
- Handler triggers when config changes

---

## Lab 2: Fix the Inventory File (2 bugs)

### File: `starter-code/inventory/hosts.ini`

| # | Hint | Impact |
|---|------|--------|
| 1 | The `[appservers]` group contains the database host, and `[dbservers]` contains an app host -- hosts are in the wrong groups | Ansible installs Java on the database server and MySQL on the app server |
| 2 | The `ansible_ssh_user` variable uses an invalid value (`root` for app servers where only `deploy` user has access) | SSH authentication fails; Ansible cannot connect to app servers |

### Verification
- `ansible all -m ping -i inventory/hosts.ini` -- all hosts respond
- `ansible appservers --list-hosts` -- shows only app servers
- `ansible dbservers --list-hosts` -- shows only db servers

---

## Lab 3: Fix the Nginx Template (2 bugs)

### File: `starter-code/templates/nginx.conf.j2`

| # | Hint | Impact |
|---|------|--------|
| 1 | The Jinja2 for-loop iterates over `groups['appserver']` (singular) instead of `groups['appservers']` (plural, matching the inventory group name) | Template rendering fails with "undefined variable" error |
| 2 | The `proxy_pass` directive uses `http://` but the upstream name is misspelled, not matching the upstream block name | nginx fails to start: "upstream not found" error |

### Verification
- Template renders without Jinja2 errors
- Generated nginx.conf has correct upstream server entries
- nginx configuration test passes: `nginx -t`

---

## Bonus Challenges

1. **Add a health check task** after deployment that uses the `uri` module to verify `/actuator/health` returns 200
2. **Encrypt the database password** using Ansible Vault and reference it in the playbook
3. **Add a rollback play** that copies the previous JAR file back and restarts the service if the health check fails
4. **Create an Ansible role** called `foodexpress-app` with proper directory structure

---

## Summary

| Lab | Files | Bugs | Focus Area |
|-----|-------|------|------------|
| 1 | deploy-foodexpress.yml | 4 | Module name, become, variable syntax, handler notify |
| 2 | inventory/hosts.ini | 2 | Host groups, SSH user |
| 3 | templates/nginx.conf.j2 | 2 | Jinja2 group name, upstream reference |
| **Total** | **3 files** | **8 bugs** | |
