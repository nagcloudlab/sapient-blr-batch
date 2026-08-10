# Infrastructure Fundamentals
## Module 14 | Sustain Engineering Training | Day 15

**1 day | Lecture + hands-on + Stage Gate Exit Assessment**

---

## Agenda

| Session | Topics |
|---------|--------|
| First half | IT Infrastructure Overview, Components, Cloud vs Traditional, Deployment Models |
| Second half | 4 Infrastructure Management Challenges, Resilience Patterns, High Availability |
| Assessment | Stage Gate Exit Assessment (60 min) |

> Understanding the infrastructure that runs FoodExpress -- from servers to cloud.

---

## What Is IT Infrastructure?

### Definition
IT Infrastructure is the **combined set of hardware, software, networks, and services** required to develop, test, deliver, monitor, and support IT services.

### Components

```
+-----------------------------------------------------------+
|                    IT Infrastructure                       |
+-----------------------------------------------------------+
|  Hardware      | Servers, storage, networking equipment    |
|  Software      | OS, middleware, databases, applications   |
|  Network       | Routers, switches, firewalls, load balancers|
|  Services      | DNS, DHCP, email, monitoring, backup      |
|  People        | System admins, network engineers, SREs     |
|  Processes     | Change management, incident management    |
|  Data Centers  | Physical facilities, power, cooling       |
+-----------------------------------------------------------+
```

---

## Infrastructure Components Deep Dive

### Compute

| Component | Description | FoodExpress Example |
|-----------|-------------|---------------------|
| **Physical Server** | Bare metal machine in data center | Legacy order database server |
| **Virtual Machine** | Software-defined server on hypervisor | Application servers on VMware |
| **Container** | Lightweight, isolated process | Microservices in Docker |
| **Serverless** | Function-as-a-Service | Image resizing for restaurant photos |

### Storage

| Type | Description | FoodExpress Example |
|------|-------------|---------------------|
| **Block Storage** | Raw disk volumes | Database storage (EBS) |
| **File Storage** | Shared file system | Config files, logs (EFS/NFS) |
| **Object Storage** | Key-value for large objects | Restaurant images, backups (S3) |
| **Database** | Structured data storage | MySQL (orders), MongoDB (menus) |

### Network

| Component | Description | FoodExpress Example |
|-----------|-------------|---------------------|
| **Load Balancer** | Distributes traffic | Nginx/ALB in front of API servers |
| **CDN** | Caches content near users | Restaurant images, static assets |
| **DNS** | Domain name resolution | foodexpress.com -> IP address |
| **Firewall** | Controls network access | Block unauthorized DB access |
| **VPN** | Secure remote access | Developer access to staging |

---

## FoodExpress Infrastructure Overview

```
                         Internet
                            |
                      +-----v------+
                      |    CDN     |  (Static assets, images)
                      +-----+------+
                            |
                      +-----v------+
                      | DNS / WAF  |  (Domain resolution, firewall)
                      +-----+------+
                            |
                      +-----v------+
                      |   Load     |  (Round-robin / least connections)
                      |  Balancer  |
                      +--+----+----+
                         |    |
               +---------+    +---------+
               |                        |
        +------v------+         +------v------+
        | App Server  |         | App Server  |
        | (Node.js)   |         | (Node.js)   |
        +------+------+         +------+------+
               |                        |
        +------v------------------------v------+
        |           Internal Network           |
        +--+----------+-----------+----------+-+
           |          |           |          |
     +-----v--+ +----v---+ +----v---+ +----v---+
     | MySQL  | | MongoDB| | Redis  | | Kafka  |
     | (Orders)| | (Menus)| | (Cache)| | (Events)|
     +--------+ +--------+ +--------+ +--------+
```

---

## Traditional Infrastructure

### On-Premises Data Center

| Aspect | Description |
|--------|-------------|
| **Ownership** | Company owns and operates everything |
| **Location** | Physical facility managed by the organization |
| **Hardware** | Purchased, installed, maintained by internal team |
| **Capacity** | Fixed -- must buy ahead of demand |
| **Lead Time** | Weeks to months for new hardware |
| **Cost Model** | Capital expenditure (CapEx) -- large upfront investment |
| **Scaling** | Vertical (bigger server) or planned horizontal |

