# Docker Part 1 -- Introduction to Containerization
## Module 24 | Sustain Engineering Training | Day 27

---

## Agenda -- Day 27

| # | Topic |
|---|-------|
| 01 | Why Containers? The Problem with Traditional Deployment |
| 02 | Virtualization vs Containerization |
| 03 | Docker Architecture & Components |
| 04 | Docker Daemon, Client & CLI |
| 05 | Docker Images & Containers |
| 06 | Docker Registry & Docker Hub |
| 07 | Writing Your First Dockerfile |
| 08 | Dockerfile for FoodExpress Order Service |
| 09 | Building & Running Containers |
| 10 | Lab: Fix the Dockerfile |
| 11 | Day Wrap-up & Key Takeaways |

---

## The Deployment Problem

### "It Works on My Machine"

```
Developer Laptop          Staging Server           Production Server
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Java 17      │         │ Java 11      │         │ Java 17      │
│ Node 18      │         │ Node 16      │         │ Node 20      │
│ MySQL 8.0    │         │ MySQL 5.7    │         │ MySQL 8.0    │
│ Ubuntu 22.04 │         │ CentOS 7     │         │ Ubuntu 20.04 │
│              │         │              │         │              │
│  "Works!"    │         │  "Broken!"   │         │  "Random     │
│              │         │              │         │   crashes!"  │
└──────────────┘         └──────────────┘         └──────────────┘
```

> **FoodExpress:** The Order Service works on developer laptops but crashes in production because of Java version mismatch and missing native libraries.

---

## What is Docker?

### Open platform for developing, shipping, and running applications

- **Package** your application with ALL its dependencies
- **Ship** the same package to any environment
- **Run** consistently on any machine with Docker installed

```
┌─────────────────────────────────────────────┐
│           Docker Container                   │
│                                              │
│  ┌──────────┐ ┌────────────┐ ┌───────────┐ │
│  │ Your App │ │ Runtime    │ │ Libraries │ │
│  │ (JAR)    │ │ (Java 17)  │ │ (deps)    │ │
│  └──────────┘ └────────────┘ └───────────┘ │
│                                              │
│  Config files, env vars, everything needed   │
└─────────────────────────────────────────────┘
     Runs identically on ANY machine
```

---

## Docker Timeline & Adoption

| Year | Milestone |
|------|-----------|
| 2013 | Docker open-sourced by dotCloud |
| 2014 | Docker 1.0 released; Docker Hub launched |
| 2015 | Docker Compose; orchestration tools emerge |
| 2016 | Docker Swarm; Windows container support |
| 2017 | Kubernetes becomes dominant orchestrator |
| 2018 | Docker Enterprise; containerd donated to CNCF |
| 2020 | Docker Desktop licensing changes |
| 2023 | Docker Scout for vulnerability scanning |
| 2024+ | Docker + AI/ML workloads, GPU support |

---

## Virtualization vs Containerization

<!--VISUAL:vm-vs-container-->

```
     Virtual Machines                    Containers
┌──────────────────────┐         ┌──────────────────────┐
│ ┌────┐ ┌────┐ ┌────┐│         │ ┌────┐ ┌────┐ ┌────┐│
│ │App1│ │App2│ │App3││         │ │App1│ │App2│ │App3││
│ ├────┤ ├────┤ ├────┤│         │ ├────┤ ├────┤ ├────┤│
│ │Bins│ │Bins│ │Bins││         │ │Bins│ │Bins│ │Bins││
│ │Libs│ │Libs│ │Libs││         │ │Libs│ │Libs│ │Libs││
│ ├────┤ ├────┤ ├────┤│         │ └────┘ └────┘ └────┘│
│ │ OS │ │ OS │ │ OS ││         │    Docker Engine      │
│ └────┘ └────┘ └────┘│         ├──────────────────────┤
│    Hypervisor        │         │     Host OS           │
├──────────────────────┤         ├──────────────────────┤
│     Host OS          │         │     Hardware          │
├──────────────────────┤         └──────────────────────┘
│     Hardware         │
└──────────────────────┘

  Each VM: Full OS copy              Shared kernel
  Size: GBs                          Size: MBs
  Boot: Minutes                      Boot: Seconds
  Overhead: High                     Overhead: Low
```

---

## VM vs Container -- Detailed Comparison

