# Runbook: UPI Payment Service 503 Errors

## Alert
- **Name:** UPI-PAY-503
- **Trigger:** 5xx error rate > 5% for 5 minutes
- **Severity:** P1
- **Dashboard:** http://grafana.internal/d/upi-payments

## Quick Diagnosis (first 5 minutes)

1. Check pod status:
   ```
   kubectl get pods -n upi-prod -l app=upi-service
   ```
2. Check recent deployments:
   ```
   kubectl rollout history deploy/upi-service -n upi-prod
   ```
3. Check database connectivity:
   ```
   kubectl exec -it upi-service-xxx -n upi-prod -- node -e "require('./db')"
   ```
4. Check memory and CPU:
   ```
   kubectl top pods -n upi-prod -l app=upi-service
   ```

## Common Causes

| Cause | How to confirm | Fix |
|-------|---------------|-----|
| SQLite lock contention | SQLITE_BUSY in logs | Scale down to 1 replica |
| Memory exhaustion (OOM) | OOMKilled in pod events | Increase memory limits |
| Bad deployment | Recent rollout in history | `kubectl rollout undo deploy/upi-service` |
| Database file corruption | SQLITE_CORRUPT in logs | Restore from backup volume |
| Connection spike | High concurrent request count | Enable rate limiting |

## Escalation

- **First 15 min:** On-call SRE (check PagerDuty schedule)
- **After 15 min:** Engineering Lead -- Nag (+91-XXXXXXXXXX)
- **After 30 min:** VP Engineering + Client notification
- **NPCI reporting:** Required within 24 hours if >100 transactions affected

## Post-Incident

- [ ] Incident record in ServiceNow
- [ ] Post-mortem within 48 hours
- [ ] Action items assigned with owners and due dates
