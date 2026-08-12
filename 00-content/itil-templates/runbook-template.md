# Runbook: [Procedure Title]

**Runbook ID:** RB-NNN
**Service:** [e.g., Order Service / Restaurant Service / Cart Service]
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Owner:** [Team or Name]

---

## When to Use This Runbook

Describe the specific condition that triggers use of this runbook. Be precise so an on-call engineer can quickly determine whether this is the right document.

Examples:
- The Order Service (port 8080) is returning HTTP 503 and the Grafana alert `order-service-down` has fired.
- The Restaurant Service (port 3000) response time exceeds 2 seconds for more than 3 consecutive minutes.
- The Cart Service (port 3001) is returning NaN totals and customer complaints have been received.
- The Delivery Service (port 3002) has stopped publishing location updates to the frontend.

---

## Prerequisites

Before starting, confirm you have the following:

- [ ] SSH access to the production server (or kubectl access if running on Kubernetes)
- [ ] Read access to application logs (Loki / CloudWatch / journalctl)
- [ ] Access to the Grafana dashboard: FoodExpress -- Service Health
- [ ] Jira access to create or update an incident ticket
- [ ] On-call contact list (Slack: #foodexpress-oncall)
- [ ] Service port reference:
  - Frontend: port 80
  - Restaurant Service: port 3000
  - Cart Service: port 3001
  - Order Service: port 8080
  - Delivery Service: port 3002
  - Payment Service: port 3003

---

## Step 1 -- Verify the Problem

Confirm the incident is real and characterise its scope before taking any action.

1. Check the Grafana dashboard for the affected service. Note the error rate, latency, and saturation metrics.
2. Verify the service is actually down or degraded:
   ```
   curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT>/health
   ```
   Expected: `200`. Anything else confirms the issue.
3. Check recent deployments: was anything released in the last 60 minutes?
4. Check whether dependent services are healthy (e.g., if the Order Service is failing, is MySQL reachable?).
5. Record your findings. Open or update an incident ticket in Jira.

---

## Step 2 -- Mitigate (Stop the Bleeding)

If customers are actively impacted, apply a mitigation to limit harm while you investigate.

Options (choose the appropriate one):

- **Restart the service** (fast, low risk for stateless Node.js services):
  ```
  pm2 restart <service-name>
  # or
  systemctl restart foodexpress-<service-name>
  ```
- **Roll back to the previous deployment** (if a recent release is suspected):
  ```
  # Example for a Node.js service managed by PM2
  git checkout <previous-tag>
  npm install --production
  pm2 restart <service-name>
  ```
- **Enable maintenance mode** (if the UI can display a friendly message):
  Update the frontend config to show a "We'll be back soon" banner.
- **Scale horizontally** (if the issue is load-related and infrastructure supports it):
  Add additional instances behind the load balancer.

Document the mitigation applied in the incident ticket before moving to investigation.

---

## Step 3 -- Investigate

Identify the root cause. Work methodically; avoid guessing.

**Check application logs:**
```
# PM2-managed service
pm2 logs <service-name> --lines 200

# systemd-managed service
journalctl -u foodexpress-<service-name> -n 200 --no-pager

# Docker container
docker logs <container-name> --tail 200
```

**Check database connectivity (MySQL -- Order Service):**
```
mysql -h <host> -u <user> -p -e "SHOW STATUS LIKE 'Threads_connected';"
mysql -h <host> -u <user> -p -e "SHOW PROCESSLIST;"
```

**Check database connectivity (MongoDB -- Restaurant/Cart/Delivery/Payment Services):**
```
mongosh --eval "db.adminCommand({ serverStatus: 1 }).connections"
```

**Check OS-level resource usage:**
```
top -b -n 1
df -h
free -m
```

**Check network and port availability:**
```
ss -tlnp | grep <PORT>
curl -v http://localhost:<PORT>/health
```

Record the root cause hypothesis in the incident ticket once identified.

---

## Step 4 -- Resolve

Apply the permanent fix once the root cause is confirmed.

- If the cause is a **code defect**: raise a Jira bug ticket; apply a hotfix following the Change Request process (see `change-request.md`).
- If the cause is a **configuration error**: correct the configuration, restart the service, and verify.
- If the cause is a **resource exhaustion** (disk, memory, connections): free the resource and add an alert to detect it earlier next time.
- If the cause is an **external dependency** (payment gateway, SMS provider): follow the third-party escalation contacts listed in the escalation section below.

Do not close the incident ticket until Step 5 is complete.

---

## Step 5 -- Verify Recovery

Confirm the service is fully healthy before standing down.

1. Health check returns 200:
   ```
   curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT>/health
   ```
2. Grafana dashboard shows error rate back at baseline (below 0.1%).
3. Grafana dashboard shows latency back within SLO thresholds.
4. Run a basic smoke test against the affected endpoint(s).
5. Confirm no new errors appearing in logs for at least 5 minutes.
6. Notify stakeholders that the service is restored (Slack: #foodexpress-oncall).

---

## Step 6 -- Document

Complete documentation before closing the incident.

1. Update the incident ticket in Jira with:
   - Confirmed root cause
   - Resolution steps taken
   - Time of recovery
2. If this incident took more than 30 minutes or was P1/P2, schedule a post-mortem using the `post-mortem.md` template.
3. If this runbook was missing a step or was unclear, update it now while the context is fresh.
4. Add any new monitoring gaps to the team backlog.

---

## Escalation

If you are unable to resolve the incident within 30 minutes, escalate:

| Situation                              | Escalate To                              | Contact                     |
|----------------------------------------|------------------------------------------|-----------------------------|
| MySQL down or corrupted                | DBA / Database team                      | [Contact details]           |
| Payment gateway errors                 | Payment provider support                 | [Support URL / phone]       |
| Infrastructure / VM / network failure  | Infrastructure / Cloud team              | [Contact details]           |
| Security concern (breach, data leak)   | Security team + Management               | [Contact details]           |
| Client escalation required             | Engagement Manager / Account Lead        | [Contact details]           |

Do not escalate without first capturing your findings from Steps 1-3 in the incident ticket.

---

## Related Links

- FoodExpress Architecture: `training-content/FoodExpress/architecture.md`
- Incident Report Template: `training-content/itil-templates/incident-report.md`
- Change Request Template: `training-content/itil-templates/change-request.md`
- Post-Mortem Template: `training-content/itil-templates/post-mortem.md`
- Grafana Dashboard: [URL]
- Jira Project: [URL]
- On-Call Rotation: [URL]