| Feature | Virtual Machine | Container |
|---------|----------------|-----------|
| Isolation | Full (hardware level) | Process level (shared kernel) |
| Size | GBs (includes OS) | MBs (just app + libs) |
| Startup | Minutes | Seconds |
| Performance | ~5-10% overhead | Near-native |
| OS Support | Any OS on any host | Same kernel family |
| Density | 10-20 per host | 100s per host |
| Resource Usage | Fixed allocation | Dynamic, shared |
| Security | Stronger isolation | Kernel-level isolation |
| Use Case | Different OS, legacy apps | Microservices, CI/CD |

> **FoodExpress:** We run 12 microservices. With VMs, we'd need 12 OS instances. With containers, they share one kernel.

---

## Docker Architecture

<!--VISUAL:docker-architecture-->

```
┌─────────────────────────────────────────────────────┐
│                    Docker Host                       │
│                                                      │
│  ┌─────────────┐          ┌───────────────────────┐ │
│  │ Docker      │  REST    │   Docker Daemon       │ │
│  │ Client      │─────────▶│   (dockerd)           │ │
│  │             │  API     │                       │ │
│  │ docker run  │          │  ┌─────┐ ┌─────┐     │ │
│  │ docker build│          │  │Cont.│ │Cont.│     │ │
│  │ docker pull │          │  │  1  │ │  2  │     │ │
│  └─────────────┘          │  └─────┘ └─────┘     │ │
│                            │                       │ │
│                            │  ┌───────────────┐   │ │
│                            │  │  Local Images  │   │ │
│                            │  │  Cache         │   │ │
│                            │  └───────────────┘   │ │
│                            └───────────────────────┘ │
│                                      │               │
└──────────────────────────────────────│───────────────┘
                                       │ pull/push
                              ┌────────▼────────┐
                              │  Docker Registry │
                              │  (Docker Hub)    │
                              └─────────────────┘
```

---

## Docker Components Explained

### 1. Docker Daemon (dockerd)

- Background service running on the host
- Manages images, containers, networks, volumes
- Listens on Unix socket or TCP
- Handles all container lifecycle operations

```bash
# Check if Docker daemon is running
sudo systemctl status docker

# View daemon logs
sudo journalctl -u docker.service -f
```

---

## Docker Components -- Client

### 2. Docker Client (docker CLI)

- Command-line tool to interact with Docker daemon
- Sends REST API calls to dockerd
- Can connect to local or remote Docker daemons

```bash
# Common Docker Client commands
docker version          # Client and server versions
docker info             # System-wide information
docker ps               # List running containers
docker images           # List local images
docker run              # Create and start container
docker build            # Build image from Dockerfile
docker pull             # Download image from registry
docker push             # Upload image to registry
```

---

## Docker Components -- Images

### 3. Docker Images

- Read-only template for creating containers
- Built from a series of layers
- Each layer = one instruction in Dockerfile
- Stored locally and in registries

```
Docker Image: foodexpress/order-service:1.0

Layer 5: COPY app.jar /app/          ← Your code
Layer 4: RUN apt-get install curl    ← Dependencies
Layer 3: ENV JAVA_HOME=/usr/lib/jvm  ← Configuration
Layer 2: RUN apt-get update          ← System update
Layer 1: FROM eclipse-temurin:17     ← Base image

Each layer is cached. Only changed layers rebuild.
```

---

## Docker Components -- Containers

### 4. Docker Containers

- Running instance of an image
- Writable layer on top of read-only image
- Isolated process with its own filesystem, network, PID space
- Ephemeral by default (data lost when container removed)

```bash
# Container lifecycle
docker create nginx          # Create (not running)
docker start <id>            # Start created container
docker run nginx             # Create + Start (combined)
docker stop <id>             # Graceful stop (SIGTERM)
docker kill <id>             # Force stop (SIGKILL)
docker rm <id>               # Remove stopped container
docker rm -f <id>            # Force remove (running)
```

---

## Docker Components -- Registry

### 5. Docker Registry

- Stores and distributes Docker images
- **Docker Hub** -- public registry (default)
- **Private registries** -- AWS ECR, Azure ACR, GCP GCR, Harbor

