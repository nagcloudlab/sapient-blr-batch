# FoodExpress Training — Environment Setup Guide

**Programme:** Publicis Sapient Sustain Engineering (SRE + ITIL)
**Duration:** 43.5 days | **Start:** July 29, 2026 | **Location:** Bangalore
**Trainer:** Nagabhushanam

---

## Prerequisites Table

| Tool | Version | Used In | Windows Install | Mac/Linux Install |
|------|---------|---------|-----------------|-------------------|
| Google Chrome | Latest | M01–M04 | Download from chrome.google.com | Same |
| VS Code | Latest | All modules | `winget install Microsoft.VisualStudioCode` | `brew install --cask visual-studio-code` |
| Git | 2.x+ | M19, All | `winget install Git.Git` | `brew install git` / `sudo apt install git` |
| Node.js | 18 LTS+ | M03–M04, M09–M11 | `winget install OpenJS.NodeJS.LTS` | `brew install node@18` / use nvm |
| Java JDK | 17+ | M05–M08 | `winget install Microsoft.OpenJDK.17` | `brew install openjdk@17` / `sudo apt install openjdk-17-jdk` |
| Maven | 3.8+ | M05–M08 | Download from maven.apache.org, add to PATH | `brew install maven` / `sudo apt install maven` |
| MySQL | 8.0 | M12 | MySQL Installer from dev.mysql.com | `brew install mysql@8.0` / `sudo apt install mysql-server` |
| MongoDB | 7.0 | M12 | MongoDB MSI from mongodb.com/try/download | `brew install mongodb-community@7.0` / apt from MongoDB repo |
| Docker Desktop | Latest | M24–M26, M32 | Download from docker.com/products/docker-desktop | Same (Desktop) or `brew install --cask docker` |
| kubectl | 1.28+ | M29 | `winget install Kubernetes.kubectl` | `brew install kubectl` / via cloud SDK |
| minikube | Latest | M29 | `winget install Kubernetes.minikube` | `brew install minikube` |
| Ansible | 2.15+ | M30 | Via WSL (see Phase 9) | `brew install ansible` / `pip3 install ansible` |
| Apache2 | 2.4+ | M21 | XAMPP from apachefriends.org | `brew install httpd` / `sudo apt install apache2` |
| Jenkins | 2.x LTS | M28 | Docker method (see Phase 7) | Docker method (same) |
| Python | 3.x | Tooling | `winget install Python.Python.3` | Pre-installed / `brew install python` |

---

## Installation Instructions by Phase

### Phase 1 — Day 1 (M01–M04: HTML, CSS, JavaScript, UI Frameworks)

**Install: Chrome, VS Code, Git, Node.js**

#### Windows

```bat
:: Install all at once via winget
winget install Google.Chrome
winget install Microsoft.VisualStudioCode
winget install Git.Git
winget install OpenJS.NodeJS.LTS
```

Restart your terminal after installation, then verify:

```bat
node -v
npm -v
git --version
code --version
```

#### VS Code Extensions (install once)

Open VS Code, press `Ctrl+Shift+X`, and install:

- ESLint
- Prettier - Code formatter
- Live Server
- GitLens
- Java Extension Pack (install now, used in Phase 2)
- Docker (install now, used in Phase 6)

#### Mac/Linux

```bash
brew install node@18 git
brew install --cask google-chrome visual-studio-code
```

---

### Phase 2 — Day 6 (M05–M08: Java Spring Boot)

**Install: Java JDK 17, Maven**

#### Windows

```bat
winget install Microsoft.OpenJDK.17
```

Set `JAVA_HOME` environment variable:

1. Open "Edit the system environment variables" (search in Start)
2. Under System Variables, click New:
   - Variable name: `JAVA_HOME`
   - Variable value: `C:\Program Files\Microsoft\jdk-17.0.x.x-hotspot` (adjust to your install path)
3. Edit the `Path` variable and add: `%JAVA_HOME%\bin`
4. Click OK, restart terminal

Install Maven:

1. Download apache-maven-3.9.x-bin.zip from https://maven.apache.org/download.cgi
2. Extract to `C:\tools\maven`
3. Add `C:\tools\maven\bin` to the system `Path` variable

```bat
java -version
mvn -version
```

#### Mac/Linux

