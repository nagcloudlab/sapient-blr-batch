# Capstone Portfolio -- 30 Unique Projects

**Programme:** Publicis Sapient Sustain Engineering (SRE + ITIL)
**Delivery:** Individual participant projects, built from scratch
**Source:** Notion workspace (authoritative), local copies for Box upload

---

## Design Standard

- 30 unique projects; one project allocated to one participant
- Every participant begins with empty repositories and creates everything independently
- Same standard tech stack across all projects; only domain, workflows, data, failure cases and incident scenario differ
- Each brief includes: business context, users, architecture, functional scope, advanced failure cases, APIs, data model, NFRs, SLI/SLO targets, incident simulation, milestones, deliverables and demo acceptance criteria

## Common Technology Stack

| Layer | Standard |
|-------|----------|
| Frontend | HTML, CSS, JavaScript |
| Core Backend | OpenJDK LTS, Maven, REST APIs |
| Integration Service | Node.js, Express |
| Data | PostgreSQL (transactional) + MongoDB (events/audit) |
| Source & Delivery | Git/GitHub, Docker, Docker Compose, Jenkins |
| Platform Automation | Kubernetes, Ansible |
| Observability | Prometheus/Grafana or Datadog |
| Work & Knowledge | Jira, Confluence |
| ITSM | ServiceNow (incident, post-incident review, knowledge article) |
| GenAI | Approved assistance with human review |

## Evaluation Model

| Dimension | Weight |
|-----------|--------|
| Requirements, architecture and system design | 10% |
| Core functional implementation | 15% |
| Advanced failure handling and data integrity | 15% |
| Testing, code quality and security | 10% |
| Git, Docker and CI/CD | 15% |
| Kubernetes and automation | 10% |
| Observability, SLI/SLO and reliability | 10% |
| ITSM documentation and incident handling | 10% |
| Final demonstration and communication | 5% |

## Client-Aligned Module Milestones (9 stages)

| # | Stage | Goal |
|---|-------|------|
| 1 | HTML & CSS | Accessible, responsive UI with all states |
| 2 | JavaScript | Client-side interaction, validation, API communication |
| 3 | Java | Core domain model and transactional REST workflow |
| 4 | Node.js | Async integration service with retry-safe handling |
| 5 | Java/Node + DB + QE/QC + SDLC + Jira | Traceable end-to-end workflow with quality controls |
| 6 | Language + Linux + Microservices | Operable services with runtime diagnosis |
| 7 | Language + DB + DevOps + Docker + K8s + Ansible + Git | Reproducible build, deploy, rollback pipeline |
| 8 | Mid: Observability + SRE | Measured reliability with automated detection |
| 9 | Final: ITSM + ITIL + ServiceNow | Complete demo with governed operational closure |

---

## Project Index

