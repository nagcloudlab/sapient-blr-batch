# Docker Part 3 -- Networking, Docker Compose, Deployments
## Module 26 | Sustain Engineering Training | Day 29

---

## Agenda -- Day 29

| # | Topic |
|---|-------|
| 01 | Docker Networking Fundamentals |
| 02 | Network Drivers: Bridge, Host, Overlay |
| 03 | Container-to-Container Communication |
| 04 | DNS & Service Discovery in Docker |
| 05 | Introduction to Docker Compose |
| 06 | docker-compose.yml Deep Dive |
| 07 | Multi-Container FoodExpress Stack |
| 08 | Docker Compose Commands & Lifecycle |
| 09 | Lab: Fix docker-compose.yml |
| 10 | Day Wrap-up & Key Takeaways |

---

## Docker Networking -- Why It Matters

### The Problem

```
Container A (Order Service :8081)
      │
      │  How does it talk to...
      ▼
Container B (MySQL :3306)     ← Different container, different filesystem
Container C (Redis :6379)     ← Different network namespace
Container D (Restaurant :3000) ← No shared localhost
```

Containers are isolated. They can't just use `localhost` to talk to each other. Docker networking solves this.

---

## Docker Network Drivers

```
┌──────────────────────────────────────────────────────┐
│                  Docker Network Drivers               │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  bridge   │  │   host   │  │ overlay  │           │
│  │  (default)│  │          │  │          │           │
│  │           │  │ No NAT   │  │ Multi-   │           │
│  │ Containers│  │ Share    │  │ host     │           │
│  │ get own   │  │ host     │  │ Swarm/   │           │
│  │ IP on     │  │ network  │  │ K8s      │           │
│  │ virtual   │  │ stack    │  │          │           │
│  │ bridge    │  │          │  │          │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                       │
│  ┌──────────┐  ┌──────────┐                          │
│  │  none     │  │ macvlan  │                          │
│  │ No network│  │ Physical │                          │
│  │ Isolated  │  │ network  │                          │
│  │           │  │ access   │                          │
│  └──────────┘  └──────────┘                          │
└──────────────────────────────────────────────────────┘
```

---

## Bridge Network (Default)

```
Host Machine
┌─────────────────────────────────────────┐
│                                          │
│  docker0 bridge (172.17.0.1)            │
│  ┌────────────┬────────────┬──────────┐ │
│  │            │            │          │ │
│  │ order-svc  │ payment-svc│ mysql    │ │
│  │ 172.17.0.2 │ 172.17.0.3 │172.17.0.4│ │
│  │ :8081      │ :8082      │ :3306    │ │
│  └────────────┘────────────┘──────────┘ │
│                                          │
│  Containers can reach each other by IP   │
│  But NOT by name on default bridge!      │
└─────────────────────────────────────────┘
```

**Default bridge limitations:**
- Containers can communicate by IP address
- NO automatic DNS resolution by container name
- NOT recommended for production

---

## User-Defined Bridge Network (Recommended)

```bash
# Create a custom network
docker network create foodexpress-net

# Run containers on the custom network
docker run -d --name mysql-db --network foodexpress-net \
  -e MYSQL_ROOT_PASSWORD=secret mysql:8.0

docker run -d --name order-svc --network foodexpress-net \
  -e DB_HOST=mysql-db \
  -p 8081:8081 \
  foodexpress/order-service:1.0
```

```
foodexpress-net (user-defined bridge)
┌────────────────────────────────────────┐
│                                         │
│  order-svc ──── DNS ────▶ mysql-db     │
│  (can use name "mysql-db" as hostname!) │
│                                         │
│  Automatic DNS resolution by name!      │
│  Better isolation from other containers │
└────────────────────────────────────────┘
```

---

## Host Network

```bash
# Container shares the host's network stack
docker run -d --network host --name order-svc \
  foodexpress/order-service:1.0

# No port mapping needed (-p is ignored)
# App listening on 8081 inside container = 8081 on host
```

