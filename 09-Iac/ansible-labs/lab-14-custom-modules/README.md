# Lab 14 - Custom Ansible Modules

## Objective
Write your own Ansible modules in Python when built-in modules aren't enough

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)
- Basic Python knowledge

---

## Why Custom Modules?

| Scenario | Use |
|----------|-----|
| Install packages, copy files, manage services | Built-in modules (apt, copy, service) |
| Interact with your company's internal API | **Custom module** |
| Complex logic not possible with shell/command | **Custom module** |
| Reusable automation for your team | **Custom module** |

## How Ansible Modules Work

```
Control Node (Mac/WSL)                    Managed Node (VM)
┌──────────────────────┐                 ┌──────────────────┐
│ 1. Ansible reads     │                 │                  │
│    playbook          │                 │                  │
│                      │   SSH + copy    │                  │
│ 2. Packages module   │ ──────────────► │ 3. Python script │
│    as Python script  │                 │    executes      │
│                      │   SSH + read    │                  │
│ 5. Parses JSON       │ ◄────────────── │ 4. Returns JSON  │
│    result            │                 │    result        │
└──────────────────────┘                 └──────────────────┘
```

- Every Ansible module is a **Python script** (or any executable)
- It receives **input as JSON** (module arguments)
- It returns **output as JSON** (changed, msg, failed, etc.)
- Ansible copies it to the remote host, runs it, reads the JSON output

---

## Step 1: Your First Custom Module (Hello World)

Look at `library/hello.py` — the simplest possible module.

```bash
# Run it
ansible-playbook playbook-hello.yml

# Run with verbose to see the JSON output
ansible-playbook playbook-hello.yml -v
```

### Expected Output
```
TASK [Say hello with custom module] ***
ok: [vm1-nginx] => {
    "changed": false,
    "message": "Hello, Ansible!"
}

TASK [Say hello to a specific name] ***
ok: [vm1-nginx] => {
    "changed": false,
    "message": "Hello, DevOps Team!"
}
```

## Step 2: Practical Module — App Health Checker

A real-world module that checks if an application is healthy.

Look at `library/app_health.py`.

```bash
# Run the health check playbook
ansible-playbook playbook-health.yml
```

### What This Module Does
1. Accepts `url` and `timeout` as parameters
2. Makes an HTTP request to the URL
3. Returns health status, response time, and status code
4. Reports `failed` if the app is down

## Step 3: Practical Module — System Info Collector

A module that collects custom system metrics not available in Ansible facts.

Look at `library/system_info.py`.

```bash
# Run the system info playbook
ansible-playbook playbook-sysinfo.yml
```

### What This Module Does
1. Collects disk usage, top processes, and service status
2. Returns structured data as JSON
3. Can be used for monitoring dashboards or alerts

## Step 4: Using Custom Modules as Ad-Hoc Commands

```bash
# Custom modules work with ad-hoc too!
ansible all -m hello -a "name=World"

# Health check ad-hoc
ansible appservers -m app_health -a "url=http://localhost:8080/actuator/health"

# System info ad-hoc
ansible all -m system_info -a "top_n=3"
```

## Step 5: Module Development Tips

### How to debug a module locally

```bash
# Test the module directly with Python (no Ansible needed)
python3 library/hello.py <<EOF
{"ANSIBLE_MODULE_ARGS": {"name": "Debug Test"}}
EOF

# You'll see raw JSON output — this is what Ansible reads
```

### Module argument validation

```python
# Ansible validates arguments for you
argument_spec = dict(
    name=dict(type='str', required=True),           # required string
    state=dict(type='str', default='present',        # with choices
               choices=['present', 'absent']),
    count=dict(type='int', default=1),               # integer with default
    force=dict(type='bool', default=False),           # boolean
)
```

### Return values convention

```python
# Success — no change
module.exit_json(changed=False, msg="Already in desired state")

# Success — something changed
module.exit_json(changed=True, msg="Created resource X")

# Failure
module.fail_json(msg="Cannot connect to API: timeout")
```

---

## Module Anatomy (Template)

```python
#!/usr/bin/python3
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # 1. Define accepted arguments
    module_args = dict(
        name=dict(type='str', required=True),
    )

    # 2. Create module instance
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # 3. Check mode — report what WOULD change without doing it
    if module.check_mode:
        module.exit_json(changed=False)

    # 4. Your logic here
    result = do_something(module.params['name'])

    # 5. Return result
    module.exit_json(changed=True, msg="Done", result=result)

def main():
    run_module()

if __name__ == '__main__':
    main()
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `library/hello.py` | Simple hello world module |
| `library/app_health.py` | HTTP health check module |
| `library/system_info.py` | System metrics collector module |
| `playbook-hello.yml` | Demo playbook for hello module |
| `playbook-health.yml` | Demo playbook for health check module |
| `playbook-sysinfo.yml` | Demo playbook for system info module |
| `ansible.cfg` | Points to shared inventory |

---

## Where to Put Custom Modules

| Location | Scope |
|----------|-------|
| `./library/` | Current playbook directory only (what we do here) |
| `~/.ansible/plugins/modules/` | All playbooks for current user |
| Role: `roles/myrole/library/` | Within a specific role |
| `ansible.cfg: library = /path` | Custom path |

---

## Troubleshooting

### "module hello not found"
- Ensure `library/` directory is in the same directory as the playbook
- Check file has `.py` extension and is executable

### Module returns error but no useful message
```bash
# Run with triple verbose to see full module output
ansible-playbook playbook-hello.yml -vvv
```

### "No module named ansible.module_utils"
- You're running the module directly without the Ansible test harness
- Use the JSON stdin method shown in Step 5

## Key Takeaways
- Custom modules are **Python scripts** that return JSON
- Place them in `library/` next to your playbook
- Use `AnsibleModule` class for argument parsing, check mode, etc.
- `module.exit_json()` = success, `module.fail_json()` = failure
- `changed=True/False` tells Ansible if something changed (idempotency!)
- Test locally with `python3 module.py <<< '{"ANSIBLE_MODULE_ARGS": {...}}'`
