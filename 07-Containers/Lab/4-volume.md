# Lab 4: Docker Volumes and Persistent Data

## Objectives

- Understand why container data is lost by default and why that matters
- Learn the three ways Docker can persist data beyond a container's lifetime
- Create and manage named volumes
- Share a volume between multiple containers
- Use bind mounts to map a host directory into a container
- Back up and restore volume data
- Mount volumes as read-only

---

## The Problem: Containers are Ephemeral

- Before learning the solution, let's see the problem firsthand
- Every container gets a fresh writable layer on top of read-only image layers
- Anything you write goes into that writable layer
- When the container is removed, Docker destroys that writable layer — and your data is gone with it

```bash
# Start an interactive ubuntu container
docker run --name temp -it ubuntu bash

# Inside the container, create a file with important data
echo "important data" > /myfile.txt
cat /myfile.txt

# Exit the container
exit

# Remove the container
docker rm temp

# Try to get the data back — it is gone forever
# There is no way to recover it
```

```
  +---------------------------+
  |  Writable Layer (R/W)     |  <-- Your data lives here (LOST on rm)
  +---------------------------+
  |  Image Layer 3 (R/O)      |
  +---------------------------+
  |  Image Layer 2 (R/O)      |
  +---------------------------+
  |  Image Layer 1 (R/O)      |  <-- Shared across all containers using this image
  +---------------------------+
```

- This design is intentional — it keeps containers lightweight and reproducible
- The solution is to store data OUTSIDE the container using one of Docker's storage options

---

## Three Ways to Persist Data

- Docker gives you three mechanisms
- Each one solves a different problem

```
  +------------------+    +------------------+    +------------------+
  |  Named Volumes   |    |  Bind Mounts     |    |  tmpfs Mounts    |
  +------------------+    +------------------+    +------------------+
  | Managed by Docker|    | You manage path  |    | RAM only         |
  | /var/lib/docker/ |    | /your/host/path  |    | Never on disk    |
  | Best for data    |    | Best for code    |    | Best for secrets |
  | Survives rm      |    | Survives rm      |    | Lost on stop     |
  +------------------+    +------------------+    +------------------+
           |                      |                       |
           v                      v                       v
       Container             Container               Container
```

- **Named Volumes**: Docker manages the storage location. Best for databases and app data
- **Bind Mounts**: You choose the directory on the host. Best for development (live code reload)
- **tmpfs Mounts**: Data lives in RAM only. Best for temporary secrets that must never touch disk
- This lab focuses on Named Volumes and Bind Mounts — the two you will use daily

---

## Part 1: Creating and Managing Named Volumes

- Named volumes are the recommended way to persist data
- Docker manages where the data lives on the host, so you do not need to worry about host directory paths
- Volumes exist independently of containers — removing a container does not remove its volume

```bash
# See all volume subcommands
docker volume

# Create a named volume
docker volume create my-vol1

# List all volumes on this machine
docker volume ls

# Inspect a volume — notice the Mountpoint field
# This is where Docker stores the data on your host filesystem
docker volume inspect my-vol1

# Create a second volume
docker volume create my-vol2
docker volume ls

# Remove volumes (they must not be in use by any container)
docker volume rm my-vol1 my-vol2
```

- The `Mountpoint` shown by `docker volume inspect` is the actual path on your host where the volume data lives (typically under `/var/lib/docker/volumes/`)
- You rarely need to access it directly — Docker manages it for you
- Volumes persist even after the container that created them is deleted

**Verification:** After running `docker volume inspect my-vol1`, confirm the output contains a `Mountpoint` field and a `CreatedAt` timestamp.

---

## Part 2: Labeled Volumes

- Labels let you tag volumes with metadata
- This helps you organize and filter volumes in production environments
- Labels are key-value pairs you attach to Docker objects

```bash
docker volume create \
  --driver local \
  --label project=myproject \
  --label environment=development \
  my-labeled-volume
```

- In production, teams use labels like `project=`, `environment=`, and `owner=` to track which volumes belong to which application and environment

**Verification:**

```bash
docker volume inspect my-labeled-volume
# Look for the "Labels" section in the output:
# "Labels": {
#     "environment": "development",
#     "project": "myproject"
# }
```

---

## Part 3: Mounting Volumes into Containers

- This is where volumes become powerful
- The same volume can be mounted into multiple containers, allowing them to share data
- Walk through this step by step

**Step 1 — Create a container with a volume mounted at /data**

```bash
docker run -dit --name alpine1 --mount source=data-vol,target=/data alpine
docker volume ls
# data-vol was created automatically because it did not exist yet
```

**Step 2 — Write data inside the alpine container**

```bash
docker exec -it alpine1 sh

# Inside the container:
echo "shared file from alpine1" > /data/shared.txt
ls /data
exit
```

