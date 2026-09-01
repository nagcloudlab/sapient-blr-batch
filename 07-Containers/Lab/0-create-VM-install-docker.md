# Lab 0: Setting Up Your Docker Environment

---

## Objectives

By the end of this lab, you will be able to:

- Create a Linux virtual machine on Azure using the CLI
- Connect to a remote VM over SSH
- Install Docker Engine on Ubuntu 24.04
- Run your first container and understand what happened
- Describe the core components of Docker architecture

---

## Prerequisites

- Azure CLI installed and logged in on your laptop (`az login`)
- An SSH key pair generated on your laptop (`~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`)
- Basic comfort with a terminal / command line

To verify your Azure CLI is ready:

```bash
az account show
```

- You should see your subscription name and ID in the output

---

## Part 1: Understanding the Lab Environment

### Why a Cloud VM instead of your laptop?

- Docker runs best on Linux — containers share the Linux kernel directly
- On macOS and Windows, Docker Desktop adds a hidden Linux VM underneath
- This adds complexity and causes "works on my machine" issues between student laptops
- Using an Azure VM running Ubuntu gives you the native Docker experience
- Every student in this batch works on an identical Ubuntu 24.04 environment
- Instructions and terminal outputs will match exactly across all machines

### How the connection works

```
+----------------+        SSH (port 22)       +-------------------------+
|                |  ------------------------> |   Azure VM (Ubuntu)     |
|  Your Laptop   |                            |                         |
|  (any OS)      |  <------------------------ |   Docker Engine runs    |
|                |     terminal output        |   inside this Linux OS  |
+----------------+                            +-------------------------+
                                                          |
                                              +-----------v-----------+
                                              |   Containers          |
                                              |   (isolated processes)|
                                              +-----------------------+
```

- Your laptop is just a terminal window
- All Docker work happens on the remote VM

---

## Part 2: Create an Azure VM

### What is a Resource Group?

- A resource group is Azure's way of bundling related cloud resources together
- It groups things like your VM, disk, network interface, and public IP under one name
- This makes it easy to manage and delete everything at once when you are done
- Think of it as a folder that holds all the pieces of your lab environment

### Step 1: Create a resource group

```bash
az group create --name myResourceGroup --location centralindia
```

Expected output (abbreviated):

```json
{
  "id": "/subscriptions/<your-id>/resourceGroups/myResourceGroup",
  "location": "centralindia",
  "name": "myResourceGroup",
  "properties": {
    "provisioningState": "Succeeded"
  }
}
```

- Look for `"provisioningState": "Succeeded"` to confirm it worked

### Step 2: Create the Ubuntu VM

```bash
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image Ubuntu2404 \
  --size Standard_D4s_v3 \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --public-ip-sku Standard
```

What each flag means:

| Flag | Meaning |
|---|---|
| `--resource-group` | Which resource group to put this VM in |
| `--name` | The name for your VM inside Azure |
| `--image` | Which OS image to use (Ubuntu 24.04 LTS here) |
| `--size` | Hardware size: Standard_D4s_v3 = 4 vCPUs, 16 GB RAM |
| `--admin-username` | The Linux user that will be created on the VM |
| `--ssh-key-values` | Your public key — Azure installs it so you can log in without a password |
| `--public-ip-sku` | Type of public IP address (Standard is required for most features) |

- This command takes 1-3 minutes to complete
- When it finishes, the output will include a `publicIpAddress` field
- Copy that IP address — you will need it to SSH in

Expected output (abbreviated):

```json
{
  "fqdns": "",
  "id": "/subscriptions/.../virtualMachines/myVM",
  "publicIpAddress": "20.204.182.165",
  "resourceGroup": "myResourceGroup",
  "zones": ""
}
```

### Step 3: Open port 80 (for later labs)

```bash
az vm open-port --resource-group myResourceGroup --name myVM --port 80
```

- This modifies the VM's Network Security Group to allow inbound HTTP traffic
- You will need this when running web server containers in later labs

### Step 4: Get the public IP address (if you need to look it up again)

```bash
az vm list-ip-addresses --resource-group myResourceGroup --name myVM --output table
```

---

## Part 3: Connect to Your VM

### What is SSH?

- SSH (Secure Shell) is a protocol that lets you open an encrypted terminal session on a remote machine
- You authenticate using your private key (`~/.ssh/id_rsa`)
- That private key matches the public key you uploaded to Azure during VM creation
- No password is needed

