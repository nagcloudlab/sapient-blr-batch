# Ansible
## Module 30 | Sustain Engineering Training | Day 33

---

## Agenda -- Day 33

| # | Topic |
|---|-------|
| 01 | Why Configuration Management? |
| 02 | Ansible Architecture & Key Concepts |
| 03 | Inventory & Ad-Hoc Commands |
| 04 | Playbooks: Structure & Execution |
| 05 | Modules, Tasks & Handlers |
| 06 | Variables, Facts & Templates |
| 07 | Roles & Galaxy |
| 08 | Lab: Fix FoodExpress Ansible Playbooks |
| 09 | Behavioral Role Play: Incident Escalation |
| 10 | Day 33 Wrap-up |

---

## Why Configuration Management?

### The Problem: Server Snowflakes

```
FoodExpress has 12 servers across dev, staging, prod.

Without config management:
  - Server A has Java 17, Server B has Java 11
  - Someone SSH'd into prod and changed nginx.conf manually
  - "It works on staging but not on prod" -- config drift
  - New server setup takes 2 days of manual work
  - No audit trail of changes
```

Configuration management automates server setup and ensures **consistency** across all environments.

---

## Configuration Management Tools

| Tool | Approach | Agent | Language |
|------|----------|-------|----------|
| **Ansible** | Agentless (SSH) | No agent needed | YAML (Playbooks) |
| Puppet | Agent-based | Agent on each node | Puppet DSL (Ruby) |
| Chef | Agent-based | Agent on each node | Ruby |
| SaltStack | Agent or agentless | Optional minion | YAML/Python |

### Why Ansible?

- **Agentless** -- uses SSH; nothing to install on managed nodes
- **YAML** -- easy to read, no programming required
- **Idempotent** -- running the same playbook twice produces the same result
- **Large module library** -- 3,400+ modules for any task

---

## Ansible Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   CONTROL NODE                           │
│                                                          │
│  ┌─────────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │  Playbooks  │  │ Inventory │  │   ansible.cfg    │  │
│  │  (YAML)     │  │ (hosts)   │  │  (configuration) │  │
│  └──────┬──────┘  └─────┬─────┘  └──────────────────┘  │
│         │               │                                │
│         ▼               ▼                                │
│  ┌────────────────────────────────┐                     │
│  │       Ansible Engine          │                      │
│  │  ┌─────────┐  ┌───────────┐  │                     │
│  │  │ Modules │  │ Plugins   │  │                     │
│  │  └─────────┘  └───────────┘  │                     │
│  └──────────────┬────────────────┘                     │
└─────────────────┼────────────────────────────────────────┘
                  │ SSH
      ┌───────────┼───────────┐
      ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Managed  │ │ Managed  │ │ Managed  │
│ Node 1   │ │ Node 2   │ │ Node 3   │
│ (web)    │ │ (app)    │ │ (db)     │
└──────────┘ └──────────┘ └──────────┘
```

No agents on managed nodes. Ansible pushes configuration over SSH.

---

## Key Concepts

| Concept | Description | FoodExpress Example |
|---------|-------------|---------------------|
| **Control Node** | Machine where Ansible runs | Your laptop or CI/CD server |
| **Managed Node** | Target server being configured | FoodExpress web/app/db servers |
| **Inventory** | List of managed nodes | `web1.foodexpress.in`, `db1.foodexpress.in` |
| **Playbook** | YAML file defining desired state | `deploy-foodexpress.yml` |
| **Task** | Single action (install, copy, restart) | Install nginx, copy config |
| **Module** | Code that performs a task | `apt`, `copy`, `service`, `template` |
| **Handler** | Task triggered by notification | Restart nginx after config change |
| **Role** | Reusable bundle of tasks, files, templates | `nginx` role, `java` role |

---

## Inventory

### Defining your managed nodes

```ini
# inventory/hosts.ini

[webservers]
web1.foodexpress.in
web2.foodexpress.in

[appservers]
app1.foodexpress.in ansible_port=2222
app2.foodexpress.in