**Step 3 — Remove the alpine container**

```bash
docker rm -f alpine1
# The container is gone, but data-vol still exists
docker volume ls
```

**Step 4 — Mount the same volume into a new nginx container**

```bash
docker run -dit --name nginx1 --mount source=data-vol,target=/data nginx
```

**Step 5 — Verify the data is still there**

```bash
docker exec -it nginx1 sh

# Inside nginx container:
ls /data
cat /data/shared.txt
# Output: shared file from alpine1
exit
```

- The data survived the removal of alpine1 because it was stored in the volume, not in the container's writable layer
- The nginx container has no idea where the data came from — it just sees a directory with files in it

```
  alpine1 (removed)       nginx1 (new)
        |                      |
        v                      v
   +--------+            +--------+
   | /data  |            | /data  |
   +--------+            +--------+
        \                    /
         \                  /
      +------------------------+
      |       data-vol         |
      |    (Named Volume)      |
      | data survives here     |
      +------------------------+
```

**Cleanup:**

```bash
docker rm -f nginx1
docker volume rm data-vol
```

---

## Part 4: Bind Mounts (Host Directory)

- A bind mount maps a directory that already exists on your host into the container
- Unlike named volumes, you choose and control the path
- Changes are visible in real-time from both sides because they are the same files

**Setup — create the host directory and set permissions**

```bash
sudo mkdir -p /var/log/nginx
sudo chown -R $USER:$(id -gn) /var/log/nginx
sudo chmod -R 755 /var/log/nginx
```

**Run nginx with a bind mount for logs**

```bash
docker run -d \
  --name my-nginx \
  -p 80:80 \
  -v /var/log/nginx:/var/log/nginx \
  nginx
```

- The `-v` flag syntax is: `-v host_path:container_path`
- Everything nginx writes to `/var/log/nginx` inside the container is immediately visible at `/var/log/nginx` on your host
- Changes are real-time in both directions because both sides point to the same files

```
  Host Machine                      Container (my-nginx)
  /var/log/nginx/       <-------->  /var/log/nginx/
  (same files, same data, real-time sync)
```

**Verification — generate traffic and watch logs appear on the host**

```bash
# Generate a request to nginx
curl http://localhost:80

# On the HOST (not inside the container), watch the log update in real-time
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

- Log lines appear on your host filesystem immediately after each request hits nginx inside the container
- Press `Ctrl+C` to stop tailing

```bash
# Inspect the container to confirm the bind mount is configured
docker inspect my-nginx
# Look for "Mounts" section — Type should be "bind"

docker exec -it my-nginx bash
exit

docker rm -f my-nginx
```

---

## Part 5: Bind Mount for Development (Live Code Reload)

- This is the most common use of bind mounts in day-to-day development
- Mount your source code directory into a container so the running server sees your edits without a rebuild
- The container does not copy the files — it reads directly from your host directory
- Every save you make in your editor is instantly reflected inside the running container

**Basic example with nginx (static files)**

```bash
# Create a simple HTML file on your host
mkdir -p ~/myapp
echo '<h1>Hello Docker</h1>' > ~/myapp/index.html

# Run nginx, mounting your local code into the web root
docker run -d --name dev-nginx -p 8080:80 -v ~/myapp:/usr/share/nginx/html nginx

# Confirm it works
curl http://localhost:8080
# Output: <h1>Hello Docker</h1>
```

Now edit the file on your host — no container restart needed:

```bash
echo '<h1>Hello Docker - Updated!</h1>' > ~/myapp/index.html

# Refresh immediately
curl http://localhost:8080
# Output: <h1>Hello Docker - Updated!</h1>
```

**Cleanup:**

```bash
docker rm -f dev-nginx
```

---

**Express.js live reload:**

```bash
# Mount source code into the container for live development
docker run -d --name dev-express \
  -p 3000:3000 \
  -v $(pwd)/express-app:/app \
  -w /app \
  node:18-alpine \
  sh -c "npm install && node server.js"

# Edit server.js on your host — restart container to see changes
# Or use nodemon for auto-restart:
docker run -d --name dev-express \
  -p 3000:3000 \
  -v $(pwd)/express-app:/app \
  -w /app \
  node:18-alpine \
  sh -c "npm install && npx nodemon server.js"
```

**Spring Boot with mounted config:**

```bash
# Mount external config file into Spring Boot container
docker run -d --name dev-spring \
  -p 8080:8080 \
  -v $(pwd)/config/application.yml:/app/config/application.yml \
  spring-boot-app:v1
