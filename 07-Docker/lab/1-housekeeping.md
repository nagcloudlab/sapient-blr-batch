# Lab 1: Docker Housekeeping

## Objectives

- Understand what Docker objects are and how they accumulate on your system
- Learn how to inspect disk usage with `docker system df`
- Remove containers, images, volumes, and networks safely
- Use the all-in-one `docker system prune` command
- Perform selective cleanup without wiping everything

---

## Why Housekeeping Matters

- Every time you pull an image, run a container, or create a volume — Docker stores data on your disk
- Over days and weeks, these objects pile up silently
- Unused images from old experiments, stopped containers you forgot about, and orphaned volumes all consume real disk space
- They can also cause confusion when you are troubleshooting
- Regular housekeeping keeps your environment clean, predictable, and fast

```
  Docker Object Relationships
  ===========================

  Registry (Docker Hub, etc.)
       |
       | docker pull
       v
    Images  <------ Dockerfile (docker build)
       |
       | docker run
       v
  Containers
       |
       +-------> Volumes  (persistent data, survives container removal)
       |
       +-------> Networks (containers talk to each other through networks)
```

- Images are the blueprint
- Containers are the running instance
- Volumes store data
- Networks connect containers

---

## Part 1: Understanding Docker Objects

| Object    | What it is                                                  | Takes up disk space? |
|-----------|-------------------------------------------------------------|----------------------|
| Image     | A read-only template used to create containers              | Yes                  |
| Container | A running (or stopped) instance created from an image       | Yes (thin writable layer on top of the image) |
| Volume    | A named storage area managed by Docker, outside the container filesystem | Yes     |
| Network   | A virtual network that lets containers communicate          | Minimal              |

Key relationships to remember:

- A container is always created FROM an image — you cannot delete an image while a container (even a stopped one) still references it
- A volume can be attached to a container but it lives independently — deleting a container does NOT delete its volume unless you use `docker rm -v`
- Dangling images are layers that are no longer tagged and not referenced by any container
- Dangling images are safe to remove and are the most common source of wasted space

---

## Part 2: Check Current State

- Before you clean anything, take a snapshot of what is on your system

```bash
docker system df
```

Sample output:

```
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          8         2         1.23GB    950MB (77%)
Containers      5         1         120MB     115MB (95%)
Local Volumes   3         1         450MB     200MB (44%)
Build Cache     12        0         300MB     300MB (100%)
```

What each column means:

- TOTAL: How many objects exist
- ACTIVE: How many are currently in use (by a running container)
- SIZE: Total disk space consumed
- RECLAIMABLE: How much you could free by cleaning up unused objects

- Run this command now and note the numbers
- You will compare them at the end of the lab

---

## Part 3: Remove All Containers

### Why stop before removing?

- Docker containers run processes
- Stopping sends SIGTERM — a polite "please shut down" signal
- The container process can then clean up open files and connections
- If you skip stop and go straight to `rm -f`, Docker sends SIGKILL which is immediate
- SIGKILL gives no time for cleanup and can cause data corruption in volumes

```bash
# List all containers (running and stopped)
docker ps -a

# Stop all running containers
docker stop $(docker ps -a -q)

# Remove all stopped containers
docker rm $(docker ps -a -q)
```

### The $() subshell pattern explained

- `$(docker ps -a -q)` runs the inner command first
- It passes its output — a list of container IDs — as arguments to the outer command
- It is equivalent to copying the IDs manually, just automated

```
docker ps -a -q   -->  a1b2c3d4
                        e5f6g7h8
                        i9j0k1l2
                        |
                        v
docker stop a1b2c3d4 e5f6g7h8 i9j0k1l2
```

### Verification

```bash
docker ps -a
```

- Expected output: an empty table with only the header row

### Alternative: prune command

```bash
docker container prune
```

- This removes only STOPPED containers, not running ones
- It is safer for production environments where some containers should keep running

> **Tip — the `--filter` flag**: Most prune commands accept `--filter` to target specific objects. For example, remove only containers stopped more than 24 hours ago:
> ```bash
> docker container prune --filter "until=24h"
> ```
> This works on `docker image prune`, `docker volume prune`, and `docker network prune` as well. Useful when you want to keep recent objects and only clean up old ones.

---

## Part 4: Remove All Images

```bash
# List all images
docker image ls

# Force remove all images
docker image rm -f $(docker image ls -q)

# Verify
docker image ls
```

### What if an image is used by a container?

- Without `-f`, Docker will refuse to remove an image that has a container (even stopped) referencing it
- The `-f` flag forces removal, but image layers are only truly deleted once no container references them
- Always remove containers first, then images — that is why the order in this lab matters

### Verification

```bash
docker image ls
```

- Expected output: empty table (no images listed)

---

## Part 5: Remove All Volumes

- WARNING: Volumes hold persistent data
- Databases, uploaded files, and application state can all live in volumes
- Removing a volume is permanent and cannot be undone
- Only run this in a lab or dev environment where you do not need the data