### Challenges

| Challenge | Impact |
|-----------|--------|
| **Over-provisioning** | Buying hardware you may never use |
| **Under-provisioning** | Cannot handle traffic spikes (Black Friday) |
| **Maintenance burden** | Hardware failures, OS patching, firmware updates |
| **Disaster recovery** | Need a second data center (expensive) |
| **Talent** | Need specialized hardware/network engineers |

---

## Cloud Infrastructure

### What Is Cloud Computing?

> On-demand delivery of IT resources over the internet with pay-as-you-go pricing.

### Cloud Service Models

```
+-----------------------------------------------+
|              YOU MANAGE LESS -->               |
+-----------------------------------------------+
|                                               |
|   On-Prem    |   IaaS    |   PaaS    | SaaS  |
|              |           |           |        |
| Application  | Application| Application| ---- |
| Data         | Data       | Data      | ---- |
| Runtime      | Runtime    | ----      | ---- |
| Middleware   | Middleware | ----      | ---- |
| OS           | OS         | ----      | ---- |
| Virtualization| ----      | ----      | ---- |
| Servers      | ----       | ----      | ---- |
| Storage      | ----       | ----      | ---- |
| Networking   | ----       | ----      | ---- |
|              |           |           |        |
+-----------------------------------------------+
  You manage      Provider manages (----)
```

---

## Cloud Service Models Explained

### IaaS (Infrastructure as a Service)

| Feature | Description | Examples |
|---------|-------------|---------|
| What you get | VMs, storage, networking | AWS EC2, Azure VMs, GCP Compute |
| You manage | OS, middleware, apps, data | |
| Provider manages | Hardware, virtualization, networking | |
| Best for | Full control, custom configurations | FoodExpress app servers |

### PaaS (Platform as a Service)

| Feature | Description | Examples |
|---------|-------------|---------|
| What you get | Runtime environment, managed services | AWS Elastic Beanstalk, Heroku, Azure App Service |
| You manage | Application code, data | |
| Provider manages | Everything else (OS, runtime, scaling) | |
| Best for | Focus on code, not infrastructure | FoodExpress API deployment |

### SaaS (Software as a Service)

| Feature | Description | Examples |
|---------|-------------|---------|
| What you get | Complete application | Gmail, Slack, Salesforce, Jira |
| You manage | Configuration, users | |
| Provider manages | Everything | |
| Best for | Standard business tools | FoodExpress monitoring (Datadog) |

---

## Cloud vs Traditional -- Comparison

| Aspect | Traditional | Cloud |
|--------|-------------|-------|
| **Cost Model** | CapEx (buy upfront) | OpEx (pay as you go) |
| **Scaling** | Manual, slow (weeks) | Automatic, fast (minutes) |
| **Availability** | Single/dual data center | Multiple regions globally |
| **Maintenance** | Your team | Cloud provider |
| **Security** | Full control | Shared responsibility |
| **Flexibility** | Limited by hardware | Near-unlimited resources |
| **Compliance** | Full control of data location | May need specific regions |
| **Vendor Lock-in** | Hardware vendor | Cloud provider APIs |

### When to Use Each

| Use Traditional When | Use Cloud When |
|---------------------|----------------|
| Strict data sovereignty requirements | Variable/unpredictable workloads |
| Already invested in data center | Need global presence |
| Predictable, stable workloads | Startup or growing company |
| Ultra-low latency requirements | Want to reduce ops burden |
| Regulatory requirements for physical control | Need rapid provisioning |

---

## Cloud Deployment Models

| Model | Description | Example |
|-------|-------------|---------|
| **Public Cloud** | Shared infrastructure, managed by provider | AWS, Azure, GCP |
| **Private Cloud** | Dedicated infrastructure, single organization | VMware vSphere, OpenStack |
| **Hybrid Cloud** | Mix of public and private | On-prem DB + cloud app servers |
| **Multi-Cloud** | Multiple public cloud providers | AWS for compute + GCP for ML |

### FoodExpress Deployment

