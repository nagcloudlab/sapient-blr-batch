# Lab 07: Full Observability Stack with Docker Compose
## 40 min | Prerequisite: Labs 02-06

---

## What You'll Learn
- How to run multiple services together with Docker Compose
- Docker networking: containers talking to each other by name
- Grafana provisioning: auto-configure data sources from code
- Incident simulation: stop a service, watch alerts fire, recover
- The on-call workflow: dashboard + alerts + logs

## Why This Matters
In real projects, you never start services individually with `docker run`. Everything is orchestrated together. This lab mirrors a production-like setup where your app, monitoring, and visualization are deployed as a single stack with one command.

## New Terms

| Term | Meaning |
|------|---------|
| **Docker Compose** | A tool for defining and running multi-container Docker applications. You describe all services in one `docker-compose.yml` file, then `docker compose up` starts everything. |
| **Docker networking** | When containers are on the same Docker network, they can reach each other using container names as hostnames. `order-service:8080` just works -- Docker's built-in DNS resolves it. |
| **Provisioning** | Auto-configuring tools from code/config files instead of manual clicking. Grafana reads a YAML file on startup and configures its data sources automatically. |
| **Infrastructure as Code (IaC)** | The practice of defining all infrastructure and configuration in version-controlled files. No manual setup -- everything is reproducible. |
| **`depends_on`** | Docker Compose directive that controls startup order. `prometheus` depends_on `order-service` means order-service starts first. |

---

## What Changed from Previous Labs

| Before (Labs 02-06) | Now (Lab 07) |
|---------------------|-------------|
| Individual `docker run` commands | Single `docker-compose.yml` |
| `host.docker.internal:8080` | `order-service:8080` (Docker DNS) |
| Manual Grafana data source setup | Auto-provisioned from YAML file |
| Start/stop containers individually | `docker compose up/down` manages everything |

---

## Step 1: Set up provisioning directory

```bash
cd ~/obs-labs
mkdir -p grafana-provisioning/datasources
```

---

## Step 2: Auto-provision Grafana data source

Create `grafana-provisioning/datasources/prometheus.yml`:

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090     # Docker DNS: container name as hostname
    isDefault: true
```

> **What this does:** When Grafana starts, it reads this file and automatically adds Prometheus as a data source. No manual clicking. In production, ALL configuration is done this way -- it's called Infrastructure as Code.

---

## Step 3: Create Docker Compose file

Copy `docker-compose.yml` from this folder, or create it:

```yaml
version: '3.8'

services:
  order-service:
    build: .
    container_name: order-service
    ports:
      - "8080:8080"
    networks:
      - observability

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
    networks:
      - observability
    depends_on:
      - order-service

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - ./grafana-provisioning:/etc/grafana/provisioning
    networks:
      - observability
    depends_on:
      - prometheus

networks:
  observability:
    driver: bridge
```

> **Key points to understand:**
> - All 3 services share the `observability` network
> - On this network, containers reach each other by name: `order-service`, `prometheus`, `grafana`
> - `depends_on` controls startup order (order-service -> prometheus -> grafana)

---

## Step 4: Update Prometheus config for Docker networking

Copy `prometheus.yml` from this folder -- the key change is using container names:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'order-service'
    scrape_interval: 10s
    static_configs:
      - targets: ['order-service:8080']    # Container name, NOT host.docker.internal
```

> **Quick Question:** Why can we now use `order-service` as a hostname instead of `host.docker.internal`? (Because both containers are on the same Docker network. Docker's built-in DNS resolves container names to their IP addresses.)

---

## Step 5: Launch the entire stack

```bash
docker stop order-service prometheus grafana 2>/dev/null
docker rm order-service prometheus grafana 2>/dev/null

# ONE COMMAND to start everything
docker compose up -d

# Verify all 3 are running
docker compose ps
```

---

## Step 6: Verify everything works

| Check | URL | Expected |
|-------|-----|----------|
| App health | http://localhost:8080 | `{"service":"FoodExpress","status":"healthy"}` |
| Metrics | http://localhost:8080/metrics | Prometheus format |
| Prometheus Targets | http://localhost:9090/targets | order-service = UP |
| Prometheus Alerts | http://localhost:9090/alerts | 3 rules visible |
| Grafana | http://localhost:3000 | Login: admin/admin123 |
| Data Source | Grafana > Connections > Data Sources | Prometheus auto-configured |

> **If something is wrong:** Check `docker compose logs <service-name>` for error messages.

---

## Step 7: Generate traffic and observe

Terminal 1 -- watch logs:
```bash
docker logs -f order-service
```

Terminal 2 -- generate traffic:
```bash
while true; do
  curl -s -X POST http://localhost:8080/api/orders > /dev/null
  curl -s http://localhost:8080/ > /dev/null
  sleep 0.1
done
```

Build your Grafana dashboard (same panels as Lab 04). The data source is already there.

---

## Step 8: Incident simulation

### Scenario: The order service crashes

```bash
docker stop order-service
```

Watch across all 3 views:

| Where | What you see |
|-------|-------------|
| **Prometheus Targets** | order-service: DOWN (red) |
| **Prometheus Alerts** | ServiceDown: PENDING -> FIRING after 1 min |
| **Grafana Dashboard** | Panels show "No data" |
| **Logs** | Traffic generator shows "Connection refused" |

### Recovery:

```bash
docker start order-service
```

Everything recovers automatically. Alerts return to Inactive. Grafana shows data again (with a visible gap in the time series).

> **Discussion:** In production, this is exactly what happens when a pod crashes. Kubernetes restarts it, Prometheus detects the recovery, alert auto-resolves. The entire cycle is automated.

---

## Step 9: The on-call engineer's screen

Open 3 browser tabs side by side:
1. **Grafana Dashboard** -- "Is anything wrong?" (visual overview)
2. **Prometheus Alerts** -- "What alerts are firing?" (notification state)
3. **Terminal with logs** -- "What exactly failed?" (details)

> **Think About It:** This is what production observability looks like. When you get paged at 2 AM:
> 1. Check **alerts** -- what fired?
> 2. Check **dashboard** -- how bad is it? When did it start?
> 3. Check **logs** -- what's the error message? Which requests are failing?

---

## Cleanup

```bash
docker compose down
```

---

## What You Built Across Labs 01-07

| Lab | Pillar | What you added |
|-----|--------|---------------|
| 01 | -- | Felt the pain of no observability |
| 02 | **Metrics** | Instrumented app with prom-client |
| 03 | **Metrics** | Prometheus scraping + PromQL |
| 04 | **Metrics** | Grafana dashboard with Golden Signals |
| 05 | **Logs** | Structured JSON logging with requestId |
| 06 | **Alerting** | Alert rules + incident simulation |
| 07 | **Full Stack** | Docker Compose + provisioning + incident drill |

---

## Discussion

1. What's the advantage of Docker Compose over individual `docker run` commands?
2. Why do we auto-provision Grafana from code instead of clicking through the UI?
3. During the incident simulation, what was the first indicator something was wrong? (Depends on which tab you were watching!)
4. In production, what replaces Docker Compose? (Kubernetes -- covered in Lab 10)

---

## What's Next

You've monitored a single service. In Lab 08, you'll add **two more microservices** (Payment + Notification) and implement **distributed tracing** -- following a single request across all three services using Trace IDs. This is the third pillar of observability.