```bash
# List all volumes
docker volume ls

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Verify
docker volume ls
```

### What are orphaned volumes?

- When you run `docker rm` without the `-v` flag, the container is deleted but its volume remains
- These orphaned (or "dangling") volumes accumulate over time
- They are safe to remove with:

```bash
docker volume prune
```

- This removes only volumes not currently attached to any container

### Verification

```bash
docker volume ls
```

- Expected output: empty table

---

## Part 6: Remove All Networks

```bash
# List all networks
docker network ls

# Remove all networks
docker network rm $(docker network ls -q)

# Verify
docker network ls
```

### Why will this partially fail?

- Docker has three built-in default networks that cannot be removed: `bridge`, `host`, and `none`
- Docker will print errors for those three but will remove any custom networks you created
- This is expected behaviour — not a bug

```
Default networks (cannot remove):
  bridge  - default network for containers
  host    - shares host machine's network stack
  none    - no networking

Custom networks (safe to remove):
  my-app-network
  database-net
  frontend-backend
```

### Verification

```bash
docker network ls
```

- Expected output: only the three default networks remain (`bridge`, `host`, `none`)

---

## Part 7: The Nuclear Option

- If you want to wipe everything in one command:

```bash
docker system prune -a --volumes
```

What this removes:

- All stopped containers
- All images not used by a running container
- All volumes not used by a running container
- All custom networks not used by a running container
- All build cache

What it does NOT touch:

- Running containers
- Images used by running containers
- Volumes attached to running containers

### When to use it

- Use `docker system prune -a --volumes` when you are resetting a lab or demo environment
- Use it when your disk is critically full and you need space fast
- Use it when you are starting a fresh project

Do NOT use it when:

- You have databases in volumes you need
- Other developers share the same Docker host
- You have images that took a long time to build and are still needed

### After snapshot

```bash
docker system df
```

- Compare the numbers to what you noted in Part 2
- The RECLAIMABLE column should now show 0 for everything

---

## Part 8: Selective Cleanup

- Sometimes you do not want to wipe everything
- The commands below let you target specific types of objects

### Remove only dangling images (untagged, unreferenced layers)

```bash
docker image prune
```

- This is the safest image cleanup
- It only removes images with no tag and no container referencing them

### Remove only stopped containers

```bash
docker container prune
```

- Running containers are not affected
- This is safe to run regularly

### Remove images by specific tag

```bash
docker image rm redis:6.0
```

- Removes one specific version without touching others

### Remove a container by name

```bash
docker rm my-container-name
```

### Remove containers matching a name pattern

```bash
docker ps -a --filter "name=test" -q | xargs docker rm
```

- Lists all containers whose name contains "test"
- Pipes the IDs to `docker rm`

### Remove volumes that are not attached to any container

```bash
docker volume prune
```

---

## Before & After: What Cleanup Looks Like

Here is a typical `docker system df` comparison showing the impact of cleanup:

```
BEFORE CLEANUP:
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          12        2         3.45GB    2.80GB (81%)
Containers      9         2         250MB     230MB (92%)
Local Volumes   6         1         1.20GB    800MB (66%)
Build Cache     18        0         650MB     650MB (100%)
                                    ------
                          Total:    5.55GB reclaimable

AFTER docker system prune -a --volumes:
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          2         2         450MB     0B (0%)
Containers      2         2         20MB      0B (0%)
Local Volumes   1         1         400MB     0B (0%)
Build Cache     0         0         0B        0B
                                    ------
                          Total:    0B reclaimable
```

- In this example, cleanup reclaimed ~5.1 GB of disk space
- Only running containers, their images, and their volumes survived

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Error: container is running` when trying to remove | Container is still active | Stop it first: `docker stop <id>`, then remove |
| `Error: image is referenced in multiple repositories` | Image has multiple tags | Use `-f` flag or remove all tags first |
| `Error: volume is in use` | A container (even stopped) still references it | Remove the container first, then the volume |
| `docker system prune` did not free much space | Running containers and their deps are preserved | This is expected — prune only touches unused objects |
| Disk still full after prune | Build cache or overlay2 data | Try `docker builder prune` to clear build cache |

---

## Challenges

1. Run `docker system df` before doing any cleanup, record the numbers, perform a full cleanup, then run `docker system df` again. How much space did you reclaim?

2. Start three containers using `docker run -d --name c1 nginx`, `docker run -d --name c2 nginx`, `docker run -d --name c3 nginx`. Stop c1 and c2 but leave c3 running. Now run `docker container prune`. Which containers were removed? What happened to c3? Why?

3. Pull three versions of Redis:
   ```bash
   docker pull redis:latest
   docker pull redis:7.0
   docker pull redis:6.0
   ```
   Now remove only the 6.0 version with `docker image rm redis:6.0`. Verify with `docker image ls` that latest and 7.0 are still present.
