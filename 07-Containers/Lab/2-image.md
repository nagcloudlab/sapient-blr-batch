# Lab 2: Docker Images

## Objectives

By the end of this lab you will be able to:

- Explain what a Docker image is and how it is structured in layers
- Pull images from Docker Hub using tags and digests
- Inspect image metadata and layer history
- Tag, build, and push images to a private registry
- Write a Dockerfile for an Express.js and a Spring Boot application
- Use build arguments and multi-architecture builds
- Apply Dockerfile best practices to produce lean, production-ready images

---

## What is a Docker Image?

- A Docker image is a read-only template used to create containers
- Think of it as a "snapshot" of a filesystem combined with metadata that tells Docker how to run the container
- Images are never modified directly — you always build a new image or create a container from one
- Images are made up of stacked, read-only layers
- Each instruction in a Dockerfile that changes the filesystem adds a new layer
- Docker reuses (caches) layers that have not changed, which makes builds and pulls much faster

```
+---------------------------+
|    Your App Code          |  <-- Layer 4 (your changes)
+---------------------------+
|    npm install / deps     |  <-- Layer 3
+---------------------------+
|    Node.js / JDK          |  <-- Layer 2
+---------------------------+
|    Ubuntu / Alpine        |  <-- Layer 1 (Base Image)
+---------------------------+
```

Key points:

- Each layer is cached and shared across images. If two images share the same base layer, Docker stores that layer only once on disk.
- Images are identified by `registry/repository:tag` (e.g., `docker.io/library/redis:latest`) or by an immutable digest (e.g., `redis@sha256:48c1...`).
- A container is simply a running image with one thin writable layer added on top.

---

## Part 1: Exploring Images on Docker Hub

- Docker Hub (`hub.docker.com`) is the default public registry
- A registry is a server that stores and serves Docker images — the same way npm serves JavaScript packages or Maven Central serves Java jars
- Two categories of images exist on Docker Hub:
  - **Official images** — maintained by Docker or the upstream project team (e.g., `redis`, `node`, `postgres`). These are vetted, regularly updated, and safe to use as base images.
  - **Unofficial / community images** — published by individuals or organisations (e.g., `nagabhushanamn/greeting-service`). Treat these with the same caution you would any third-party code.

How images flow from Docker Hub to a running container:

```
Docker Hub
(hub.docker.com)
      |
      |  docker pull
      v
Local Image Store
(your machine's disk)
      |
      |  docker run
      v
Running Container
```

---

## Part 2: Pull and Inspect Images

### List images already on your machine

```bash
docker images
docker image ls
```

- Both commands show the same output
- `docker image ls` is the newer, more explicit form

### Pull the latest Redis image

```bash
docker pull docker.io/redis:latest
docker pull redis
```

- Both commands are identical
- When you omit the registry, Docker assumes `docker.io`
- When you omit the tag, Docker assumes `latest`
- The full form is always `registry/repository:tag`

### Pull an image using a specific tag

```bash
docker pull redis:6.0.9
docker image ls
```

- `latest` is just a convention — it is not automatically the newest image and it changes over time
- Pinning to a specific tag like `6.0.9` means your build will always use exactly that version
- Pinned tags make your builds reproducible

### Pull an image using a specific digest

```bash
docker pull redis@sha256:48c1431bed43fb2645314e4a22d6ca03cf36c5541d034de6a4f3330e7174915b
docker image ls
```

- A digest is a SHA256 hash of the image manifest
- Unlike a tag, a digest can never be reassigned to a different image
- Use digests in production pipelines where you need a 100% immutable reference
- Digests protect you from a tag being silently updated to a different image

### Pull an unofficial image

```bash
docker pull docker.io/nagabhushanamn/greeting-service:v1
docker image ls
```

- This image lives in a personal namespace (`nagabhushanamn`) rather than the official `library` namespace
- The pull syntax is identical to pulling official images

### Inspect image metadata

```bash
docker inspect redis
```

