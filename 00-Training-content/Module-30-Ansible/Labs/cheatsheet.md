# Ansible Quick Reference

> Single-page reference for Ansible ad-hoc commands, playbooks, common modules, and project structure. Replace `<inventory>`, `<host-pattern>`, `<playbook>` with actual values.

---

## Ad-hoc Commands

| Command | Example | Description |
|---|---|---|
| `ansible <hosts> -i <inv> -m <module>` | `ansible all -i inventory.ini -m ping` | Run module against hosts |
| `ansible <hosts> -i <inv> -m shell -a "cmd"` | `ansible webservers -i inventory.ini -m shell -a "uptime"` | Run shell command |
| `ansible <hosts> -i <inv> -m command -a "cmd"` | `ansible all -i inventory.ini -m command -a "df -h"` | Run command (no shell expansion) |
| `ansible <hosts> -m setup` | `ansible web1 -i inventory.ini -m setup` | Gather all facts from host |
| `ansible <hosts> -m setup -a "filter=ansible_distribution*"` | `ansible all -i inventory.ini -m setup -a "filter=ansible_distribution*"` | Gather specific facts |
| `ansible <hosts> -m copy -a "src=f dest=d"` | `ansible all -i inventory.ini -m copy -a "src=app.conf dest=/etc/app.conf"` | Copy file to hosts |
| `ansible <hosts> -m service -a "name=nginx state=started"` | `ansible webservers -i inventory.ini -m service -a "name=nginx state=started"` | Manage a service |
| `ansible <hosts> -m apt -a "name=pkg state=present" --become` | `ansible all -i inventory.ini -m apt -a "name=curl state=present" --become` | Install package (Debian/Ubuntu) |
| `ansible <hosts> -b -K` | `ansible all -i inventory.ini -m ping -b -K` | Run with become (sudo), prompt for password |
| `ansible-playbook <pb> -i <inv>` | `ansible-playbook site.yml -i inventory.ini` | Run a playbook |
| `ansible-playbook <pb> --check` | `ansible-playbook site.yml -i inventory.ini --check` | Dry run (no changes applied) |
| `ansible-playbook <pb> --diff` | `ansible-playbook site.yml -i inventory.ini --diff` | Show file diffs for changes |
| `ansible-playbook <pb> -v / -vvv` | `ansible-playbook site.yml -i inventory.ini -vvv` | Verbose output (more v = more detail) |
| `ansible-playbook <pb> --tags <tag>` | `ansible-playbook site.yml -i inventory.ini --tags deploy` | Run only tagged tasks |
| `ansible-playbook <pb> --skip-tags <tag>` | `ansible-playbook site.yml -i inventory.ini --skip-tags cleanup` | Skip tagged tasks |
| `ansible-playbook <pb> --limit <hosts>` | `ansible-playbook site.yml -i inventory.ini --limit webservers` | Limit to host group |
| `ansible-playbook <pb> -e "key=value"` | `ansible-playbook site.yml -e "app_version=1.2"` | Pass extra variable |
| `ansible-inventory -i <inv> --list` | `ansible-inventory -i inventory.ini --list` | Show parsed inventory as JSON |
| `ansible-inventory -i <inv> --graph` | `ansible-inventory -i inventory.ini --graph` | Show inventory tree |

---

## Inventory File Format

**INI format (`inventory.ini`):**
```ini
# Ungrouped hosts
server1.example.com
192.168.1.100

[webservers]
web1.foodexpress.com
web2.foodexpress.com ansible_user=deploy

[dbservers]
db1.foodexpress.com ansible_port=2222

[appservers:children]
webservers
dbservers

[webservers:vars]
ansible_user=ubuntu
ansible_python_interpreter=/usr/bin/python3
http_port=80

[all:vars]
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

**YAML format (`inventory.yml`):**
```yaml
all:
  vars:
    ansible_user: ubuntu
  children:
    webservers:
      hosts:
        web1.foodexpress.com:
          http_port: 80
        web2.foodexpress.com:
          http_port: 8080
    dbservers:
      hosts:
        db1.foodexpress.com:
          ansible_port: 2222
```

**Common connection variables:**

| Variable | Description |
|---|---|
| `ansible_host` | IP or hostname to connect to |
| `ansible_user` | SSH username |
| `ansible_port` | SSH port (default 22) |
| `ansible_ssh_private_key_file` | Path to private key |
| `ansible_become` | Enable privilege escalation |
| `ansible_become_user` | User to become (default root) |
| `ansible_python_interpreter` | Python path on remote host |

---

## Playbook Structure

```yaml
---
- name: Deploy FoodExpress API
  hosts: webservers          # target hosts or group
  become: yes                # run tasks as sudo
  gather_facts: yes          # collect host facts (default: yes)

  vars:
    app_name: foodexpress-api
    app_version: "1.2.0"
    app_port: 3000
    app_dir: /opt/foodexpress

  vars_files:
    - vars/common.yml
    - vars/secrets.yml

  pre_tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

  tasks:
    - name: Ensure app directory exists
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: deploy
        group: deploy
        mode: "0755"

    - name: Copy application config
      template:
        src: app.conf.j2
        dest: "{{ app_dir }}/app.conf"
        owner: deploy
        mode: "0644"
      notify: Restart app service

    - name: Pull latest Docker image
      docker_image:
        name: "foodexpress-api:{{ app_version }}"
        source: pull

  post_tasks:
    - name: Verify service is running
      uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200

  handlers:
    - name: Restart app service
      service:
        name: "{{ app_name }}"
        state: restarted