[dbservers]
db1.foodexpress.in ansible_user=dbadmin

[foodexpress:children]
webservers
appservers
dbservers

[webservers:vars]
nginx_port=80
max_connections=1024
```

Groups allow targeting subsets: `ansible webservers -m ping`

---

## Ad-Hoc Commands

### Quick one-off tasks without a playbook

```bash
# Ping all hosts
ansible all -m ping -i inventory/hosts.ini

# Check disk space on web servers
ansible webservers -m shell -a "df -h" -i inventory/hosts.ini

# Install a package
ansible appservers -m apt -a "name=openjdk-17-jdk state=present" \
  -i inventory/hosts.ini --become

# Copy a file
ansible webservers -m copy -a "src=nginx.conf dest=/etc/nginx/nginx.conf" \
  -i inventory/hosts.ini --become

# Restart a service
ansible webservers -m service -a "name=nginx state=restarted" \
  -i inventory/hosts.ini --become
```

Ad-hoc is for quick checks. Use playbooks for repeatable automation.

---

## Playbook Structure

### YAML-based automation scripts

```yaml
---
# deploy-foodexpress.yml
- name: Configure FoodExpress web servers
  hosts: webservers
  become: yes                    # Run as root (sudo)

  vars:
    app_port: 8080
    nginx_worker_processes: 4

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Copy nginx configuration
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx      # Trigger handler

    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

---

## Playbook Execution Flow

```
$ ansible-playbook deploy-foodexpress.yml -i inventory/hosts.ini

PLAY [Configure FoodExpress web servers] **********

TASK [Gathering Facts] ****************************
ok: [web1.foodexpress.in]
ok: [web2.foodexpress.in]

TASK [Install nginx] ******************************
changed: [web1.foodexpress.in]
changed: [web2.foodexpress.in]

TASK [Copy nginx configuration] *******************
changed: [web1.foodexpress.in]
changed: [web2.foodexpress.in]

TASK [Ensure nginx is running] ********************
ok: [web1.foodexpress.in]
ok: [web2.foodexpress.in]

RUNNING HANDLER [restart nginx] *******************
changed: [web1.foodexpress.in]
changed: [web2.foodexpress.in]

PLAY RECAP ****************************************
web1.foodexpress.in  : ok=5  changed=3  failed=0
web2.foodexpress.in  : ok=5  changed=3  failed=0
```

---

## Common Ansible Modules

| Module | Purpose | Example |
|--------|---------|---------|
| `apt` / `yum` | Package management | Install Java, nginx |
| `copy` | Copy files to remote | Deploy config files |
| `template` | Copy with Jinja2 templating | Generate nginx.conf from template |
| `service` / `systemd` | Manage services | Start/stop/restart nginx |
| `file` | File/directory management | Create dirs, set permissions |
| `user` | User management | Create application user |
| `git` | Git operations | Clone application repo |
| `docker_container` | Docker management | Run containers |
| `command` / `shell` | Run commands | Custom scripts |
| `lineinfile` | Modify single line in file | Update a config value |

---

## Tasks & Conditionals

### Control task execution

```yaml
tasks:
  - name: Install Java 17 (Debian/Ubuntu)
    apt:
      name: openjdk-17-jdk
      state: present
    when: ansible_os_family == "Debian"

  - name: Install Java 17 (RedHat/CentOS)
    yum:
      name: java-17-openjdk
      state: present
    when: ansible_os_family == "RedHat"

  - name: Deploy FoodExpress JAR
    copy:
      src: "foodexpress-order-service-{{ app_version }}.jar"
      dest: /opt/foodexpress/order-service.jar
      owner: foodexpress
      group: foodexpress
      mode: '0644'
    notify: restart order-service

  - name: Wait for service to start
    uri:
      url: "http://localhost:{{ app_port }}/actuator/health"
      status_code: 200
    retries: 10
    delay: 5
    register: health_check
    until: health_check.status == 200
```

---

## Handlers

### Triggered only when notified; run once at end of play

