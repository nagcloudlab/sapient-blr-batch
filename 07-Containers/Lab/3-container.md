# Lab 3: Working with Containers

## Objectives

By the end of this lab you will be able to:

- Understand what a container is and how it differs from an image
- Create, start, stop, and remove containers
- Run containers in interactive and detached modes
- Execute commands inside running containers
- Apply resource limits to containers
- Apply basic security practices when running containers

---

## What is a Container?

- A container is a running instance of a Docker image
- Think of the image as a blueprint (like a class in programming) and the container as the actual running object created from that blueprint
- You can create many containers from the same image, and they all start with identical filesystems but remain completely isolated from each other
- Internally, a container is just a Linux process with its own isolated filesystem (from the image layers), its own network stack, and its own process tree
- From inside the container it looks like a full operating system, but it is sharing the host kernel

```
Container Lifecycle:

  docker create       docker start       docker stop        docker rm
  [Created] --------> [Running] --------> [Stopped] --------> [Removed]
                          |                    ^
                          |   docker kill      |
                          +--------------------+
                          |
                          |   docker pause / docker unpause
                          +---> [Paused] --------------------+
```

---

## Part 1: Your First Container

- Run a container and observe its behavior

```bash
docker run ubuntu:20.04
docker container ls
docker container ls -a
docker run -it ubuntu:20.04
docker container ls
```

**Why did the first container exit immediately?**

- A container runs as long as its main process is alive
- The default command for the ubuntu image is `bash`
- Since no terminal was attached, bash had nothing to do and exited instantly
- When the main process exits, the container stops

**What do `-i` and `-t` do?**

- `-i` keeps STDIN open so you can type commands into the container
- `-t` allocates a pseudo-TTY (a virtual terminal), giving you a proper shell prompt
- Together `-it` gives you an interactive shell session inside the container

**Verification - understand the columns in `docker container ls -a`:**

| Column       | Meaning                                                        |
|--------------|----------------------------------------------------------------|
| CONTAINER ID | A short unique identifier for this container instance          |
| IMAGE        | The image this container was created from                      |
| COMMAND      | The command that was run as the main process                   |
| CREATED      | How long ago the container was created                         |
| STATUS       | Current state: Up X seconds, Exited (0) X seconds ago, etc.   |
| PORTS        | Any published port mappings (covered in networking labs)       |
| NAMES        | A human-readable name (auto-assigned or set with --name)       |

- Run `docker container ls -a` after each step above and watch the STATUS column change

---

## Part 2: Overriding the Default Command

- Every Docker image has a default command baked in
- You can inspect it and override it at runtime

```bash
docker history ubuntu:20.04
docker run -it ubuntu:20.04 /bin/sh
```

**Why override the command?**

- `docker history` shows the layers that built the image
- The last CMD instruction is what runs by default
- Passing `/bin/sh` at the end of `docker run` replaces that default with your own command
- This is useful when the default command is a server process and you want a shell instead for debugging

**CMD vs ENTRYPOINT (brief):**

- `CMD` sets the default command and can be fully replaced from the command line
- `ENTRYPOINT` sets the main executable; command-line arguments are appended to it rather than replacing it
- You will explore this in the Dockerfile labs

---

## Part 3: Running in the Background (Detached Mode)

- For long-running processes (web servers, databases) you want the container to run in the background without blocking your terminal

```bash
docker rm my-ubuntu
docker run --name my-ubuntu -d ubuntu:20.04 sleep 1000
docker attach my-ubuntu
```

**What does `-d` do?**

- The `-d` flag (detached mode) starts the container in the background
- It immediately returns the container ID to your prompt
- Your terminal is free to use for other commands

**What does `--name` do?**

- By default Docker assigns a random name like `jovial_turing`
- Using `--name` gives the container a predictable, human-readable name
- This lets you reference it in later commands without copying long IDs

**What does `docker attach` do?**

- It reconnects your terminal to the container's main process (PID 1)
- You will see its output and can interact with it

> WARNING: If you press Ctrl+C while attached, you send a SIGINT signal to PID 1, which may stop the container. To safely detach without stopping the container, press Ctrl+P followed by Ctrl+Q.

**Verification:**

```bash
docker ps
```

- You should see `my-ubuntu` listed with status `Up X seconds`

---

## Part 4: Execute Commands in Running Containers

- `docker exec` lets you run an additional command inside a container that is already running

```bash
docker exec -it my-ubuntu /bin/bash
ps aux
```

**How is `exec` different from `attach`?**

- `docker attach` connects you to the existing main process (PID 1)
- `docker exec` spawns a brand new process inside the container's namespace
- When you exit an exec session, the container keeps running because you only stopped the extra process, not PID 1