```

---

## Common Modules

### Package Management

| Module | Example | Description |
|---|---|---|
| `apt` | `apt: name=nginx state=present update_cache=yes` | Install/remove package (Debian/Ubuntu) |
| `apt` | `apt: name=nginx state=absent` | Remove package |
| `apt` | `apt: upgrade=dist` | Upgrade all packages |
| `yum` | `yum: name=httpd state=present` | Install/remove package (RHEL/CentOS) |
| `dnf` | `dnf: name=httpd state=latest` | Install/remove package (Fedora/RHEL 8+) |

### File Operations

| Module | Example | Description |
|---|---|---|
| `copy` | `copy: src=app.conf dest=/etc/app.conf owner=root mode=0644` | Copy file from controller to host |
| `template` | `template: src=nginx.conf.j2 dest=/etc/nginx/nginx.conf` | Copy Jinja2 template, render vars |
| `file` | `file: path=/opt/app state=directory mode=0755` | Manage files, dirs, symlinks |
| `file` | `file: path=/opt/app/old.log state=absent` | Remove a file |
| `file` | `file: src=/opt/app/current path=/opt/app/live state=link` | Create symlink |
| `fetch` | `fetch: src=/var/log/app.log dest=./logs/` | Fetch file from remote to controller |
| `lineinfile` | `lineinfile: path=/etc/hosts line="192.168.1.1 db.internal"` | Ensure a line exists in a file |
| `blockinfile` | `blockinfile: path=/etc/nginx/conf.d/app.conf block="..."` | Manage a block of lines in a file |

### Services

| Module | Example | Description |
|---|---|---|
| `service` | `service: name=nginx state=started enabled=yes` | Start and enable service |
| `service` | `service: name=nginx state=restarted` | Restart service |
| `service` | `service: name=nginx state=stopped` | Stop service |
| `systemd` | `systemd: name=nginx state=restarted daemon_reload=yes` | systemd-aware service management |

### Shell and Commands

| Module | Example | Description |
|---|---|---|
| `command` | `command: /usr/bin/app --version` | Run command (no shell; preferred for safety) |
| `shell` | `shell: echo $HOME > /tmp/home.txt` | Run via shell (supports pipes, variables) |
| `raw` | `raw: apt-get install -y python3` | Send raw SSH command (no Python needed) |
| `script` | `script: scripts/setup.sh` | Run local script on remote host |

### Source Control

| Module | Example | Description |
|---|---|---|
| `git` | `git: repo=https://github.com/org/foodexpress.git dest=/opt/foodexpress version=main` | Clone or pull git repo |

### Docker

| Module | Example | Description |
|---|---|---|
| `docker_image` | `docker_image: name=foodexpress-api:1.0 source=pull` | Pull Docker image |
| `docker_container` | `docker_container: name=fe-api image=foodexpress-api:1.0 state=started ports=["3000:3000"]` | Manage container lifecycle |
| `docker_container` | `docker_container: name=fe-api state=stopped` | Stop container |
| `docker_container` | `docker_container: name=fe-api state=absent` | Remove container |
| `docker_network` | `docker_network: name=fe-network state=present` | Create Docker network |

### Users and Groups

| Module | Example | Description |
|---|---|---|
| `user` | `user: name=deploy shell=/bin/bash groups=docker append=yes` | Create or modify user |
| `group` | `group: name=deploy state=present` | Create group |
| `authorized_key` | `authorized_key: user=deploy key="{{ lookup('file', '~/.ssh/id_rsa.pub') }}"` | Add SSH public key |

---

## Variables and Facts

**Variable precedence (lowest to highest):**
1. Role defaults (`roles/role/defaults/main.yml`)
2. Inventory group vars
3. Inventory host vars
4. Playbook `vars:`
5. `vars_files:` files
6. Task `vars:` (block/task level)
7. Extra vars (`-e` on command line) -- highest priority

**Using variables:**
```yaml
vars:
  app_port: 3000
  db_host: "db.foodexpress.internal"

tasks:
  - name: Configure app
    template:
      src: app.conf.j2
      dest: /etc/app.conf
    # In template: {{ app_port }}, {{ db_host }}
```

**Common facts (from `gather_facts: yes`):**