- `docker inspect` returns a large JSON document
- The most useful fields for beginners are:

| Field | What it tells you |
|---|---|
| `RootFS.Layers` | The SHA256 digests of every layer that makes up the image |
| `Config.Env` | Environment variables baked into the image |
| `Config.Cmd` | The default command run when you do `docker run` without extra arguments |
| `Config.ExposedPorts` | Ports the image author documented as used by the app (does not open them automatically) |
| `Architecture` | The CPU architecture the image was built for (amd64, arm64, etc.) |

### Show layer history and sizes

```bash
docker history redis
```

- Each row in the output is one layer
- The columns are:
  - `IMAGE` — the layer ID
  - `CREATED` — when the layer was created
  - `CREATED BY` — the Dockerfile instruction that produced this layer
  - `SIZE` — how much disk space this layer adds
  - `COMMENT` — optional note
- Use `docker history` to understand where an image's size comes from
- Large layers are often caused by installing packages without cleaning up the package manager cache in the same `RUN` instruction

---

## Part 3: Tag an Image

```bash
docker tag nagabhushanamn/greeting-service:v1 nagabhushanamn/greeting-service:tng
docker image ls
```

- Tagging does not copy the image or any of its layers
- It creates an alias — a new name that points to the exact same image data
- You can confirm this by looking at the `IMAGE ID` column in `docker image ls` — both `v1` and `tng` will show the same ID
- Tagging is also how you prepare an image for pushing to a different registry
- To push to a private registry at `localhost:5000`, first tag the image with that registry prefix, then push

---

## Part 4: Explore Image Layers with Dive

- Dive is an open-source tool that lets you navigate image layers interactively
- It shows exactly which files were added, modified, or deleted in each layer

### Install Dive (Ubuntu/Debian)

```bash
DIVE_VERSION=$(curl -sL "https://api.github.com/repos/wagoodman/dive/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
curl -OL https://github.com/wagoodman/dive/releases/download/v${DIVE_VERSION}/dive_${DIVE_VERSION}_linux_amd64.deb
sudo apt install ./dive_${DIVE_VERSION}_linux_amd64.deb
```

### Explore an image

```bash
dive nagabhushanamn/greeting-service:v1
```

- In the Dive UI, use the arrow keys to select a layer on the left panel
- Use the Tab key to switch to the filesystem view on the right
- Look for:
  - **Large layers** — a single layer that is much bigger than the others often means package caches were not cleaned up
  - **Wasted space** — files added in one layer and deleted in a later layer still consume disk space in the final image because each layer is immutable

---

## Part 5: Build an Express.js Image

### What is a Dockerfile?

- A Dockerfile is a plain-text recipe that tells Docker how to build an image
- Each instruction becomes a layer
- Docker reads the file top to bottom, executing each instruction in order

### A simple Express.js Dockerfile

```dockerfile
FROM node:18-alpine          # Base image — Node.js 18 on Alpine Linux
WORKDIR /app                 # Set working directory inside the container
COPY package*.json ./        # Copy dependency files first (layer caching!)
RUN npm install              # Install dependencies
COPY . .                     # Copy the rest of the app source code
EXPOSE 8080                  # Document that the app listens on port 8080
CMD ["node", "server.js"]    # Default command when the container starts
```

### What each instruction does

| Instruction | Purpose |
|---|---|
| `FROM` | Declares the base image. Every Dockerfile must start with FROM. |
| `WORKDIR` | Sets the current directory for all subsequent instructions. Creates the directory if it does not exist. |
| `COPY` | Copies files from your machine (build context) into the image. |
| `RUN` | Executes a shell command during the build and saves the result as a new layer. |
| `EXPOSE` | Documents which port the application uses. It is metadata only — it does not publish the port. |
| `CMD` | Defines the default command to run when a container starts. Can be overridden at `docker run`. |

### Why copy package.json before the source code?

