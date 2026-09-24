# Lab 08: Service Portfolio & Business Services — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-08-service-portfolio-business-services.md`

---

## Pre-check

- [ ] Lab 07 done (12 CIs exist in CMDB — servers, databases, apps, monitoring)
- [ ] Users exist: Sanjay Manager, Ravi Kumar, Amit Verma, Priya Sharma
- [ ] Group exists: Platform Engineering
- [ ] Logged into PDI as admin

---

## Step 1: Create 3 Business Services

Navigate: `cmdb_ci_service_business.list` > **New**

### Business Service #1: UPI Payment Processing

| Field | Value |
|-------|-------|
| Name | UPI Payment Processing |
| Service classification | Business Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | Core UPI real-time payment processing for member banks and fintech partners |
| Business criticality | 1 - Most Critical |
| Used for | Production |
| Owned by | Sanjay Manager |
| Managed by | Ravi Kumar |
| Support group | Platform Engineering |

> Submit.

---

### Business Service #2: UPI Dispute Resolution

Navigate: `cmdb_ci_service_business.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI Dispute Resolution |
| Service classification | Business Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | UPI dispute handling and resolution for member banks and consumers |
| Business criticality | 2 - Somewhat Critical |
| Owned by | Sanjay Manager |
| Managed by | Ravi Kumar |
| Support group | Platform Engineering |

> Submit.

---

### Business Service #3: UPI Merchant Onboarding

Navigate: `cmdb_ci_service_business.list` > **New**

| Field | Value |
|-------|-------|
| Name | UPI Merchant Onboarding |
| Service classification | Business Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | Merchant registration and activation for UPI payment acceptance |
| Business criticality | 2 - Somewhat Critical |
| Owned by | Sanjay Manager |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

> Submit.

---

## Checkpoint

Navigate: `cmdb_ci_service_business.list`

Expected: **3 Business Services** — UPI Payment Processing (Most Critical), UPI Dispute Resolution, UPI Merchant Onboarding.

---

## Step 2: Create 5 Technical Services

Navigate: `cmdb_ci_service_technical.list` > **New** (create 5 records)

### Technical Service #1: UPI Transaction Processing

| Field | Value |
|-------|-------|
| Name | UPI Transaction Processing |
| Service classification | Technical Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | Real-time UPI transaction switching and processing engine |
| Business criticality | 1 - Most Critical |
| Owned by | Ravi Kumar |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

---

### Technical Service #2: UPI Settlement & Reconciliation

| Field | Value |
|-------|-------|
| Name | UPI Settlement & Reconciliation |
| Service classification | Technical Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | UPI inter-bank settlement and transaction reconciliation engine |
| Business criticality | 1 - Most Critical |
| Owned by | Ravi Kumar |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

---

### Technical Service #3: UPI Database Service

| Field | Value |
|-------|-------|
| Name | UPI Database Service |
| Service classification | Technical Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | PostgreSQL database cluster for UPI transaction and configuration data |
| Business criticality | 1 - Most Critical |
| Owned by | Ravi Kumar |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

---

### Technical Service #4: UPI Monitoring & Observability

| Field | Value |
|-------|-------|
| Name | UPI Monitoring & Observability |
| Service classification | Technical Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | Prometheus + Grafana + Snow Bridge monitoring stack for UPI platform |
| Business criticality | 2 - Somewhat Critical |
| Owned by | Ravi Kumar |
| Managed by | Priya Sharma |
| Support group | Platform Engineering |

---

### Technical Service #5: UPI Network & Load Balancing

| Field | Value |
|-------|-------|
| Name | UPI Network & Load Balancing |
| Service classification | Technical Service |
| Service status | Catalog |
| Operational status | Operational |
| Short description | Load balancer and network services for UPI API traffic distribution |
| Business criticality | 1 - Most Critical |
| Owned by | Ravi Kumar |
| Managed by | Amit Verma |
| Support group | Platform Engineering |

> Submit each one.

---

## Checkpoint

Navigate: `cmdb_ci_service_technical.list`

Expected: **5 Technical Services** listed with Status = Catalog, Operational = Operational.

---

## Step 3: Create Service Relationships — Business to Technical

Open each Business Service > scroll to **Depends on::Used by** related list > **New**

### UPI Payment Processing depends on (5 relationships)

| Type | Child (Technical Service) |
|------|--------------------------|
| Depends on::Used by | UPI Transaction Processing |
| Depends on::Used by | UPI Settlement & Reconciliation |
| Depends on::Used by | UPI Database Service |
| Depends on::Used by | UPI Network & Load Balancing |
| Depends on::Used by | UPI Monitoring & Observability |

### UPI Dispute Resolution depends on (2 relationships)

| Type | Child (Technical Service) |
|------|--------------------------|
| Depends on::Used by | UPI Transaction Processing |
| Depends on::Used by | UPI Database Service |

### UPI Merchant Onboarding depends on (2 relationships)

| Type | Child (Technical Service) |
|------|--------------------------|
| Depends on::Used by | UPI Database Service |
| Depends on::Used by | UPI Network & Load Balancing |

---

## Step 4: Create Service Relationships — Technical to CIs (from Lab 07)

Open each Technical Service > **Depends on::Used by** related list > **New**

| Technical Service | Type | Child CI (from Lab 07) |
|-------------------|------|----------------------|
| UPI Transaction Processing | Depends on::Used by | UPI Transaction Service |
| UPI Transaction Processing | Depends on::Used by | UPI App Server 01 |
| UPI Transaction Processing | Depends on::Used by | UPI App Server 02 |
| UPI Transaction Processing | Depends on::Used by | UPI Production LB |
| UPI Settlement & Reconciliation | Depends on::Used by | UPI Settlement Service |
| UPI Settlement & Reconciliation | Depends on::Used by | UPI App Server 01 |
| UPI Settlement & Reconciliation | Depends on::Used by | UPI App Server 02 |
| UPI Database Service | Depends on::Used by | UPI PostgreSQL Primary |
| UPI Database Service | Depends on::Used by | UPI PostgreSQL Replica |
| UPI Database Service | Depends on::Used by | UPI DB Server 01 |
| UPI Monitoring & Observability | Depends on::Used by | Prometheus |
| UPI Monitoring & Observability | Depends on::Used by | Grafana |
| UPI Monitoring & Observability | Depends on::Used by | Snow Bridge |
| UPI Network & Load Balancing | Depends on::Used by | UPI Production LB |

Total: **14 Technical-to-CI relationships**

---

## Checkpoint

Open **UPI Payment Processing** > click **View Map** or **Dependency Map**.

Expected: Full hierarchy visible — Business Service > 5 Technical Services > CIs from Lab 07.

---

## Step 5: Create Service Offerings

Navigate: **Service Portfolio > Service Offerings** > **New**

### UPI Payment Processing Offerings (4)

| Name | Service | Status |
|------|---------|--------|
| Real-time P2P Transfer | UPI Payment Processing | Operational |
| Merchant Payment | UPI Payment Processing | Operational |
| UPI Bill Payment | UPI Payment Processing | Operational |
| UPI Autopay | UPI Payment Processing | Operational |

### UPI Dispute Resolution Offerings (3)

| Name | Service | Status |
|------|---------|--------|
| Transaction Dispute Filing | UPI Dispute Resolution | Operational |
| Chargeback Processing | UPI Dispute Resolution | Operational |
| Dispute Status Inquiry | UPI Dispute Resolution | Operational |

### UPI Merchant Onboarding Offerings (3)

| Name | Service | Status |
|------|---------|--------|
| New Merchant Registration | UPI Merchant Onboarding | Operational |
| Merchant QR Code Generation | UPI Merchant Onboarding | Operational |
| Merchant Settlement Configuration | UPI Merchant Onboarding | Operational |

> Submit each one.

---

## Checkpoint

Open **UPI Payment Processing** > scroll to **Service Offerings** related list.

Expected: 4 offerings listed. Repeat for other Business Services (3 each).

---

## Step 6: Verify Service Hierarchy

1. Navigate: `cmdb_ci_service.list` > filter: **Name starts with UPI**
2. Expected: **8 services** (3 Business + 5 Technical)
3. Group by **Service classification** to verify the split
4. Open **UPI Payment Processing** > **View Map** to see full dependency tree

---

## Quick Verification Checklist

- [ ] 3 Business Services created (cmdb_ci_service_business)
- [ ] 5 Technical Services created (cmdb_ci_service_technical)
- [ ] 9 Business-to-Technical relationships created
- [ ] 14 Technical-to-CI relationships created
- [ ] 10 Service Offerings created (4 + 3 + 3)
- [ ] Service dependency map shows full hierarchy from Business Service down to infrastructure CIs
- [ ] All services have owners, managed by, and support group set

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the script from the Appendix in `lab-08-service-portfolio-business-services.md`. Creates all 3 Business Services, 5 Technical Services, 10 Service Offerings, and 23 relationships in one run.

---

*For detailed ITIL theory, service cost modeling, exercises, and background script code, see the full lab doc.*
