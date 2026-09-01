# Lab 7: Multi-Container Applications with Docker Compose

## Objectives

By the end of this lab you will be able to:

- Understand why Docker Compose exists and what problem it solves
- Read and understand a docker-compose.yaml file
- Deploy a real multi-container application (the Docker Voting App)
- Understand service discovery, named volumes, and networking in Compose
- Manage the lifecycle of a Compose stack (start, stop, scale, tear down)

---

## The Problem: Managing Multiple Containers

- Real applications are never a single container
- A typical web application needs a frontend, a backend, a database, a cache, and maybe a background worker
- Running all of these manually with `docker run` is painful and error-prone

Here is what you would have to type just to start the Voting App without Compose:

```bash
# WITHOUT Compose -- you'd have to run all of this:
docker network create app-network
docker volume create db-data
docker run -d --name db --network app-network -e POSTGRES_PASSWORD=postgres -v db-data:/var/lib/postgresql/data postgres:15
docker run -d --name redis --network app-network redis:alpine
docker run -d --name worker --network app-network docker/example-voting-app-worker
docker run -d --name vote --network app-network -p 5000:80 docker/example-voting-app-vote
docker run -d --name result --network app-network -p 5001:80 docker/example-voting-app-result

# And to stop and clean up:
docker stop db redis worker vote result
docker rm db redis worker vote result
docker network rm app-network
docker volume rm db-data
```

- That is 10+ commands, all of which you have to remember exactly
- If you make one mistake, the whole thing breaks
- Docker Compose solves this by letting you declare all of it in one file and manage it with a single command

---

## What is Docker Compose?

- Docker Compose is a tool for defining and running multi-container applications
- You describe your entire application stack in a single YAML file (`docker-compose.yaml`)
- Compose handles creating all the containers, networks, and volumes for you
- Think of it as a blueprint for your application -- you write down what you want once, and Compose makes it happen

```
  docker-compose.yaml
  +---------------------+
  | services:           |      docker compose up
  |   - db              | ----------------------->  Running Application
  |   - redis           |                           (all containers, networks,
  |   - worker          |                            and volumes created)
  |   - vote            |
  |   - result          |      docker compose down
  | networks:           | ----------------------->  Everything cleaned up
  |   - app-network     |
  | volumes:            |
  |   - db-data         |
  +---------------------+
```

Key benefits:
- One command to start everything: `docker compose up -d`
- One command to stop everything: `docker compose down`
- The YAML file is version-controlled alongside your code
- Everyone on the team gets the exact same environment

---

## The Voting App Architecture

- Before you touch any commands, understand what you are building
- The Voting App is a classic demo from Docker that uses five separate services wired together

```
  Browser          Browser
     |                |
     v                v
 +--------+       +--------+
 |  VOTE  |       | RESULT |
 | Python |       | NodeJS |
 | :5000  |       | :5001  |
 +--------+       +--------+
     |                ^
     | stores vote    | reads results
     v                |
 +---------+      +----------+
 |  REDIS  |      |    DB    |
 | (Queue) |      | Postgres |
 |         |      |  :5432   |
 +---------+      +----------+
     ^                ^
     |                |
     +----+------+----+
          |
       +--------+
       | WORKER |
       |  .NET  |
       +--------+
       picks votes from REDIS,
       writes them to POSTGRES
```

Data flow step by step:

1. A user opens the VOTE app on port 5000 and clicks "Cats" or "Dogs"
2. The VOTE app stores that vote in REDIS (an in-memory queue)
3. The WORKER service is always watching REDIS; it picks up the vote and writes it permanently to the POSTGRES database
4. The RESULT app on port 5001 reads from POSTGRES and shows a live percentage breakdown

- Each service does one job
- This is the microservices pattern in miniature

---

## Part 1: Understanding the docker-compose.yaml

- Before running anything, read the file
- Understanding the file is more important than running the commands

