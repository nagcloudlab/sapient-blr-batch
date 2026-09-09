# Lab 13 - Full End-to-End Deployment (Expert)

## Objective
Complete production-like deployment with rolling updates, health checks, and optimization

## Prerequisites
- All previous labs completed (this is the capstone lab)
- Lab 06 JAR built (`../lab-06-springboot-playbook/app/target/hello-api-1.0.0.jar` must exist)
- Update `<VM2_IP>` in `deploy.yml` and `<YOUR_GCP_USERNAME>` in `ansible.cfg`
- Run all commands from this lab directory (`cd lab-13-full-deployment`)

---

## What We'll Cover
- **Rolling deployments** — update one server at a time
- **Health checks** — verify app is healthy before proceeding
- **Serial execution** — control parallelism
- **Async tasks** — don't wait for slow tasks
- **Pre/Post tasks** — run tasks before/after roles
- **Delegation** — run a task on a different host
- **Full pipeline** — deploy Spring Boot update via NGINX reverse proxy

## Rolling Deployment Strategy
```
Without rolling:  ALL servers down → update → ALL servers up (DOWNTIME!)
With rolling:     Server1 down → update → up → Server2 down → update → up (ZERO DOWNTIME)
```

---

## Step 1: Run the Full Deployment

```bash
# Deploy everything
ansible-playbook deploy.yml --ask-vault-pass

# Deploy only the app (skip NGINX)
ansible-playbook deploy.yml --tags app --ask-vault-pass

# Deploy with verbose output
ansible-playbook deploy.yml --ask-vault-pass -v
```

## Step 2: Simulate a Rolling Update

```bash
# Run the rolling update playbook
ansible-playbook rolling-update.yml
```

## Step 3: Check Deployment Status

```bash
# Verify both services are running
ansible-playbook health-check.yml

# Quick ad-hoc check
ansible webservers -m uri -a "url=http://localhost/health return_content=yes"
ansible appservers -m shell -a "curl -s http://localhost:8080/actuator/health"
```

## Step 4: Optimization Techniques

```bash
# Time a playbook run
time ansible-playbook deploy.yml --ask-vault-pass

# Run with pipelining enabled (faster SSH)
ANSIBLE_PIPELINING=true ansible-playbook deploy.yml --ask-vault-pass

# Run with increased parallelism
ansible-playbook deploy.yml --ask-vault-pass -f 10
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `deploy.yml` | Full deployment playbook |
| `rolling-update.yml` | Rolling update demo |
| `health-check.yml` | Health check playbook |
| `ansible.cfg` | Optimized configuration |
| `group_vars/all.yml` | Shared variables |

---

## Production Best Practices Checklist
- [ ] Use roles for organization
- [ ] Use vault for secrets
- [ ] Use dynamic inventory for cloud
- [ ] Implement health checks
- [ ] Use rolling deployments (serial)
- [ ] Enable pipelining for speed
- [ ] Use tags for selective deployment
- [ ] Use `--check` before real runs
- [ ] Version your playbooks in Git
- [ ] Use CI/CD to trigger Ansible (Jenkins, GitHub Actions)

---

## Key Takeaways
- `serial: 1` = rolling deployment (one host at a time)
- `max_fail_percentage` = stop if too many hosts fail
- `pre_tasks` / `post_tasks` = run before/after roles
- `delegate_to` = run a task on a different host
- `async` + `poll` = non-blocking tasks
- `wait_for` = wait until a port/URL is available
- Combine all techniques for production-grade deployments
