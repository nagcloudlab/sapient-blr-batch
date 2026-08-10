# Module 26: Docker Part 3 (Compose) -- Lab Setup

## Prerequisites

- Docker Desktop 4.x or higher (includes `docker compose`)
- `docker compose version` to confirm Compose is available
- Ports 3000, 3306, and 27017 must be free on your machine

## Running the Starter Code

```bash
cd Labs/starter-code
docker compose up
```

The first run pulls base images -- this may take several minutes. Bugs will cause one or more
services to fail to start. Check the Compose log output to identify which service failed and why.

## Verifying Your Fixes

```bash
# Check all services are running (should show 4+ services)
docker compose ps

# Test API service
curl http://localhost:3000/api/health

# Check service logs individually
docker compose logs api
docker compose logs mysql
docker compose logs mongo

# Bring everything down cleanly
docker compose down -v    # -v removes volumes (clean slate for re-testing)
```

## Expected Behavior

- `docker compose ps` shows all services with status "running".
- Services start in dependency order (databases before app services).
- Named volumes persist data between `docker compose down` and `docker compose up`.
- Services on the same Compose network can reach each other by service name.
- `docker compose down` stops all services cleanly with no orphan containers.

## Troubleshooting

**Service exits immediately after starting:** Run `docker compose logs <service-name>` to see the
error. A missing environment variable or wrong database hostname is the most common cause.

**Services cannot reach each other by hostname:** Ensure all services are defined under the same
named network in `docker-compose.yml`. Service names resolve as hostnames only within the same
Compose network.