```yaml
version: "3.8"            # The Compose file format version. 3.8 is a stable, widely-used version.

services:

  db:                     # Service name. Other containers will refer to this as "db" by name.
    image: postgres:15    # Use the official Postgres image, version 15.
    environment:
      POSTGRES_PASSWORD: postgres         # Set the superuser password via environment variable.
      POSTGRES_HOST_AUTH_METHOD: trust    # Allow connections without a password (fine for dev).
    networks:
      - app-network       # Join the shared network so other services can reach this container.
    volumes:
      - db-data:/var/lib/postgresql/data  # Mount the named volume to persist database files.

  redis:
    image: redis:alpine   # Redis using the lightweight Alpine Linux base image.
    networks:
      - app-network

  worker:
    image: docker/example-voting-app-worker
    depends_on:           # Start the worker AFTER db and redis containers are created.
      - db                # IMPORTANT: depends_on controls start ORDER, not readiness.
      - redis             # The worker may still fail if db/redis aren't fully ready yet.
    networks:
      - app-network

  vote:
    image: docker/example-voting-app-vote
    ports:
      - 5000:80           # Map port 80 inside the container to port 5000 on your host machine.
    depends_on:
      - redis
    networks:
      - app-network

  result:
    image: docker/example-voting-app-result
    ports:
      - 5001:80           # Map port 80 inside the container to port 5001 on your host machine.
    depends_on:
      - db
    networks:
      - app-network

volumes:
  db-data:                # Declare a named volume. Compose creates this automatically.
                          # Named volumes survive "docker compose down" (data is NOT deleted).
                          # Only "docker compose down -v" deletes this volume.

networks:
  app-network:            # Declare a custom bridge network. Compose creates this automatically.
                          # All services on this network can reach each other by service name.
```

Key things to notice:
- The `services` section is where you define each container
- Every service that needs to talk to another service must be on the same network
- `volumes` and `networks` at the bottom level are declarations -- Compose will create them
- Port mapping format is always `HOST_PORT:CONTAINER_PORT`

---

## Part 2: Launch the Application

- Navigate to the lab directory and start the stack:

```bash
cd /path/to/07-Containers/Lab/7-docker-voting-app
docker compose up -d
```

- The `-d` flag runs all containers in detached mode (in the background)
- Without `-d`, the logs from all five containers would stream directly to your terminal and you would not get your prompt back

What Compose does when you run this command:
1. Reads `docker-compose.yaml` in the current directory
2. Creates the `app-network` bridge network
3. Creates the `db-data` named volume
4. Pulls any images that are not already on your machine
5. Starts all five containers in dependency order

You will see output like:

```
[+] Running 6/6
 - Network 7-docker-voting-app_app-network  Created
 - Volume "7-docker-voting-app_db-data"     Created
 - Container 7-docker-voting-app-db-1       Started
 - Container 7-docker-voting-app-redis-1    Started
 - Container 7-docker-voting-app-worker-1   Started
 - Container 7-docker-voting-app-vote-1     Started
 - Container 7-docker-voting-app-result-1   Started
```

- Notice the naming pattern: Compose prefixes every resource with the project name (the directory name)
- This avoids collisions with other Compose stacks you might be running

### Verification steps

- Run these commands after `docker compose up -d` to confirm everything is healthy:

```bash
# All 5 services should show status "Up" or "running"
docker compose ps

# View logs from all services at once -- look for errors
docker compose logs

# View logs from a single service
docker compose logs vote
docker compose logs worker

# Confirm the network was created
docker network ls | grep app-network

# Confirm the volume was created
docker volume ls | grep db-data
```

Expected output for `docker compose ps`:

```
NAME                             IMAGE                                COMMAND   SERVICE   CREATED   STATUS    PORTS
7-docker-voting-app-db-1         postgres:15                          ...       db        ...       Up        5432/tcp
7-docker-voting-app-redis-1      redis:alpine                         ...       redis     ...       Up        6379/tcp
7-docker-voting-app-result-1     docker/example-voting-app-result     ...       result    ...       Up        0.0.0.0:5001->80/tcp
7-docker-voting-app-vote-1       docker/example-voting-app-vote       ...       vote      ...       Up        0.0.0.0:5000->80/tcp
7-docker-voting-app-worker-1     docker/example-voting-app-worker     ...       worker    ...       Up
```

- If any service shows "Exit" or "Restarting", check its logs:

```bash
docker compose logs <service-name>
```

---

## Part 3: Explore the Running Application

- With all five containers running, open a browser and test the application end to end

**Step 1 -- Open the Vote UI**

- Open your browser and go to:

```
http://<YOUR-VM-IP>:5000
```

- You will see a simple page with two buttons: "Cats" and "Dogs"
- Click one to cast a vote

**Step 2 -- Open the Result UI**

- Open a new tab and go to:

```
http://<YOUR-VM-IP>:5001
```

- You will see a live results page showing the percentage split between Cats and Dogs
- If you voted in Step 1, your vote should appear here (it may take a second for the worker to process it)

**Step 3 -- Verify the data flow**

- Go back to the Vote UI and cast several more votes
- Watch the Result UI update
- You are seeing all five services working together:
  - The Vote app writes to Redis
  - The Worker reads from Redis and writes to Postgres
  - The Result app reads from Postgres

---

## Part 4: Inspect the Compose Stack

- Dig under the hood with these commands to understand what Compose actually created

