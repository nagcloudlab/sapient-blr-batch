# Module 32: Observability -- Lab Setup

## Prerequisites

- Docker Desktop with docker compose
- Ports 9090 (Prometheus) and 3000 (Grafana) must be free
- Optionally stop any local Node.js dev servers using port 3000 before starting

## Running the Starter Code

```bash
cd Labs/starter-code
docker compose up -d
```

This starts Prometheus, Grafana, and a mock FoodExpress metrics exporter. Bugs are in the
Prometheus config, Grafana dashboard JSON, and alert rule files.

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default login: admin / admin)

## Verifying Your Fixes

```bash
# Check all containers are running
docker compose ps

# Confirm Prometheus targets are UP
# Browser: http://localhost:9090/targets
# All targets should show state = UP

# Check alert rules loaded
# Browser: http://localhost:9090/alerts
```

In Grafana:
1. Go to Dashboards > FoodExpress Overview.
2. All panels should display data, not "No data" or "Error".
3. Set the time range to "Last 5 minutes" if panels appear empty.

## Expected Behavior

- All Prometheus scrape targets show state UP.
- Grafana dashboards display request rate, error rate, and p99 latency panels with live data.
- Alert rules fire correctly when the mock exporter exceeds configured thresholds.
- No "datasource not found" errors in Grafana.

## Troubleshooting

**Grafana "No data" on all panels:** The Grafana data source URL must be `http://prometheus:9090`
(Docker service name), not `http://localhost:9090` -- Grafana runs inside Docker and cannot reach
the host's localhost.

**Prometheus target DOWN:** Check that the target address in `prometheus.yml` matches the service
name and port defined in `docker-compose.yml`.