| ID | Project | Domain | Incident Scenario | Notion Brief |
|----|---------|--------|-------------------|--------------|
| CAP-01 | Omnichannel Retail Order and Fulfilment Platform | Retail | Payment callback delays during sales event | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e78142994ecb4497fc0c76) |
| CAP-02 | Digital Banking Transaction Reconciliation Platform | Banking | Mapping change collapses auto-match rate | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781598872e24e0a2c01e9) |
| CAP-03 | Healthcare Appointment and Care Coordination Platform | Healthcare | Provider schedule sync failure causes double-bookings | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e7814ca342d203ab9ea13d) |
| CAP-04 | Insurance Claims Processing and Review Platform | Insurance | Rules engine update misclassifies claim severity | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e7817eb35ac38b3b646891) |
| CAP-05 | Logistics Shipment Tracking and Exception Platform | Logistics | GPS feed delay causes phantom delivery status | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e78114b972d40f4bcd1e6f) |
| CAP-06 | Learning Management and Skills Progress Platform | Education | Course content publish corrupts progress records | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781739766ec15487942be) |
| CAP-07 | Utility Billing and Meter Reconciliation Platform | Utilities | Meter reading batch import duplicates charges | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781b8a251e5895c07f3a5) |
| CAP-08 | Travel Booking and Availability Platform | Travel | Seat inventory cache desync during flash sale | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781c8a598fa94f6acda83) |
| CAP-09 | Food Delivery Order and Dispatch Platform | Food Delivery | Driver assignment service timeout during peak hours | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e78146af52ccd1a894a21f) |
| CAP-10 | Telecom Customer Activation and Provisioning Platform | Telecom | Provisioning queue backup causes activation delays | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e7812a91c5e65a277aeb92) |
| CAP-11 | Payroll Processing and Approval Platform | HR/Payroll | Tax calculation update applies retroactively to processed payslips | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e7812ca8c7fa7e9c8f8650) |
| CAP-12 | Warehouse Inventory and Fulfilment Platform | Warehouse | Barcode scanner batch upload creates phantom stock | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781f0a761ec6afaee7a7d) |
| CAP-13 | Subscription Billing and Renewal Platform | SaaS | Auto-renewal job runs twice, double-charging customers | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781beace3d9998616f701) |
| CAP-14 | Parking Reservation and Operations Platform | Parking | Sensor data lag causes occupied spots shown as available | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781c2a5a2f09e267491c4) |
| CAP-15 | Property Maintenance Service Desk Platform | Property | Work order routing change sends tickets to wrong team | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781c68a99d672466631a3) |
| CAP-16 | Public Transport Pass and Fare Platform | Transport | Top-up gateway timeout leaves balance inconsistent | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e78179b80ec9a988866499) |
| CAP-17 | Customer Loyalty and Rewards Platform | Retail | Points calculation rule change applies to historical transactions | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781e3bdeafbde75e00e6e) |
| CAP-18 | Hotel Reservation and Guest Operations Platform | Hospitality | Channel manager sync failure causes overbooking | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e78123b170dc6f52ab1f5b) |
| CAP-19 | E-commerce Returns and Refunds Platform | E-commerce | Refund processor timeout leaves return in limbo state | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e78191b918ec04948e4d8d) |
| CAP-20 | Employee Onboarding and Access Provisioning Platform | HR | LDAP integration failure blocks access for new hires | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e7816bbe4ee5eaa228da4f) |
| CAP-21 | Pharmacy Prescription and Dispensing Platform | Pharmacy | Drug interaction check service timeout allows unsafe dispensing | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e78199a4b6f07d39259511) |
| CAP-22 | Vehicle Service and Maintenance Platform | Automotive | Service schedule calculation error skips mandatory checks | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e7816a863cd58e9115b801) |
| CAP-23 | Loan Origination and Repayment Platform | Lending | Interest calculation rounding error accumulates over installments | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e781eda40ddd3071729610) |
| CAP-24 | Event Ticketing and Venue Access Platform | Events | QR validation service down during venue entry rush | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e781b8b2b1d03076994b7a) |
| CAP-25 | Procurement and Supplier Fulfilment Platform | Procurement | PO approval workflow skips mandatory sign-off level | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e7811b82e4dad49574cd43) |
| CAP-26 | Field Service Dispatch and Work Order Platform | Field Service | GPS-based auto-dispatch assigns technician already on-site elsewhere | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e781ac88a0f46eb63d54d0) |
| CAP-27 | Equipment Rental and Maintenance Platform | Rental | Return processing delay causes double-billing overlap | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e781d183a3c754b6096e8a) |
| CAP-28 | Digital Wallet and Merchant Settlement Platform | Fintech | Settlement batch job timeout leaves merchants unsettled | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e78151965cc12395b31233) |
| CAP-29 | Restaurant Reservation and Kitchen Operations Platform | Restaurant | Table status sync failure causes double-seating | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e78166a7bdef84b39458ef) |
| CAP-30 | University Admissions and Enrollment Platform | Education | Offer letter generation sends duplicates to accepted students | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e781e5a798cbb9d9d590bc) |

---

## Candidate Allocation

See `CANDIDATE-ALLOCATION.md` for the blank allocation tracker (populated after Sri shares participant list).

Allocation tracker on Notion: [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e781d4a7cccb2f5235cac0)

## Notion Links

| Page | Link |
|------|------|
| Capstone Portfolio (parent) | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e78189b012e9cbcb5f3442) |
| Allocation & Tagging Tracker | [Open](https://tangy-hubcap-d0c.notion.site/3a3cde5d05e781d4a7cccb2f5235cac0) |
| Programme Workspace | [Open](https://tangy-hubcap-d0c.notion.site/3a1cde5d05e781f6af7dff89b1ef905b) |
