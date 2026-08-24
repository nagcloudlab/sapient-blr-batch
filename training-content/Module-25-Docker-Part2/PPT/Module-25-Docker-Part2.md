# Docker Part 2 -- Images, Layers, Dockerfile Deep Dive, Volumes
## Module 25 | Sustain Engineering Training | Day 28

---

## Agenda -- Day 28

| # | Topic |
|---|-------|
| 01 | Docker Image Layers Deep Dive |
| 02 | Dockerfile Directives -- FROM, RUN, COPY, ADD |
| 03 | Dockerfile Directives -- ENV, EXPOSE, CMD, ENTRYPOINT |
| 04 | Multi-Stage Builds |
| 05 | Building & Tagging Images |
| 06 | Publishing to Registry (Docker Hub, ECR) |
| 07 | Docker Volumes -- Persistent Data |
| 08 | Volume Types & Best Practices |
| 09 | Lab: Fix Restaurant Service Dockerfile + Volumes |
| 10 | Day Wrap-up & Key Takeaways |

---

## Docker Image Layers -- How They Work

```
$ docker history foodexpress/order-service:1.0

IMAGE          CREATED        CREATED BY                          SIZE
a1b2c3d4       2 min ago      CMD ["java", "-jar", "app.jar"]    0B
e5f6a7b8       2 min ago      EXPOSE 8081                         0B
c9d0e1f2       2 min ago      COPY app.jar /app/app.jar           45MB
3a4b5c6d       2 min ago      RUN apt-get install -y curl         15MB
7e8f9a0b       5 min ago      RUN apt-get update                  25MB
1c2d3e4f       3 days ago     (base: eclipse-temurin:17-jre)      190MB

Total: 275MB
Each instruction = one layer. Layers are cached and shared.
```

---

## Layer Caching -- Why Order Matters

### Bad Dockerfile (cache busted on every build)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .                       # Any file change busts cache here
RUN npm install                # Reinstalls ALL deps every time
EXPOSE 3000
CMD ["node", "server.js"]
```

### Good Dockerfile (leverages cache)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json ./   # Only deps files
RUN npm ci                               # Cached unless deps change
COPY . .                                 # Code changes don't bust npm cache
EXPOSE 3000
CMD ["node", "server.js"]
```

> **FoodExpress:** Rebuilding the Restaurant Service went from 4 minutes to 15 seconds by reordering COPY statements.

---

## Layer Caching Visualized

```
Build 1 (fresh):                Build 2 (only code changed):
┌──────────────────┐           ┌──────────────────┐
│ CMD ["node"...]  │ ← build   │ CMD ["node"...]  │ ← build
├──────────────────┤           ├──────────────────┤
│ COPY . .         │ ← build   │ COPY . .         │ ← build (new code)
├──────────────────┤           ├──────────────────┤
│ RUN npm ci       │ ← build   │ RUN npm ci       │ ← CACHED!
├──────────────────┤           ├──────────────────┤
│ COPY package*    │ ← build   │ COPY package*    │ ← CACHED!
├──────────────────┤           ├──────────────────┤
│ WORKDIR /app     │ ← build   │ WORKDIR /app     │ ← CACHED!
├──────────────────┤           ├──────────────────┤
│ FROM node:18     │ ← pull    │ FROM node:18     │ ← CACHED!
└──────────────────┘           └──────────────────┘

Build 1: 4 minutes             Build 2: 15 seconds
```

---

## FROM -- Choosing the Right Base Image

### Image Size Comparison

| Base Image | Size | Use Case |
|-----------|------|----------|
| `ubuntu:22.04` | ~78MB | When you need full OS tools |
| `debian:bookworm-slim` | ~80MB | Debian without extras |
| `alpine:3.18` | ~7MB | Minimal; uses musl libc |
| `eclipse-temurin:17-jre` | ~270MB | Java apps (full Debian) |
| `eclipse-temurin:17-jre-alpine` | ~190MB | Java apps (minimal) |
| `node:18` | ~340MB | Node.js (full Debian) |
| `node:18-alpine` | ~175MB | Node.js (minimal) |
| `scratch` | 0MB | Go binaries, static apps |

