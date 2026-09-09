# Lab 11 - Conditionals & Loops

## Objective
Use `when`, `loop`, `block/rescue/always` for dynamic playbooks

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)

---

## Conditionals (`when`)
- Skip or run tasks based on conditions
- Uses **Jinja2 expressions** (Python-like)
- No `{{ }}` needed inside `when:` — it's already a Jinja2 context

```yaml
# Common conditions
when: ansible_os_family == "Debian"
when: ansible_memtotal_mb >= 1024
when: env == "production"
when: result is failed
when: my_var is defined
when: my_var | bool
when: item.enabled
```

## Loops
```yaml
# Simple loop
loop:
  - nginx
  - curl
  - vim

# Loop with index
loop: "{{ packages }}"
loop_control:
  index_var: idx

# Dict loop
loop: "{{ lookup('dict', my_dict) }}"
```

## Error Handling (`block/rescue/always`)
```yaml
block:     # Try this
rescue:    # If block fails, do this (like catch)
always:    # Always do this (like finally)
```

---

## Step 1: Run the Conditionals Playbook

```bash
ansible-playbook conditionals.yml
```

## Step 2: Run the Loops Playbook

```bash
ansible-playbook loops.yml
```

## Step 3: Run the Error Handling Playbook

```bash
ansible-playbook error-handling.yml
```

## Step 4: Experiment

```bash
# Change the environment to see different behavior
ansible-playbook conditionals.yml -e "env=production"
ansible-playbook conditionals.yml -e "env=staging"
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `conditionals.yml` | When conditions demo |
| `loops.yml` | Loop patterns demo |
| `error-handling.yml` | block/rescue/always demo |

---

## Key Takeaways
- `when:` = if statement for tasks
- `loop:` replaces old `with_items`
- `block/rescue/always` = try/catch/finally
- `register` + `when` = powerful combo
- `failed_when` / `changed_when` = customize task status
- Next: **Dynamic Inventory** with GCP
