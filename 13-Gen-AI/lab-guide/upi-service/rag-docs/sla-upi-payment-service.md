# SLA: UPI Payment Service

## Service Level Agreement

### Availability
- **Target:** 99.95% uptime per month
- **Measurement:** Based on successful transaction processing rate
- **Excluded:** Scheduled maintenance windows (max 4 hours/month, announced 72 hours prior)

### Performance
- **P50 latency:** < 500ms
- **P95 latency:** < 2,000ms
- **P99 latency:** < 5,000ms
- **Transaction throughput:** Minimum 500 TPS sustained

### Incident Response

| Severity | Response Time | Resolution Target |
|----------|--------------|-------------------|
| P1 (Critical) | 15 minutes | 1 hour |
| P2 (High) | 30 minutes | 4 hours |
| P3 (Medium) | 2 hours | 24 hours |
| P4 (Low) | 8 hours | 5 business days |

### Breach Penalties
- **Availability < 99.95%:** 5% service credit
- **Availability < 99.9%:** 10% service credit
- **Availability < 99.5%:** 25% service credit + mandatory review
- **P1 resolution > 2 hours:** Rs 1,00,000 penalty per incident

### Reporting
- Monthly SLA report due by 5th of following month
- Quarterly review meeting with stakeholders
- Real-time dashboard access for client
