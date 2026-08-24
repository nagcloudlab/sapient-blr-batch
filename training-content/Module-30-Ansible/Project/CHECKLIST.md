# Ansible -- Submission Checklist
## Module 30 | Day 33

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Playbook: `apt` module name corrected | [ ] |
| 2 | Playbook: `become: yes` added at play level | [ ] |
| 3 | Playbook: Variable uses `{{ app_port }}` Jinja2 syntax | [ ] |
| 4 | Playbook: `notify` matches handler name exactly | [ ] |
| 5 | Inventory: db1 moved to `[dbservers]` group | [ ] |
| 6 | Inventory: app2 moved to `[appservers]` group | [ ] |
| 7 | Inventory: SSH user corrected (no root access) | [ ] |
| 8 | Template: Group name `appservers` (plural) in Jinja2 loop | [ ] |
| 9 | Template: `proxy_pass` upstream name matches upstream block | [ ] |
| 10 | Behavioral: Participated in incident role play | [ ] |

---

## Self-Check Questions

1. **Why is `become: yes` needed?** Tasks like installing packages require root privileges. `become` tells Ansible to use sudo.
2. **Why is `$app_port` wrong?** Ansible uses Jinja2 templating (`{{ }}`), not shell variable syntax (`$`).
3. **Why do handler names need to match exactly?** Ansible uses string matching to connect `notify` to handlers. Case sensitivity matters.
4. **Why not SSH as root?** Security best practice: disable root SSH, use a service account with sudo access, and log all actions.
