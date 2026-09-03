# Ansible -- Trainer Solutions & Hints
## Module 30 | Day 33

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Deployment Playbook | `apt` not `atp`; add `become: yes`; use `{{ app_port }}` not `$app_port`; handler name must match exactly (case-sensitive) | Students fix the module name but miss the `become` directive. They then see a different error (permission denied) and think the fix didn't work | Ask: "Who is running this task? What user does Ansible SSH as? Does that user have sudo?" |
| 2 | Fix Inventory | Swap db1 and app2 to correct groups; change root to dbadmin | Students fix the groups but leave the SSH user as root. Ask them to check SSH configuration on the target server | Ask: "If root SSH is disabled on production servers (as it should be), what user do you use?" |
| 3 | Fix Nginx Template | `groups['appservers']` (plural); upstream name `foodexpress_backend` matches the upstream block | Students fix the group name but miss the upstream mismatch. nginx -t catches this easily | Ask: "How do you test nginx config without restarting?" (`nginx -t`) |
| 4 | Behavioral Role Play | Follow incident process: diagnose, communicate, fix/rollback, document | Students either panic and skip diagnosis, or take too long diagnosing without communicating | Ask: "What is the first thing you tell the on-call manager? What do they need to know?" |

---

## Key Discussion Points

1. Why is Ansible agentless? What are the trade-offs vs. agent-based tools?
2. Why is idempotency important for sustain engineering? (Safe to re-run playbooks)
3. When should you use `command`/`shell` vs. a specific module? (Always prefer modules)
4. Why are handler names case-sensitive? What happens if notify doesn't match?
5. How does Ansible Vault compare to HashiCorp Vault?
6. What is the role of Ansible in a CI/CD pipeline? (Post-deploy configuration)