```bash
# Working with registries
docker pull nginx:1.25                  # Pull from Docker Hub
docker pull myregistry.com/myapp:1.0    # Pull from private registry

docker tag myapp:1.0 myregistry.com/myapp:1.0   # Tag for registry
docker push myregistry.com/myapp:1.0             # Push to registry

# Login to private registry
docker login myregistry.com
```

> **FoodExpress:** We use AWS ECR to store our microservice images. Each service has its own repository: `foodexpress/order-service`, `foodexpress/payment-service`, etc.

---

## Image Naming Convention

### Understanding Image Tags

```
registry / repository : tag
─────────  ──────────   ───
docker.io / nginx     : 1.25
            library/    latest   (default tag)

Examples:
  nginx                    = docker.io/library/nginx:latest
  nginx:1.25               = docker.io/library/nginx:1.25
  mycompany/myapp:v2       = docker.io/mycompany/myapp:v2
  ecr.aws/foodexpress/order:1.0.3
```

| Convention | Example | When to Use |
|-----------|---------|-------------|
| `latest` | `nginx:latest` | Development only (never in prod!) |
| Semantic | `nginx:1.25.3` | Production deployments |
| Git SHA | `order:a1b2c3d` | CI/CD pipelines |
| Date | `order:2026-08-03` | Nightly builds |

---

## Docker Installation

### Platform-Specific Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Add user to docker group (avoid sudo)
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker run hello-world
```

### Docker Desktop vs Docker Engine

| Feature | Docker Desktop | Docker Engine |
|---------|---------------|---------------|
| Platform | Windows, Mac, Linux | Linux only |
| GUI | Yes | No (CLI only) |
| Licensing | Free for personal/small biz | Free (open source) |
| Includes | Compose, Kubernetes, GUI | Just the engine |
| Use Case | Development | Servers/Production |

---

## Your First Docker Commands

### Hello World

```bash
# Run your first container
$ docker run hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation is working.

# What happened:
# 1. Docker client contacted Docker daemon
# 2. Daemon pulled "hello-world" image from Docker Hub
# 3. Daemon created a container from the image
# 4. Container ran, printed message, exited
```

---

## Essential Docker Commands

### Container Management

```bash
# Run a container (interactive)
docker run -it ubuntu:22.04 /bin/bash

# Run in background (detached)
docker run -d --name my-nginx -p 8080:80 nginx:1.25

# List containers
docker ps                    # Running only
docker ps -a                 # All (including stopped)

# View logs
docker logs my-nginx
docker logs -f my-nginx      # Follow (like tail -f)

# Execute command in running container
docker exec -it my-nginx /bin/bash

# Inspect container details
docker inspect my-nginx
```

---

## Essential Docker Commands -- Images

### Image Management

```bash
# List local images
docker images

# Pull an image
docker pull eclipse-temurin:17-jre

# Remove an image
docker rmi nginx:1.25

# Remove all unused images
docker image prune -a

# Image history (see layers)
docker history nginx:1.25

# Search Docker Hub
docker search foodexpress
```

---

## Writing a Dockerfile

### Dockerfile = Blueprint for an Image

```dockerfile
# Every Dockerfile starts with FROM
FROM eclipse-temurin:17-jre-alpine

# Set working directory inside container
WORKDIR /app

# Copy files from host to container
COPY target/order-service-1.0.0.jar app.jar

# Set environment variables
ENV SPRING_PROFILES_ACTIVE=production
ENV SERVER_PORT=8081

# Document which port the app uses
EXPOSE 8081

# Command to run when container starts
CMD ["java", "-jar", "app.jar"]
```

---

## Dockerfile Directives -- Detailed

| Directive | Purpose | Example |
|-----------|---------|---------|
| `FROM` | Base image (required, must be first) | `FROM eclipse-temurin:17-jre` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host to image | `COPY app.jar /app/` |
| `ADD` | Like COPY but supports URLs, tar extraction | `ADD config.tar.gz /app/` |
| `RUN` | Execute command during build | `RUN apt-get update` |
| `ENV` | Set environment variable | `ENV PORT=8081` |
| `EXPOSE` | Document exposed port | `EXPOSE 8081` |
| `CMD` | Default command at container start | `CMD ["java", "-jar", "app.jar"]` |
| `ENTRYPOINT` | Fixed command (CMD becomes args) | `ENTRYPOINT ["java"]` |
| `LABEL` | Add metadata | `LABEL version="1.0"` |
| `USER` | Set non-root user | `USER appuser` |

---

## FoodExpress Order Service Dockerfile

### Real-World Example

```dockerfile
# Multi-stage build for smaller image
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy only the JAR from build stage
COPY --from=builder /build/target/order-service-*.jar app.jar