| Feature | Bridge | Host |
|---------|--------|------|
| Isolation | Yes (own IP) | No (shares host) |
| Port mapping | Required (-p) | Not needed |
| Performance | Slight overhead (NAT) | Best (no NAT) |
| Security | Better (isolated) | Lower (shared stack) |
| Use case | Most containers | Performance-critical apps |

> **FoodExpress:** We use bridge networks for all services. Host network only for the monitoring agent that needs to see all host traffic.

---

## Network Commands

```bash
# List networks
docker network ls

# Create a network
docker network create foodexpress-net

# Inspect a network
docker network inspect foodexpress-net

# Connect a running container to a network
docker network connect foodexpress-net order-svc

# Disconnect from a network
docker network disconnect foodexpress-net order-svc

# Remove a network
docker network rm foodexpress-net

# Remove all unused networks
docker network prune
```

---

## Container DNS Resolution

### How containers find each other

```
┌─────────────────────────────────────────────┐
│  foodexpress-net (user-defined bridge)       │
│                                              │
│  ┌──────────┐          ┌──────────────┐     │
│  │ order-svc│          │ mysql-db     │     │
│  │          │ ─DNS──▶  │              │     │
│  │ DB_HOST= │          │ Resolves to  │     │
│  │ mysql-db │          │ 172.18.0.3   │     │
│  └──────────┘          └──────────────┘     │
│                                              │
│  Docker's embedded DNS server resolves       │
│  container names to their IP addresses       │
│  automatically on user-defined networks      │
└─────────────────────────────────────────────┘

# In application.yml:
spring:
  datasource:
    url: jdbc:mysql://mysql-db:3306/foodexpress
    # "mysql-db" resolves to the container's IP
```

---

## Container Linking (Legacy)

### --link is deprecated, use networks instead

```bash
# OLD WAY (don't use)
docker run --link mysql-db:db order-svc

# NEW WAY (use networks)
docker network create foodexpress-net
docker run --network foodexpress-net --name mysql-db ...
docker run --network foodexpress-net --name order-svc ...
```

---

## Introduction to Docker Compose

### The Problem with docker run

```bash
# Starting FoodExpress without Compose:
docker network create foodexpress-net
docker volume create mysql-data
docker volume create redis-data

docker run -d --name mysql-db --network foodexpress-net \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8.0

docker run -d --name redis --network foodexpress-net \
  -v redis-data:/data \
  redis:7-alpine

docker run -d --name order-svc --network foodexpress-net \
  -p 8081:8081 -e DB_HOST=mysql-db \
  foodexpress/order-service:1.0

docker run -d --name payment-svc --network foodexpress-net \
  -p 8082:8082 -e DB_HOST=mysql-db \
  foodexpress/payment-service:1.0

# 6 commands, easy to mess up, hard to version control
```

---

## Docker Compose -- The Solution

### One YAML file, one command

```yaml
# docker-compose.yml
version: '3.8'

services:
  mysql-db:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

  order-service:
    image: foodexpress/order-service:1.0
    ports:
      - "8081:8081"
    environment:
      DB_HOST: mysql-db
    depends_on:
      - mysql-db

volumes:
  mysql-data:
  redis-data:
```

```bash
# One command to start everything:
docker compose up -d
```

---

## docker-compose.yml Structure

```yaml
version: '3.8'              # Compose file version

services:                    # Define your containers
  service-name:
    image: ...               # Docker image to use
    build: ./path            # OR build from Dockerfile
    ports:                   # Port mappings
      - "host:container"
    environment:             # Environment variables
      KEY: value
    volumes:                 # Volume mounts
      - named-vol:/path
      - ./local:/container
    depends_on:              # Startup order
      - other-service
    networks:                # Network membership
      - my-network
    restart: unless-stopped  # Restart policy

volumes:                     # Named volumes
  named-vol:

networks:                    # Custom networks
  my-network:
```

---