> **FoodExpress:** We saved 400MB per image by switching from `node:18` to `node:18-alpine` for our Node.js services.

---

## RUN -- Executing Build Commands

### Best Practices

```dockerfile
# BAD: Multiple RUN creates multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN rm -rf /var/lib/apt/lists/*

# GOOD: Single RUN with && chains
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget && \
    rm -rf /var/lib/apt/lists/*
```

**Why?** Each RUN creates a layer. The `rm` in a later layer doesn't reduce the size of earlier layers. Combine operations that add and clean up in one layer.

---

## COPY vs ADD

### When to Use Each

```dockerfile
# COPY -- Simple, predictable
COPY app.jar /app/app.jar          # Copy a file
COPY config/ /app/config/          # Copy a directory
COPY --chown=appuser:appgroup app.jar /app/   # Set ownership

# ADD -- Extra features (use sparingly)
ADD config.tar.gz /app/config/     # Auto-extracts tar archives
ADD https://example.com/file.txt /app/   # Downloads from URL (avoid!)
```

| Feature | COPY | ADD |
|---------|------|-----|
| Copy files | Yes | Yes |
| Copy directories | Yes | Yes |
| Auto-extract tar | No | Yes |
| Download URLs | No | Yes (but use curl instead) |
| Predictable | Yes | Can surprise you |
| Recommended | Default choice | Only for tar extraction |

---

## ENV -- Environment Variables

```dockerfile
# Set environment variables
ENV SPRING_PROFILES_ACTIVE=production
ENV SERVER_PORT=8081
ENV DB_HOST=mysql
ENV DB_PORT=3306

# Use variables in subsequent instructions
ENV APP_HOME=/opt/foodexpress
WORKDIR ${APP_HOME}
COPY app.jar ${APP_HOME}/app.jar

# Override at runtime
docker run -e DB_HOST=production-db foodexpress/order-service:1.0
```

> **FoodExpress:** We use ENV for defaults in the Dockerfile and override with `-e` flags for different environments (dev, staging, prod).

---

## EXPOSE -- Documenting Ports

```dockerfile
# EXPOSE documents which ports the container uses
EXPOSE 8081         # HTTP API
EXPOSE 8443         # HTTPS API
EXPOSE 5005         # Java debug port

# EXPOSE does NOT publish ports!
# You still need -p when running:
docker run -p 8081:8081 foodexpress/order-service:1.0
```

### Port Mapping Options

```bash
# Specific mapping
docker run -p 8081:8081 myapp        # host:container

# Random host port
docker run -p 8081 myapp             # Random host port -> 8081

# All exposed ports to random host ports
docker run -P myapp                  # Publishes all EXPOSE ports

# Bind to specific interface
docker run -p 127.0.0.1:8081:8081 myapp   # Only localhost
```

---

## CMD vs ENTRYPOINT -- The Key Difference

```dockerfile
# CMD -- Default command, can be overridden
FROM eclipse-temurin:17-jre-alpine
CMD ["java", "-jar", "app.jar"]

# Override CMD at runtime:
docker run myapp                     # Runs: java -jar app.jar
docker run myapp echo hello          # Runs: echo hello (CMD replaced!)

# ENTRYPOINT -- Fixed command, CMD becomes arguments
FROM eclipse-temurin:17-jre-alpine
ENTRYPOINT ["java"]
CMD ["-jar", "app.jar"]

# Override only arguments:
docker run myapp                     # Runs: java -jar app.jar
docker run myapp -version            # Runs: java -version
```

---

## CMD vs ENTRYPOINT -- Decision Table

| Scenario | Use | Example |
|----------|-----|---------|
| Simple app with one command | CMD | `CMD ["node", "server.js"]` |
| App that should always run one binary | ENTRYPOINT + CMD | `ENTRYPOINT ["java"]` + `CMD ["-jar", "app.jar"]` |
| Need to pass flags at runtime | ENTRYPOINT | `docker run myapp --debug` |
| Script wrapper with app as default | ENTRYPOINT script + CMD app | `ENTRYPOINT ["entrypoint.sh"]` |
| Need full flexibility | CMD only | `CMD ["python", "manage.py", "runserver"]` |