### Step 1: Fix permissions on your private key

```bash
chmod 600 ~/.ssh/id_rsa
```

- SSH will refuse to use a private key file that is readable by other users on your system
- `chmod 600` sets the file to owner-read/write only

### Step 2: Connect

Replace `20.204.182.165` with the actual IP address from the `az vm create` output.

```bash
ssh -i ~/.ssh/id_rsa azureuser@20.204.182.165
```

- If prompted "Are you sure you want to continue connecting (yes/no)?", type `yes` and press Enter

Verification: You should now see a prompt that looks like this:

```
azureuser@myVM:~$
```

- You are now inside the Ubuntu VM
- All subsequent commands in this lab run here, not on your laptop

### Confirm the OS

```bash
cat /etc/os-release
```

- Look for `PRETTY_NAME="Ubuntu 24.04 LTS"` in the output

---

## Part 4: Set Up Your Shell (Optional)

- The default shell on Ubuntu is `bash`
- This section installs `zsh` with `oh-my-zsh`, a popular configuration framework
- It gives you a cleaner prompt, command history search, and better tab completion
- This is optional but recommended for a better experience during the labs

### Install zsh

```bash
sudo apt update
sudo apt install zsh -y
```

### Install oh-my-zsh

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" -y
```

- When prompted whether to make zsh your default shell, type `Y`
- You will need to log out and back in for the change to take effect

---

## Part 5: Install Docker

### What is Docker?

- Docker is a platform that packages an application and everything it needs to run into a single unit called a container
- A container includes the code, runtime, libraries, and config — all bundled together
- Containers are isolated from each other and from the host OS
- They share the host's Linux kernel, making them much lighter than virtual machines
- A container that runs on your VM will run identically on a colleague's VM, a CI server, or in production
- The environment travels with the application

### Docker Architecture Overview

```
+------------------+          +-----------------------------+
|   Docker Client  |  ------> |      Docker Daemon          |
|  (docker CLI)    |  (API)   |  (dockerd)                  |
+------------------+          |                             |
                               |  +--------+  +--------+   |
                               |  | Image  |  | Image  |   |
                               |  +--------+  +--------+   |
                               |       |                    |
                               |  +----v---+  +--------+   |
                               |  |Container|  |Container|  |
                               |  +--------+  +--------+   |
                               +-----------------------------+
                                              |
                                    +---------v---------+
                                    |  Docker Registry   |
                                    |  (Docker Hub, etc) |
                                    +-------------------+
```

- The CLI (`docker`) is the tool you type commands into
- The Daemon (`dockerd`) is the background service that actually manages containers and images
- A Registry (e.g., Docker Hub) is a remote store where images are published and downloaded from

### Step 1: Update package lists and install dependencies

```bash
sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
```

- These packages allow `apt` to fetch packages over HTTPS
- They also allow `apt` to verify package authenticity using certificates

### Step 2: Add Docker's official GPG key

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

- This downloads Docker's signing key and registers it with `apt`
- It ensures that any package you download from Docker's repository has not been tampered with

### Step 3: Add Docker's apt repository

```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

- This adds Docker's own package repository to your system's list of sources
- After this, `apt` can find and install the `docker-ce` package

### Step 4: Check available Docker versions (optional but useful)

```bash
apt-cache policy docker-ce
```

- This shows which version of Docker CE is available and from which repository
- Useful for confirming the Docker repo was added correctly

### Step 5: Install Docker CE

```bash
sudo apt install docker-ce -y
```

- `docker-ce` is the Community Edition of Docker Engine
- This is the open-source version and is what most developers and labs use

### Step 6: Verify the Docker service is running

```bash
sudo systemctl status docker
```

- Look for `Active: active (running)` in the output
- If you see anything else, Docker did not start correctly

### Step 7: Add your user to the docker group

```bash
sudo usermod -aG docker ${USER}
```

- By default, running `docker` commands requires `sudo`
- Adding your user to the `docker` group allows you to run `docker` without `sudo`
- You must log out and log back in for this to take effect

```bash
# Log out
exit

# Log back in
ssh -i ~/.ssh/id_rsa azureuser@20.204.182.165
```

### Step 8: Verify the Docker installation

```bash
docker version
```

