# Section 20: Service Catalog in ServiceNow

## Purpose

How the Service Catalog concepts from Section 6 become a **self-service portal** with forms, approval workflows, and fulfillment automation in ServiceNow.

---

## Service Catalog Structure

```
Service Catalog
  |
  +-- Category (grouping)
  |     |
  |     +-- Catalog Item (what users can request)
  |           |
  |           +-- Variables (form fields users fill in)
  |           +-- Workflow (approval + fulfillment logic)
  |           +-- SLA (how long it should take)
```

Think of it like an e-commerce site:

```
Amazon          =  ServiceNow Service Catalog
Category        =  "Electronics" / "Books"
Product         =  Catalog Item
Product options =  Variables (size, color, quantity)
Checkout flow   =  Workflow (approval + fulfillment)
Delivery SLA    =  "Delivered in 2 days"
```

---

## UPI Example: NPCI's Service Catalog

### Categories

```
Service Catalog Portal
|
+-- Bank Services
|     +-- Bank Onboarding
|     +-- TPS Limit Change
|     +-- API Credential Request
|     +-- Settlement Report Access
|
+-- Access Management
|     +-- Production Access
|     +-- VPN Credential Reset
|     +-- Database Read Access
|     +-- Dashboard Access
|
+-- Infrastructure
|     +-- New Environment
|     +-- Server Provisioning
|     +-- Monitoring Dashboard
|     +-- License Request
|
+-- Support
      +-- Report an Issue (-> Incident)
      +-- General Inquiry
      +-- Dispute Filing
```

---

## Catalog Item: Anatomy

```
+------------------------------------------------------------------+
| Catalog Item: Production Database Access                          |
+------------------------------------------------------------------+
|                                                                    |
| ITEM DETAILS (admin configures):                                  |
|   Name:         Production Database Access                        |
|   Category:     Access Management                                 |
|   Short desc:   Request read-only access to production databases  |
|   Icon:         database-icon.png                                 |
|   Price:        Free (internal)                                   |
|   SLA:          4 hours                                           |
|   Availability: All NPCI employees (L2+)                          |
|                                                                    |
| VARIABLES (user fills in):                                        |
|   Database name:     [dropdown: UPI-Txn-DB, Settlement-DB, ...]  |
|   Access type:       [radio: Read-only, Read-write]              |
|   Duration:          [dropdown: 24 hours, 1 week, Permanent]     |
|   Justification:     [text area: Why do you need this?]          |
|   Manager approval:  [auto-populated from user's profile]        |
|                                                                    |
| WORKFLOW:                                                          |
|   1. User submits -> REQ created                                  |
|   2. Manager receives approval notification                       |
|   3. Manager approves -> routes to DBA team                       |
|   4. DBA provisions access                                        |
|   5. User notified -> REQ closed                                  |
+------------------------------------------------------------------+
```

---

## Variables: Form Field Types

| Variable Type | What it looks like | UPI Example |
|---|---|---|
| **Single Line Text** | `[_______________]` | Merchant name |
| **Multi Line Text** | `[text area]` | Justification for access |
| **Select Box (Dropdown)** | `[Choose one]` | Database name |
| **Radio Button** | `( ) Option A ( ) Option B` | Read-only / Read-write |
| **Checkbox** | `[ ] Option A [ ] Option B` | Select environments: Dev, Staging, Prod |
| **Date** | `[Pick date]` | Access start date |
| **Reference** | `[Search user]` | Select the user who needs access |
| **Attachment** | `[Upload file]` | Compliance documents for bank onboarding |
| **Yes/No** | `( ) Yes ( ) No` | Do you need write access? |

### Variable Sets (Reusable Groups)

Common fields grouped and reused across multiple catalog items:

```
Variable Set: "Standard Access Fields"
  - Justification (text area)
  - Duration (dropdown)
  - Manager (auto-populated reference)
  - Environment (checkbox: Dev/Staging/Prod)

Used in:
  - Production Database Access (+ DB name variable)
  - Dashboard Access (+ dashboard name variable)
  - Server SSH Access (+ server name variable)
```

---

## Request Workflow: What Happens After "Submit"

ServiceNow creates a chain of records:

```
User clicks "Order Now"
       |
       v
+-- REQ (Request) ---------+
|   REQ0008834              |
|   Requested by: Ravi      |
|   Requested for: Ravi     |
|                           |
|   +-- RITM (Req Item) --+|
|   |  RITM0012045         ||
|   |  Item: Prod DB Access||
|   |  Stage: Approval     ||
|   |                      ||
|   |  +-- TASK ----------+||
|   |  | SCTASK0023001    |||
|   |  | Assign: DBA team |||
|   |  | "Provision access"|||
|   |  +------------------+||
|   +----------------------+|
+---------------------------+
```