```
+------------------+     +-------------------+
|  Private Cloud   |     |   Public Cloud    |
|  (On-Premises)   |     |   (AWS)           |
|                  |     |                   |
|  - Customer DB   | <-> |  - App Servers    |
|  - Payment Data  |     |  - CDN            |
|  - PCI Compliant |     |  - Object Storage |
|                  |     |  - Load Balancer  |
+------------------+     +-------------------+
     Sensitive data         Scalable compute
     stays on-prem          in the cloud
```

---

## Major Cloud Providers

### Service Comparison

| Service | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Compute** | EC2 | Virtual Machines | Compute Engine |
| **Containers** | ECS/EKS | AKS | GKE |
| **Serverless** | Lambda | Functions | Cloud Functions |
| **Object Storage** | S3 | Blob Storage | Cloud Storage |
| **Database (SQL)** | RDS | SQL Database | Cloud SQL |
| **Database (NoSQL)** | DynamoDB | Cosmos DB | Firestore |
| **Load Balancer** | ALB/NLB | Load Balancer | Cloud LB |
| **CDN** | CloudFront | CDN | Cloud CDN |
| **Monitoring** | CloudWatch | Monitor | Cloud Monitoring |
| **CI/CD** | CodePipeline | DevOps | Cloud Build |

### Market Share (2026)
- AWS: ~31%
- Azure: ~25%
- GCP: ~11%
- Others: ~33%

---

## 4 Infrastructure Management Challenges

### Challenge 1: Capacity Planning

| Problem | Impact | Solution |
|---------|--------|----------|
| Under-provisioned | Service outages during peak traffic | Auto-scaling groups |
| Over-provisioned | Wasting money on idle resources | Right-sizing, spot instances |
| Unpredictable growth | Cannot plan budget | Historical data + forecasting |

### FoodExpress Example

```
Order Volume Pattern:
  Lunch (12-2 PM):   ███████████████  Peak
  Dinner (7-10 PM):  ████████████████████  Higher Peak
  Late Night:        ████  Low
  Weekend:           ████████████████████████  Highest

Auto-scaling rule:
  IF CPU > 70% for 5 min -> Add 2 instances
  IF CPU < 30% for 15 min -> Remove 1 instance
  MIN instances: 2 (always running)
  MAX instances: 10 (cost control)
```

---

## Challenge 2: Security

### The Shared Responsibility Model

```
+--------------------------------------------+
|              YOUR Responsibility            |
| - Application security                     |
| - Data encryption                          |
| - Access control (IAM)                     |
| - Network security (security groups)       |
| - OS patching (for IaaS)                   |
+--------------------------------------------+
|           PROVIDER's Responsibility         |
| - Physical security                        |
| - Network infrastructure                   |
| - Hypervisor security                      |
| - Global infrastructure                    |
+--------------------------------------------+
```

### Common Security Failures

| Failure | Example | Prevention |
|---------|---------|------------|
| Open S3 bucket | Customer data exposed to internet | Default deny, bucket policies |
| Hardcoded credentials | DB password in source code | Use secrets manager (AWS SSM, Vault) |
| Missing patches | Known CVE exploited | Automated patching, scanning |
| No encryption | Data at rest in plain text | Enable encryption by default |
| Over-permissive IAM | Service has admin access | Principle of least privilege |

---

## Challenge 3: Cost Management

### Cloud Cost Optimization

| Strategy | Savings | How |
|----------|---------|-----|
| **Right-sizing** | 20-40% | Match instance size to actual usage |
| **Reserved Instances** | 30-60% | Commit to 1-3 year terms |
| **Spot Instances** | 60-90% | Use spare capacity (can be interrupted) |
| **Auto-scaling** | Variable | Scale down during low traffic |
| **Storage tiering** | 50-80% | Move old data to cheaper storage |
| **Delete unused resources** | 100% | Find and remove orphaned volumes, IPs |

### FoodExpress Cost Breakdown