```bash
# See all containers in the stack and their status
docker compose ps

# See CPU and memory usage for all running containers (press Ctrl+C to exit)
docker stats

# Inspect the network -- see all containers connected to it and their IP addresses
docker network inspect 7-docker-voting-app_app-network

# Inspect the volume -- see where Docker stores the data on your host
docker volume inspect 7-docker-voting-app_db-data

# Run a command inside the db container to query the votes table
docker compose exec db psql -U postgres -c "SELECT * FROM votes;"
```

What to look for in `docker network inspect`:
- The "Containers" section will list all five services with their internal IP addresses
- All containers are on the same subnet, which is why they can talk to each other by name

What `docker compose exec` does:
- It runs a command inside an already-running container
- Here you are running the `psql` command inside the `db` container to directly query the Postgres database
- You should see rows for each vote that was cast

---

## Part 5: Scaling Services

- One of Compose's features is the ability to run multiple instances of a service
- This is useful when one instance cannot handle the load

```bash
# Scale the vote service to 3 instances
docker compose up -d --scale vote=3

# Check that 3 vote containers are now running
docker compose ps
```

- You will immediately hit a problem:

```
Error: address already in use
```

- This happens because all three vote instances are trying to bind to port 5000 on your host
- Only one process can own a port at a time
- This is a fundamental port conflict

To fix this, you would need to remove the fixed host port from the vote service in `docker-compose.yaml`:

```yaml
# Change this:
  vote:
    ports:
      - 5000:80

# To this (let Docker assign a random available port for each instance):
  vote:
    ports:
      - 80    # No host port specified -- Docker picks one automatically
```

- After making that change, `docker compose up -d --scale vote=3` would work
- Run `docker compose ps` to see what random ports were assigned to each instance

Scale back to 1 for now:

```bash
docker compose up -d --scale vote=1
```

---

## Part 6: Lifecycle Management

- Understanding how to manage the lifecycle of a Compose stack is essential
- There are several commands with important differences between them

```bash
# STOP: pause all containers but keep them (and their data) intact
docker compose stop
docker compose ps -a    # You should see all containers in "Exited" state

# START: resume stopped containers
docker compose start
docker compose ps       # All containers should be "Up" again

# RESTART: stop and start a single service (useful after a config change)
docker compose restart vote

# LOGS: follow real-time log output from a service (Ctrl+C to stop)
docker compose logs -f worker

# DOWN: stop and REMOVE all containers and networks (volumes are kept)
docker compose down
docker compose ps -a    # No containers should appear
docker volume ls        # db-data volume still exists

# DOWN with -v: stop and remove containers, networks, AND volumes (data is gone)
docker compose down -v
docker volume ls        # db-data volume is now gone
```

The critical difference between `stop` and `down`:

```
  docker compose stop
  - Containers are stopped (paused)
  - Containers still exist on disk
  - Networks still exist
  - Volumes still exist
  - You can resume with "docker compose start"

  docker compose down
  - Containers are stopped AND deleted
  - Networks are deleted
  - Volumes are KEPT (your data survives)
  - You need "docker compose up" to start again

  docker compose down -v
  - Everything above PLUS volumes are deleted
  - ALL DATA IS LOST -- use with caution
```

Rule of thumb:
- Use `stop`/`start` when you want to pause work and come back later
- Use `down` when you want a clean slate but need to keep your database data
- Use `down -v` only when you want to completely reset everything

---

## Part 7: Key Compose Concepts

### Service Discovery

- In Docker Compose, every service can reach every other service simply by using the service name as a hostname
- You do not need to know IP addresses

For example, in the Voting App:
- The worker service connects to Redis using the hostname `redis`
- The worker service connects to Postgres using the hostname `db`
- The result service connects to Postgres using the hostname `db`

Why this works:
- Compose creates a custom bridge network with a built-in DNS server
- When a container asks "what is the IP address of `db`?", the Docker DNS server answers with the internal IP of the `db` container

```
  worker container asks: "what is the IP of redis?"
        |
        v
  Docker DNS (built into app-network)
        |
        v
  Returns: 172.18.0.3  (or whatever internal IP redis has)
        |
        v
  worker connects to redis successfully
```

- This is why every service is declared under the same `networks: - app-network`
- If a service is not on the same network, it cannot be reached by name (or at all)

### depends_on

- The `depends_on` key tells Compose to start services in a particular order
- In the Voting App:

```yaml
worker:
  depends_on:
    - db
    - redis
```

- This means: start `db` and `redis` containers before starting `worker`

**Important limitation:**
- `depends_on` only waits for the container to START, not for the application inside the container to be READY
- Postgres takes a few seconds to initialize after the container starts
- The worker might start, try to connect to Postgres, find it not ready yet, and crash
- For production use, you would add a `healthcheck` to the `db` service so Compose knows when Postgres is actually accepting connections
- The challenge section at the end of this lab asks you to do exactly that

### Volumes in Compose

