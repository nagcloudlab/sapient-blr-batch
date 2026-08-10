# Secure Engineering & DevSecOps -- Lab Exercises
## Module 27 | Day 30

---

## Client Email

```
From: security-team@foodexpress.in
To: sustain-engineering@team.com
Subject: URGENT -- Security Audit Findings
Date: 2026-08-07

Team,

Our annual security audit found 8 critical and high vulnerabilities
in the FoodExpress codebase. These must be fixed before our
compliance deadline on Friday.

Findings:
1. SQL Injection in restaurant search (CRITICAL)
2. Cross-Site Scripting in review rendering (HIGH)
3. Hardcoded secrets in source code (CRITICAL)
4. Missing input validation (HIGH)
5. Insecure Direct Object Reference in orders API (HIGH)
6. Weak password hashing (CRITICAL)
7. Missing security headers (MEDIUM)
8. Debug mode in production config (HIGH)

Fix all issues in the starter-code/ files.

-- Ravi Kumar, CISO, FoodExpress
```

---

## Lab 1: Fix Security Vulnerabilities (8 bugs)

### Duration: 45 minutes | Points: 30

**Files to fix:**
- `starter-code/RestaurantController.java`
- `starter-code/OrderController.java`
- `starter-code/app-config.js`
- `starter-code/application-security.yml`

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact | OWASP |
|---|------|-------------|--------|-------|
| 1 | Check SQL query in searchRestaurants | String concatenation in SQL query | SQL Injection -- attacker can dump/delete DB | A03 |
| 2 | Check how review.comment is rendered | User input inserted without escaping | XSS -- attacker steals session cookies | A03 |
| 3 | Check class constants in both Java files | API key and DB password hardcoded | Secrets exposed in source control | A02 |
| 4 | Check createOrder method | No validation on totalAmount or quantity | Negative order amounts, free food exploit | A04 |
| 5 | Check getOrder method | No authorization check on order ownership | Any user can view any order (IDOR) | A01 |
| 6 | Check password hashing method | Uses MD5 hash | Crackable in seconds with rainbow tables | A02 |
| 7 | Check Express app setup in app-config.js | Missing Helmet (security headers) | XSS, clickjacking, MIME sniffing | A05 |
| 8 | Check application-security.yml | debug: true in production | Stack traces exposed, verbose errors | A05 |

### Verification Checklist

```
[ ] SQL query uses parameterized query (? placeholder)
[ ] Review comment is HTML-escaped before rendering
[ ] No hardcoded secrets in source code
[ ] Order amount validated: positive number, within range
[ ] getOrder checks that order belongs to authenticated user
[ ] Password hashing uses bcrypt (not MD5)
[ ] Helmet middleware enabled in Express
[ ] Debug mode disabled in production config
```

---

## Lab 2: Secrets Management (3 tasks)

### Duration: 15 minutes | Points: 10

### Task 1: Create a .env file
```bash
# Move all hardcoded secrets to a .env file
# Ensure .env is in .gitignore
```

### Task 2: Update code to read from environment
```java
// Java: System.getenv("STRIPE_API_KEY")
// Node: process.env.STRIPE_API_KEY
```

### Task 3: Verify no secrets in Git
```bash
# Use git log search to find previously committed secrets
git log -p -S "API_KEY" -- .
# If found, the secret must be rotated (changed on the service side)
```

---

## Lab 3: Container Security Scan (Bonus)

### Duration: 15 minutes | Points: 10

```bash
# Scan the Order Service Docker image
docker scout cves foodexpress/order-service:1.0

# OR use Trivy
trivy image foodexpress/order-service:1.0

# Document:
# - How many HIGH/CRITICAL vulnerabilities found?
# - What is the most critical CVE?
# - What is the fix (upgrade which package)?
```

---

## Scoring

| Task | Points |
|------|--------|
| Lab 1: Fix 8 security vulnerabilities | 30 |
| Lab 2: Secrets management | 10 |
| Lab 3: Bonus container scan | 10 |
| **Total** | **50** |