```
Monthly Cloud Bill: $15,000
+------------------+-------+
| Service          | Cost  |
+------------------+-------+
| Compute (EC2)    | $6,000|  40% -- right-size candidates
| Database (RDS)   | $3,500|  23% -- reserved instance candidate
| Storage (S3)     | $1,500|  10% -- lifecycle policies
| Load Balancer    | $1,000|   7%
| Data Transfer    | $1,500|  10% -- CDN can reduce
| Other            | $1,500|  10%
+------------------+-------+
```

---

## Challenge 4: Monitoring and Observability

### The Three Pillars

| Pillar | What | Tool Examples | FoodExpress Use |
|--------|------|---------------|-----------------|
| **Metrics** | Numerical measurements over time | Prometheus, CloudWatch, Datadog | CPU usage, request rate, error rate |
| **Logs** | Timestamped event records | ELK Stack, CloudWatch Logs, Splunk | Application errors, access logs |
| **Traces** | Request flow across services | Jaeger, X-Ray, Zipkin | Order flow through microservices |

### Key Infrastructure Metrics

| Metric | What to Monitor | Alert Threshold |
|--------|----------------|-----------------|
| **CPU Utilization** | Processing load | > 80% for 5 min |
| **Memory Usage** | RAM consumption | > 85% |
| **Disk Space** | Storage capacity | > 90% |
| **Network I/O** | Bandwidth usage | > 80% of capacity |
| **Error Rate** | Failed requests | > 1% of total |
| **Response Time** | P95 latency | > 500ms |
| **Availability** | Uptime percentage | < 99.9% |

---

## Infrastructure Resilience

### What Is Resilience?

> The ability of a system to **withstand failures** and **recover quickly** from disruptions.

### Failure Is Inevitable

| Failure Type | Probability | Impact | Example |
|-------------|-------------|--------|---------|
| **Hardware** | Low | High | Server disk failure |
| **Software** | Medium | Medium | Application crash, memory leak |
| **Network** | Medium | High | ISP outage, DNS failure |
| **Human** | High | Variable | Misconfiguration, wrong deployment |
| **Environmental** | Low | Critical | Power outage, natural disaster |
| **Third-party** | Medium | Variable | Payment gateway down, API rate limit |

### Design Principle
> **Design for failure.** Assume everything will fail and build systems that survive it.

---

## Resilience Patterns

### Pattern 1: Redundancy

```
Single Point of Failure:        Redundant:
+--------+                   +--------+  +--------+
| Server | <-- users         | Server |  | Server |  <-- users
+--------+                   +--------+  +--------+
If it dies, everything dies   If one dies, the other handles traffic
```

### Types of Redundancy

| Type | Description | FoodExpress Example |
|------|-------------|---------------------|
| **Active-Active** | Both nodes handle traffic | Two app servers behind LB |
| **Active-Passive** | Standby takes over on failure | Database primary + replica |
| **N+1** | One extra node beyond minimum | 3 servers when 2 can handle load |
| **Geographic** | Copies in different regions | US-East + EU-West deployment |

---

## Resilience Patterns (continued)

### Pattern 2: Load Balancing

```
                +--------+
  Users ------> |  Load  |
                |Balancer|
                +---+----+
                    |
         +----------+----------+
         |          |          |
    +----v---+ +----v---+ +----v---+
    |Server 1| |Server 2| |Server 3|
    +--------+ +--------+ +--------+
```

| Algorithm | Description | Best For |
|-----------|-------------|----------|
| **Round Robin** | Distribute evenly in order | Identical servers |
| **Least Connections** | Send to least busy server | Variable request duration |
| **IP Hash** | Same client -> same server | Session-based apps |
| **Weighted** | More traffic to stronger servers | Mixed server specs |

### Pattern 3: Circuit Breaker

```
Closed (normal)  -->  Open (failing)  -->  Half-Open (testing)
   |                      |                      |
   | Requests pass        | Requests fail fast   | Test one request
   | through normally     | (don't call service) | If success -> Close
   |                      | Timer expires ->      | If fail -> Open
```

---

## Resilience Patterns (continued)

### Pattern 4: Auto-Scaling

```
Traffic increases:
  Monitoring detects high CPU -> Launch new instance -> LB adds it -> Traffic distributed

Traffic decreases:
  Monitoring detects low CPU -> Terminate instance -> LB removes it -> Cost reduced
```

