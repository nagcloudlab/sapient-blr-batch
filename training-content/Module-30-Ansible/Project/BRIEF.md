# Ansible -- Project Brief
## Module 30 | Day 33

---

## Sustain Context

FoodExpress uses Ansible for automated deployment across dev, staging, and production. The previous DevOps engineer left, and the playbooks are broken. As a sustain engineer, you must fix the playbooks, inventory, and templates so that automated deployment works again.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Deployment Playbook | Fix 4 bugs: module name, become, variable syntax, handler notify | 25 min | 10 |
| 2 | Fix Inventory | Fix 2 bugs: hosts in wrong groups, wrong SSH user | 15 min | 6 |
| 3 | Fix Nginx Template | Fix 2 bugs: Jinja2 group name, upstream reference | 15 min | 6 |
| 4 | Behavioral Role Play | Incident escalation scenario: Order Service down at 2 AM | 30 min | 8 |
| 5 | Bonus: Add Health Check | Add a post-deployment health check using uri module | 15 min | 5 |
| 6 | Bonus: Create Ansible Role | Restructure playbook into a proper Ansible role | 15 min | 5 |

**Total Points Available:** 40

---

## Deliverables

1. Fixed `deploy-foodexpress.yml` with all 4 bugs resolved
2. Fixed `inventory/hosts.ini` with correct host groupings
3. Fixed `templates/nginx.conf.j2` with correct Jinja2 syntax
4. Role play participation with clear escalation and communication
5. (Bonus) Health check task that verifies deployment success
6. (Bonus) Ansible role with proper directory structure