- Docker caches each layer
- If you copy your source code first and then run `npm install`, Docker re-runs `npm install` every time any source file changes
- By copying `package*.json` first, Docker only re-runs `npm install` when your dependencies actually change
- This can save minutes on every build

### Create a .dockerignore file

Before building, always create a `.dockerignore` file in the same directory as your Dockerfile. This prevents unnecessary files from being sent to the Docker daemon during build:

```
node_modules
.git
.gitignore
*.log
.DS_Store
README.md
```

- Without `.dockerignore`, Docker sends everything in the current directory (the "build context") to the daemon
- This can include `node_modules` (hundreds of MB) or `.git` history, slowing every build
- Think of it as `.gitignore` but for Docker builds

### Build and run the Express.js image

The project files are already provided in `Lab/services/node-web-service/`. Navigate there:

```bash
cd /path/to/07-Containers/Lab/services/node-web-service
ls
# You should see: server.js  package.json  .dockerignore
```

Here is what each file contains:

`server.js`:

```javascript
const express = require('express');
const app = express();

app.get('/api/info', (req, res) => {
  res.json({ service: 'node-web-service', version: '1.0.0' });
});

app.listen(8080, () => console.log('Listening on port 8080'));
```

`package.json`:

```json
{
  "name": "node-web-service",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

Now write a `Dockerfile` in this directory (the lab teaches you the instructions above) and build:

```bash
docker build -t node-web-service:v1 .
docker image ls
docker run -d -p 8080:8080 node-web-service:v1
```

Verification:

```bash
curl http://localhost:8080/api/info
```

Expected output:

```json
{"service":"node-web-service","version":"1.0.0"}
```

---

## Part 6: Build a Spring Boot Image

### The multi-stage Spring Boot Dockerfile

- Spring Boot applications are compiled from Java source code into a JAR file using Maven
- A naive approach puts the entire Maven toolchain into the final image, making it very large (~800MB)
- The solution is a **multi-stage build**: compile in one stage, run in a second minimal stage

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

### How the two stages work

- **Stage 1 (builder)** — uses the full Maven image to compile Java source code into a JAR file
  - `RUN mvn dependency:go-offline` downloads all dependencies first, so they are cached as a separate layer
  - `RUN mvn package -DskipTests` compiles the source and packages the JAR
- **Stage 2 (runtime)** — starts fresh from a slim JRE-only Alpine image
  - `COPY --from=builder` copies only the compiled JAR from Stage 1 — nothing else
  - No compiler, no Maven, no source code ends up in the final image
  - Result: image shrinks from ~800MB down to ~200MB

### Run the Spring Boot image

The project files are already provided in `Lab/services/java-web-service/`. Navigate there and write a `Dockerfile` using the multi-stage pattern above:

```bash
cd /path/to/07-Containers/Lab/services/java-web-service
ls
# You should see: pom.xml  src/  .dockerignore
docker build -t java-web-service:v1 .
docker image ls
docker run -d -p 8080:8080 -e SPRING_PROFILES_ACTIVE=stage java-web-service:v1
curl http://localhost:8080/api/info
```

### Understanding the flags

**Port mapping: `-p 8080:8080`**

- The format is `host_port:container_port`
- The container has its own isolated network — without port mapping, nothing outside the container can reach the application
- The `-p` flag creates a rule that forwards traffic from port 8080 on your machine to port 8080 inside the container

```
Host Machine                       Container
+--------------------+           +--------------------+
|                    |           |                    |
|  localhost:8080 ---+-----------+---> :8080 (app)   |
|                    |           |                    |
+--------------------+           +--------------------+
         ^
         |
    curl / browser
