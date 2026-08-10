# Module 24: Docker Part 1 -- Lab Setup

## Prerequisites

- Docker Desktop 4.x or higher (`docker --version` to confirm)
- Docker Desktop must be running before executing any `docker` commands

## Running the Starter Code

```bash
cd Labs/starter-code
docker build -t foodexpress-order .
```

The build will fail with errors -- this is expected. Each build error corresponds to a bug in the
`Dockerfile`. Fix the issue and re-run `docker build` after each change.

## Verifying Your Fixes

```bash
# Build must succeed first
docker build -t foodexpress-order .

# Run the container
docker run --rm -p 8080:8080 foodexpress-order

# In a second terminal, test the running container
curl http://localhost:8080/api/health

# Stop the container (Ctrl+C in the first terminal, or)
docker stop $(docker ps -q --filter ancestor=foodexpress-order)
```

## Expected Behavior

- `docker build` completes with "Successfully built" and no errors.
- `docker run` starts the container and the service is reachable on port 8080.
- `curl http://localhost:8080/api/health` returns `200 OK`.
- Container exits cleanly when stopped -- no zombie processes.
- Image size is reasonable (check with `docker images foodexpress-order`).

## Troubleshooting

**`COPY` fails with "file not found":** The source path in `COPY` is relative to the build context
(the directory passed to `docker build`). Ensure the file exists at that path on the host.

**Container starts then exits immediately:** Run `docker logs <container-id>` to see the application
error. The `CMD` or `ENTRYPOINT` instruction likely has a wrong path or command syntax.
