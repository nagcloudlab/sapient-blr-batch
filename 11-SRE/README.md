# SRE Training - Incremental Labs for Freshers

## Philosophy

This training builds SRE concepts **incrementally** using a Node.js order-service +
Spring Boot payment-service stack. Each lab adds one new concept on top of the previous one.

```
Lab 01: Why Reliability? (break things, feel the pain)
  |
Lab 02: SLIs/SLOs/SLAs (measure the pain)
  |
Lab 03: Error Budgets (quantify acceptable pain)
  |
Lab 04: SLI-Based Monitoring & Alerting (detect the pain early)
  |
Lab 05: Incident Response (structured reaction to pain)
  |
Lab 06: Blameless Post-Mortems (learn from the pain)
  |
Lab 07: Toil & Automation (prevent recurring pain)
  |
Lab 08: Chaos Engineering (deliberately cause pain to get stronger)
```

## Prerequisites

- Docker & Docker Compose installed
- Terminal / shell access
- A text editor
- Basic familiarity with Prometheus/Grafana (helpful, not required)

## Quick Start

```bash
# Start all services (order-service, payment-service, prometheus, grafana)
cd services
docker compose up -d --build

# Verify
curl http://localhost:3000/health   # order-service
curl http://localhost:8080/health   # payment-service
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3001 (admin/admin)

# Generate test traffic
./generate-load.sh
```

## Structure

```
11-SRE/
├── services/                     <-- Shared service stack (start once, use everywhere)
│   ├── docker-compose.yml
│   ├── order-service/            (Node.js + Express + Prometheus metrics)
│   ├── payment-service/          (Spring Boot + Micrometer + random failures)
│   ├── prometheus/               (Scrapes both services)
│   ├── grafana/                  (Pre-built SRE/SLI dashboard)
│   └── generate-load.sh          (Traffic generator)
│
├── lab-01-why-reliability/       <-- Start here
├── lab-02-sli-slo-sla/
├── lab-03-error-budgets/
├── lab-04-sli-monitoring/
├── lab-05-incident-response/
├── lab-06-postmortems/
├── lab-07-toil-automation/
│   └── health-check.sh           (Automation script)
└── lab-08-chaos-engineering/
```

Each lab folder has a `LAB.md` with step-by-step instructions.
Labs build on each other -- do them in order.

## Lab Overview

| Lab | Topic | Type |
|-----|-------|------|
| 01 | Why Reliability Matters | Hands-on + Discussion |
| 02 | SLIs, SLOs, and SLAs | Hands-on + Exercises |
| 03 | Error Budgets | Calculation + Policy Design |
| 04 | SLI-Based Monitoring & Alerting | Hands-on (Grafana) |
| 05 | Incident Response | Group Role-Play Simulation |
| 06 | Blameless Post-Mortems | Writing Exercise + Peer Review |
| 07 | Toil & Automation | Classification + Scripting |
| 08 | Chaos Engineering | Hands-on Failure Injection |

## Key SRE Concepts Map

```
                     SRE
                      |
       +--------------+--------------+
       |              |              |
    MEASURE        RESPOND        IMPROVE
       |              |              |
   SLI/SLO/SLA   Incidents      Automation
   Error Budgets  Post-Mortems   Chaos Eng
   Monitoring     Escalation     Toil Reduction
```

## Cleanup

```bash
cd services
docker compose down
```
