# Lab 06 - Spring Boot Playbook

## Objective
Build a Spring Boot app locally, deploy it to VM2 using Ansible

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)
- Java 17 and Maven installed locally (`brew install maven` / `sudo apt install maven`)

> **IMPORTANT:** You must build the JAR before running the playbook!
> ```bash
> cd app && mvn clean package -DskipTests && cd ..
> ```

---

## What We'll Do
- Build a simple REST API (hello-api) locally
- Use Ansible to **copy the JAR** to VM2
- Install Java, create systemd service, start the app
- Verify with health checks

## App Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /` | App status + timestamp |
| `GET /api/hello?name=Ansible` | Hello greeting |
| `GET /api/info` | JVM and OS info |
| `GET /actuator/health` | Spring Boot health check |

---

## Step 1: Build the JAR Locally

```bash
cd app

# Build the JAR (requires Maven + Java 17 locally)
mvn clean package -DskipTests

# Verify the JAR was created
ls -lh target/hello-api-1.0.0.jar

# (Optional) Test locally before deploying
java -jar target/hello-api-1.0.0.jar
# Visit http://localhost:8080
# Ctrl+C to stop

cd ..
```

### Don't have Maven?
```bash
# Mac
brew install maven

# WSL/Ubuntu
sudo apt install -y maven
```

## Step 2: Deploy with Ansible

```bash
# Dry run first
ansible-playbook springboot-setup.yml --check

# Deploy!
ansible-playbook springboot-setup.yml
```

### What the playbook does:
1. Installs Java 17 on VM2
2. Creates a `springboot` system user (no login shell — security)
3. Creates `/opt/springboot/` directory
4. **Copies** `app/target/hello-api-1.0.0.jar` from your Mac to VM2
5. Copies `application.yml` config
6. Creates a systemd service file
7. Starts the service + waits for port 8080
8. Runs a health check

## Step 3: Verify the Application

```bash
# Hit the API from your Mac
curl http://<VM2_IP>:8080/
curl http://<VM2_IP>:8080/api/hello
curl http://<VM2_IP>:8080/api/hello?name=Ansible
curl http://<VM2_IP>:8080/api/info
curl http://<VM2_IP>:8080/actuator/health

# Check service status via Ansible
ansible appservers -m shell -a "systemctl status springboot"

# Check logs
ansible appservers -m shell -a "journalctl -u springboot --no-pager -n 20"
```

### Expected Output
```json
# curl http://<VM2_IP>:8080/
{"app":"hello-api","status":"running","timestamp":"2024-..."}

# curl http://<VM2_IP>:8080/api/hello?name=Ansible
{"message":"Hello, Ansible!","from":"vm2-springboot"}

# curl http://<VM2_IP>:8080/actuator/health
{"status":"UP"}
```

## Step 4: Test Service Recovery

```bash
# Kill the Java process
ansible appservers -m shell -a "pkill -f hello-api" --become

# Wait 10 seconds (RestartSec=10 in systemd), then check
# systemd should auto-restart it!
ansible appservers -m shell -a "systemctl status springboot" --become
```

## Step 5: Update and Re-deploy

```bash
# Make a code change in app/src/...
# Rebuild
cd app && mvn clean package -DskipTests && cd ..

# Re-deploy — Ansible detects the JAR changed, copies it, restarts
ansible-playbook springboot-setup.yml

# Only the changed tasks trigger handlers (smart!)
```

---

## App Source Code

```
app/
├── pom.xml                                    # Maven config
└── src/main/
    ├── java/com/example/helloapi/
    │   ├── HelloApiApplication.java           # Main class
    │   └── HelloController.java               # REST endpoints
    └── resources/
        └── application.yml                    # App config
```

## Ansible Files

| File | Description |
|------|-------------|
| `springboot-setup.yml` | Main playbook (copy JAR + deploy) |
| `files/springboot.service` | systemd unit file |
| `files/application.yml` | Spring Boot config for VM |
| `app/` | Spring Boot source code |

---

## copy vs get_url

| Module | Use When |
|--------|----------|
| `copy` | JAR is built locally (what we do here) |
| `get_url` | JAR is hosted on a URL (Nexus, GitHub Releases, S3) |

```yaml
# What we use — copy from local machine to remote
- name: Copy JAR
  copy:
    src: app/target/hello-api-1.0.0.jar
    dest: /opt/springboot/hello-api-1.0.0.jar

# Alternative — download from URL
- name: Download JAR
  get_url:
    url: https://nexus.example.com/hello-api-1.0.0.jar
    dest: /opt/springboot/hello-api-1.0.0.jar
```

---

## Troubleshooting

### "the file app/target/hello-api-1.0.0.jar does not exist"
```bash
# You forgot to build the JAR! Run:
cd app && mvn clean package -DskipTests && cd ..
```

### "mvn: command not found"
```bash
# Mac
brew install maven
# WSL/Ubuntu
sudo apt install -y maven
```

### App starts but port 8080 not accessible
```bash
# Check GCP firewall allows port 8080
gcloud compute firewall-rules list --filter="allowed:8080"
# If missing:
gcloud compute firewall-rules create allow-8080 --allow tcp:8080 --target-tags=http-server
```

### Check app logs for errors
```bash
ansible appservers -m shell -a "journalctl -u springboot --no-pager -n 50"
```

## Key Takeaways
- Build locally, deploy with Ansible — simple CI/CD
- `copy` module transfers files from control node to managed node
- `systemd` manages the app lifecycle (start/stop/auto-restart)
- `wait_for` + `uri` = built-in health checks
- Handlers avoid unnecessary restarts
- `journalctl -u springboot` = check app logs
- Next: Use **templates** to connect NGINX to Spring Boot
