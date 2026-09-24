# Lab 07: CMDB — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-07-cmdb-configuration-management.md`

---

## Pre-check

- [ ] Labs 01-06 done (users ravi.kumar, amit.verma, priya.sharma, meera.joshi, sanjay.mgr exist)
- [ ] Groups exist: Platform Engineering, NOC, Service Desk
- [ ] Logged into PDI as admin

---

## Step 1: Create 12 CIs

### CI #1: UPI Payment Platform

Navigate: `cmdb_ci_business_app.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI Payment Platform |
| Short description | NPCI UPI — 10B+ transactions/month across 350+ banks |
| Operational status | Operational |
| Managed by | Ravi Kumar |
| Owned by | Sanjay Manager |
| Support group | Platform Engineering |
| Environment | Production |

> Submit. This is the top-level business application.

---

### CI #2: UPI Transaction Service

Navigate: `cmdb_ci_app_server.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI Transaction Service |
| Short description | Spring Boot — real-time UPI payments (port 8081) |
| Operational status | Operational |
| Host name | upi-txn-01.npci.org.in |
| IP Address | 10.100.1.11 |
| TCP port | 8081 |
| Version | 3.2.1 |
| Managed by | Ravi Kumar |
| Support group | Platform Engineering |
| Environment | Production |

---

### CI #3: UPI Settlement Service

Navigate: `cmdb_ci_app_server.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI Settlement Service |
| Short description | Spring Boot — settlement & reconciliation (port 8082) |
| Host name | upi-stl-01.npci.org.in |
| IP Address | 10.100.1.12 |
| TCP port | 8082 |
| Version | 3.2.1 |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

---

### CI #4: UPI PostgreSQL Primary

Navigate: `cmdb_ci_db_instance.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI PostgreSQL Primary |
| Short description | Primary PostgreSQL 16 — transactions & settlements |
| Host name | upi-db-01.npci.org.in |
| IP Address | 10.100.2.11 |
| TCP port | 5432 |
| Type | PostgreSQL |
| Version | 16.2 |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

---

### CI #5: UPI PostgreSQL Replica

Navigate: `cmdb_ci_db_instance.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI PostgreSQL Replica |
| Short description | Read replica for reporting & failover |
| Host name | upi-db-02.npci.org.in |
| IP Address | 10.100.2.12 |
| TCP port | 5432 |
| Type | PostgreSQL |
| Version | 16.2 |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

---

### CI #6: UPI Production LB

Navigate: `cmdb_ci_lb.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI Production LB |
| Short description | HAProxy — API traffic distribution |
| Host name | upi-lb-01.npci.org.in |
| IP Address | 10.100.0.10 |
| Managed by | Ravi Kumar |
| Support group | Platform Engineering |

---

### CI #7-9: Servers

Navigate: `cmdb_ci_server.list` > **New** (create 3 records)

| Field | App Server 01 | App Server 02 | DB Server 01 |
|-------|--------------|---------------|--------------|
| Name | UPI App Server 01 | UPI App Server 02 | UPI DB Server 01 |
| Short desc | Hosts Transaction Svc | Hosts Settlement Svc | Hosts PostgreSQL DBs |
| Host name | upi-app-01.npci.org.in | upi-app-02.npci.org.in | upi-db-srv-01.npci.org.in |
| OS | Linux | Linux | Linux |
| RAM (MB) | 16384 | 16384 | 65536 |
| CPU count | 8 | 8 | 16 |
| Support group | Platform Engineering | Platform Engineering | Platform Engineering |

---

### CI #10-12: Monitoring Stack

Navigate: `cmdb_ci_appl.list` > **New** (create 3 records)

| Name | Short Description | Managed by |
|------|-------------------|------------|
| Prometheus Monitoring | Metrics collection & alerting | Ravi Kumar |
| Grafana Dashboard | Visualization & dashboards | Ravi Kumar |
| Snow Bridge Integration | AlertManager to ServiceNow bridge | Ravi Kumar |

All: Support group = Platform Engineering, Operational status = Operational

---

## Checkpoint

Navigate: `cmdb_ci.list` > filter: **Support group = Platform Engineering**

Expected: **12 CIs**. If any are missing, go back and create them.

---

## Step 2: Create 21 Relationships

Open each CI > scroll to **Related Items** > **CI Relationships** > **New**

### Depends on (6 relationships)

| Open this CI | Type | Select this CI |
|-------------|------|---------------|
| UPI Transaction Service | Depends on::Used by | UPI PostgreSQL Primary |
| UPI Settlement Service | Depends on::Used by | UPI PostgreSQL Primary |
| UPI Production LB | Depends on::Used by | UPI Transaction Service |
| UPI Production LB | Depends on::Used by | UPI Settlement Service |
| UPI PostgreSQL Replica | Depends on::Used by | UPI PostgreSQL Primary |
| Snow Bridge Integration | Depends on::Used by | Prometheus Monitoring |

### Runs on (4 relationships)

| Open this CI | Type | Select this CI |
|-------------|------|---------------|
| UPI Transaction Service | Runs on::Runs | UPI App Server 01 |
| UPI Settlement Service | Runs on::Runs | UPI App Server 02 |
| UPI PostgreSQL Primary | Runs on::Runs | UPI DB Server 01 |
| UPI PostgreSQL Replica | Runs on::Runs | UPI DB Server 01 |

### Contains (11 relationships)

Open **UPI Payment Platform** > add 11 "Contains::Contained by" relationships:

| # | UPI Payment Platform Contains |
|---|------------------------------|
| 1 | UPI Transaction Service |
| 2 | UPI Settlement Service |
| 3 | UPI PostgreSQL Primary |
| 4 | UPI PostgreSQL Replica |
| 5 | UPI Production LB |
| 6 | UPI App Server 01 |
| 7 | UPI App Server 02 |
| 8 | UPI DB Server 01 |
| 9 | Prometheus Monitoring |
| 10 | Grafana Dashboard |
| 11 | Snow Bridge Integration |

---

## Step 3: View the Service Map

1. Open **UPI Payment Platform** (`cmdb_ci_business_app.list` > click on it)
2. Click **View Map**
3. Explore:
   - Click any CI to see details
   - Follow arrows for dependencies
   - Trace upstream/downstream impact

---

## Step 4: Test CI Lifecycle

1. Open **UPI PostgreSQL Replica**
2. Change **Operational status** to **In Maintenance**
3. Check the **History** tab (audit trail)
4. Check the **Service Map** (how does it look now?)
5. Change status back to **Operational**

---

## Quick Verification Checklist

- [ ] 12 CIs created across 6 tables
- [ ] 21 relationships created (6 Depends on + 4 Runs on + 11 Contains)
- [ ] Service Map shows full UPI topology
- [ ] CI lifecycle tested (status change + history)
- [ ] Identified SPOF: both PostgreSQL instances on same DB Server 01

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the script from the Appendix in `lab-07-cmdb-configuration-management.md`. Creates all 12 CIs + 21 relationships in ~2 minutes.

---

*For detailed ITIL theory, CI descriptions, exercises, and background script code, see the full lab doc.*
