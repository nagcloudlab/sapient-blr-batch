# Secure Engineering & DevSecOps -- Trainer Solutions & Hints
## Module 27 | Day 30

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | SQL Injection | Change string concatenation to parameterized query with `?` placeholder | Students add escaping/sanitization instead of parameterized queries. Sanitization is fragile; parameterized queries are the correct solution | Ask: "What if someone finds a new way to bypass your sanitization?" (Parameterized queries are immune by design) |
| 2 | XSS | Use HtmlUtils.htmlEscape() on user input before rendering | Students sometimes escape at input time instead of output time. Always escape at the point of rendering | Ask: "Should you sanitize when storing or when displaying?" (Display -- different contexts need different escaping) |
| 3 | Hardcoded Secrets | Move to @Value("${ENV_VAR}") or process.env | Students create a constants file instead of using env vars. A constants file in Git is still exposed | Ask: "If your repo becomes public tomorrow, are your secrets safe?" |
| 4 | Input Validation | Add @Valid, @NotNull, @DecimalMin, @Max constraints | Students validate in the controller instead of using bean validation annotations | Show how @Valid automatically returns 400 with field-level error messages |
| 5 | IDOR | Add `if (!order.getCustomerId().equals(auth.getUserId()))` check | Students add role-based check but forget resource ownership check | Ask: "Can an admin impersonate a customer?" (Discuss principle of least privilege) |
| 6 | Password Hashing | BCryptPasswordEncoder with cost 12 | Students use SHA-256 with salt -- better than MD5 but still too fast | Ask: "How many SHA-256 hashes per second can a GPU compute?" (~5 billion) |
| 7 | Security Headers | Add `app.use(helmet())` | Students add individual headers instead of using Helmet | Show `curl -I http://localhost:3000` before and after Helmet |
| 8 | Debug Mode | Set debug: false, restrict actuator, remove stack traces | Students disable debug but leave actuator/env exposed | Ask: "What can an attacker learn from /actuator/env?" (All environment variables including secrets) |

---

## Key Discussion Points

1. Why parameterized queries over sanitization? (Sanitization is fragile; parameterized queries make injection structurally impossible)
2. Why bcrypt over SHA-256 for passwords? (bcrypt is slow by design; SHA-256 is fast = attacker can try billions per second)
3. Why escape at output, not input? (Different outputs need different escaping: HTML vs JSON vs SQL)
4. Why restrict actuator endpoints? (/actuator/env exposes all env vars; /actuator/shutdown allows DoS)
5. Why secrets in env vars? (Never in code, config files, or Docker images -- all are extractable)
6. What is the OWASP Top 10? (Industry standard list of most critical web application security risks)
