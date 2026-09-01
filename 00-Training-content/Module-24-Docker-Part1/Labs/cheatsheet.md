# Docker Quick Reference

> Single-page reference for Docker CLI, Dockerfile directives, and Docker Compose. FoodExpress examples used throughout.

---

## Images

| Command | Example | Description |
|---|---|---|
| `docker build -t <name>:<tag> <context>` | `docker build -t foodexpress-api:1.0 .` | Build image from Dockerfile in context dir |
| `docker build -f <file> -t <name> <ctx>` | `docker build -f Dockerfile.prod -t foodexpress-api:prod .` | Build using a specific Dockerfile |
| `docker build --no-cache -t <name> .` | `docker build --no-cache -t foodexpress-api:latest .` | Build without layer cache |
| `docker pull <image>:<tag>` | `docker pull node:20-alpine` | Download image from registry |
| `docker push <image>:<tag>` | `docker push registry.example.com/foodexpress-api:1.0` | Push image to registry |
| `docker tag <src> <dst>` | `docker tag foodexpress-api:1.0 registry.example.com/foodexpress-api:1.0` | Tag an image |
| `docker images` | `docker images` | List local images |
| `docker images -a` | `docker images -a` | List all images including intermediates |
| `docker rmi <image>` | `docker rmi foodexpress-api:old` | Remove image |
| `docker rmi $(docker images -q -f dangling=true)` | `docker rmi $(docker images -q -f dangling=true)` | Remove all dangling images |
| `docker image prune` | `docker image prune` | Remove all unused images |
| `docker image inspect <image>` | `docker image inspect foodexpress-api:1.0` | Show image metadata |
| `docker history <image>` | `docker history foodexpress-api:1.0` | Show layer history |
| `docker save -o <file> <image>` | `docker save -o api.tar foodexpress-api:1.0` | Export image to tar |
| `docker load -i <file>` | `docker load -i api.tar` | Import image from tar |

---

## Containers

| Command | Example | Description |
|---|---|---|
| `docker run <image>` | `docker run node:20-alpine` | Create and start a container |
| `docker run -d <image>` | `docker run -d foodexpress-api:1.0` | Run in detached (background) mode |
| `docker run -d -p <host>:<ctr> <image>` | `docker run -d -p 3000:3000 foodexpress-api:1.0` | Map host port to container port |
| `docker run -d --name <name> <image>` | `docker run -d --name fe-api foodexpress-api:1.0` | Assign container name |
| `docker run -e KEY=VALUE <image>` | `docker run -e NODE_ENV=production foodexpress-api:1.0` | Set environment variable |
| `docker run --env-file <file> <image>` | `docker run --env-file .env foodexpress-api:1.0` | Load env vars from file |
| `docker run -v <host>:<ctr> <image>` | `docker run -v /opt/data:/app/data foodexpress-api:1.0` | Bind-mount host path |
| `docker run -v <vol>:<ctr> <image>` | `docker run -v fe-data:/app/data foodexpress-api:1.0` | Mount named volume |
| `docker run --network <net> <image>` | `docker run --network fe-network foodexpress-api:1.0` | Attach to network |
| `docker run --rm <image>` | `docker run --rm node:20-alpine node --version` | Auto-remove container on exit |
| `docker run -it <image> <cmd>` | `docker run -it foodexpress-api:1.0 sh` | Interactive terminal |
| `docker start <container>` | `docker start fe-api` | Start a stopped container |
| `docker stop <container>` | `docker stop fe-api` | Stop container gracefully (SIGTERM) |
| `docker stop -t 5 <container>` | `docker stop -t 5 fe-api` | Stop with 5s timeout before SIGKILL |
| `docker restart <container>` | `docker restart fe-api` | Stop then start container |
| `docker kill <container>` | `docker kill fe-api` | Force-stop container (SIGKILL) |
| `docker rm <container>` | `docker rm fe-api` | Remove stopped container |
| `docker rm -f <container>` | `docker rm -f fe-api` | Force remove running container |
| `docker ps` | `docker ps` | List running containers |
| `docker ps -a` | `docker ps -a` | List all containers (including stopped) |
| `docker logs <container>` | `docker logs fe-api` | View container stdout/stderr |
| `docker logs -f <container>` | `docker logs -f fe-api` | Follow logs live |
| `docker logs --tail 100 <ctr>` | `docker logs --tail 100 fe-api` | Last 100 log lines |
| `docker exec -it <ctr> <cmd>` | `docker exec -it fe-api sh` | Run command inside running container |
| `docker exec <ctr> <cmd>` | `docker exec fe-api cat /etc/hosts` | Non-interactive exec |
| `docker inspect <container>` | `docker inspect fe-api` | Full container metadata (JSON) |
| `docker stats` | `docker stats` | Live CPU/memory/network stats |
| `docker stats <container>` | `docker stats fe-api` | Stats for specific container |
| `docker cp <ctr>:<path> <host>` | `docker cp fe-api:/app/app.log ./app.log` | Copy file from container to host |
| `docker cp <host> <ctr>:<path>` | `docker cp ./config.json fe-api:/app/config.json` | Copy file from host to container |

---

## Dockerfile Directives

