# Module 25: Docker Part 2 -- Lab Setup

## Prerequisites

- Docker Desktop 4.x or higher (`docker --version` to confirm)
- Docker Desktop must be running
- Understanding of Docker volumes from Module 24

## Running the Starter Code

```bash
cd Labs/starter-code
docker build -t foodexpress-restaurant .
```

This module focuses on multi-stage builds and volume mounts. Bugs are in the Dockerfile and the
volume configuration.

## Verifying Your Fixes

```bash
# Build the image
docker build -t foodexpress-restaurant .

# Run with a named volume for MySQL data persistence
docker run --rm \
  -p 3306:3306 \
  -v foodexpress-db:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=foodexpress \
  foodexpress-restaurant

# Verify the volume was created
docker volume ls | grep foodexpress-db

# Inspect the volume mount point
docker volume inspect foodexpress-db
```

## Expected Behavior

- Multi-stage build produces a smaller final image than a single-stage build.
- `docker build` completes without errors.
- Named volume `foodexpress-db` is created on first run.
- Data persists in the volume across container restarts.
- `docker volume ls` shows the named volume (not only anonymous volumes).

## Troubleshooting

**Volume not persisting data:** Confirm the `VOLUME` instruction in the Dockerfile (or `-v` flag)
points to the directory where MySQL actually stores data (`/var/lib/mysql`), not a different path.

**Final image too large:** Check the multi-stage build -- the second `FROM` stage should copy only
the compiled artefact from the builder stage, not the entire build environment.