| Fact | Description |
|---|---|
| `ansible_hostname` | Short hostname |
| `ansible_fqdn` | Fully qualified domain name |
| `ansible_distribution` | OS name (Ubuntu, CentOS, etc.) |
| `ansible_distribution_version` | OS version |
| `ansible_os_family` | Debian, RedHat, etc. |
| `ansible_default_ipv4.address` | Primary IP address |
| `ansible_memtotal_mb` | Total RAM in MB |
| `ansible_processor_vcpus` | Number of vCPUs |

**Register and use task output:**
```yaml
- name: Check app version
  command: /opt/app/bin/app --version
  register: app_version_output

- name: Show version
  debug:
    msg: "App version: {{ app_version_output.stdout }}"

- name: Continue only if version matches
  fail:
    msg: "Wrong version"
  when: "'1.2' not in app_version_output.stdout"
```

---

## Handlers

Handlers run once at the end of a play, only if notified. They do not run if no task that notified them changed.

```yaml
tasks:
  - name: Update nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify:
      - Reload nginx
      - Send alert

handlers:
  - name: Reload nginx
    service:
      name: nginx
      state: reloaded

  - name: Send alert
    mail:
      to: ops@foodexpress.com
      subject: "nginx config updated on {{ inventory_hostname }}"
      body: "Config reloaded at {{ ansible_date_time.iso8601 }}"
```

**Force handler execution immediately:**
```yaml
- name: Run handlers now
  meta: flush_handlers
```

---

## Roles Directory Structure

```
roles/
  foodexpress-api/
    defaults/
      main.yml          # Default variable values (lowest precedence)
    vars/
      main.yml          # Role variables (higher precedence than defaults)
    tasks/
      main.yml          # Main task list (entry point)
      install.yml       # Imported task file
      configure.yml     # Imported task file
    handlers/
      main.yml          # Role handlers
    templates/
      app.conf.j2       # Jinja2 templates
      nginx.conf.j2
    files/
      startup.sh        # Static files to copy
    meta/
      main.yml          # Role metadata, dependencies
    README.md           # Role documentation
```

**Using a role in a playbook:**
```yaml
- name: Deploy FoodExpress
  hosts: webservers
  roles:
    - role: foodexpress-api
      vars:
        app_version: "1.2.0"
    - common
    - nginx
```

**Install roles from Ansible Galaxy:**
```bash
ansible-galaxy install geerlingguy.docker
ansible-galaxy install -r requirements.yml
ansible-galaxy role list
```

**`requirements.yml`:**
```yaml
roles:
  - name: geerlingguy.docker
    version: "6.1.0"
  - src: https://github.com/org/ansible-role-foodexpress.git
    name: foodexpress-api
    version: main
```

---

## ansible-vault

| Command | Example | Description |
|---|---|---|
| `ansible-vault create <file>` | `ansible-vault create vars/secrets.yml` | Create new encrypted file |
| `ansible-vault edit <file>` | `ansible-vault edit vars/secrets.yml` | Edit encrypted file |
| `ansible-vault view <file>` | `ansible-vault view vars/secrets.yml` | View encrypted file (decrypted) |
| `ansible-vault encrypt <file>` | `ansible-vault encrypt vars/prod.yml` | Encrypt an existing file |
| `ansible-vault decrypt <file>` | `ansible-vault decrypt vars/prod.yml` | Decrypt file in-place |
| `ansible-vault encrypt_string 'value' --name 'var'` | `ansible-vault encrypt_string 'db_pass_123' --name 'db_password'` | Encrypt a single string value |
| `ansible-vault rekey <file>` | `ansible-vault rekey vars/secrets.yml` | Change vault password |

**Run playbook with vault:**
```bash
# Prompt for vault password
ansible-playbook site.yml -i inventory.ini --ask-vault-pass

# Use password file (do not commit to version control)
ansible-playbook site.yml -i inventory.ini --vault-password-file ~/.vault_pass

# Use environment variable
ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass ansible-playbook site.yml
```

**Encrypted vars file example (`vars/secrets.yml`):**
```yaml
# Plain form before encryption:
db_password: "super_secret_pass"
api_secret_key: "jwt_signing_key_here"
registry_token: "docker_registry_token"
```

---

## Conditionals and Loops

**Conditionals:**
```yaml
- name: Install on Debian only
  apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"

- name: Only run if var is set
  command: /opt/app/migrate.sh
  when: run_migrations is defined and run_migrations | bool
```

**Loops:**
```yaml
- name: Install required packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - curl
    - git
    - nodejs
    - npm

- name: Create app directories
  file:
    path: "{{ item }}"
    state: directory
    mode: "0755"
  loop:
    - /opt/foodexpress/logs
    - /opt/foodexpress/data
    - /opt/foodexpress/config
```

---

*FoodExpress Training | Module 30: Ansible | Publicis Sapient Sustain Eng 2026*