**Why is the process tree isolated?**

- Run `ps aux` inside the container and you will see very few processes (just `sleep` and your bash session)
- Run `ps aux` on the host and you will see hundreds of processes
- The container's process namespace is isolated, so processes inside cannot see host processes and vice versa

**Verification:**

```bash
# Inside the container:
ps aux

# Open a separate terminal on the host and run:
ps aux | grep sleep
```

- Notice that `sleep 1000` appears on the host (it is a real process) but inside the container the process tree is tiny and isolated

---

## Part 5: Stop and Start Containers

```bash
# Stop a named container gracefully
docker stop my-ubuntu
docker container ls
docker container ls -a

# Stop all running containers at once
docker container ls
docker container ls -q
docker stop $(docker container ls -q)
docker container ls

# Start a stopped container
docker start my-ubuntu
docker container ls
```

**How does `docker stop` work?**

- `docker stop` sends a SIGTERM signal to PID 1, giving the process a chance to clean up (flush buffers, close connections)
- If the process does not exit within 10 seconds, Docker sends a SIGKILL to force-terminate it
- This graceful shutdown is important for databases and application servers

**How is `docker kill` different?**

- `docker kill` sends SIGKILL immediately, with no grace period
- Use it when a container is unresponsive and `docker stop` hangs

**What is the `$()` pattern?**

- `$(docker container ls -q)` is a shell command substitution
- It runs the inner command first, captures its output (a list of container IDs), and passes that as arguments to `docker stop`
- This is how you bulk-operate on all running containers

**Verification:**

- After `docker stop`, run `docker container ls -a` and confirm the STATUS shows `Exited`
- After `docker start`, confirm STATUS shows `Up`

---

## Part 6: Remove Containers

- Stopped containers still consume disk space
- Remove them when you no longer need them

```bash
docker rm my-ubuntu
docker stop $(docker container ls -q)
docker container ls
docker container ls -a

# Remove all stopped containers in one command
docker container prune
docker container ls -a
```

**Important rules for removal:**

- You cannot remove a running container with `docker rm` alone
- Either stop it first, or use `docker rm -f` to force-remove it (sends SIGKILL then removes)
- `docker container prune` removes every container in the Exited or Created state
- It will ask for confirmation — use with care in shared environments

**Verification:**

- After `docker container prune`, run `docker container ls -a`
- The list should be empty (or contain only running containers)

---

## Part 7: Create vs Run

- You can split container creation and startup into two separate steps

```bash
docker create --name my-ubuntu -it ubuntu:20.04
docker container ls -a
docker start my-ubuntu
docker attach my-ubuntu
```

**How does this relate to `docker run`?**

```
docker run = docker create + docker start + (optional: docker attach if -it is used)
```

- `docker run` is a convenience command that chains all three steps
- Using `docker create` separately lets you configure the container fully (attach volumes, set environment variables, configure networks) before it ever starts running
- This is useful in scripted deployments where you need to validate configuration before launch

---

## Part 8: Inspect a Container

- `docker inspect` returns a detailed JSON document describing every aspect of a container's configuration and current state

```bash
docker inspect my-ubuntu
```

**Key fields to look for:**

| Field                          | What it tells you                              |
|--------------------------------|------------------------------------------------|
| `State.Status`                 | running, exited, paused, etc.                  |
| `State.ExitCode`               | 0 = clean exit, non-zero = error               |
| `NetworkSettings.IPAddress`    | The container's IP on the Docker bridge network|
| `Mounts`                       | Any volumes or bind mounts attached            |
| `Config.Env`                   | Environment variables set in the container     |
| `Config.Cmd`                   | The command the container runs                 |

**Extract a single field with a format template:**

```bash
docker inspect --format '{{.NetworkSettings.IPAddress}}' my-ubuntu
```

- This is much faster than scrolling through the full JSON output
- The `--format` flag uses Go template syntax to pull out exactly the field you need

---

## Part 9: Environment Variables

- Applications running in containers read their configuration from environment variables rather than config files
- This follows the 12-factor app principle: keep configuration separate from code
- The same image can behave differently in dev, staging, and production — just by changing env vars at runtime

```bash
docker rm my-ubuntu
docker run --name my-ubuntu -e MY_VAR=Hello -it ubuntu:20.04
echo $MY_VAR
exit
docker rm my-ubuntu
```

**Why use environment variables for configuration?**

- The same container image can be deployed to development, staging, and production simply by changing the environment variables passed at runtime
- The image itself does not need to change

**Spring Boot and Express.js examples:**

```bash
# Spring Boot — switch profile via env var
docker run -d -p 8080:8080 -e SPRING_PROFILES_ACTIVE=prod spring-boot-app:v1

# Express.js — switch config via env var
docker run -d -p 3000:3000 -e NODE_ENV=production -e PORT=3000 express-app:v1
```

