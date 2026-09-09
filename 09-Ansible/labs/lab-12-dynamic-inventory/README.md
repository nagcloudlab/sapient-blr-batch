# Lab 12 - Dynamic Inventory (GCP)

## Objective
Auto-discover GCP VMs instead of manually listing them

## Prerequisites
- Lab 02 completed (inventory configured)
- gcloud CLI installed and authenticated (`gcloud auth application-default login`)
- Install GCP collection: `ansible-galaxy collection install google.cloud`
- Install Python deps: `pip install google-auth requests`

---

## What is Dynamic Inventory?
- **Static inventory** = manually list IPs (what we've been doing)
- **Dynamic inventory** = auto-discover servers from cloud provider
- VMs come and go — dynamic inventory keeps up automatically
- Supports: GCP, AWS, Azure, Docker, Kubernetes, etc.

## Why Dynamic Inventory?
| Static | Dynamic |
|--------|---------|
| Hardcoded IPs | Auto-discovered |
| Manual updates | Always current |
| Fine for 2 VMs | Essential for 100+ VMs |
| Simple | Scalable |

---

## Step 1: Install GCP Plugin Dependencies

```bash
# Install the Google Cloud collection
ansible-galaxy collection install google.cloud

# Install Python dependencies
pip install google-auth requests
```

## Step 2: Setup GCP Authentication

```bash
# Option 1: Use gcloud application-default credentials
gcloud auth application-default login

# Option 2: Use a service account key
# Download from GCP Console → IAM → Service Accounts
# Set env var:
export GCP_SERVICE_ACCOUNT_FILE=~/path/to/service-account.json
```

## Step 3: Test Dynamic Inventory

```bash
# List discovered hosts
ansible-inventory -i gcp-inventory.yml --list

# Graph view
ansible-inventory -i gcp-inventory.yml --graph

# Ping all discovered hosts
ansible all -i gcp-inventory.yml -m ping
```

## Step 4: Use Labels for Groups

```bash
# In GCP, add labels to your VMs:
gcloud compute instances add-labels vm1-nginx --labels=role=webserver --zone=us-central1-a
gcloud compute instances add-labels vm2-springboot --labels=role=appserver --zone=us-central1-a

# Now the dynamic inventory groups them by label!
ansible-inventory -i gcp-inventory.yml --graph
```

## Step 5: Run Playbook with Dynamic Inventory

```bash
ansible-playbook -i gcp-inventory.yml site.yml
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `gcp-inventory.gcp.yml` | GCP dynamic inventory config (must end in `.gcp.yml`) |
| `site.yml` | Playbook using dynamic inventory |
| `ansible.cfg` | Points to static inventory as fallback |

---

## Troubleshooting

### "google.cloud.gcp_compute plugin not found"
```bash
ansible-galaxy collection install google.cloud
pip install google-auth requests
```

### "Could not determine project"
```bash
# Authenticate first
gcloud auth application-default login
# Or set env var
export GCP_SERVICE_ACCOUNT_FILE=~/path/to/service-account.json
```

### "No hosts matched"
```bash
# Check if VMs have labels
gcloud compute instances describe vm1-nginx --zone=us-central1-a --format="get(labels)"
# Add labels if missing
gcloud compute instances add-labels vm1-nginx --labels=role=webserver --zone=us-central1-a
```

## Key Takeaways
- Dynamic inventory auto-discovers servers from cloud APIs
- File must end in `.gcp.yml` for the GCP plugin
- GCP labels become Ansible groups
- `keyed_groups` maps cloud metadata to Ansible groups
- Essential for auto-scaling environments
- Next: **Advanced patterns** — rolling deployments, optimization
