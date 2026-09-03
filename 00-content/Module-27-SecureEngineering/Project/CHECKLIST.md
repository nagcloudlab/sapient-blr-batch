# Secure Engineering & DevSecOps -- Submission Checklist
## Module 27 | Day 30

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | SQL query uses parameterized query (? placeholder, not concatenation) | [ ] |
| 2 | Review comments are HTML-escaped before rendering | [ ] |
| 3 | No hardcoded API keys or passwords in source code | [ ] |
| 4 | Order totalAmount validated (positive, within range) | [ ] |
| 5 | Order quantity validated (1-99) | [ ] |
| 6 | getOrder checks order belongs to authenticated user | [ ] |
| 7 | Password hashing uses bcrypt (not MD5 or SHA) | [ ] |
| 8 | Helmet middleware enabled in Express app | [ ] |
| 9 | CORS restricted to specific domains (not *) | [ ] |
| 10 | Stack traces not exposed to clients in production | [ ] |
| 11 | Debug mode disabled in production config | [ ] |
| 12 | Actuator endpoints restricted to health and info only | [ ] |
| 13 | Remote shutdown endpoint disabled | [ ] |
| 14 | Logging level set to INFO (not DEBUG) in production | [ ] |
| 15 | .env file created with all secrets | [ ] |
| 16 | .env file is in .gitignore | [ ] |

---

## Self-Check Questions

1. **What is SQL injection?** An attack where user input is treated as SQL code because of string concatenation in queries. Fix: parameterized queries.
2. **What is XSS (Cross-Site Scripting)?** An attack where malicious JavaScript is injected into a page via user input. Fix: HTML-escape output.
3. **Why is MD5 unsuitable for passwords?** It's extremely fast (~25 billion hashes/sec on GPU), making brute-force attacks trivial. bcrypt is deliberately slow.
4. **What is IDOR?** Insecure Direct Object Reference -- when an application exposes internal IDs without authorization checks, allowing users to access other users' data.
5. **What does Helmet do?** Sets security-related HTTP headers: Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, and others.
6. **Why restrict CORS to specific origins?** `origin: '*'` allows any website to make authenticated requests to your API, enabling CSRF-like attacks.
7. **Why disable /actuator/env in production?** It exposes all environment variables, which may include database passwords, API keys, and other secrets.
8. **What is the principle of least privilege?** Give users/processes only the minimum permissions needed to perform their task. Applies to DB users, container users, API scopes.
9. **What is "shift left" in security?** Moving security testing earlier in the development lifecycle (code/build phase) rather than only testing in production.
10. **What should you do if you find a hardcoded secret in Git history?** Rotate the secret immediately (change the password/key on the service side), then clean Git history with tools like BFG.
