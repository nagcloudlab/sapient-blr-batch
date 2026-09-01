# Secure Engineering & DevSecOps -- Project Brief
## Module 27 | Day 30

---

## Sustain Context

FoodExpress's annual security audit has uncovered 8 critical and high vulnerabilities across the codebase. As a sustain engineer, you must fix all vulnerabilities before the compliance deadline. This includes SQL injection, XSS, hardcoded secrets, missing access controls, weak cryptography, and security misconfigurations.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Security Vulnerabilities | Fix 8 security bugs: SQL injection, XSS, hardcoded secrets, missing validation, IDOR, weak hashing, missing headers, debug mode | 45 min | 30 |
| 2 | Secrets Management | Move all hardcoded secrets to .env, update code to use env vars | 15 min | 10 |
| 3 | Bonus: Container Scan | Run vulnerability scan on Docker image, document findings | 15 min | 10 |

**Total Points Available:** 50

---

## Deliverables

1. Fixed `RestaurantController.java` -- parameterized SQL, escaped XSS, bcrypt
2. Fixed `OrderController.java` -- authorization check, input validation, no hardcoded secrets
3. Fixed `app-config.js` -- Helmet enabled, secrets from env, restricted CORS
4. Fixed `application-security.yml` -- debug off, actuator restricted, minimal errors
5. `.env` file with all secrets (gitignored)
6. (Bonus) Container scan report with CVE list
