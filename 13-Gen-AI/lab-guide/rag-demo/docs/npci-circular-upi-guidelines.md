# NPCI Circular: UPI Transaction Processing Guidelines
## Circular No: NPCI/UPI/OC-174/2024

### 1. Transaction Processing SLA

- **Payment initiation to completion:** Maximum 30 seconds
- **Deemed approved:** If no response within 30 seconds, transaction is deemed approved by the payer's bank
- **Settlement cycle:** T+1 business day (next business day settlement)
- **Real-time confirmation:** Both payer and payee must receive confirmation within 5 seconds of completion

### 2. Transaction Failure Reporting

- **Threshold:** If transaction failure rate exceeds 0.5% in any 1-hour window
- **Reporting deadline:** Within 24 hours of detection
- **Report to:** NPCI Operations Centre (npci-ops@npci.org.in)
- **Required details:** Failure count, affected time window, root cause, remediation steps

### 3. Downtime Penalties

| Downtime Duration | Penalty |
|-------------------|---------|
| 15-30 minutes | Warning letter |
| 30-60 minutes | Rs 50,000 per incident |
| 1-4 hours | Rs 2,00,000 per incident |
| > 4 hours | Rs 5,00,000 + review hearing |

- Penalties apply per member bank per incident
- Repeated violations (3+ in a quarter) trigger enhanced monitoring

### 4. Refund Timelines

- **Failed transactions:** Auto-refund within T+5 business days
- **Customer-initiated refund:** Process within 48 hours of request
- **Disputed transactions:** Resolution within 30 calendar days
- **Interest on delayed refunds:** RBI repo rate + 2% per annum

### 5. Security Requirements

- **2FA mandatory:** For transactions above Rs 5,000
- **Device binding:** UPI PIN must be entered on registered device
- **Daily transaction limit:** Rs 1,00,000 per VPA per day
- **Cool-off period:** 24 hours for new VPA registration before high-value transactions

### 6. Data Retention

- Transaction records: Minimum 10 years
- Audit logs: Minimum 5 years
- Customer dispute records: 8 years from resolution date