| Directive | Example | Description |
|---|---|---|
| `FROM <image>:<tag>` | `FROM node:20-alpine` | Base image (must be first instruction) |
| `WORKDIR <path>` | `WORKDIR /app` | Set working directory for subsequent instructions |
| `COPY <src> <dst>` | `COPY package*.json ./` | Copy files from build context into image |
| `COPY --chown=user:group <src> <dst>` | `COPY --chown=node:node . .` | Copy with ownership |
| `ADD <src> <dst>` | `ADD https://example.com/file.tar.gz /tmp/` | Like COPY but also extracts archives and fetches URLs |
| `RUN <command>` | `RUN npm ci --omit=dev` | Execute command in a new layer during build |
| `RUN <cmd1> && <cmd2>` | `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*` | Chain commands in one layer |
| `ENV KEY=VALUE` | `ENV NODE_ENV=production` | Set environment variable (persists in image) |
| `ARG NAME=default` | `ARG APP_VERSION=1.0.0` | Build-time variable (`docker build --build-arg`) |
| `EXPOSE <port>` | `EXPOSE 3000` | Document the port the container listens on |
| `USER <user>` | `USER node` | Switch to non-root user |
| `VOLUME <path>` | `VOLUME ["/app/data"]` | Declare a mount point for external volumes |
| `CMD ["exec", "arg"]` | `CMD ["node", "server.js"]` | Default command (overridable at `docker run`) |
| `ENTRYPOINT ["exec", "arg"]` | `ENTRYPOINT ["node", "server.js"]` | Fixed entry point (not easily overridden) |
| `ENTRYPOINT + CMD` | `ENTRYPOINT ["node"]` + `CMD ["server.js"]` | ENTRYPOINT = executable, CMD = default args |
| `HEALTHCHECK --interval=30s --timeout=5s CMD <cmd>` | `HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:3000/health || exit 1` | Container health probe |
| `LABEL key=value` | `LABEL maintainer="naga@sapient.com" version="1.0"` | Image metadata |
| `ONBUILD <instruction>` | `ONBUILD COPY . /app` | Instruction deferred to child image builds |

**Multi-stage build example (FoodExpress API):**
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

---

## Docker Compose

| Command | Example | Description |
|---|---|---|
| `docker compose up` | `docker compose up` | Create and start all services |
| `docker compose up -d` | `docker compose up -d` | Start in detached mode |
| `docker compose up --build` | `docker compose up --build` | Rebuild images before starting |
| `docker compose up <service>` | `docker compose up api` | Start specific service only |
| `docker compose down` | `docker compose down` | Stop and remove containers, networks |
| `docker compose down -v` | `docker compose down -v` | Also remove named volumes |
| `docker compose down --rmi all` | `docker compose down --rmi all` | Also remove images |
| `docker compose build` | `docker compose build` | Build all service images |
| `docker compose build <service>` | `docker compose build api` | Build specific service |
| `docker compose build --no-cache` | `docker compose build --no-cache` | Build without cache |
| `docker compose logs` | `docker compose logs` | View logs for all services |
| `docker compose logs -f` | `docker compose logs -f` | Follow logs for all services |
| `docker compose logs -f <service>` | `docker compose logs -f api` | Follow logs for specific service |
| `docker compose ps` | `docker compose ps` | List service containers |
| `docker compose exec <svc> <cmd>` | `docker compose exec api sh` | Run command in running service container |
| `docker compose run <svc> <cmd>` | `docker compose run api npm test` | Run one-off command in new container |
| `docker compose restart <service>` | `docker compose restart api` | Restart a service |
| `docker compose stop <service>` | `docker compose stop api` | Stop a service |
| `docker compose pull` | `docker compose pull` | Pull latest images for all services |
| `docker compose config` | `docker compose config` | Validate and show merged compose config |

**docker-compose.yml example (FoodExpress):**
```yaml
version: "3.9"
services:
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - fe-network
    volumes:
      - api-logs:/app/logs

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: foodexpress
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - fe-network

volumes:
  db-data:
  api-logs:

networks:
  fe-network:
    driver: bridge
```

---

## Volumes

| Command | Example | Description |
|---|---|---|
| `docker volume create <name>` | `docker volume create fe-db-data` | Create named volume |
| `docker volume ls` | `docker volume ls` | List all volumes |
| `docker volume inspect <name>` | `docker volume inspect fe-db-data` | Volume details (mountpoint, etc.) |
| `docker volume rm <name>` | `docker volume rm fe-db-data` | Remove volume |
| `docker volume prune` | `docker volume prune` | Remove all unused volumes |

**Volume types:**

| Type | Syntax | Use Case |
|---|---|---|
| Named volume | `-v fe-data:/app/data` | Persistent data managed by Docker |
| Bind mount | `-v /host/path:/app/data` | Share host files with container |
| tmpfs mount | `--tmpfs /tmp` | In-memory, non-persistent |

---

## Networks

| Command | Example | Description |
|---|---|---|
| `docker network create <name>` | `docker network create fe-network` | Create custom bridge network |
| `docker network ls` | `docker network ls` | List networks |
| `docker network inspect <name>` | `docker network inspect fe-network` | Network details and connected containers |
| `docker network connect <net> <ctr>` | `docker network connect fe-network fe-api` | Connect running container to network |
| `docker network disconnect <net> <ctr>` | `docker network disconnect fe-network fe-api` | Disconnect container from network |
| `docker network rm <name>` | `docker network rm fe-network` | Remove network |
| `docker network prune` | `docker network prune` | Remove all unused networks |

**Default drivers:** `bridge` (single host), `host` (share host network), `none` (no networking), `overlay` (multi-host Swarm).

---

## System Cleanup

| Command | Description |
|---|---|
| `docker system df` | Show disk usage by images, containers, volumes |
| `docker system prune` | Remove stopped containers, unused networks, dangling images |
| `docker system prune -a` | Also remove unused images (not just dangling) |
| `docker system prune -a --volumes` | Full cleanup including unused volumes |

---

*FoodExpress Training | Module 24: Docker Part 1 | Publicis Sapient Sustain Eng 2026*