### Shell Form vs Exec Form

```dockerfile
# Shell form (NOT recommended)
CMD java -jar app.jar                # Runs as: /bin/sh -c "java -jar app.jar"
                                     # PID 1 = sh, java is child
                                     # SIGTERM goes to sh, not java

# Exec form (recommended)
CMD ["java", "-jar", "app.jar"]      # java is PID 1
                                     # Receives SIGTERM directly
                                     # Graceful shutdown works
```

---

## Multi-Stage Builds

### Problem: Build tools bloat the production image

```dockerfile
# WITHOUT multi-stage: 800MB image!
FROM maven:3.9-eclipse-temurin-17
WORKDIR /app
COPY . .
RUN mvn package -DskipTests
CMD ["java", "-jar", "target/app.jar"]
# Image includes: Maven, JDK, source code, test deps, build cache
```

### Solution: Multi-stage build

```dockerfile
# Stage 1: Build (discarded after use)
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime (final image, only ~200MB)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar
EXPOSE 8081
CMD ["java", "-jar", "app.jar"]
```

---

## Multi-Stage Build -- Size Comparison

```
Single-stage:          Multi-stage:
┌──────────────────┐  ┌──────────────────┐
│ Maven 3.9         │  │                  │
│ JDK 17            │  │                  │
│ Source code        │  │ JRE 17 (alpine)  │
│ Test dependencies  │  │ app.jar          │
│ Build cache        │  │                  │
│ JRE 17             │  │                  │
│ app.jar            │  │                  │
├──────────────────┤  ├──────────────────┤
│    ~800 MB        │  │    ~200 MB       │
└──────────────────┘  └──────────────────┘

75% smaller image!
```

> **FoodExpress:** Multi-stage builds reduced our CI/CD pipeline time by 60% because smaller images push and pull faster.

---

## Building & Tagging Images

```bash
# Build with tag
docker build -t foodexpress/order-service:1.0.0 .

# Tag an existing image
docker tag foodexpress/order-service:1.0.0 \
           foodexpress/order-service:latest

# Multiple tags
docker build -t foodexpress/order-service:1.0.0 \
             -t foodexpress/order-service:latest .

# Tag for private registry
docker tag foodexpress/order-service:1.0.0 \
           123456789.dkr.ecr.ap-south-1.amazonaws.com/foodexpress/order-service:1.0.0
```

### Tagging Convention

```
foodexpress/order-service:1.0.0      # Semantic version
foodexpress/order-service:1.0.0-rc1  # Release candidate
foodexpress/order-service:a1b2c3d    # Git commit SHA
foodexpress/order-service:2026.08.04 # Date-based
```

---

## Publishing to Docker Hub

```bash
# 1. Login to Docker Hub
docker login
Username: foodexpress
Password: ****

# 2. Tag the image
docker tag order-service:1.0.0 foodexpress/order-service:1.0.0

# 3. Push to Docker Hub
docker push foodexpress/order-service:1.0.0

# 4. Verify on Docker Hub
# https://hub.docker.com/r/foodexpress/order-service

# Pull on another machine
docker pull foodexpress/order-service:1.0.0
```

---

## Publishing to Private Registry (AWS ECR)

```bash
# 1. Authenticate with AWS ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.ap-south-1.amazonaws.com

# 2. Create repository (one-time)
aws ecr create-repository --repository-name foodexpress/order-service

# 3. Tag for ECR
docker tag order-service:1.0.0 \
  123456789.dkr.ecr.ap-south-1.amazonaws.com/foodexpress/order-service:1.0.0

# 4. Push
docker push \
  123456789.dkr.ecr.ap-south-1.amazonaws.com/foodexpress/order-service:1.0.0
```

> **FoodExpress:** We use AWS ECR in the ap-south-1 (Mumbai) region for faster pulls from our production servers.