```

- Express.js: mount the entire source directory for live code editing
- Spring Boot: mount config files (application.yml) to change settings without rebuilding
- Both patterns avoid rebuilding the image for every change during development

---

## Part 6: Volume Drivers (NFS and Bind)

- Volume drivers let Docker manage storage on remote systems, not just the local disk
- This matters when you run the same application across multiple servers and need them to share the same data

**Bind driver — mount a specific host path as a named volume**

```bash
docker volume create \
  --driver local \
  --opt type=none \
  --opt device=/path/on/host \
  --opt o=bind \
  my-bind-volume
```

- Creates a named volume that behaves like a bind mount
- You get the organizational benefits of a named volume while specifying an exact host path

**NFS driver — mount a network file share**

```bash
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/exported/path \
  my-nfs-volume
```

- Use NFS volumes when multiple Docker hosts need to read and write the same data
- Example: a shared upload directory across a cluster of web servers
- The `addr=` option points to the NFS server's IP address

---

## Part 7: Volume Backup and Restore

- Docker volumes have no built-in backup command
- The standard pattern is to spin up a temporary container that can see the volume and use standard Linux tools (`tar`) to create an archive
- The temporary container (`--rm`) is created just to run the tar command, then destroyed
- The data ends up in the new volume, not in the container
- This pattern works for any named volume regardless of which application uses it

**Backup a volume to a tar file**

```bash
# Make sure data-vol exists and has data
docker volume create data-vol
docker run --rm -v data-vol:/data alpine sh -c "echo 'backup test' > /data/important.txt"

# Backup: mount the volume read-only at /source, mount current directory at /backup
# Use tar to compress everything from /source into /backup/data-vol-backup.tar.gz
docker run --rm \
  -v data-vol:/source \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-vol-backup.tar.gz -C /source .

ls -lh data-vol-backup.tar.gz
```

**Restore from backup**

```bash
# Create a new empty volume
docker volume create restored-vol

# Mount the new volume at /target and current directory at /backup
# Extract the archive into /target
docker run --rm \
  -v restored-vol:/target \
  -v $(pwd):/backup \
  alpine tar xzf /backup/data-vol-backup.tar.gz -C /target

# Verify the restore worked
docker run --rm -v restored-vol:/data alpine cat /data/important.txt
# Output: backup test
```

**Cleanup:**

```bash
docker volume rm data-vol restored-vol
rm data-vol-backup.tar.gz
```

---

## Part 8: Read-Only Volumes

- Sometimes you want a container to read data from a volume but not be allowed to modify it
- Add `:ro` to the end of a `-v` flag to enforce this
- The `:ro` flag tells the Linux kernel to mount the directory read-only inside that container's namespace
- The files on your host are unchanged and still fully writable from your host
- Use read-only mounts for configuration files and static assets that a container should serve but never modify

```bash
# Make sure ~/myapp/index.html exists from Part 5, or recreate it
mkdir -p ~/myapp
echo '<h1>Read Only Test</h1>' > ~/myapp/index.html

# Mount the directory as read-only with :ro
docker run -d --name ro-nginx -v ~/myapp:/usr/share/nginx/html:ro nginx

# Verify the container can serve the file
curl http://localhost:80
```

Now try to write to the mounted path from inside the container:

```bash
docker exec -it ro-nginx bash

# Inside the container — try to modify the file
echo "trying to write" > /usr/share/nginx/html/index.html
# Output: bash: /usr/share/nginx/html/index.html: Read-only file system

# Try to create a new file
touch /usr/share/nginx/html/newfile.txt
# Output: touch: cannot touch '/usr/share/nginx/html/newfile.txt': Read-only file system

exit
```

**Cleanup:**

```bash
docker rm -f ro-nginx
```

---

## Challenges

Work through these on your own. Each one tests a concept from this lab.

1. Create a MySQL container with a named volume for its data directory (`/var/lib/mysql`). Use `-e MYSQL_ROOT_PASSWORD=secret` to set the root password. Connect to MySQL and create a database. Run a Spring Boot app container that connects to it. Also run an Express.js app container that connects to the same MySQL. Remove both app containers and the MySQL container, then recreate them all pointing to the same volume. Connect again and verify your database and data are still there.

2. Use a bind mount to serve a custom HTML page with nginx on port 8080. Edit the HTML file on your host using any text editor and verify the changes appear immediately when you refresh `curl http://localhost:8080` — without restarting the container.

3. Create a named volume and put some files in it using an alpine container. Back it up to a `.tar.gz` file on your host using the temporary-container pattern from Part 7. Delete the original volume. Restore the backup into a new volume with a different name. Verify all files are present.

4. Mount the same named volume into two separate alpine containers at the same time. Write a file from inside the first container. Without stopping the first container, read that file from inside the second container. Explain why this works.

5. Start a container with a read-only volume mount. Try to write to the mounted path inside the container. Note the exact error message. Then try the same write on the host to confirm the host path is not affected.