```

**Environment variable: `-e SPRING_PROFILES_ACTIVE=stage`**

- The `-e` flag injects an environment variable into the container at runtime
- Spring Boot reads `SPRING_PROFILES_ACTIVE` to decide which `application-{profile}.yml` file to load
- This lets you use the same image in dev, stage, and production by changing only the environment variable — the image itself does not change

---

## Part 7: Build Arguments (ARG vs ENV)

- Build arguments let you pass values into the Docker build process without hardcoding them in the Dockerfile
- This is useful for changing the build behaviour without editing the Dockerfile

Example Dockerfile using `ARG`:

```dockerfile
FROM node:18-alpine
ARG APP_PORT=8080
ENV PORT=${APP_PORT}
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE ${APP_PORT}
CMD ["node", "server.js"]
```

Build and run with a custom port:

```bash
cd /path/to/07-Containers/Lab/services/node-web-service

# Build with default port (8080)
docker build -t node-web-service:v1 .

# Build with a custom port passed at build time
docker build --build-arg APP_PORT=3000 -t node-web-service:v2 .
docker run -d -p 3000:3000 node-web-service:v2
curl http://localhost:3000/api/info
```

### ARG vs ENV — what is the difference?

| | ARG | ENV |
|---|---|---|
| Available during | Build time only | Build time AND runtime |
| Visible in running container | No | Yes (`docker inspect` shows it) |
| Set with | `--build-arg KEY=VALUE` | `-e KEY=VALUE` at `docker run` |
| Use case | Controlling build behaviour (e.g., which file to copy) | Application configuration (e.g., database URL) |

- Do not put secrets in either ARG or ENV
- ARG values are visible in `docker history`
- ENV values are visible in `docker inspect`
- Use Docker secrets or a secrets manager for credentials

---

## Part 8: Multi-Architecture Builds

### Prerequisites — enable buildx

`docker buildx` is included with Docker Engine 19.03+ but needs a builder instance for multi-platform builds:

```bash
# Check if buildx is available
docker buildx version

# Create and use a new builder that supports multi-platform
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap
```

- The default builder only supports your host architecture
- The `multiarch` builder uses QEMU emulation to build for other architectures
- You only need to do this setup once

### Build for multiple CPU architectures

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t java-web-service:v1 .
docker image ls
docker inspect greeting-service:v1
```

### Pull an image for a specific architecture

```bash
docker pull --platform linux/arm64 redis
docker image ls
```

### Why multi-architecture matters

- Cloud servers typically run on `linux/amd64` (Intel/AMD x86-64)
- Apple Silicon Macs (M1, M2, M3) run on `arm64`
- If you build an image on your Mac and push it as `amd64` only, it will not run on an ARM-based cloud instance, and vice versa
- Building for both architectures means the same image tag works everywhere

Verify the architecture of a pulled image:

```bash
docker inspect redis | grep Architecture
```

---

## Part 9: Private Registry

- A private registry is your own image server
- You run it inside your infrastructure instead of using Docker Hub

### Why use a private registry?

- **Security** — your proprietary application images never leave your network
- **Speed** — images are pulled from a local server rather than over the internet
- **Air-gapped environments** — some production environments have no internet access at all

### How images flow with a private registry

```
Developer                  Private Registry             Server / CI
                           (localhost:5000)
    |                            |                          |
    |--- docker build ---------->|                          |
    |--- docker push ----------->|                          |
    |                            |<--- docker pull ---------|
    |                            |                          |
```

### Start a local registry

```bash
docker run -d -p 5000:5000 --name registry registry:2
docker ps
```

Verification — the catalog should be empty at first:

```bash
curl http://localhost:5000/v2/_catalog
```

Expected output: `{"repositories":[]}`

### Tag and push to the private registry

```bash
docker tag java-web-service:v1 localhost:5000/java-web-service:v1
docker image ls
docker push localhost:5000/java-web-service:v1
```

Verification — the image should now appear in the catalog:

```bash
curl http://localhost:5000/v2/_catalog
```

Expected output: `{"repositories":["java-web-service"]}`

### Pull from the private registry

```bash
docker pull localhost:5000/java-web-service:v1
docker image ls
```

---

## Part 10: Dockerfile Best Practices

### 1. Use official base images