- You should see two sections in the output: `Client` and `Server`
- The Client is the CLI tool
- The Server is the Docker Daemon
- If you only see Client information and get an error for Server, either the daemon is not running or the group membership has not taken effect yet

Example output (versions may differ):

```
Client: Docker Engine - Community
 Version:           27.x.x
 ...

Server: Docker Engine - Community
 Engine:
  Version:          27.x.x
  ...
```

```bash
docker info
```

- This shows a detailed summary of your Docker installation
- It includes storage driver, number of running containers, images, CPUs, and total memory
- Useful for health checks

### Step 9: Run your first container

```bash
docker run hello-world
```

Expected output:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image...
 4. The Docker daemon streamed that output to the Docker client...
```

What just happened, step by step:

1. You typed `docker run hello-world`
2. The Docker CLI sent a request to the Docker Daemon
3. The Daemon checked your local machine — the `hello-world` image was not there
4. The Daemon pulled the image from Docker Hub (a public registry)
5. The Daemon created a new container from that image and ran it
6. The container printed the message to your terminal, then exited
7. The container no longer exists, but the image is now cached locally

- This entire sequence — pull, create, run, output, exit — happened in under a second

---

## Part 6: Understanding Docker Architecture

```
                         DOCKER ARCHITECTURE
+---------------------------------------------------------------+
|                        Docker Host (Your VM)                  |
|                                                               |
|   +----------------+       REST API      +----------------+  |
|   |  Docker Client |  -----------------> |  Docker Daemon |  |
|   |  (docker CLI)  |                     |  (dockerd)     |  |
|   +----------------+                     +-------+--------+  |
|                                                  |            |
|                              +-------------------+            |
|                              |                                |
|                   +----------v-----------+                    |
|                   |     Local Images     |                    |
|                   |  hello-world:latest  |                    |
|                   |  ubuntu:24.04        |                    |
|                   |  nginx:latest        |                    |
|                   +----------+-----------+                    |
|                              |                                |
|                   +----------v-----------+                    |
|                   |     Containers       |                    |
|                   |  [container-1] run   |                    |
|                   |  [container-2] stop  |                    |
|                   +----------------------+                    |
+---------------------------------------------------------------+
                              |
                              | pull / push
                              v
                   +----------------------+
                   |   Docker Registry    |
                   |   (hub.docker.com)   |
                   +----------------------+
```

Component breakdown:

- **Docker Client**: The `docker` command you type — it communicates with the daemon via a local socket or over a network using a REST API
- **Docker Daemon** (`dockerd`): The background service that does all the real work — building images, running containers, managing networks and volumes
- **Images**: Read-only templates used to create containers — built from a `Dockerfile`, layered and cached
- **Containers**: A running instance of an image — isolated with their own filesystem, network, and process space, but sharing the host kernel
- **Registry**: A storage and distribution system for images — Docker Hub is the default public registry, but you can also run a private registry

---

## Cleanup

- Run these commands only when you are completely done with ALL labs
- Deleting the resource group removes the VM, disk, network interface, and public IP — everything

### Delete just the VM (keeps the resource group)

```bash
az vm delete --resource-group myResourceGroup --name myVM
```

### Delete the entire resource group (deletes everything inside it)

```bash
az group delete --name myResourceGroup
```

- You will be prompted to confirm — type `y` and press Enter
- This may take 2-5 minutes

---

## Challenges

- Work through these after completing the main lab steps
- They are designed to deepen your understanding through exploration

**Challenge 1: Inspect your Docker environment**

Run `docker info` and answer the following:
- What is the storage driver being used?
- How many CPUs does the Docker host have?
- How much total memory is available?
- How many images are currently stored locally?

**Challenge 2: Run a web server container**

Pull and run the `nginx` image:

```bash
docker run -d -p 80:80 nginx
```

- The `-d` flag runs the container in the background
- The `-p 80:80` flag maps port 80 on the VM to port 80 inside the container

Can you open a browser on your laptop and reach the nginx welcome page using your VM's public IP address? (Hint: port 80 is already open from Part 2, Step 3.)

**Challenge 3: Run a command inside a container**

```bash
docker run ubuntu echo "Hello Docker"
```

Observe what happens:
- Did Docker pull an image? Which one?
- How long did the container run?
- Run `docker ps` — is the container still listed? Why or why not?
- Run `docker ps -a` — what do you see now?

Try to explain in your own words: what is the difference between an image and a container?