```bash
brew install openjdk@17 maven
echo 'export JAVA_HOME=$(brew --prefix openjdk@17)' >> ~/.zshrc
source ~/.zshrc
```

---

### Phase 3 — Day 10 (M09–M11: Node.js Backend)

Node.js is already installed from Phase 1. Install MongoDB:

**Install: MongoDB 7.0**

#### Windows

1. Download the MongoDB Community Server MSI from https://www.mongodb.com/try/download/community
2. Select Version 7.0, Platform Windows, Package MSI
3. Run installer — choose "Complete" setup, check "Install MongoDB as a Service"
4. MongoDB will run on port **27017** by default

Install MongoDB Shell separately:

1. Download mongosh from https://www.mongodb.com/try/download/shell
2. Extract and add the `bin` folder to system `Path`

```bat
mongosh --version
```

#### Mac/Linux

```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

---

### Phase 4 — Day 13 (M12: Databases — SQL)

**Install: MySQL 8.0**

#### Windows

1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Choose "mysql-installer-community" (full package)
3. Select "Developer Default" setup type
4. During configuration: set root password (note it down — you will need it)
5. Leave port as **3306**, enable "Configure MySQL Server as a Windows Service"

```bat
mysql --version
mysql -u root -p
```

#### Mac/Linux

```bash
brew install mysql@8.0
brew services start mysql@8.0
mysql_secure_installation
```

---

### Phase 5 — Day 21 (M21: Apache Web Server)

**Install: Apache2**

#### Windows

Install XAMPP (includes Apache2 + PHP, easiest on Windows):

1. Download from https://www.apachefriends.org/download.html
2. Install to `C:\xampp`
3. Open XAMPP Control Panel, click "Start" next to Apache
4. Apache listens on port **80** (or **8080** if port 80 is taken)

Alternatively, use the standalone Apache Lounge builds from https://www.apachelounge.com/download/

#### Mac/Linux

```bash
# Mac
brew install httpd
brew services start httpd

# Linux
sudo apt update && sudo apt install apache2
sudo systemctl start apache2
sudo systemctl enable apache2
```

---

### Phase 6 — Day 27 (M24–M26: Docker)

**Install: Docker Desktop**

#### Windows

1. Download Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Run installer — requires WSL 2 backend (installer prompts you to install if missing)
3. After install, launch Docker Desktop and wait for the engine to start (whale icon in system tray turns solid)
4. Allocate at least **4 GB RAM** in Docker Desktop Settings > Resources > Memory

```bat
docker --version
docker run hello-world
```

**Note:** Docker Desktop requires Windows 10/11 with WSL 2. If WSL 2 is not installed, run in PowerShell (as Admin):

```powershell
wsl --install
```

Then restart and re-run the Docker Desktop installer.

#### Mac/Linux

```bash
# Mac
brew install --cask docker
# Then open Docker.app from Applications

# Linux
sudo apt install docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
```

---

### Phase 7 — Day 31 (M28: Jenkins)

**Install: Jenkins via Docker**

This avoids Java version conflicts. Docker Desktop must be running.

#### Windows / Mac / Linux (same command)

```bash
docker network create jenkins

docker run --name jenkins --detach \
  --network jenkins \
  --publish 8081:8080 \
  --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  jenkins/jenkins:lts-jdk17
```

Jenkins will be available at http://localhost:8081

Get the initial admin password:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open browser, paste the password, install suggested plugins, create an admin user.

**Note:** Jenkins runs on port **8081** here to avoid conflict with Spring Boot apps on **8080**.

---

### Phase 8 — Day 32 (M29: Kubernetes)

**Install: kubectl + minikube**

#### Windows

```bat
winget install Kubernetes.kubectl
winget install Kubernetes.minikube
```

Start minikube (uses Docker as the driver — Docker Desktop must be running):

```bat
minikube start --driver=docker --memory=4096 --cpus=2
```

#### Mac/Linux

```bash
brew install kubectl minikube
minikube start --driver=docker --memory=4096 --cpus=2
```

Verify:

```bash
kubectl version --client
minikube status
```

---

### Phase 9 — Day 33 (M30: Ansible)

Ansible does not run natively on Windows. Use WSL (Windows Subsystem for Linux).

**Install: WSL + Ansible**

#### Windows

Step 1 — Install WSL (run in PowerShell as Administrator):

```powershell
wsl --install -d Ubuntu
```

Restart your machine. On first launch, create a Linux username and password.

Step 2 — Install Ansible inside WSL:

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible
ansible --version
```