| Record | What it is | UPI Example |
|---|---|---|
| **REQ** | The overall request (shopping cart) | "Ravi ordered 2 items" |
| **RITM** | One specific item requested | "Production DB Access" |
| **SCTASK** | A fulfillment task for a team | "DBA team: grant access to UPI-Txn-DB" |

One REQ can have multiple RITMs. Each RITM can generate multiple SCTASKs.

---

## Approval Workflow

```
RITM0012045: Production Database Access

Approval chain:
+-------+          +--------+          +---------+
| Ravi  |  submit  | Manager|  approve | DBA Lead|  approve
| (user)|--------->| (Meera)|--------->| (Vijay) |--------> Fulfillment
+-------+          +--------+          +---------+
                       |                    |
                   (reject)             (reject)
                       |                    |
                       v                    v
                   Ravi notified        Ravi notified
```

### Approval Types

| Type | How it works | UPI Example |
|---|---|---|
| **Anyone approves** | Any one approver is enough | VPN reset -- any manager |
| **Everyone approves** | ALL approvers must approve | Prod write access -- Manager + DBA + Security |
| **Sequential** | Must approve in order | Bank onboarding -- Compliance -> Security -> Infra |
| **Auto-approve** | No human needed | Password reset, report download |

---

## Self-Service Portal

What end users see:

```
+------------------------------------------------------------------+
| NPCI Self-Service Portal                     Welcome, Ravi        |
+------------------------------------------------------------------+
|                                                                    |
| [Search: "database access"                                      ] |
|                                                                    |
| Popular Items:                                                     |
| +------------+ +------------+ +------------+ +------------+      |
| |            | |            | |            | |            |      |
| | VPN Reset  | | New Env    | | Dashboard  | | TPS Change |      |
| | 30 min SLA | | 2 day SLA  | | 1 day SLA  | | 1 day SLA  |      |
| +------------+ +------------+ +------------+ +------------+      |
|                                                                    |
| My Requests:                                                       |
| +----+-----------------+-----------+----------+------------------+|
| | #  | Item            | Status    | SLA      | Submitted        ||
| +----+-----------------+-----------+----------+------------------+|
| |8834| Prod DB Access   | Approval  | 3h left  | Sep 21, 08:30   ||
| |8820| Grafana License  | Fulfilled | Met      | Sep 19, 14:00   ||
| |8815| Staging Env      | In Prog   | 1d left  | Sep 18, 10:00   ||
| +----+-----------------+-----------+----------+------------------+|
+------------------------------------------------------------------+
```

---

## Building a Catalog Item: Step by Step

How an admin creates "TPS Limit Change" in ServiceNow:

```
Step 1: Create the Catalog Item
  Navigate: Service Catalog > Catalog Definitions > Maintain Items
  Click: New
  Fill:
    Name: TPS Limit Change
    Category: Bank Services
    Short description: Request increase/decrease of transaction rate limit
    SLA: 1 business day

Step 2: Add Variables
  Tab: Variables
  Add:
    - Bank name (Reference to cmdb_ci, class = Bank)
    - Current TPS limit (Read-only, auto-populated from CMDB)
    - Requested TPS limit (Single line text, mandatory)
    - Justification (Multi-line text, mandatory)
    - Effective date (Date field)

Step 3: Configure Workflow
  Tab: Process Engine > Flow Designer
  Create flow:
    Trigger: RITM created for "TPS Limit Change"
    Action 1: Request approval from Capacity Manager
    If approved:
      Action 2: Create SCTASK for Platform team
      Action 3: Send email notification to requesting bank
    If rejected:
      Action 4: Notify requester with reason

Step 4: Set Fulfillment Rules
  Assignment group: Platform Engineering
  SLA: 1 business day
  Auto-close: After bank confirms new limit working

Step 5: Publish
  Active: Yes
  Visible on portal: Yes
```

---

## Connection to Previous Sections

```
Service Catalog in ServiceNow connects to:
  |
  +-- Service Request (Sec 5): REQ/RITM/SCTASK lifecycle
  +-- Service Catalog concept (Sec 6): categories, items, SLAs
  +-- SLA (Sec 8): each catalog item has fulfillment SLA
  +-- CMDB (Sec 7): variables can reference CIs
  +-- Change (Sec 19): some catalog items create Standard Changes
  +-- Knowledge (Sec 9): catalog items can link to KB articles
```

---

## Key Takeaway

> The Service Catalog in ServiceNow is a **self-service shop** for IT services.
>
> - **Categories** organize the menu
> - **Catalog Items** are the products
> - **Variables** are the order form
> - **Workflows** handle approval and fulfillment
> - **REQ -> RITM -> SCTASK** tracks everything end to end
>
> The goal: users get what they need **without emails, Slack messages, or hallway conversations** -- everything tracked, SLA-bound, and auditable.