- There are two types of volumes in a Compose file:

```
  Named Volume (declared at top level)          Bind Mount (not used here)
  +----------------------------------+          +----------------------------------+
  | volumes:                         |          | volumes:                         |
  |   db-data:                       |          |   - ./data:/var/lib/data          |
  |                                  |          |                                  |
  | services:                        |          | Maps a directory on your HOST    |
  |   db:                            |          | directly into the container.     |
  |     volumes:                     |          | Good for development (live code  |
  |       - db-data:/var/lib/...     |          | changes appear inside container).|
  |                                  |          +----------------------------------+
  | Docker manages the storage.      |
  | Survives "docker compose down".  |
  | Deleted by "docker compose down  |
  | -v" only.                        |
  +----------------------------------+
```

- Named volumes are the right choice for database data
- Docker manages the storage location
- The data persists across restarts and `docker compose down` cycles

---

## Cleanup

- When you are done with the lab, tear down the entire stack including volumes:

```bash
docker compose down -v
```

- Confirm everything is gone:

```bash
docker compose ps -a        # Should show nothing
docker volume ls            # db-data volume should be gone
docker network ls           # app-network should be gone
```

---

## Challenges

- These challenges are designed to deepen your understanding
- Try them in order

**Challenge 1 -- Add a healthcheck to the db service**

- The `depends_on` ordering is not enough for production because `db` might not be ready when `worker` starts
- Add a healthcheck so Compose knows when Postgres is actually accepting connections
- The command to check if Postgres is ready is `pg_isready -U postgres`
- Add this under the `db` service in `docker-compose.yaml`:

```yaml
db:
  image: postgres:15
  healthcheck:
    test: ["CMD", "pg_isready", "-U", "postgres"]
    interval: 5s
    timeout: 3s
    retries: 5
```

- Then update `worker` and `result` to use `condition: service_healthy` in their `depends_on`

**Challenge 2 -- Add an Adminer service**

- Adminer is a web-based database browser
- Add it to the Compose file so you can explore the Postgres database through a web UI without using `psql`
- Add this service to your `docker-compose.yaml`:

```yaml
adminer:
  image: adminer
  ports:
    - 8080:8080
  networks:
    - app-network
  depends_on:
    - db
```

- After `docker compose up -d`, open `http://<VM-IP>:8080`
- Use these connection details:
  - System: PostgreSQL
  - Server: db
  - Username: postgres
  - Password: postgres
  - Database: postgres

**Challenge 3 -- Query the votes table directly**

- Use `docker compose exec` to connect to the running Postgres container and query the votes table
- You should see a row for each vote cast through the Vote UI

```bash
docker compose exec db psql -U postgres -c "SELECT * FROM votes;"
docker compose exec db psql -U postgres -c "SELECT vote, COUNT(*) FROM votes GROUP BY vote;"
```

- What does the schema of the votes table look like?
- Use `\d votes` inside an interactive psql session to find out

**Challenge 4 -- Add memory limits to each service**

- Resource limits prevent a single misbehaving container from consuming all the memory on your host
- Add a memory limit of 256MB to each service
- Under each service, add a `deploy` section:

```yaml
vote:
  image: docker/example-voting-app-vote
  deploy:
    resources:
      limits:
        memory: 256m
```

- After adding limits to all five services, bring the stack down and back up
- Use `docker stats` to watch memory usage and confirm no service exceeds 256MB

**Challenge 5 -- Write a Spring Boot + Express.js + Postgres Compose file**

Create a new directory and write a `docker-compose.yaml` from scratch with 3 services:

```yaml
# Your task: create this file from memory
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - pg-data:/var/lib/postgresql/data
    networks:
      - backend

  spring-api:
    image: spring-boot-app:v1    # or any Spring Boot image you built in Lab 2
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/myapp
      SPRING_DATASOURCE_USERNAME: postgres
      SPRING_DATASOURCE_PASSWORD: secret
    depends_on:
      - postgres
    networks:
      - backend
      - frontend

  express-frontend:
    image: express-web-service:v1  # or any Express image you built in Lab 2
    ports:
      - "3000:3000"
    environment:
      API_URL: http://spring-api:8080
    depends_on:
      - spring-api
    networks:
      - frontend

volumes:
  pg-data:

networks:
  frontend:
  backend:
```

- This mirrors a real-world architecture: Express frontend -> Spring Boot API -> Postgres DB
- `spring-api` is on BOTH networks (it is the bridge between frontend and backend)
- `express-frontend` cannot reach `postgres` directly (different networks)
- Service discovery by name: Express calls `http://spring-api:8080`, Spring Boot calls `jdbc:postgresql://postgres:5432`
- This tests everything you learned: images, containers, volumes, networking, and Compose
