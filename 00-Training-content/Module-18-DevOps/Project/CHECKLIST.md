# DevOps Fundamentals -- Submission Checklist
## Module 18 | Day 19

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Jenkinsfile: All 6 bugs identified and fixed | [ ] |
| 2 | Jenkinsfile: Credentials use Jenkins credential store | [ ] |
| 3 | Jenkinsfile: Docker images tagged with build number | [ ] |
| 4 | Jenkinsfile: Approval gate before production | [ ] |
| 5 | Deployment strategy: Big-bang replaced with zero-downtime strategy | [ ] |
| 6 | Deployment strategy: Automated rollback procedure defined | [ ] |
| 7 | Deployment strategy: Proper health checks defined | [ ] |
| 8 | Pipeline design: At least 7 stages with tools | [ ] |
| 9 | Pipeline design: Testing at every stage | [ ] |
| 10 | 7 C's mapping completed | [ ] |
| 11 | DevOps maturity assessment completed | [ ] |

---

## Self-Check Questions

1. **Are credentials secure?** No passwords, API keys, or tokens in code or pipeline files.
2. **Can you rollback?** Is your rollback automated and tested?
3. **Is every deployment traceable?** Can you tell exactly what version is running in production?
4. **Are tests meaningful?** Do they catch real bugs, or just pass for the sake of coverage?
5. **Is your monitoring proactive?** Will you know about a problem before customers do?
6. **Is your deployment schedule sensible?** Does it account for team availability and risk?
7. **Can you explain the difference between CI, CD (delivery), and CD (deployment)?**
8. **Did you consider cost?** Not every organization needs Kubernetes on day one.
9. **Is your pipeline fast?** Target: under 15 minutes from commit to staging.
10. **Would you trust this pipeline to deploy your code at 2 AM?** If not, what's missing?
