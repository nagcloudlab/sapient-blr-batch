# Step 1: Create a Virtual Machine

## Objective
Create an Ubuntu VM on Google Cloud Platform to host Apache Web Server.

---

## Command

```bash
gcloud compute instances create apache-lab \
  --zone=asia-south1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --tags=http-server,https-server
```

## Flag Breakdown

| Flag | What it does |
|------|-------------|
| `apache-lab` | VM name -- pick something meaningful |
| `--zone=asia-south1-a` | Mumbai data centre (closest to Bangalore) |
| `--machine-type=e2-medium` | 2 vCPU, 4GB RAM -- enough for a web server |
| `--image-family=ubuntu-2204-lts` | Ubuntu 22.04 Long Term Support |
| `--image-project=ubuntu-os-cloud` | Google's official Ubuntu images |
| `--boot-disk-size=20GB` | Storage for OS + Apache + your files |
| `--tags=http-server,https-server` | Network tags -- firewall rules target these |

## Why These Choices Matter

- **LTS** = 5 years of security patches. In production, never use non-LTS.
- **Tags** = how GCP firewall rules find this VM. Without `http-server` tag, port 80 rules won't apply.
- **Zone** = physical location. Closer zone = lower latency for your users.

## Useful Commands After Creation

```bash
# List all VMs
gcloud compute instances list

# Full details of a VM
gcloud compute instances describe apache-lab --zone=asia-south1-a

# Available zones in Mumbai region
gcloud compute zones list --filter="region:asia-south1"

# Available machine sizes
gcloud compute machine-types list --zone=asia-south1-a | head -20
```

## SSH Into the VM

```bash
gcloud compute ssh apache-lab --zone=asia-south1-a
```

## Explore the Clean Machine

Once inside, verify the environment:

```bash
hostname
whoami
cat /etc/os-release
free -h
df -h
```

---

## Key Takeaway

A VM is just a remote computer in the cloud. You SSH into it and work exactly like a local Linux machine. GCP manages the hardware; you manage the software.