Step 3 — Access your Windows files from WSL at `/mnt/c/Users/YourName/`

#### Mac/Linux

```bash
# Mac
brew install ansible

# Linux
sudo apt install ansible
# or
pip3 install ansible
```

---

### Phase 10 — Day 36 (M32: Observability — Prometheus + Grafana)

**Install: Prometheus + Grafana via Docker Compose**

Docker Desktop must be running.

Create a file `C:\tools\observability\docker-compose.yml`:

```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

Create `C:\tools\observability\prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

Start the stack:

```bash
cd C:/tools/observability
docker compose up -d
```

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (login: admin / admin)

---

## Verification Commands

Run this checklist at the start of each phase to confirm your environment is ready.

| Tool | Command | Expected Output |
|------|---------|-----------------|
| Node.js | `node -v` | `v18.x.x` or higher |
| npm | `npm -v` | `9.x.x` or higher |
| Git | `git --version` | `git version 2.x.x` |
| Java | `java -version` | `openjdk version "17.x.x"` |
| Maven | `mvn -version` | `Apache Maven 3.8.x` |
| MySQL | `mysql --version` | `mysql  Ver 8.0.x` |
| MongoDB Shell | `mongosh --version` | `2.x.x` |
| Docker | `docker --version` | `Docker version 24.x.x` |
| Docker test | `docker run hello-world` | `Hello from Docker!` |
| kubectl | `kubectl version --client` | `Client Version: v1.28.x` |
| minikube | `minikube version` | `minikube version: v1.x.x` |
| Ansible | `ansible --version` | `ansible [core 2.15.x]` |
| Python | `python --version` | `Python 3.x.x` |
| VS Code | `code --version` | version number printed |

---

## Troubleshooting

### Java: JAVA_HOME not set

**Symptom:** `mvn` or Spring Boot run fails with "JAVA_HOME not set" or "java not found"

**Fix (Windows):**
1. Find your JDK install path: `where java` or check `C:\Program Files\Microsoft\`
2. Open System Properties > Environment Variables
3. Add System Variable: `JAVA_HOME` = `C:\Program Files\Microsoft\jdk-17.x.x-hotspot`
4. Edit `Path`, add `%JAVA_HOME%\bin`
5. Restart all terminals

**Fix (Mac/Linux):**
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)   # Mac
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64  # Ubuntu
echo 'export JAVA_HOME=...' >> ~/.bashrc && source ~/.bashrc
```

---

### Node.js: `node` or `npm` not recognized

**Symptom:** `'node' is not recognized as an internal or external command`

**Fix (Windows):**
1. Close and reopen your terminal after installation
2. Check if Node is on PATH: `where node`
3. If missing, open System Properties > Environment Variables > Path
4. Add the Node.js install folder (typically `C:\Program Files\nodejs`)
5. Restart terminal

---

### Docker: Not enough memory

**Symptom:** Containers crash, `OOMKilled` errors, or minikube fails to start

**Fix:**
1. Open Docker Desktop > Settings > Resources > Memory
2. Increase to at least **4 GB** (6 GB recommended for Kubernetes labs)
3. Click "Apply & Restart"

For minikube, explicitly set resources:
```bash
minikube delete
minikube start --driver=docker --memory=4096 --cpus=2
```

---

### MySQL: Root password reset

**Symptom:** Cannot login to MySQL, forgot root password

**Fix (Windows — MySQL as a service):**

```bat
:: Stop MySQL service
net stop MySQL80

:: Start in skip-grant-tables mode (run as Admin)
mysqld --skip-grant-tables --skip-networking

:: In a new terminal, connect without password
mysql -u root

:: Reset the password
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewPassword123';
EXIT;

:: Stop the temporary instance (Ctrl+C in the first terminal)
:: Restart MySQL service normally
net start MySQL80
```

---

### Port Conflicts

If a service fails to start because a port is in use:

| Port | Service | How to Check (Windows) | How to Free |
|------|---------|------------------------|-------------|
| 3000 | Node.js / React dev server | `netstat -ano \| findstr :3000` | Kill the PID: `taskkill /PID <pid> /F` |
| 3001 | Grafana | `netstat -ano \| findstr :3001` | Same |
| 8080 | Spring Boot / Jenkins | `netstat -ano \| findstr :8080` | Same |
| 8081 | Jenkins (alt) | `netstat -ano \| findstr :8081` | Same |
| 27017 | MongoDB | `netstat -ano \| findstr :27017` | Same |
| 3306 | MySQL | `netstat -ano \| findstr :3306` | Same |
| 9090 | Prometheus | `netstat -ano \| findstr :9090` | Same |

**Mac/Linux equivalent:**
```bash
lsof -i :8080
kill -9 <PID>
```

**Alternative:** Change the port in your app config instead of killing the existing service.
For Spring Boot, edit `application.properties`: `server.port=8082`
For Node.js: `PORT=3002 node server.js`

---

### WSL Installation for Ansible (Windows)

**Symptom:** `wsl --install` fails or WSL version is 1 not 2

**Fix:**

Ensure virtualization is enabled in BIOS (Intel VT-x or AMD-V). Check in Task Manager > Performance > CPU > Virtualization: Enabled.

```powershell
# Run in PowerShell as Administrator

# Ensure WSL feature is enabled
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart, then set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu
wsl --install -d Ubuntu
```

If WSL is already installed as version 1:
```powershell
wsl --list --verbose           # check version
wsl --set-version Ubuntu 2     # upgrade to WSL 2
```

---

### minikube Driver Issues

**Symptom:** `minikube start` fails with driver errors

**Common fixes:**

```bash
# If Docker driver fails, check Docker is running first
docker info

# Delete and recreate with explicit driver
minikube delete
minikube start --driver=docker

# If Docker driver is unavailable, try Hyper-V (Windows Pro/Enterprise only)
minikube start --driver=hyperv

# Check minikube logs for details
minikube logs
```

**Windows Home users:** Hyper-V is not available. Use Docker Desktop (WSL 2 backend) as the driver.

---

## Network Requirements

Ensure the training machines can reach the following hosts. Contact IT/network admin to whitelist if on a restricted corporate network.

| Category | URLs / Domains | Used In |
|----------|----------------|---------|
| CDN — Bootstrap | cdn.jsdelivr.net, cdnjs.cloudflare.com | M01–M04 |
| CDN — Google Fonts | fonts.googleapis.com, fonts.gstatic.com | M01–M04 |
| npm Registry | registry.npmjs.org | M03, M09–M11 |
| Maven Central | repo.maven.apache.org, central.sonatype.com | M05–M08 |
| Docker Hub | hub.docker.com, registry-1.docker.io, auth.docker.io | M24–M32 |
| GitHub | github.com, raw.githubusercontent.com | M19, All |
| MongoDB Atlas (optional) | cloud.mongodb.com, *.mongodb.net | M12 |
| Java downloads | aka.ms (Microsoft OpenJDK), adoptium.net | M05 setup |

**Proxy configuration (if behind a corporate proxy):**

```bash
# npm
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# Maven — add to ~/.m2/settings.xml
# Docker Desktop — Settings > Resources > Proxies

# Git
git config --global http.proxy http://proxy.company.com:8080

# WSL / apt
export http_proxy=http://proxy.company.com:8080
export https_proxy=http://proxy.company.com:8080
```

---

## Quick-Start Checklist by Day

| Day | Phase | Must Have Ready |
|-----|-------|-----------------|
| Day 1 | 1 | Chrome, VS Code, Git, Node.js 18 |
| Day 6 | 2 | Java JDK 17, Maven 3.8+ |
| Day 10 | 3 | MongoDB 7.0, mongosh |
| Day 13 | 4 | MySQL 8.0 |
| Day 21 | 5 | Apache2 / XAMPP |
| Day 27 | 6 | Docker Desktop (engine running) |
| Day 31 | 7 | Jenkins container running on :8081 |
| Day 32 | 8 | kubectl, minikube (cluster started) |
| Day 33 | 9 | WSL 2 + Ansible |
| Day 36 | 10 | Prometheus (:9090) + Grafana (:3001) via Docker |
