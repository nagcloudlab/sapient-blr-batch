# FoodExpress SSL Certificate Renewal Runbook

## Overview
This runbook describes the steps to renew SSL certificates for FoodExpress.

---

## Pre-Renewal Checklist
- [ ] Current certificate expiry date checked
- [ ] New certificate obtained from CA
- [ ] Maintenance window scheduled
- [ ] Stakeholders notified
- [ ] Rollback plan reviewed

---

## Step 1: Check Current Certificate Expiry

```bash
TODO: Write the openssl command to check certificate expiry date
# Hint: Use openssl x509 -enddate -noout -in <cert-path>
```

**Expected Output:** A date in the future (if still valid)

---

## Step 2: Backup Current Certificates

```bash
TODO: Write commands to backup the current certificate and key files
# Hint: Copy files from /etc/ssl/certs/ and /etc/ssl/private/
```

---

## Step 3: Install New Certificate

```bash
TODO: Write commands to:
# 1. Copy new certificate to /etc/ssl/certs/foodexpress.pem
# 2. Copy new private key to /etc/ssl/private/foodexpress.pem
# 3. Set correct file permissions (644 for cert, 600 for key)
# 4. Set correct ownership (root:root)
```

---

## Step 4: Verify New Certificate

```bash
TODO: Write commands to verify:
# 1. Certificate is valid (openssl verify)
# 2. Certificate matches the private key
# 3. Certificate chain is complete
# Hint: Compare modulus of cert and key using openssl
```

---

## Step 5: Test Apache Configuration

```bash
TODO: Write the command to test Apache configuration
# Hint: apachectl configtest or apache2ctl configtest
```

**Expected Output:** "Syntax OK"

---

## Step 6: Reload Apache

```bash
TODO: Write the command to gracefully reload Apache
# Note: Use reload (not restart) to avoid downtime
```

---

## Step 7: Post-Renewal Verification

```bash
TODO: Write commands to verify the new certificate is active:
# 1. Check the certificate served by the website
# 2. Verify the expiry date of the new certificate
# 3. Test HTTPS connectivity
# Hint: Use openssl s_client -connect and curl
```

---

## Step 8: Update Monitoring

- [ ] TODO: Update certificate expiry monitoring/alerting
- [ ] TODO: Set reminder for next renewal (30 days before expiry)
- [ ] TODO: Update documentation with new expiry date

---

## Rollback Procedure

If the new certificate causes issues:

```bash
TODO: Write commands to restore the backup certificates
TODO: Reload Apache with the old certificates
```

---

## Automation (Future Improvement)

TODO: Describe how you would automate this process using:
- Let's Encrypt with certbot
- Cron job for auto-renewal
- Monitoring alerts for expiry