---

## Docker Volumes -- The Problem

### Containers are ephemeral

```bash
# Start MySQL container
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=secret mysql:8.0

# Add data
docker exec -it mysql-db mysql -uroot -psecret -e \
  "CREATE DATABASE foodexpress; USE foodexpress; CREATE TABLE orders(id INT);"

# Remove container
docker rm -f mysql-db

# Start new container
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=secret mysql:8.0

# DATA IS GONE! The orders table doesn't exist.
```

---

## Docker Volumes -- The Solution

```
Without Volume:                  With Volume:
┌───────────────────┐           ┌───────────────────┐
│ Container         │           │ Container         │
│ ┌───────────────┐ │           │ ┌───────────────┐ │
│ │ Writable Layer│ │           │ │ Writable Layer│ │
│ │ (DATA HERE)   │ │           │ │               │ │
│ └───────────────┘ │           │ └───────┬───────┘ │
│ ┌───────────────┐ │           │         │ mount   │
│ │ Image Layers  │ │           │ ┌───────▼───────┐ │
│ └───────────────┘ │           │ │ /var/lib/mysql│ │
└───────────────────┘           │ └───────┬───────┘ │
                                └─────────│─────────┘
Container removed =                       │
DATA LOST                       ┌─────────▼─────────┐
                                │ Docker Volume      │
                                │ (Host filesystem)  │
                                │ DATA PERSISTS      │
                                └───────────────────┘
```

---

## Volume Types

### 1. Named Volumes (Recommended)

```bash
# Create a named volume
docker volume create mysql-data

# Use it when running a container
docker run -d --name mysql-db \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8.0

# Volume persists after container is removed
docker rm -f mysql-db
docker volume ls    # mysql-data still exists!
```

---

## Volume Types (continued)

### 2. Bind Mounts (Host directory)

```bash
# Mount a host directory into the container
docker run -d --name order-svc \
  -v /opt/foodexpress/config:/app/config \
  -v /var/log/foodexpress:/app/logs \
  foodexpress/order-service:1.0

# Changes in /opt/foodexpress/config on host
# are immediately visible inside the container at /app/config
```

### 3. tmpfs Mounts (RAM only)

```bash
# Data stored in memory, never written to disk
docker run -d --name secure-svc \
  --tmpfs /app/secrets:rw,size=64m \
  foodexpress/payment-service:1.0

# Use for sensitive data that shouldn't persist on disk
```

---

## Volume Comparison

| Feature | Named Volume | Bind Mount | tmpfs |
|---------|-------------|-----------|-------|
| Managed by Docker | Yes | No | No |
| Location | Docker manages | You choose path | Memory |
| Persists after container removal | Yes | Yes (host dir) | No |
| Pre-populated with image data | Yes | No | No |
| Performance | Good | Good | Best (RAM) |
| Backup with `docker volume` | Yes | Manual | N/A |
| Best for | Databases, app data | Config, source code (dev) | Secrets, temp data |

---

## Volume Commands

```bash
# List volumes
docker volume ls

# Create a volume
docker volume create foodexpress-mysql-data

# Inspect a volume
docker volume inspect foodexpress-mysql-data

# Remove a volume
docker volume rm foodexpress-mysql-data

# Remove all unused volumes (CAREFUL!)
docker volume prune

# Backup a volume
docker run --rm -v mysql-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/mysql-backup.tar.gz /data
```

---

## FoodExpress Volume Strategy

```
┌─────────────────────────────────────────────────────┐
│  FoodExpress Docker Volumes                          │
│                                                      │
│  Named Volumes (managed by Docker):                  │
│  ├── fe-mysql-data    → /var/lib/mysql               │
│  ├── fe-redis-data    → /data                        │
│  └── fe-uploads       → /app/uploads                 │
│                                                      │
│  Bind Mounts (host directories):                     │
│  ├── /opt/fe/config/  → /app/config   (configs)      │
│  ├── /var/log/fe/     → /app/logs     (log files)    │
│  └── /opt/fe/ssl/     → /app/certs    (TLS certs)    │
│                                                      │
│  tmpfs (memory only):                                │
│  └── /app/secrets     → payment service secrets      │
└─────────────────────────────────────────────────────┘
```

