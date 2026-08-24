# Module 28: Jenkins -- Lab Setup

## Prerequisites

- Docker Desktop (recommended method to run Jenkins)
- Alternatively: Jenkins LTS installed natively
- Access to the starter-code Jenkinsfile in a Git-accessible location

## Running Jenkins via Docker

```bash
docker run -d -p 8090:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins/jenkins:lts
```

Get the initial admin password:
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open Jenkins at `http://localhost:8090` and complete the setup wizard.

## Running the Starter Code

1. In Jenkins, create a new Pipeline job.
2. Copy the content of `Labs/starter-code/Jenkinsfile` into the Pipeline Script field (or configure
   the job to pull from your Git repository).
3. Click "Build Now" -- the pipeline will fail at one or more buggy stages.

## Verifying Your Fixes

After each fix, rebuild the job and confirm:
- The previously failing stage now shows green in the Stage View.
- All stages are present and in order: Checkout, Build, Test, Package, Deploy.
- No credentials or hard-coded secrets appear in the console log.
- Post-build notifications run on both success and failure.
- Docker image is built and tagged correctly (check with `docker images`).

## Expected Behavior

- All pipeline stages appear in Stage View with green checkmarks.
- Build artefact is generated after the Build stage.
- Test report is published and visible on the job page.
- Pipeline completes without unhandled exceptions or skipped critical stages.

## Troubleshooting

**Port 8090 already in use:** Change the host port in the `docker run` command (e.g., `-p 8091:8080`).

**Docker-in-Docker errors:** Ensure the Docker socket is mounted into the Jenkins container with
`-v /var/run/docker.sock:/var/run/docker.sock`. On Windows with WSL2 this requires Docker Desktop
"Expose daemon on tcp://" to be enabled in settings.