```yaml
tasks:
  - name: Update nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: restart nginx          # Notify the handler

  - name: Update SSL certificate
    copy:
      src: foodexpress.crt
      dest: /etc/ssl/certs/foodexpress.crt
    notify: restart nginx          # Same handler, runs only once

handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

**Key facts:**
- Handlers run **only if notified** (task changed something)
- Handlers run **once** at the end, even if notified multiple times
- Handler name must **exactly match** the notify string

---

## Variables & Precedence

### Multiple places to define variables

```yaml
# 1. In the playbook
vars:
  app_port: 8080

# 2. In a vars file
vars_files:
  - vars/foodexpress.yml

# 3. In inventory
[appservers:vars]
app_port=8080

# 4. On the command line (highest precedence)
# ansible-playbook deploy.yml -e "app_port=9090"
```

### Variable precedence (lowest to highest):
1. Role defaults
2. Inventory vars
3. Playbook vars
4. Role vars
5. Extra vars (`-e` flag) -- **always wins**

---

## Jinja2 Templates

### Dynamic configuration files

```
# templates/nginx.conf.j2

worker_processes {{ nginx_worker_processes }};

http {
    upstream foodexpress_backend {
        {% for host in groups['appservers'] %}
        server {{ hostvars[host]['ansible_host'] }}:{{ app_port }};
        {% endfor %}
    }

    server {
        listen {{ nginx_port }};
        server_name {{ server_name }};

        location /api/ {
            proxy_pass http://foodexpress_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /health {
            return 200 'OK';
        }
    }
}
```

Templates use **Jinja2** syntax: `{{ variable }}`, `{% for %}`, `{% if %}`.

---

## Ansible Facts

### Auto-discovered system information

```bash
$ ansible web1.foodexpress.in -m setup | head -30

"ansible_facts": {
    "ansible_os_family": "Debian",
    "ansible_distribution": "Ubuntu",
    "ansible_distribution_version": "22.04",
    "ansible_processor_cores": 4,
    "ansible_memtotal_mb": 8192,
    "ansible_hostname": "web1",
    "ansible_default_ipv4": {
        "address": "10.0.1.10"
    }
}
```

Use facts in playbooks: `{{ ansible_memtotal_mb }}`, `{{ ansible_os_family }}`

---

## Roles: Reusable Automation

### Standard directory structure

```
roles/
  foodexpress-app/
    tasks/
      main.yml          # Task list
    handlers/
      main.yml          # Handlers
    templates/
      app.service.j2    # Systemd service file
      application.yml.j2 # Spring Boot config
    files/
      foodexpress.jar   # Static files
    vars/
      main.yml          # Role variables
    defaults/
      main.yml          # Default values (lowest precedence)
    meta/
      main.yml          # Dependencies
```

```yaml
# Use the role in a playbook
- hosts: appservers
  become: yes
  roles:
    - common
    - java
    - foodexpress-app
```

---

## Ansible Galaxy

### Community roles & collections

```bash
# Install a role from Galaxy
ansible-galaxy install geerlingguy.docker

# Install a collection
ansible-galaxy collection install community.docker

# Create a new role skeleton
ansible-galaxy init foodexpress-app
```

### Popular Galaxy roles for FoodExpress:
- `geerlingguy.docker` -- Install Docker
- `geerlingguy.java` -- Install Java
- `geerlingguy.nginx` -- Configure nginx
- `geerlingguy.mysql` -- Set up MySQL

---

## Idempotency

### Running playbooks multiple times is safe

```
First run:
TASK [Install nginx]           changed    ← installed
TASK [Copy config]             changed    ← file copied
TASK [Start nginx]             changed    ← started

Second run (nothing changed):
TASK [Install nginx]           ok         ← already installed
TASK [Copy config]             ok         ← file unchanged
TASK [Start nginx]             ok         ← already running

Third run (config file updated):
TASK [Install nginx]           ok         ← already installed
TASK [Copy config]             changed    ← new config copied
TASK [Start nginx]             ok         ← already running
HANDLER [restart nginx]        changed    ← restarted (notified)
```

**Avoid:** `command` and `shell` modules are NOT idempotent by default. Use `creates` parameter.

---

## Ansible Vault

### Encrypt sensitive data

```bash
# Create an encrypted file
ansible-vault create secrets.yml