```dockerfile
FROM node:18-alpine    # Good
FROM somerandomperson/node-custom   # Risky
```

- Official images are maintained by Docker or the upstream project
- They receive security patches promptly and are regularly audited
- Community images may contain outdated packages, malware, or simply stop being maintained

### 2. Minimize the number of layers by combining commands

```dockerfile
# Bad — creates 3 layers, each one caches the intermediate state
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good — one layer, cache is cleaned in the same step
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

- Every `RUN` instruction creates a layer
- Files deleted in a later layer are still present in earlier layers and count towards the final image size
- Combining into one `RUN` keeps the image smaller

### 3. Use multi-stage builds to reduce image size

Express.js multi-stage build:

```dockerfile
# Stage 1: Install only production dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Run — only the app code and production node_modules
FROM node:18-alpine
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY server.js .
EXPOSE 8080
CMD ["node", "server.js"]
```

Spring Boot multi-stage build:

```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Run — only the compiled JAR, no Maven, no source code
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

Side-by-side comparison:

| Concern | Express.js | Spring Boot |
|---|---|---|
| Builder base image | `node:18-alpine` | `maven:3.9-eclipse-temurin-21` |
| Build command | `npm ci --only=production` | `mvn package -DskipTests` |
| Runtime base image | `node:18-alpine` | `eclipse-temurin:21-jre-alpine` |
| What is copied to runtime | `node_modules` + `server.js` | compiled `*.jar` |
| Typical image size reduction | ~400MB -> ~180MB | ~800MB -> ~200MB |

- Multi-stage builds discard compilers, build tools, and source code
- Only the final artifact (JAR or compiled Node app) lands in the runtime image
- The runtime image has a much smaller attack surface

### 4. Use .dockerignore to exclude unnecessary files

Create a `.dockerignore` file in the same directory as your Dockerfile:

```
node_modules
.git
.gitignore
*.log
target
.DS_Store
README.md
```

- The Docker build context is everything in the current directory sent to the Docker daemon before the build starts
- Without `.dockerignore`, `node_modules` (potentially hundreds of MB) or `.git` history is sent every time
- This slows every build even if those files are never used inside the image

### 5. Pin dependency versions

```dockerfile
FROM node:18.20.4-alpine3.20    # Pinned — reproducible
FROM node:18-alpine             # Floating — may change tomorrow
```

- A floating tag like `node:18-alpine` resolves to a different image each time the upstream maintainer updates it
- Pinning to a full version ensures your builds are reproducible
- A new base image cannot silently break your application when you pin versions

### 6. Use COPY instead of ADD

```dockerfile
COPY app.tar.gz /app/    # Good — just copies the file
ADD  app.tar.gz /app/    # Avoid — automatically extracts archives
```

- `ADD` has two special behaviours: it auto-extracts tar archives and it can fetch files from URLs
- These implicit behaviours make Dockerfiles harder to reason about
- Use `COPY` for all local files
- Use `RUN curl` or `RUN wget` if you need to fetch from a URL, so the intention is explicit

### 7. Order instructions from least to most frequently changed (layer caching)

```
Time 0 — First build
+-----------+   +-----------+   +-----------+   +-----------+
|  FROM     |-->| COPY pkgs |-->| RUN       |-->| COPY src  |
|  (cached) |   | (cached)  |   | npm i     |   | (new)     |
+-----------+   +-----------+   (cached)        +-----------+
                                                      |
                                                 CMD  v

Time 1 — You change server.js
  FROM     -> still cached
  COPY pkgs -> still cached (package.json unchanged)
  RUN npm i -> still cached
  COPY src  -> INVALIDATED (server.js changed)
  CMD       -> rebuilt
```

- When a layer changes, every layer after it is rebuilt
- Put instructions that change rarely (installing system packages, copying `package.json`) near the top
- Put instructions that change often (copying your source code) near the bottom
- This keeps rebuilds fast

---

## Part 11: HEALTHCHECK in Dockerfiles