## FoodExpress Full Stack -- docker-compose.yml

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - order-service
      - restaurant-service
    networks:
      - frontend

  order-service:
    build: ./order-service
    ports:
      - "8081:8081"
    environment:
      DB_HOST: mysql-db
      REDIS_HOST: redis
    depends_on:
      - mysql-db
      - redis
    networks:
      - frontend
      - backend

  restaurant-service:
    build: ./restaurant-service
    ports:
      - "3000:3000"
    depends_on:
      - mysql-db
    networks:
      - frontend
      - backend

  mysql-db:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: foodexpress
    networks:
      - backend

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - backend

volumes:
  mysql-data:
  redis-data:

networks:
  frontend:
  backend:
```

---

## depends_on -- Startup Order

```yaml
services:
  order-service:
    depends_on:
      - mysql-db
      - redis

  # BUT: depends_on only waits for container START, not READY
  # MySQL may not be accepting connections yet!
```

### Solution: Health Check + Condition

```yaml
services:
  mysql-db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  order-service:
    depends_on:
      mysql-db:
        condition: service_healthy
```

---

## Docker Compose Commands

```bash
# Start all services (detached)
docker compose up -d

# Start specific service
docker compose up -d order-service

# Stop all services
docker compose down

# Stop and remove volumes (CAREFUL!)
docker compose down -v

# View running services
docker compose ps

# View logs
docker compose logs
docker compose logs -f order-service

# Rebuild and restart
docker compose up -d --build

# Scale a service
docker compose up -d --scale order-service=3

# Execute command in a service
docker compose exec mysql-db mysql -uroot -psecret
```

---

## Docker Compose -- Build vs Image

```yaml
services:
  # Use a pre-built image
  mysql-db:
    image: mysql:8.0

  # Build from Dockerfile in directory
  order-service:
    build: ./order-service
    # Uses ./order-service/Dockerfile

  # Build with custom Dockerfile
  restaurant-service:
    build:
      context: ./restaurant-service
      dockerfile: Dockerfile.prod
      args:
        NODE_ENV: production

  # Both: build and tag
  payment-service:
    build: ./payment-service
    image: foodexpress/payment-service:1.0
    # Builds AND tags the image
```

---

## Network Isolation with Compose

```
┌─────────────────────────────────────────────────┐
│  frontend network                                │
│  ┌──────┐  ┌────────────┐  ┌─────────────────┐ │
│  │nginx │  │order-service│  │restaurant-svc   │ │
│  │:80   │  │:8081        │  │:3000            │ │
│  └──────┘  └──────┬─────┘  └────────┬────────┘ │
│                    │                  │          │
├────────────────────┼──────────────────┼──────────┤
│  backend network   │                  │          │
│               ┌────┴─────┐     ┌─────┴────┐     │
│               │mysql-db  │     │ redis    │     │
│               │:3306     │     │ :6379    │     │
│               └──────────┘     └──────────┘     │
│                                                  │
│  nginx CANNOT reach mysql-db (different network) │
│  order-service CAN reach both (on both networks) │
└─────────────────────────────────────────────────┘
```

> **FoodExpress:** We separate frontend and backend networks so the NGINX reverse proxy can't directly access the database.

---

## Environment Variables in Compose

```yaml
services:
  order-service:
    environment:
      # Inline values
      DB_HOST: mysql-db
      DB_PORT: 3306
      SPRING_PROFILES_ACTIVE: production

    # OR from .env file
    env_file:
      - .env
      - .env.production