- Spring Boot reads `SPRING_PROFILES_ACTIVE` to load the right `application-{profile}.yml`
- Express.js reads `NODE_ENV` to toggle debug mode, logging, and error detail
- Same image, different behavior — just by changing env vars

**Verification:**

- After running the container with `-e MY_VAR=Hello`, exec into it and confirm the variable is set:

```bash
docker exec -it my-ubuntu bash
echo $MY_VAR
# Expected output: Hello
```

---

## Part 10: Auto-Remove Containers

- Use `--rm` when you want the container to be deleted automatically as soon as it exits

```bash
docker run --rm -it ubuntu:20.04
exit
docker container ls -a
```

**When is `--rm` useful?**

- It is ideal for one-off tasks: running a quick script, debugging a build step, or testing a command
- Without `--rm`, each test run leaves behind a stopped container that you have to clean up manually
- With `--rm`, the filesystem is discarded the moment the container exits

**Verification:**

- Run `docker container ls -a` immediately after exit
- The container should not appear in the list at all

---

## Part 11: Resource Limits

- By default a container can use all available CPU and memory on the host
- This can cause a "noisy neighbor" problem: one misbehaving container starves others or crashes the host
- Resource limits give you predictable, stable performance and help control cloud costs

```
Host Machine (8 CPU, 16 GB RAM)
+-----------------------------------------------+
|                                               |
|   Container A          Container B            |
|   --cpus="0.5"         --cpus="1.0"           |
|   -m 200m              -m 512m                |
|                                               |
|   Remaining for other containers:             |
|   6.5 CPU, ~15.3 GB RAM                       |
|                                               |
+-----------------------------------------------+
```

### Memory limits

```bash
# Hard limit: container is killed (OOMKilled) if it exceeds 200 MB
docker run --name my-limited-memory -m 200m -it ubuntu:20.04

# Soft limit: Docker tries to keep the container under 100 MB when memory is tight
docker run --name my-memory-reservation --memory-reservation=100m -it ubuntu:20.04

# Swap limit: total memory + swap = 300 MB (so swap = 300 - 200 = 100 MB)
docker run --name my-limited-swap --memory-swap=300m -it ubuntu:20.04

# Kernel memory limit: limits memory used by kernel structures for this container
docker run --name my-limited-kernel --kernel-memory=100m -it ubuntu:20.04
```

- `-m` / `--memory`: The maximum RAM the container can use. If it exceeds this, Linux OOM killer terminates it.
- `--memory-reservation`: A soft lower bound. Docker will try to reclaim memory from this container first when the host is under pressure.
- `--memory-swap`: The combined RAM + swap limit. Set equal to `-m` to disable swap entirely.
- `--kernel-memory`: Caps the kernel memory (socket buffers, slab cache) allocated for this container.

### CPU limits

```bash
# Assign 0.5 CPU cores (50% of one core, any core)
docker run --name my-limited-cpu --cpus="0.5" -it ubuntu:20.04

# CPU shares: relative weight. Default is 1024. 256 = 1/4 the priority.
docker run --name my-cpu-shares -c 256 -it ubuntu:20.04

# CPU quota/period: 10000 us of CPU time per 50000 us period = 20% of one core
docker run --name my-cpu-quota --cpu-quota=10000 --cpu-period=50000 -it ubuntu:20.04
```

- `--cpus`: The simplest way to limit CPU. `"0.5"` means half a core.
- `-c` / `--cpu-shares`: A relative weight used during contention. Only kicks in when multiple containers compete for CPU.
- `--cpu-quota` / `--cpu-period`: Fine-grained control. Quota is the microseconds of CPU time granted per period.

### I/O limits

```bash
# Read limit: maximum 1 MB/s read throughput from /dev/sda
docker run --name my-limited-io --device-read-bps /dev/sda:1mb -it ubuntu:20.04
```

- `--device-read-bps` / `--device-write-bps`: Limits the bytes per second a container can read or write to a specific block device. Useful to prevent a container from saturating disk I/O.

### Process limits

```bash
# PID limit: container cannot create more than 100 processes/threads
docker run --name my-limited-pids --pids-limit=100 -it ubuntu:20.04
```

- `--pids-limit`: Prevents fork bombs and runaway processes from exhausting the host's process table.

### Practical example: Spring Boot vs Express.js

```bash
# Run Spring Boot with memory limits (JVM needs more memory)
docker run -d --name spring-app -m 512m --cpus="1.0" -p 8080:8080 spring-boot-app:v1

# Run Express.js with tighter limits (Node.js is lighter)
docker run -d --name express-app -m 256m --cpus="0.5" -p 3000:3000 express-app:v1

# Watch both
docker stats spring-app express-app
```