---

## .dockerignore File

### Keep build context small

```
# .dockerignore
.git
.gitignore
node_modules
npm-debug.log
target
*.class
*.jar
!target/order-service-*.jar
Dockerfile
docker-compose*.yml
*.md
.env
.env.*
tests
__pycache__
.idea
.vscode
```

> Without `.dockerignore`, `COPY . .` sends the entire directory (including `.git` and `node_modules`) to the Docker daemon. For FoodExpress, this reduced build context from 500MB to 2MB.

---

## Image Best Practices Summary

| Practice | Why |
|----------|-----|
| Use specific base image tags | Reproducible builds |
| Minimize layers (combine RUN) | Smaller image |
| Order: least-changing first | Better cache usage |
| Use multi-stage builds | Smaller production image |
| Don't install unnecessary packages | Smaller attack surface |
| Use .dockerignore | Faster builds |
| Run as non-root USER | Security |
| Use COPY, not ADD (usually) | Predictable behavior |
| Set HEALTHCHECK | Orchestrator monitoring |
| Label your images | Metadata for tracking |

---

## MCQ -- Quick Check 1

**Question:** You change one line of JavaScript code and rebuild. Which Dockerfile rebuilds faster?

A) `COPY . . && RUN npm install`
B) `COPY package*.json ./ && RUN npm ci && COPY . .`

> **Answer:** B -- The `package*.json` hasn't changed, so `npm ci` is cached. Only the final `COPY . .` runs. In A, every code change re-runs `npm install`.

---

## MCQ -- Quick Check 2

**Question:** What is the purpose of a multi-stage Docker build?

A) To run multiple containers at once
B) To reduce the final image size by separating build and runtime dependencies
C) To add more layers to the image
D) To run tests in parallel

> **Answer:** B -- Multi-stage builds use one stage for building (with JDK, Maven, etc.) and copy only the artifact to a minimal runtime stage.

---

## MCQ -- Quick Check 3

**Question:** You run `docker run -v mydata:/app/data myapp` and then `docker rm myapp`. What happens to the data?

A) Data is deleted with the container
B) Data persists in the named volume "mydata"
C) Data is moved to /tmp
D) Data is corrupted

> **Answer:** B -- Named volumes persist independently of containers. You must explicitly `docker volume rm mydata` to delete it.

---

## MCQ -- Quick Check 4

**Question:** Which Dockerfile instruction should you prefer for copying local files?

A) ADD
B) COPY
C) RUN cp
D) VOLUME

> **Answer:** B -- COPY is simpler and more predictable. ADD has extra features (URL download, tar extraction) that can cause unexpected behavior. Use COPY by default.

---

## MCQ -- Quick Check 5

**Question:** Why should containers use exec form `CMD ["java", "-jar", "app.jar"]` instead of shell form `CMD java -jar app.jar`?

A) Exec form is faster
B) Shell form doesn't work on alpine
C) Exec form makes the process PID 1, enabling correct signal handling for graceful shutdown
D) Shell form uses more memory

> **Answer:** C -- With exec form, `java` is PID 1 and receives SIGTERM directly. With shell form, `/bin/sh` is PID 1 and may not forward signals, preventing graceful shutdown.

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | Docker images are built from layers; each instruction = one layer |
| 2 | Order Dockerfile instructions for maximum cache efficiency (least-changing first) |
| 3 | Multi-stage builds separate build tools from runtime, reducing image size 50-75% |
| 4 | Use COPY (not ADD) for predictable file copying |
| 5 | Use exec form for CMD/ENTRYPOINT so processes receive signals correctly |
| 6 | Named volumes persist data beyond container lifecycle |
| 7 | Bind mounts are best for config files and development; named volumes for databases |
| 8 | Always use .dockerignore to keep build context small |

> **Next: Module 26 -- Docker Part 3: Networking, Docker Compose, Multi-Container Deployments**