### Pattern 5: Backup and Disaster Recovery

| Strategy | RPO | RTO | Cost | Description |
|----------|-----|-----|------|-------------|
| **Backup & Restore** | Hours | Hours | $ | Regular backups, restore when needed |
| **Pilot Light** | Minutes | 10-30 min | $$ | Minimal standby in DR region |
| **Warm Standby** | Seconds | Minutes | $$$ | Scaled-down copy always running |
| **Active-Active** | Near-zero | Near-zero | $$$$ | Full capacity in both regions |

RPO = Recovery Point Objective (how much data can you lose?)
RTO = Recovery Time Objective (how fast must you recover?)

---

## High Availability

### Availability Targets

| Level | Annual Downtime | Monthly Downtime | Common Name |
|-------|----------------|-----------------|-------------|
| 99% | 3.65 days | 7.2 hours | "Two nines" |
| 99.9% | 8.76 hours | 43.8 minutes | "Three nines" |
| 99.95% | 4.38 hours | 21.9 minutes | |
| 99.99% | 52.6 minutes | 4.4 minutes | "Four nines" |
| 99.999% | 5.26 minutes | 26.3 seconds | "Five nines" |

### FoodExpress Availability Requirements

| Component | Target | Justification |
|-----------|--------|---------------|
| Order API | 99.95% | Revenue-generating, customer-facing |
| Payment Service | 99.99% | Financial transactions, compliance |
| Restaurant Search | 99.9% | Important but brief outage acceptable |
| Admin Dashboard | 99% | Internal tool, used during business hours |
| Reporting/Analytics | 95% | Batch processing, not real-time |

---

## Infrastructure as Code (IaC)

### Why IaC?

| Manual Provisioning | Infrastructure as Code |
|--------------------|----------------------|
| Click through console | Write code, run script |
| Hard to reproduce | Reproducible (same code = same infra) |
| No version history | Git-tracked changes |
| Error-prone | Automated, consistent |
| Slow for large scale | Fast, parallelized |

### IaC Tools

| Tool | Type | Provider | Language |
|------|------|----------|----------|
| **Terraform** | Provisioning | Multi-cloud | HCL |
| **CloudFormation** | Provisioning | AWS only | YAML/JSON |
| **Ansible** | Configuration | Any | YAML |
| **Puppet** | Configuration | Any | Puppet DSL |
| **Chef** | Configuration | Any | Ruby |

### FoodExpress IaC Example (Terraform)

```hcl
resource "aws_instance" "app_server" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.medium"
  tags = {
    Name = "foodexpress-app-server"
    Environment = "production"
  }
}
```

---

## Networking Fundamentals

### OSI Model (Simplified)

| Layer | Name | FoodExpress Example |
|-------|------|---------------------|
| 7 | Application | HTTP/HTTPS API requests |
| 4 | Transport | TCP connections, port 443 |
| 3 | Network | IP addresses, routing |
| 2 | Data Link | MAC addresses, switches |
| 1 | Physical | Cables, wireless |

### Key Networking Concepts

| Concept | Description | FoodExpress Use |
|---------|-------------|-----------------|
| **IP Address** | Network identifier | `10.0.1.50` (app server) |
| **Subnet** | IP range within a network | `10.0.1.0/24` (app subnet) |
| **Port** | Application endpoint | `443` (HTTPS), `3000` (Node.js) |
| **DNS** | Name to IP resolution | `api.foodexpress.com` -> `52.1.2.3` |
| **HTTPS/TLS** | Encrypted communication | All customer-facing traffic |
| **VPC** | Virtual private network | Isolate FoodExpress from other tenants |

---

## FoodExpress Network Architecture