- A `HEALTHCHECK` instruction tells Docker how to test whether your container's application is actually working
- Without it, Docker only knows if the process is running — not if it's responding to requests

### Express.js Dockerfile with healthcheck

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/api/health || exit 1
CMD ["node", "server.js"]
```

### Spring Boot Dockerfile with healthcheck

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 \
  CMD wget --spider -q http://localhost:8080/actuator/health || exit 1
CMD ["java", "-jar", "app.jar"]
```

- `--start-period=30s` gives Spring Boot time to start before checks begin counting
- Spring Boot Actuator provides `/actuator/health` out of the box

### Check container health status

```bash
docker ps
# HEALTH column shows: starting, healthy, or unhealthy

docker inspect --format '{{.State.Health.Status}}' <container_name>
```

---

## Part 12: Registry Authentication

- Lab Part 9 showed a local registry without authentication
- In production you will push/pull from authenticated registries

### Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
# Credentials are stored in ~/.docker/config.json

docker push yourusername/myimage:v1
docker logout
```

### Cloud registries (overview)

| Cloud Provider | Registry | Login Command |
|---------------|----------|---------------|
| AWS | ECR | `aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com` |
| Google Cloud | GCR/Artifact Registry | `gcloud auth configure-docker` |
| Azure | ACR | `az acr login --name <registry_name>` |

- The pattern is always: authenticate first, then `docker push`/`docker pull` as normal
- CI/CD pipelines use service accounts or tokens instead of interactive login

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `COPY failed: file not found` | File path is wrong or file is excluded by `.dockerignore` | Check the file exists in the build context directory and is not in `.dockerignore` |
| `npm install` fails with network errors | Build environment has no internet access | Check DNS and network; use `--network=host` during build if needed |
| Image is unexpectedly large (500MB+) | Dev dependencies included, or no multi-stage build | Use `npm ci --only=production`, add multi-stage build, check with `docker history` |
| `WORKDIR` directory does not exist | Not an error — `WORKDIR` creates it automatically | This is expected behaviour |
| Layer cache not working | Changed a file in an earlier COPY step | Reorder Dockerfile: copy dependency files first, source code last |
| `exec format error` when running container | Image built for wrong architecture | Rebuild with `--platform linux/amd64` or use `docker buildx` |
| `denied: requested access to the resource is denied` | Not logged in or wrong registry prefix | Run `docker login` and ensure the image tag includes the correct registry/namespace |

---

## Challenges

These exercises are optional but strongly recommended. Each one reinforces a concept from this lab.

**Challenge 1 — Build an Express.js "Hello World" image from scratch**

- Create a new directory
- Inside it, write a `server.js` using Express.js that responds with `{"message": "hello world"}` on `GET /`
- Add a `package.json` with `express` as a dependency
- Write a `Dockerfile`, build the image, run a container, and verify the response with `curl`

**Challenge 2 — Find the largest layer**

- Run `docker history node-web-service:v1` (or any image you built)
- Identify which layer contributes the most to the image size
- Think about what that layer does and whether there is a way to reduce it

**Challenge 3 — Multi-stage build for a Java app**

- Write a two-stage Dockerfile: the first stage uses `maven:3.9-eclipse-temurin-21` to compile a Spring Boot jar
- The second stage uses `eclipse-temurin:21-jre-alpine` to run it
- Compare the final image size to a single-stage build using the full Maven image

**Challenge 4 — Push to your private registry and pull it back**

- Start the local registry (`registry:2`)
- Tag one of your images with the `localhost:5000/` prefix and push it
- Delete the local copy with `docker rmi`
- Pull it back from the registry and confirm the container runs correctly

**Challenge 5 — Observe layer caching in action**

- Build any of your Dockerfiles twice in a row
- On the second build, watch the output and note how Docker prints `CACHED` for each layer
- Now change one line in your source code and build again
- Observe which layers are rebuilt and which are still served from cache