# Set environment
ENV SPRING_PROFILES_ACTIVE=production
ENV JAVA_OPTS="-Xms256m -Xmx512m"
EXPOSE 8081

# Run as non-root user
USER appuser

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

---

## Building an Image

### docker build

```bash
# Build from current directory
docker build -t foodexpress/order-service:1.0 .

# Build with specific Dockerfile
docker build -f Dockerfile.prod -t foodexpress/order-service:1.0 .

# Build output
Step 1/8 : FROM eclipse-temurin:17-jre-alpine
 ---> a1b2c3d4e5f6
Step 2/8 : WORKDIR /app
 ---> Running in 1234abcd
 ---> f6e5d4c3b2a1
Step 3/8 : COPY target/order-service-1.0.0.jar app.jar
 ---> 9876fedc
...
Successfully built abc123def456
Successfully tagged foodexpress/order-service:1.0
```

---

## Running the FoodExpress Container

### docker run with Options

```bash
# Basic run
docker run foodexpress/order-service:1.0

# Production run with all options
docker run -d \
  --name order-service \
  -p 8081:8081 \
  -e SPRING_PROFILES_ACTIVE=production \
  -e DB_HOST=mysql-host \
  -e DB_PASSWORD=secret \
  --restart unless-stopped \
  --memory 512m \
  --cpus 1.0 \
  foodexpress/order-service:1.0

# Verify
docker ps
curl http://localhost:8081/actuator/health
```

---

## docker run Flags Explained

| Flag | Purpose | Example |
|------|---------|---------|
| `-d` | Run in background (detached) | `docker run -d nginx` |
| `--name` | Assign a name | `--name order-service` |
| `-p` | Map host:container port | `-p 8081:8081` |
| `-e` | Set environment variable | `-e DB_HOST=mysql` |
| `-v` | Mount volume | `-v /data:/app/data` |
| `--restart` | Restart policy | `--restart unless-stopped` |
| `--memory` | Memory limit | `--memory 512m` |
| `--cpus` | CPU limit | `--cpus 1.5` |
| `--network` | Connect to network | `--network foodexpress-net` |
| `-it` | Interactive + terminal | `docker run -it ubuntu bash` |
| `--rm` | Remove after exit | `docker run --rm alpine echo hi` |

---

## Container vs Image -- Mental Model

```
            Image (Blueprint)              Container (Running Instance)
         ┌──────────────────┐           ┌──────────────────────┐
         │  Read-Only       │           │  Read-Write Layer    │
         │                  │           │  (your changes)      │
         │  Layer 3: COPY   │    run    ├──────────────────────┤
         │  Layer 2: RUN    │ ────────▶ │  Read-Only Layers    │
         │  Layer 1: FROM   │           │  (from image)        │
         └──────────────────┘           └──────────────────────┘

  docker images                          docker ps
  Can create many containers             Runs as isolated process
  Stored on disk                         Has own network, PID, filesystem
  Shared/reusable                        Ephemeral (data lost on remove)
```

> One image can run as many containers. Like a class (image) and objects (containers) in Java.

---

## Container Isolation -- What's Isolated?

| Resource | Isolated? | Details |
|----------|----------|---------|
| Filesystem | Yes | Each container has its own root filesystem |
| Process IDs | Yes | PID 1 inside container != PID 1 on host |
| Network | Yes | Own IP, ports, routing table |
| Users | Yes | Root in container != root on host (usually) |
| CPU/Memory | Configurable | Use --cpus, --memory to limit |
| Kernel | No | Shared with host (unlike VMs) |

---

## Docker in the FoodExpress Architecture