```
+--------------------------------------------------+
|                    VPC (10.0.0.0/16)             |
|                                                   |
|  +--------------------+  +--------------------+  |
|  | Public Subnet      |  | Public Subnet      |  |
|  | 10.0.1.0/24 (AZ-a) |  | 10.0.2.0/24 (AZ-b)|  |
|  |                    |  |                    |  |
|  |  [Load Balancer]   |  |  [Load Balancer]   |  |
|  |  [NAT Gateway]     |  |  [NAT Gateway]     |  |
|  +--------------------+  +--------------------+  |
|                                                   |
|  +--------------------+  +--------------------+  |
|  | Private Subnet     |  | Private Subnet     |  |
|  | 10.0.3.0/24 (AZ-a) |  | 10.0.4.0/24 (AZ-b)|  |
|  |                    |  |                    |  |
|  |  [App Server 1]    |  |  [App Server 2]    |  |
|  |  [App Server 3]    |  |  [App Server 4]    |  |
|  +--------------------+  +--------------------+  |
|                                                   |
|  +--------------------+  +--------------------+  |
|  | Data Subnet        |  | Data Subnet        |  |
|  | 10.0.5.0/24 (AZ-a) |  | 10.0.6.0/24 (AZ-b)|  |
|  |                    |  |                    |  |
|  |  [MySQL Primary]   |  |  [MySQL Replica]   |  |
|  |  [MongoDB Primary] |  |  [MongoDB Replica] |  |
|  +--------------------+  +--------------------+  |
+--------------------------------------------------+
```

---

## Stage Gate Exit Assessment

### Purpose
- Validates understanding of Modules 01-14
- Determines readiness to proceed to DevOps and SRE modules
- Covers: HTML/CSS, JavaScript, Java, Node.js, Database, QE/QC, Infrastructure

### Format

| Section | Questions | Duration | Weight |
|---------|-----------|----------|--------|
| MCQ | 30 questions | 30 min | 40% |
| Scenario-Based | 5 scenarios | 20 min | 30% |
| Short Answer | 5 questions | 10 min | 30% |

### Passing Criteria
- Overall score: **60% or higher** to proceed
- No section below **40%**
- Candidates below threshold receive additional coaching

---

## Stage Gate -- Sample MCQ Topics

| Module | Sample Question Topic |
|--------|----------------------|
| HTML/CSS | Semantic HTML elements, CSS specificity |
| JavaScript | Closures, promises, array methods |
| Java | OOP concepts, exception handling, collections |
| Node.js | Event loop, Express middleware, async/await |
| Database | JOIN types, indexing, transactions |
| QE/QC | QA vs QC, severity vs priority, test pyramid |
| Infrastructure | Cloud models, HA levels, IaC benefits |

---

## Stage Gate -- Sample Scenarios

### Scenario 1: FoodExpress Order Service Down

> "The FoodExpress order service is returning 500 errors for 30% of requests. The error started 20 minutes ago after a deployment. CPU is at 45%, memory at 72%, database connections at 95%."

**Questions:**
1. What is the most likely root cause?
2. What is your immediate action?
3. How would you prevent this in the future?

### Scenario 2: Database Performance

> "The restaurant search query takes 8 seconds. EXPLAIN shows `type: ALL` (full table scan) on the restaurants table (500,000 rows)."

**Questions:**
1. What does `type: ALL` mean?
2. What would you add to fix this?
3. How would you verify the fix worked?

---

## Key Takeaways

| Concept | Key Lesson |
|---------|------------|
| IT Infrastructure | Hardware + software + network + services + people + processes |
| Cloud vs Traditional | Cloud: OpEx, elastic, fast; Traditional: CapEx, fixed, full control |
| Service Models | IaaS (you manage most), PaaS (focus on code), SaaS (just use it) |
| Deployment Models | Public, Private, Hybrid, Multi-Cloud -- choose based on requirements |
| Capacity Planning | Auto-scaling solves variable demand; right-sizing reduces waste |
| Security | Shared responsibility; least privilege; encrypt everything |
| Cost Management | Right-size, reserve, spot instances, delete unused resources |
| Monitoring | Metrics + Logs + Traces -- the three pillars of observability |
| Resilience | Design for failure: redundancy, load balancing, circuit breakers |
| High Availability | 99.9% = 8.76 hrs/year downtime; 99.99% = 52.6 min/year |
| IaC | Infrastructure as code: reproducible, version-controlled, automated |

> **Next: Module 15 -- SDLC Fundamentals: Software Development Lifecycle stages, methodologies, and environments.**