- Spring Boot / JVM apps typically need 256MB-512MB minimum
- Node.js / Express apps can run comfortably in 128MB-256MB
- Always set limits in production to prevent one container from starving others

### Combined example

```bash
docker run --name my-limited-container \
  -m 200m \
  --memory-reservation=100m \
  --cpus="0.5" \
  -c 256 \
  --cpu-quota=10000 \
  --cpu-period=50000 \
  --device-read-bps /dev/sda:1mb \
  --device-write-bps /dev/sda:1mb \
  --pids-limit=100 \
  --memory-swap=300m \
  --kernel-memory=50m \
  -it ubuntu:20.04
```

### Verification: docker stats

```bash
docker stats my-limited-container
```

- `docker stats` streams live resource usage

| Column       | Meaning                                                   |
|--------------|-----------------------------------------------------------|
| CPU %        | Current CPU usage as a percentage of the allocated limit  |
| MEM USAGE    | Current RAM used vs the hard limit (-m value)             |
| MEM %        | Memory used as a percentage of the limit                  |
| NET I/O      | Network bytes received / sent since container started     |
| BLOCK I/O    | Disk bytes read / written since container started         |
| PIDS         | Number of processes/threads running inside the container  |

- Press Ctrl+C to exit `docker stats`

---

## Part 12: Container Security Basics

- Running containers securely is as important as running them correctly
- The default Docker configuration is permissive for convenience, but production workloads need hardening

**Run as a non-root user**

- By default, processes inside a container run as root (UID 0)
- If an attacker escapes the container, they arrive on the host as root
- Add a `USER` instruction in your Dockerfile:

```dockerfile
FROM node:18
RUN useradd -m appuser
USER appuser
```

- Or enforce it at runtime: `docker run --user 1001:1001 myimage`

**Read-only filesystem**

- Prevent the container from writing to its own filesystem, limiting what an attacker can do if they gain code execution:

```bash
docker run --read-only -it ubuntu:20.04
```

- Files that the app genuinely needs to write (logs, temp files) can be put on a writable volume using `-v` (covered in the volumes lab)

**Drop Linux capabilities**

- Linux capabilities break the all-or-nothing root privilege into fine-grained permissions
- Drop all capabilities then add back only what the application needs:

```bash
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE -it ubuntu:20.04
```

- `NET_BIND_SERVICE` lets the process bind to ports below 1024
- Without it (and without root), this is not normally allowed

**Prevent privilege escalation**

- Stop processes inside the container from gaining more privileges than they started with (e.g., via setuid binaries):

```bash
docker run --security-opt=no-new-privileges -it ubuntu:20.04
```

**Additional security best practices:**

- Use official or verified base images from trusted publishers
- Regularly scan images for known CVEs using `docker scout` or tools like Trivy
- Use Docker Content Trust (DCT) to verify image signatures: `export DOCKER_CONTENT_TRUST=1`
- Never store secrets (passwords, API keys) in environment variables for production; use Docker secrets or a vault

---

## Challenges

- Work through these independently
- They reinforce everything covered in this lab

**Challenge 1 - Custom nginx page via exec**

- Run an nginx container in detached mode on port 8080
- Use `docker exec` to create a custom `/usr/share/nginx/html/index.html` inside the running container
- Open `http://localhost:8080` in a browser to verify your change is served
- Hint: `docker run -d --name my-nginx -p 8080:80 nginx`

**Challenge 2 - Hit the memory limit**

- Start a container with a 100 MB memory limit
- Inside the container, install the `stress` tool and try to allocate 200 MB of memory
- Observe what happens
- Check `docker inspect` for the `OOMKilled` field
- Hint: `apt-get install -y stress && stress --vm 1 --vm-bytes 200M`

**Challenge 3 - Prove filesystem isolation**

- Start two separate containers from the same `ubuntu:20.04` image
- Create a file inside container A
- Log into container B and verify the file does not exist there
- This proves that containers have independent, isolated filesystems even when they share the same image

**Challenge 4 - Container-to-container ping**

- Run two containers
- Use `docker inspect --format '{{.NetworkSettings.IPAddress}}'` to find the IP address of the first container
- Then exec into the second container and ping that IP
- This demonstrates that containers on the same Docker network can communicate
- Hint: You may need to install ping inside the ubuntu container: `apt-get install -y iputils-ping`

**Challenge 5 - Verify auto-remove**

- Run a container with `--rm`
- Exit the container
- Immediately run `docker container ls -a` and confirm the container is not listed
- Compare this to a container started without `--rm` to see the difference