```
Host Machine (Linux Server)
┌──────────────────────────────────────────────────┐
│  Docker Engine                                    │
│                                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ order-svc   │ │ payment-svc │ │ restaurant │ │
│  │ :8081       │ │ :8082       │ │ :3000      │ │
│  │ Java 17     │ │ Java 17     │ │ Node 18    │ │
│  │ 512MB       │ │ 512MB       │ │ 256MB      │ │
│  └─────────────┘ └─────────────┘ └────────────┘ │
│                                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ mysql       │ │ redis       │ │ nginx      │ │
│  │ :3306       │ │ :6379       │ │ :80/:443   │ │
│  │ MySQL 8.0   │ │ Redis 7    │ │ Nginx 1.25 │ │
│  │ 1GB         │ │ 256MB       │ │ 128MB      │ │
│  └─────────────┘ └─────────────┘ └────────────┘ │
│                                                   │
│  All services packaged, versioned, reproducible   │
└──────────────────────────────────────────────────┘
```

---

## Common Dockerfile Mistakes

### What Sustain Engineers Fix Often

| Mistake | Problem | Fix |
|---------|---------|-----|
| `FROM ubuntu:latest` | Unpredictable, large image | Use specific tags: `FROM ubuntu:22.04` |
| Running as root | Security vulnerability | Add `USER appuser` |
| No `.dockerignore` | Build context too large | Add `.git`, `node_modules`, `target` |
| `COPY . .` before `RUN npm install` | Cache busted on every code change | Copy package.json first, install, then copy code |
| `RUN apt-get update && apt-get install` on separate lines | Update cached, install gets stale packages | Combine in single RUN |
| No health check | Orchestrator can't detect failures | Add `HEALTHCHECK` directive |

---

## MCQ -- Quick Check 1

**Question:** What is the main difference between a VM and a container?

A) Containers are slower than VMs
B) Containers share the host kernel; VMs have their own kernel
C) VMs are smaller than containers
D) Containers provide better security isolation than VMs

> **Answer:** B -- Containers share the host OS kernel, making them lightweight and fast to start. VMs include a full guest OS with its own kernel.

---

## MCQ -- Quick Check 2

**Question:** Which Dockerfile directive should be the FIRST line?

A) RUN
B) COPY
C) FROM
D) CMD

> **Answer:** C -- Every Dockerfile must start with `FROM` (or `ARG` before `FROM`). It defines the base image.

---

## MCQ -- Quick Check 3

**Question:** What happens when you run `docker run -d --name web -p 8080:80 nginx`?

A) Runs nginx in foreground on port 80
B) Creates a container named "web" running nginx, maps host port 8080 to container port 80, runs in background
C) Pulls nginx and shows its Dockerfile
D) Builds a new image called "web"

> **Answer:** B -- The `-d` flag runs detached (background), `--name web` names it, `-p 8080:80` maps host:container ports.

---

## MCQ -- Quick Check 4

**Question:** You see this error: `COPY failed: file not found in build context`. What's wrong?

A) Docker daemon is not running
B) The file you're trying to COPY doesn't exist relative to the Dockerfile location
C) The container doesn't have enough memory
D) The base image is corrupted

> **Answer:** B -- `COPY` works relative to the build context (usually the directory where you run `docker build`). The file must exist there.

---

## MCQ -- Quick Check 5

**Question:** Why should you NOT use `latest` tag in production?

A) It's slower to pull
B) It's always the oldest version
C) It's mutable -- it points to different images over time, making builds non-reproducible
D) Docker Hub doesn't support it

> **Answer:** C -- `latest` is a moving target. Today it might be v1.25, tomorrow v1.26. In production, use specific version tags for reproducible deployments.

---

## Lab Preview: Fix the FoodExpress Dockerfile

### What You'll Fix

The Order Service Dockerfile has **7 bugs** that prevent it from building and running correctly:

1. Wrong base image (not Java-compatible)
2. Missing COPY for the JAR file
3. Wrong EXPOSE port
4. Missing WORKDIR
5. Running as root (security issue)
6. No health check
7. Wrong CMD syntax

> You'll find the buggy Dockerfile in `Labs/starter-code/Dockerfile`

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | Docker solves "works on my machine" by packaging app + dependencies together |
| 2 | Containers share the host kernel -- lighter and faster than VMs |
| 3 | Docker architecture: Client -> Daemon -> Registry |
| 4 | Images are read-only templates; containers are running instances |
| 5 | Dockerfiles are blueprints: FROM, COPY, RUN, EXPOSE, CMD |
| 6 | Always use specific image tags in production, never `latest` |
| 7 | Run containers as non-root users for security |

> **Next: Module 25 -- Docker Part 2: Images, Layers, Dockerfile Deep Dive, Volumes**