# Edit an encrypted file
ansible-vault edit secrets.yml

# Encrypt an existing file
ansible-vault encrypt vars/passwords.yml

# Run playbook with vault password
ansible-playbook deploy.yml --ask-vault-pass
```

```yaml
# secrets.yml (encrypted at rest, decrypted at runtime)
db_password: "Pr0d_P@ssw0rd_2026!"
jwt_secret: "mySecretKey123"
api_keys:
  payment_gateway: "pk_live_xyz123"
```

---

## Behavioral Role Play: Incident Escalation

### Scenario

You are a sustain engineer on the FoodExpress night shift. At 2:00 AM, you receive an alert: "Order Service DOWN on all app servers." You have Ansible playbooks for deployment and rollback.

### Roles
- **Sustain Engineer** (you): Diagnose, decide, and act
- **On-Call Manager** (trainer): Available for escalation decisions
- **Client Stakeholder** (trainer): Wants status updates

### Discussion Points
1. What Ansible ad-hoc commands would you run first to diagnose?
2. When do you escalate vs. fix yourself?
3. How do you communicate status to the client?
4. When do you decide to rollback vs. fix forward?
5. How do you write the post-incident report?

---

## Behavioral Role Play: Rubric

| Dimension | Exceeds | Meets | Below |
|-----------|---------|-------|-------|
| **Diagnosis** | Uses systematic approach: check service status, logs, recent changes | Checks basics but misses some steps | Jumps to conclusions without data |
| **Escalation** | Escalates appropriately with clear context | Escalates but missing key information | Either escalates too early or too late |
| **Communication** | Proactive updates with ETA and impact | Responds when asked, accurate updates | Vague updates, no ETA |
| **Decision Making** | Weighs rollback vs fix with data, chooses correctly | Makes reasonable choice with some analysis | Makes impulsive decision without analysis |
| **Documentation** | Writes clear post-incident with timeline and action items | Documents basics but misses root cause | No documentation |

---

## Lab: Fix FoodExpress Ansible Playbooks

### Scenario

FoodExpress deployment playbooks have bugs causing:
- Playbook fails with "MODULE FAILURE" errors
- Tasks run without sudo (permission denied on apt install)
- Variables not rendering in templates
- Services not restarting after config changes

### Files to fix:
1. `deploy-foodexpress.yml` -- 4 bugs
2. `inventory/hosts.ini` -- 2 bugs
3. `templates/nginx.conf.j2` -- 2 bugs

See `Labs/lab-exercises.md` for detailed bug list.

---

## Ansible Best Practices

| Practice | Why |
|----------|-----|
| Use `state: present` not `state: latest` | Predictable, idempotent installs |
| Always use `become: yes` for system tasks | Explicit privilege escalation |
| Use `template` over `copy` for config files | Dynamic configuration |
| Use Ansible Vault for secrets | Never commit plaintext passwords |
| Use roles for reusable automation | DRY principle, Galaxy sharing |
| Name every task | Readable output, easier debugging |
| Test with `--check --diff` | Dry run before applying |
| Use `block/rescue/always` for error handling | Graceful failure handling |

---

## Key Takeaways

| Concept | Key Point |
|---------|-----------|
| Agentless | Ansible uses SSH; no software needed on managed nodes |
| Inventory | Defines hosts and groups; supports variables per group |
| Playbook | YAML file declaring desired state; runs top to bottom |
| Module | Pre-built code for a specific task (apt, copy, template, service) |
| Handler | Runs only when notified; triggers once at end of play |
| Variables | Multiple sources; extra vars (`-e`) always win |
| Templates | Jinja2 templating for dynamic config files |
| Idempotency | Running playbooks multiple times is safe; same result every time |

> **Next:** Module 31 -- DevOps Capsule Project (Docker + K8s + Jenkins + Ansible + Git)