# .env file:
DB_HOST=mysql-db
DB_PORT=3306
MYSQL_ROOT_PASSWORD=super_secret_password
```

> **Important:** Never commit `.env` files with real secrets to Git. Use `.env.example` with placeholder values.

---

## Docker Compose for Development vs Production

| Feature | Development | Production |
|---------|------------|------------|
| Build | `build: .` (from source) | `image: registry/app:1.0` (pre-built) |
| Volumes | Bind mount source code | Named volumes only |
| Ports | Expose all ports | Only expose needed ports |
| Restart | `restart: no` | `restart: unless-stopped` |
| Logging | Default (stdout) | Log driver (json-file with limits) |
| Secrets | `.env` file | Docker secrets / Vault |
| Resources | No limits | CPU/memory limits |

---

## Production Compose Enhancements

```yaml
services:
  order-service:
    image: foodexpress/order-service:1.0.3
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/actuator/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 40s
```

---

## MCQ -- Quick Check 1

**Question:** Two containers on the default bridge network try to communicate by container name. What happens?

A) They communicate successfully
B) DNS resolution fails -- container names don't resolve on the default bridge
C) Docker blocks the communication for security
D) The containers crash

> **Answer:** B -- The default bridge network does NOT provide DNS resolution. You must use a user-defined bridge network for name-based communication.

---

## MCQ -- Quick Check 2

**Question:** In docker-compose.yml, what does `depends_on: [mysql-db]` guarantee?

A) MySQL is fully ready to accept connections before the service starts
B) MySQL container is started before this service, but may not be ready yet
C) MySQL container is built first
D) MySQL and this service share the same container

> **Answer:** B -- `depends_on` only controls startup ORDER, not readiness. Use health checks with `condition: service_healthy` to wait for actual readiness.

---

## MCQ -- Quick Check 3

**Question:** You have this in docker-compose.yml:
```yaml
services:
  web:
    ports:
      - "8080:80"
  db:
    # no ports section
```
Can the `web` service connect to `db` on port 3306?

A) No, because db doesn't have a ports section
B) Yes, containers on the same Compose network can reach any port on any other container
C) Only if you add `--link db:db`
D) Only if db uses host network

> **Answer:** B -- The `ports` section publishes ports to the HOST. Container-to-container communication works on all ports within the same Docker network, regardless of `ports`.

---

## MCQ -- Quick Check 4

**Question:** What does `docker compose down -v` do differently from `docker compose down`?

A) It runs in verbose mode
B) It also removes named volumes, potentially deleting database data
C) It validates the compose file
D) It removes the Docker images

> **Answer:** B -- The `-v` flag removes named volumes declared in the `volumes` section. This will DELETE your database data. Use with extreme caution.

---

## MCQ -- Quick Check 5

**Question:** In the FoodExpress Compose setup, nginx is on the `frontend` network and mysql-db is on the `backend` network. Can nginx connect to mysql-db?

A) Yes, all Compose services can talk to each other
B) No, they are on different networks and cannot communicate
C) Yes, but only if you use the IP address
D) Only if you restart nginx

> **Answer:** B -- Network isolation prevents cross-network communication. Only services sharing a network can communicate. This is a security feature.

---

## Troubleshooting Docker Compose

### Common Issues and Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Port conflict | "port is already allocated" | Change host port or stop conflicting container |
| Network not found | "network X not found" | Check network name spelling; run `docker compose up` |
| Volume permissions | "permission denied" | Check USER in Dockerfile matches volume ownership |
| depends_on timing | "connection refused" to DB | Add healthcheck + condition: service_healthy |
| Build cache stale | Old code running | `docker compose up -d --build --force-recreate` |
| Container exit | Exits immediately | Check `docker compose logs <service>` for error |

---

## Deployment Strategies with Docker

| Strategy | How | Risk | Use Case |
|----------|-----|------|----------|
| Recreate | Stop old, start new | Downtime | Dev/staging |
| Rolling | Replace one at a time | Minimal | Production |
| Blue-Green | Run both, switch traffic | Low (instant rollback) | Critical services |
| Canary | Route % traffic to new | Very low | Gradual rollout |

```bash
# Simple rolling update with Compose
docker compose pull order-service
docker compose up -d --no-deps order-service
# --no-deps: only restart this service, not its dependencies
```

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | Use user-defined bridge networks, not the default bridge (for DNS resolution) |
| 2 | Container-to-container communication works on all ports within a shared network |
| 3 | `ports` publishes to the host; containers don't need it to talk to each other |
| 4 | Docker Compose replaces multiple `docker run` commands with one YAML file |
| 5 | `depends_on` controls start order, NOT readiness -- use health checks |
| 6 | Network isolation (frontend/backend) prevents unauthorized cross-service access |
| 7 | Never use `docker compose down -v` in production unless you want to lose data |
| 8 | Environment variables via `.env` files; never commit secrets to Git |

> **Next: Module 27 -- Secure Engineering & DevSecOps**
