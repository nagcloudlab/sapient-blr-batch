# CI/CD with Jenkins -- Trainer Solutions & Hints
## Module 28 | Day 31

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Missing Test Stage | Add `stage('Test')` with `sh 'mvn test'` and `junit` reporting | Students add the stage but forget to publish junit results -- test trends aren't tracked | Ask: "If tests pass today but fail tomorrow, how do you know which commit broke them?" (junit history) |
| 2 | Wrong Branch | Change `development` to `main` | Students might change to `master` -- verify the actual branch name | Ask: "What's the difference between main and master?" (Just naming convention; check the repo) |
| 3 | No Cleanup | Add `cleanWs()` in `post { always }` | Students put cleanWs in post/success -- it won't run on failures | Ask: "If a build fails, does post/success run?" (No -- only post/always and post/failure) |
| 4 | No Artifacts | Add `archiveArtifacts artifacts: 'target/*.jar'` | Students archive `target/**` which includes test reports and classes -- just need the JAR | Ask: "Why archive only *.jar and not the entire target/?" (Size; we only need the deployable) |
| 5 | No Timeout | Add `options { timeout(time: 30, unit: 'MINUTES') }` | Students set timeout per-stage instead of pipeline-wide | Both are valid; pipeline-wide is simpler, per-stage allows different limits |
| 6 | Hardcoded Creds | Change to `credentials('docker-hub-credentials')`, use `DOCKER_CREDS_USR` and `DOCKER_CREDS_PSW` | Students remove the password but don't add credentials() | Walk through Jenkins UI: Manage Jenkins > Credentials > Add |
| 7 | No Failure Notification | Add `post { failure { slackSend ... } }` | Students add email notification but not Slack (check what the team actually uses) | Ask: "Where does your team monitor build status?" (Slack, email, dashboard) |
| 8 | Docker Tag | Change `latest` to `${BUILD_NUMBER}` | Students use git SHA which is better but more complex. BUILD_NUMBER is fine for now | Ask: "If latest points to build #50, can you roll back to build #48?" (Not easily -- need specific tags) |

---

## Key Discussion Points

1. Why is deploying untested code dangerous? (Bugs reach production, customer impact, reputation damage)
2. Why `credentials()` over environment variables in Jenkinsfile? (Jenkinsfile is in Git -- env vars defined in Jenkins are encrypted)
3. Why tag with build number? (Traceability, rollback capability, audit trail)
4. Why `cleanWs()` in `always`? (Runs regardless of build result; prevents stale file issues)
5. When should you deploy automatically vs require approval? (Staging: auto. Production: approval gate)
6. What is the cost of a broken build? (30 min developer time * 5 devs = 2.5 hours per incident)

---

## Jenkinsfile Fix Details

| # | Bug | Buggy | Fixed |
|---|-----|-------|-------|
| 1 | Missing test stage | (absent) | `stage('Test') { sh 'mvn test' }` + junit |
| 2 | Wrong branch | `branch: 'development'` | `branch: 'main'` |
| 3 | No cleanup | (no post section) | `post { always { cleanWs() } }` |
| 4 | No artifacts | (absent) | `archiveArtifacts artifacts: 'target/*.jar'` |
| 5 | No timeout | (absent) | `options { timeout(time: 30, unit: 'MINUTES') }` |
| 6 | Hardcoded creds | `DOCKER_PASSWORD = 'MyD0ck3rP@ssw0rd!'` | `DOCKER_CREDS = credentials('docker-hub-credentials')` |
| 7 | No failure notification | (absent) | `post { failure { slackSend ... } }` |
| 8 | Wrong tag | `:latest` only | `:${BUILD_NUMBER}` + `:latest` |
