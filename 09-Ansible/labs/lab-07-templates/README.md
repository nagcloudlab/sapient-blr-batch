# Lab 07 - Templates (Jinja2)

## Objective
Use Jinja2 templates to dynamically generate NGINX reverse proxy config

## Prerequisites
- Lab 05 completed (NGINX installed on VM1)
- Lab 06 completed (Spring Boot running on VM2)
- Update `backend_host` in `reverse-proxy.yml` with VM2's external IP

---

## What are Templates?
- Files with **dynamic placeholders** → `{{ variable_name }}`
- Uses **Jinja2** templating engine (Python)
- `.j2` extension by convention
- Rendered on the **control node**, result pushed to managed node

## Why Templates?
- `copy` module = static files (same content everywhere)
- `template` module = dynamic files (content varies per host/variable)
- Real-world example: NGINX config needs the **Spring Boot VM's IP**

## Jinja2 Syntax Quick Reference
```jinja2
{{ variable }}              # Variable substitution
{{ ansible_hostname }}      # Use Ansible facts
{% if condition %}          # Conditional
{% endif %}
{% for item in list %}      # Loop
{% endfor %}
{# This is a comment #}    # Comment (not in output)
```

---

## Step 1: Run the Template Playbook

```bash
# Update the backend_host variable in the playbook with VM2's IP first!
ansible-playbook reverse-proxy.yml
```

## Step 2: Verify Reverse Proxy

```bash
# Hit NGINX (VM1) — it should proxy to Spring Boot (VM2)
curl http://<VM1_IP>
curl http://<VM1_IP>/api

# Direct Spring Boot access still works
curl http://<VM2_IP>:8080
```

## Step 3: Check Generated Config on VM1

```bash
ansible webservers -m shell -a "cat /etc/nginx/sites-available/default"

# You'll see VM2's actual IP in the proxy_pass line!
```

## Step 4: Change a Variable and Re-run

```bash
# Change max_body_size or worker_connections in the playbook
# Then re-run — only the changed parts trigger handlers
ansible-playbook reverse-proxy.yml
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `reverse-proxy.yml` | Playbook that uses templates |
| `templates/nginx-proxy.conf.j2` | Jinja2 template for NGINX reverse proxy |
| `templates/app-config.j2` | Jinja2 template for Spring Boot config |

---

## Key Takeaways
- `template` module = dynamic file generation
- `copy` module = static files
- `{{ }}` for variables, `{% %}` for logic
- Ansible facts (like `ansible_default_ipv4.address`) are auto-available
- Templates are rendered locally, then pushed to remote
- Next: Deep dive into **variables and facts**
