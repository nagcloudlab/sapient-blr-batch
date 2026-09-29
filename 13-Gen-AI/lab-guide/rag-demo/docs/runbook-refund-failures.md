# Runbook: UPI Refund Processing Failures

## Alert
- **Name:** UPI-REFUND-FAIL
- **Trigger:** Refund failure rate > 10% for 10 minutes
- **Severity:** P2
- **Dashboard:** http://grafana.internal/d/upi-refunds

## Quick Diagnosis

1. Check refund endpoint health:
   ```
   curl -s http://upi-service:3000/api/balance/test@upi
   ```
2. Check for double-refund attempts in logs:
   ```
   kubectl logs -n upi-prod -l app=upi-service --since=15m | grep "Cannot refund"
   ```
3. Check payee balance (insufficient balance for refund):
   ```
   kubectl exec -it upi-service-xxx -n upi-prod -- \
     node -e "const db=require('./db'); console.log(db.prepare('SELECT * FROM accounts WHERE balance < 100').all())"
   ```

## Common Causes

| Cause | How to confirm | Fix |
|-------|---------------|-----|
| Double refund attempt | "Cannot refund transaction with status: REFUNDED" in logs | No action -- expected behavior |
| Payee insufficient balance | Payee balance < refund amount | Manual settlement required |
| Transaction still processing | Status = PENDING or PROCESSING | Wait for settlement, retry |
| Database lock during refund | SQLITE_BUSY on refund write | Retry with exponential backoff |

## SLA
- Refund processing: must complete within 48 hours per NPCI guidelines
- Auto-refund for failed transactions: must process within 24 hours

## Escalation
- **P2:** On-call SRE handles
- **If >50 refunds stuck:** Escalate to P1, notify Engineering Lead
