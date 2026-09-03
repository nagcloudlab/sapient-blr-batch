# CI/CD with Jenkins -- Submission Checklist
## Module 28 | Day 31

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Test stage present with `mvn test` | [ ] |
| 2 | JUnit test results published with `junit` step | [ ] |
| 3 | Git branch is `main` (not `development`) | [ ] |
| 4 | `cleanWs()` in `post { always }` block | [ ] |
| 5 | `archiveArtifacts` for `target/*.jar` | [ ] |
| 6 | Pipeline timeout set (e.g., 30 minutes) | [ ] |
| 7 | Docker credentials use `credentials()` plugin (no hardcoded password) | [ ] |
| 8 | `post { failure }` block with notification | [ ] |
| 9 | Docker image tagged with `${BUILD_NUMBER}` | [ ] |
| 10 | Node.js Jenkinsfile: `npm ci` for install | [ ] |
| 11 | Node.js Jenkinsfile: Lint stage present | [ ] |
| 12 | Node.js Jenkinsfile: Test stage with coverage | [ ] |
| 13 | Node.js Jenkinsfile: Timeout configured | [ ] |

---

## Self-Check Questions

1. **What is the difference between CI, CD (Delivery), and CD (Deployment)?** CI = merge + test frequently. Delivery = automated pipeline + manual prod deploy. Deployment = fully automated including production.
2. **Why should the test stage come BEFORE the Docker build stage?** If tests fail, there's no point building and pushing a Docker image. Fail fast saves time and resources.
3. **What does `cleanWs()` do?** Deletes the entire workspace directory, ensuring the next build starts clean without stale files from previous builds.
4. **Why archive artifacts?** So you can download a specific build's JAR without rebuilding. Essential for rollbacks.
5. **Why use `credentials()` instead of hardcoding secrets?** Jenkinsfiles are stored in Git. Hardcoded secrets are visible to anyone with repo access. `credentials()` stores secrets encrypted in Jenkins.
6. **What does `junit '**/surefire-reports/*.xml'` do?** Publishes test results so Jenkins can show test trends, identify flaky tests, and track test count over time.
7. **Why tag Docker images with build number?** `latest` is a moving target. Build number gives you traceability (build #42 = specific code state) and easy rollback.
8. **What happens if a pipeline has no timeout?** A hung build (e.g., waiting for user input, network timeout) runs forever, blocking the executor for other builds.
9. **What is a webhook?** A callback from GitHub to Jenkins that triggers a build immediately when code is pushed, instead of polling on a schedule.
10. **Why use `post { always }` instead of `post { success }`?** `always` runs on success, failure, and unstable builds. Cleanup and test reporting should happen regardless of build outcome.
