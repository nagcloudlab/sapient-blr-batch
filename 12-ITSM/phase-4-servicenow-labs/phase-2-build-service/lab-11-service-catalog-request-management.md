# Lab 11: Service Catalog & Request Management

**Level:** Intermediate-Advanced | **Duration:** 90 minutes | **Prerequisites:** Labs 07-10 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand the ITIL 4 Service Request Management practice and how it differs from Incident Management
- Master the ServiceNow Service Catalog architecture (Catalogs, Categories, Items, Variables, Variable Sets)
- Build a complete Service Catalog for the NPCI UPI Payment Platform
- Create 6 fully functional Catalog Items with variables, approvals, and fulfillment tasks
- Configure Record Producers, Catalog Client Scripts, and Catalog UI Policies
- Implement approval workflows with sequential and conditional logic
- Execute end-to-end request fulfillment through the REQ, RITM, and SCTASK lifecycle

---

## Scenario Context

You are continuing to build out the NPCI UPI Payment Platform's ITSM configuration in ServiceNow. In previous labs (07-10), you created the CMDB topology, defined Business and Technical Services, configured SLAs, and built a Knowledge Base. Now you will create the self-service experience: a Service Catalog that allows NPCI teams to request standard services without raising incidents or sending emails.

**Key Teams and Personnel:**
| Name | Role | Group |
|---|---|---|
| Vijay Admin | System Administrator | — |
| Ravi Kumar | Technical Lead | Platform Engineering |
| Amit Verma | Developer | Platform Engineering |
| Priya Sharma | NOC Analyst | NOC |
| Meera Joshi | Service Desk Agent | Service Desk |
| Sanjay Manager | IT Manager | Management |

---

## Part 1: ITIL 4 Service Request Management — Theory

### 1.1 What Is Service Request Management?

The ITIL 4 Service Request Management practice handles pre-defined, pre-approved service actions that users can request through a standardized process. Unlike incidents (which are unplanned interruptions) or changes (which alter the infrastructure), service requests are routine, low-risk, and often pre-authorized.

**Definition (ITIL 4):**
> A service request is a request from a user or a user's authorized representative that initiates a service action which has been agreed as a normal part of service delivery.

### 1.2 Service Request vs Incident — The Critical Difference

This is one of the most commonly confused concepts in ITSM. Understanding the difference is essential.

| Aspect | Service Request | Incident |
|---|---|---|
| **Nature** | Planned, expected | Unplanned, unexpected |
| **Risk** | Low / None | Varies (can be critical) |
| **Pre-approved?** | Yes (follows a model) | No (needs investigation) |
| **Example** | "Give me API access" | "The API is returning 500 errors" |
| **Goal** | Fulfill a known need | Restore normal service |
| **Process** | Standardized fulfillment | Investigation and resolution |
| **SLA Type** | Fulfillment SLA | Resolution SLA |
| **Table (ServiceNow)** | sc_req_item (RITM) | incident |
| **Trigger** | User choice | Service disruption |

**UPI Platform Examples:**

| Service Request | Incident |
|---|---|
| Request merchant onboarding | Merchant onboarding portal is down |
| Request API access for sandbox | API gateway returning authentication errors |
| Request new environment provisioning | Production environment unreachable |
| Request compliance audit report | Audit system not generating reports |

### 1.3 The Request Fulfillment Process

The ITIL 4 request fulfillment process follows these steps:

```
User submits request
        |
        v
  Request logged (REQ created)
        |
        v
  Request Item created (RITM)
        |
        v
  Approval required? ──── No ──── Proceed to fulfillment
        |
       Yes
        |
        v
  Approval granted? ──── No ──── Request rejected (Closed)
        |
       Yes
        |
        v
  Fulfillment tasks created (SCTASKs)
        |
        v
  Tasks assigned to fulfillment groups
        |
        v
  Tasks completed
        |
        v
  RITM closed ──── REQ closed
        |
        v
  User notified
```

### 1.4 Request Models and Standard Changes

A **Request Model** defines the standard way a particular type of request is fulfilled. It includes:
- Who approves it
- What tasks are created
- Who fulfills each task
- What the SLA is
- What variables (form fields) are needed

In ITIL 4, many service requests correspond to **Standard Changes** — pre-authorized changes that follow a well-known procedure. For example, "Provision a new sandbox environment" might be both a service request and a standard change.

### 1.5 Self-Service and Automation

The Service Catalog is the primary self-service channel for users. ITIL 4 emphasizes:
- **Self-service portals** reduce service desk calls
- **Automation** of fulfillment reduces human effort
- **Request models** ensure consistency
- **Knowledge articles** linked to catalog items provide guidance

### 1.6 The Request Lifecycle: REQ, RITM, and SCTASK

ServiceNow uses three related tables to manage service requests:

```
sc_request (REQ)           ── The overall request (shopping cart)
    |
    +── sc_req_item (RITM) ── Individual requested item (one per catalog item)
            |
            +── sc_task (SCTASK) ── Fulfillment task (one or more per RITM)
            +── sc_task (SCTASK) ── Another fulfillment task
```

**Key relationships:**
- A user submits one REQ, which can contain multiple RITMs (like a shopping cart)
- Each RITM corresponds to one Catalog Item
- Each RITM can have multiple SCTASKs (fulfillment steps)
- The RITM does not close until all its SCTASKs are closed
- The REQ does not close until all its RITMs are closed

**Tables in ServiceNow:**

| Table | Label | Prefix | Purpose |
|---|---|---|---|
| sc_request | Request | REQ | The parent container |
| sc_req_item | Requested Item | RITM | The individual catalog item requested |
| sc_task | Catalog Task | SCTASK | A fulfillment task within an RITM |

---

## Part 2: ServiceNow Service Catalog Architecture

### 2.1 Architecture Overview

The Service Catalog in ServiceNow is built on several interconnected components:

```
Service Catalog (sc_catalog)
    |
    +── Catalog Category (sc_category)
    |       |
    |       +── Catalog Item (sc_cat_item)
    |       |       |
    |       |       +── Variables (item_option_new)
    |       |       +── Variable Sets (item_option_new_set)
    |       |       +── Catalog Client Scripts
    |       |       +── Catalog UI Policies
    |       |       +── Execution Plan / Workflow / Flow
    |       |
    |       +── Record Producer (sc_cat_item_producer)
    |       +── Order Guide (sc_cat_item_guide)
    |
    +── Catalog Category (another category)
            |
            +── ...
```

### 2.2 Component Deep Dive

#### Service Catalog (sc_catalog)

The top-level container. An instance can have multiple catalogs (e.g., IT Service Catalog, HR Service Catalog, Facilities Catalog). Each catalog can have its own look, feel, and access controls.

**Navigate to:** Service Catalog > Catalog Definitions > Maintain Catalogs

#### Catalog Categories (sc_category)

Categories organize catalog items into logical groups. Categories can be nested (parent-child) to create a hierarchy. Each category belongs to one catalog.

**Navigate to:** Service Catalog > Catalog Definitions > Maintain Categories

#### Catalog Items (sc_cat_item)

A catalog item represents a single requestable service or product. It defines what the user sees, what information they must provide (variables), who approves, and how it is fulfilled.

**Navigate to:** Service Catalog > Catalog Definitions > Maintain Items

**Key fields on a Catalog Item:**

| Field | Description |
|---|---|
| Name | Display name in the catalog |
| Category | Which category it belongs to |
| Short description | Brief description shown in catalog |
| Description | Full description (supports HTML) |
| Picture | Icon/image for the item |
| Price | Cost (if applicable) |
| Recurring price | For subscription items |
| Delivery time | Expected fulfillment duration |
| Active | Whether the item is available |
| Catalogs | Which catalog(s) it appears in |
| Available for | Users/groups who can see and request it |

#### Record Producers (sc_cat_item_producer)

A Record Producer is a special type of catalog item that creates a record on a different table (e.g., Incident, Problem, Change) instead of creating an RITM. It looks like a catalog item to the user but works differently behind the scenes.

**Navigate to:** Service Catalog > Catalog Definitions > Record Producers

**Use cases:**
- "Report UPI Payment Issue" creates an Incident
- "Report Settlement Discrepancy" creates a Problem
- "Submit Emergency Change" creates a Change Request

#### Order Guides (sc_cat_item_guide)

An Order Guide bundles multiple catalog items into a single, guided ordering experience. The user answers questions, and the Order Guide determines which items to include.

**Navigate to:** Service Catalog > Catalog Definitions > Maintain Order Guides

**Example:** "New Team Member Setup" bundles "Request Team Member Access" + "Request API Access" + hardware provisioning.

#### Variables (item_option_new)

Variables are the form fields that appear when a user requests a catalog item. They capture the information needed for fulfillment.

**Variable Types:**

| Type | Description | Example |
|---|---|---|
| Single Line Text | Short text input | Merchant Name |
| Multi Line Text | Long text input | Justification |
| Select Box | Dropdown with choices | Environment: Dev/QA/Prod |
| Check Box | Boolean toggle | "I acknowledge the terms" |
| Reference | Lookup to another table | User (sys_user) |
| Date | Date picker | Go-live Date |
| Date/Time | Date and time picker | Incident Timestamp |
| Integer | Numeric input | Expected TPS |
| Decimal | Decimal number | Transaction Amount |
| Lookup Select Box | Filtered reference | Select from filtered list |
| Multi Row Variable Set | Repeatable row set | Resource list (CPU, Mem, Storage per row) |
| Macro | UI Macro display | Display formatted content |
| Label | Display-only text | Section header |

#### Variable Sets (item_option_new_set)

A Variable Set is a reusable group of variables that can be attached to multiple catalog items. This avoids duplicating the same variables across items.

**Example:** A "UPI Common Info" variable set containing Transaction ID, Service Name, and Environment can be attached to multiple items.

#### Catalog Client Scripts

Catalog Client Scripts run on the client side (browser) when a user interacts with the catalog item form. They differ from regular Client Scripts because they operate on catalog variables, not form fields.

**Types:**
- **onLoad** — Runs when the form loads
- **onChange** — Runs when a variable value changes
- **onSubmit** — Runs when the user submits the request

#### Catalog UI Policies

Catalog UI Policies control the visibility, mandatory status, and read-only status of variables based on conditions. They are the catalog equivalent of regular UI Policies.

**Example:** When Environment = "Production", make "Manager Approval" mandatory and show a warning label.

#### Execution Plans, Workflows, and Flows

These define what happens after a request is submitted and approved:
- **Execution Plan** — Simple task generation (ordered or unordered)
- **Workflow** — Legacy visual process automation
- **Flow Designer** — Modern low-code automation (recommended for Zurich)

---

## Part 3: Create Catalog Structure

### Step 3.1: Verify the Service Catalog

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Catalogs**
2. Open the **Service Catalog** record (this is the default catalog)
3. Note the sys_id — you will reference this later
4. Confirm it is **Active**

### Step 3.2: Create the Parent Category — "UPI Platform Services"

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Categories**
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Title | UPI Platform Services |
   | Catalog | Service Catalog |
   | Description | Self-service catalog for NPCI UPI Payment Platform. Request access, onboarding, infrastructure, and compliance services. |
   | Active | Checked |
   | Icon | Choose an appropriate icon (e.g., "fa-university") |
   | Parent | (leave empty — this is a top-level category) |

4. Click **Submit**

### Step 3.3: Create Sub-Categories

Create each of the following sub-categories. For each one, navigate to **Service Catalog > Catalog Definitions > Maintain Categories**, click **New**, and fill in:

**Sub-Category 1: Access & Onboarding**

| Field | Value |
|---|---|
| Title | Access & Onboarding |
| Catalog | Service Catalog |
| Parent | UPI Platform Services |
| Description | Request access to systems, APIs, and onboard new team members or merchants. |
| Active | Checked |

**Sub-Category 2: Merchant Services**

| Field | Value |
|---|---|
| Title | Merchant Services |
| Catalog | Service Catalog |
| Parent | UPI Platform Services |
| Description | Merchant onboarding, configuration, and lifecycle management services. |
| Active | Checked |

**Sub-Category 3: Report an Issue**

| Field | Value |
|---|---|
| Title | Report an Issue |
| Catalog | Service Catalog |
| Parent | UPI Platform Services |
| Description | Report payment issues, settlement discrepancies, and system problems. |
| Active | Checked |

**Sub-Category 4: Infrastructure Requests**

| Field | Value |
|---|---|
| Title | Infrastructure Requests |
| Catalog | Service Catalog |
| Parent | UPI Platform Services |
| Description | Request new environments, infrastructure changes, and resource provisioning. |
| Active | Checked |

**Sub-Category 5: Compliance & Security**

| Field | Value |
|---|---|
| Title | Compliance & Security |
| Catalog | Service Catalog |
| Parent | UPI Platform Services |
| Description | Request compliance audit reports, security reviews, and regulatory documentation. |
| Active | Checked |

### Step 3.4: Verify the Category Hierarchy

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Categories**
2. Filter by: Catalog = Service Catalog, Parent = UPI Platform Services
3. Confirm you see all 5 sub-categories
4. Open the Service Portal and navigate to the Service Catalog to verify the visual layout

---

## Part 4: Create Catalog Items

### Catalog Item 1: "Request Merchant Onboarding"

This is a full-featured catalog item with variables, approvals, and multi-task fulfillment.

#### Step 4.1.1: Create the Catalog Item

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Items**
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | Request Merchant Onboarding |
   | Catalogs | Service Catalog |
   | Category | Merchant Services |
   | Short description | Request onboarding of a new merchant to the UPI payment platform |
   | Description | Use this form to request onboarding of a new merchant to the NPCI UPI Payment Platform. This process includes document verification, technical configuration, and sandbox testing. Expected completion: 5 business days. |
   | Picture | Choose a suitable icon |
   | Delivery time | 5 Days |
   | Active | Checked |

4. Click **Submit**
5. Note the item number (e.g., SC0010001) and reopen the record

#### Step 4.1.2: Add Variables

Open the catalog item record. Scroll down to the **Variables** related list. Click **New** for each variable:

**Variable 1: Merchant Name**

| Field | Value |
|---|---|
| Type | Single Line Text |
| Order | 100 |
| Question | Merchant Name |
| Name | merchant_name |
| Mandatory | Checked |
| Tooltip | Enter the registered business name of the merchant |

**Variable 2: Business Type**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 200 |
| Question | Business Type |
| Name | business_type |
| Mandatory | Checked |

After submitting, open the variable and add these **Question Choices**:

| Text | Value | Order |
|---|---|---|
| Retail | retail | 100 |
| E-commerce | ecommerce | 200 |
| Government | government | 300 |
| Education | education | 400 |

**Variable 3: Merchant ID**

| Field | Value |
|---|---|
| Type | Single Line Text |
| Order | 300 |
| Question | Merchant ID |
| Name | merchant_id |
| Mandatory | Checked |
| Tooltip | Unique merchant identifier assigned by NPCI |

**Variable 4: Integration Type**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 400 |
| Question | Integration Type |
| Name | integration_type |
| Mandatory | Checked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| SDK | sdk | 100 |
| API | api | 200 |
| Plugin | plugin | 300 |

**Variable 5: Expected TPS (Transactions Per Second)**

| Field | Value |
|---|---|
| Type | Integer |
| Order | 500 |
| Question | Expected TPS (Transactions Per Second) |
| Name | expected_tps |
| Mandatory | Checked |
| Tooltip | Estimated peak transactions per second for capacity planning |

**Variable 6: Go-live Date**

| Field | Value |
|---|---|
| Type | Date |
| Order | 600 |
| Question | Planned Go-live Date |
| Name | golive_date |
| Mandatory | Checked |

#### Step 4.1.3: Configure Approval

1. On the catalog item form, scroll to the **Process Engine** tab
2. Set **Flow** to: (we will create this in Part 7; for now, leave it)
3. Alternatively, go to the **Approvals** related list and configure:
   - Navigate to the catalog item record
   - Under the **Related Links** section, click **Approval Definitions**
   - Click **New**

   | Field | Value |
   |---|---|
   | Approval type | User |
   | User | Sanjay Manager |
   | When to approve | Before fulfillment |
   | Condition | (leave blank — always requires approval) |

4. Click **Submit**

#### Step 4.1.4: Configure Fulfillment Tasks (Execution Plan)

1. On the catalog item record, click the **Execution Plan** related link
2. Click **New** to create the execution plan
3. Add **Task 1:**

   | Field | Value |
   |---|---|
   | Short description | Verify merchant documents |
   | Order | 100 |
   | Assignment group | Service Desk |
   | Instructions | Verify the merchant's GST certificate, PAN card, bank account details, and business registration. Confirm all documents are valid and match the information provided in the request. |

4. Add **Task 2:**

   | Field | Value |
   |---|---|
   | Short description | Configure merchant in UPI Switch |
   | Order | 200 |
   | Assignment group | Platform Engineering |
   | Instructions | Create the merchant profile in the UPI Switch configuration. Set up MCC codes, transaction limits, and settlement account. Run smoke tests in sandbox before activating. |

> **Important:** Setting Order 200 > Order 100 makes these tasks sequential. Task 2 will not be created until Task 1 is completed.

---

### Catalog Item 2: "Request API Access"

#### Step 4.2.1: Create the Catalog Item

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Items**
2. Click **New**

   | Field | Value |
   |---|---|
   | Name | Request API Access |
   | Catalogs | Service Catalog |
   | Category | Access & Onboarding |
   | Short description | Request access credentials for UPI platform APIs |
   | Description | Request API access for UPI platform services. Sandbox and UAT access is auto-approved. Production access requires Technical Lead approval. |
   | Delivery time | 2 Days |
   | Active | Checked |

3. Click **Submit** and reopen

#### Step 4.2.2: Add Variables

**Variable 1: API Name**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 100 |
| Question | API Name |
| Name | api_name |
| Mandatory | Checked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| Transaction API | transaction | 100 |
| Settlement API | settlement | 200 |
| Dispute API | dispute | 300 |
| Reporting API | reporting | 400 |

**Variable 2: Environment**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 200 |
| Question | Target Environment |
| Name | target_environment |
| Mandatory | Checked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| Sandbox | sandbox | 100 |
| UAT | uat | 200 |
| Production | production | 300 |

**Variable 3: Purpose**

| Field | Value |
|---|---|
| Type | Multi Line Text |
| Order | 300 |
| Question | Purpose / Use Case |
| Name | purpose |
| Mandatory | Checked |
| Tooltip | Describe how you intend to use this API |

**Variable 4: Requestor Team**

| Field | Value |
|---|---|
| Type | Reference |
| Order | 400 |
| Question | Requestor Team |
| Name | requestor_team |
| Reference | Group (sys_user_group) |
| Mandatory | Checked |

#### Step 4.2.3: Conditional Approval (Production Only)

This is an important pattern. We want approval only when Environment = Production.

**Option A — Catalog UI Policy for Visual Feedback (configured in Part 6)**

**Option B — Approval Definition with Condition:**

1. On the catalog item record, navigate to **Approval Definitions**
2. Click **New**

   | Field | Value |
   |---|---|
   | Approval type | User |
   | User | Ravi Kumar |
   | When to approve | Before fulfillment |
   | Condition | Variable target_environment equals production |

3. Click **Submit**

> **How the condition works:** The approval is only generated when the condition evaluates to true. For Sandbox and UAT requests, no approval is needed and the request goes directly to fulfillment.

#### Step 4.2.4: Fulfillment Task

1. Create an Execution Plan with one task:

   | Field | Value |
   |---|---|
   | Short description | Provision API credentials |
   | Order | 100 |
   | Assignment group | Platform Engineering |
   | Instructions | Generate API key and secret for the requested API and environment. Configure rate limits based on the requestor's team tier. Send credentials securely via the internal credential vault. |

---

### Catalog Item 3: "Report UPI Payment Issue" (Record Producer)

This is a **Record Producer** — it creates an Incident record directly, not an RITM.

#### Step 4.3.1: Create the Record Producer

1. Navigate to **Service Catalog > Catalog Definitions > Record Producers**
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | Report UPI Payment Issue |
   | Catalogs | Service Catalog |
   | Category | Report an Issue |
   | Table name | Incident (incident) |
   | Short description | Report a UPI payment transaction issue for investigation |
   | Description | Use this form to report a failed, stuck, or incorrect UPI payment transaction. This will create an incident for the Platform Engineering team to investigate. |
   | Active | Checked |

4. Click **Submit** and reopen

#### Step 4.3.2: Add Variables

**Variable 1: Transaction ID**

| Field | Value |
|---|---|
| Type | Single Line Text |
| Order | 100 |
| Question | UPI Transaction ID |
| Name | transaction_id |
| Mandatory | Checked |
| Tooltip | The unique UPI transaction reference (e.g., UPI123456789012) |

**Variable 2: Transaction Amount**

| Field | Value |
|---|---|
| Type | Decimal |
| Order | 200 |
| Question | Transaction Amount (INR) |
| Name | transaction_amount |
| Mandatory | Checked |

**Variable 3: Error Code**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 300 |
| Question | UPI Error Code |
| Name | error_code |
| Mandatory | Checked |

Question Choices (common UPI error codes):

| Text | Value | Order |
|---|---|---|
| U30 - Device fingerprint mismatch | u30 | 100 |
| U16 - Risk threshold exceeded | u16 | 200 |
| U28 - Transaction timed out | u28 | 300 |
| U09 - Duplicate request | u09 | 400 |
| U67 - Account frozen | u67 | 500 |
| U78 - PSP not available | u78 | 600 |
| U69 - NPCI system error | u69 | 700 |
| Other | other | 800 |

**Variable 4: Timestamp**

| Field | Value |
|---|---|
| Type | Date/Time |
| Order | 400 |
| Question | Transaction Timestamp |
| Name | txn_timestamp |
| Mandatory | Checked |

**Variable 5: Bank Name**

| Field | Value |
|---|---|
| Type | Single Line Text |
| Order | 500 |
| Question | Remitter Bank Name |
| Name | bank_name |
| Mandatory | Checked |

#### Step 4.3.3: Configure the Record Producer Script

The Record Producer script maps the variables to the target Incident record fields. Open the Record Producer and add this script:

```javascript
// Record Producer Script - Report UPI Payment Issue
// This script runs server-side when the record producer form is submitted

// Set standard incident fields
current.category = 'software';
current.subcategory = 'UPI';
current.contact_type = 'self-service';
current.impact = 2;
current.urgency = 2;

// Set assignment
current.assignment_group.setDisplayValue('Platform Engineering');

// Build the short description from variables
current.short_description = 'UPI Payment Issue - Transaction: ' + producer.transaction_id;

// Build the detailed description
var desc = 'UPI Payment Issue Report\n';
desc += '========================\n';
desc += 'Transaction ID: ' + producer.transaction_id + '\n';
desc += 'Amount (INR): ' + producer.transaction_amount + '\n';
desc += 'Error Code: ' + producer.error_code + '\n';
desc += 'Timestamp: ' + producer.txn_timestamp + '\n';
desc += 'Remitter Bank: ' + producer.bank_name + '\n';
desc += '\nSubmitted via Service Catalog Record Producer';

current.description = desc;
```

> **Key difference from a regular Catalog Item:** This script uses `current` to set fields on the target table (Incident) and `producer` to access the variable values. No RITM or SCTASK is created.

---

### Catalog Item 4: "Request New UPI Service Environment"

#### Step 4.4.1: Create the Catalog Item

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Items**
2. Click **New**

   | Field | Value |
   |---|---|
   | Name | Request New UPI Service Environment |
   | Catalogs | Service Catalog |
   | Category | Infrastructure Requests |
   | Short description | Request provisioning of a new UPI service environment |
   | Description | Request a new environment for UPI services. Includes compute, storage, and network provisioning. Requires management and admin approval. |
   | Delivery time | 10 Days |
   | Active | Checked |

3. Click **Submit** and reopen

#### Step 4.4.2: Add Variables

**Variable 1: Environment Type**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 100 |
| Question | Environment Type |
| Name | env_type |
| Mandatory | Checked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| Development | dev | 100 |
| QA / Testing | qa | 200 |
| Staging / Pre-Production | staging | 300 |
| Disaster Recovery | dr | 400 |

**Variable 2: Justification**

| Field | Value |
|---|---|
| Type | Multi Line Text |
| Order | 200 |
| Question | Business Justification |
| Name | justification |
| Mandatory | Checked |
| Tooltip | Explain why this environment is needed and what project it supports |

**Variable 3: Project Code**

| Field | Value |
|---|---|
| Type | Single Line Text |
| Order | 300 |
| Question | Project Code |
| Name | project_code |
| Mandatory | Checked |
| Tooltip | The project code for cost allocation (e.g., UPI-2024-PROJ-001) |

**Variable 4: Required Resources (Multi Row Variable Set)**

This uses a Multi Row Variable Set — a powerful feature that lets users add multiple rows of structured data.

**Create the Multi Row Variable Set first:**

1. Navigate to **Service Catalog > Catalog Definitions > Variable Sets**
2. Click **New**
3. Select **Multi-Row Variable Set**

   | Field | Value |
   |---|---|
   | Title | Environment Resources |
   | Internal name | env_resources |
   | Description | Specify compute, memory, and storage requirements per component |
   | Order | 400 |

4. Click **Submit** and reopen
5. Add the following variables to the Variable Set:

   **Row Variable 1: Component Name**

   | Field | Value |
   |---|---|
   | Type | Single Line Text |
   | Order | 100 |
   | Question | Component |
   | Name | component_name |

   **Row Variable 2: CPU Cores**

   | Field | Value |
   |---|---|
   | Type | Integer |
   | Order | 200 |
   | Question | CPU Cores |
   | Name | cpu_cores |

   **Row Variable 3: Memory (GB)**

   | Field | Value |
   |---|---|
   | Type | Integer |
   | Order | 300 |
   | Question | Memory (GB) |
   | Name | memory_gb |

   **Row Variable 4: Storage (GB)**

   | Field | Value |
   |---|---|
   | Type | Integer |
   | Order | 400 |
   | Question | Storage (GB) |
   | Name | storage_gb |

6. Go back to the catalog item "Request New UPI Service Environment"
7. In the **Variable Sets** related list, click **Edit**
8. Add "Environment Resources" to the selected list
9. Click **Save**

#### Step 4.4.3: Sequential Approval (Manager then Admin)

1. On the catalog item, navigate to **Approval Definitions**
2. Create **Approval 1:**

   | Field | Value |
   |---|---|
   | Approval type | User |
   | User | Sanjay Manager |
   | Order | 100 |
   | When to approve | Before fulfillment |

3. Create **Approval 2:**

   | Field | Value |
   |---|---|
   | Approval type | User |
   | User | Vijay Admin |
   | Order | 200 |
   | When to approve | Before fulfillment |

> **Sequential approval:** Because Approval 1 has Order 100 and Approval 2 has Order 200, Vijay Admin's approval request is only generated after Sanjay Manager approves. If Sanjay Manager rejects, Vijay Admin never sees the request.

#### Step 4.4.4: Multi-Stage Fulfillment

Create an Execution Plan with three sequential tasks:

**Task 1:**

| Field | Value |
|---|---|
| Short description | Provision compute and network infrastructure |
| Order | 100 |
| Assignment group | Platform Engineering |
| Instructions | Provision VMs/containers per the resource specifications. Configure network segmentation, firewall rules, and load balancers. |

**Task 2:**

| Field | Value |
|---|---|
| Short description | Deploy UPI application stack |
| Order | 200 |
| Assignment group | Platform Engineering |
| Instructions | Deploy the UPI application stack (PSP Switch, Settlement Engine, Dispute Manager) to the new environment. Run deployment verification tests. |

**Task 3:**

| Field | Value |
|---|---|
| Short description | Security hardening and compliance check |
| Order | 300 |
| Assignment group | NOC |
| Instructions | Perform security hardening per NPCI standards. Run vulnerability scan. Verify compliance with RBI IT framework requirements. Document results. |

---

### Catalog Item 5: "Request Compliance Audit Report"

#### Step 4.5.1: Create the Catalog Item

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Items**
2. Click **New**

   | Field | Value |
   |---|---|
   | Name | Request Compliance Audit Report |
   | Catalogs | Service Catalog |
   | Category | Compliance & Security |
   | Short description | Request generation of a compliance audit report |
   | Description | Request a compliance audit report for regulatory submissions. Reports are generated from the NPCI compliance database and delivered within 3 business days. |
   | Delivery time | 3 Days |
   | Active | Checked |

3. Click **Submit** and reopen

#### Step 4.5.2: Add Variables

**Variable 1: Audit Type**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 100 |
| Question | Audit Framework |
| Name | audit_type |
| Mandatory | Checked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| PCI-DSS | pci_dss | 100 |
| SOC 2 Type II | soc2 | 200 |
| RBI IT Framework | rbi_it | 300 |
| ISO 27001 | iso27001 | 400 |

**Variable 2: Date Range — From**

| Field | Value |
|---|---|
| Type | Date |
| Order | 200 |
| Question | Audit Period Start Date |
| Name | audit_from_date |
| Mandatory | Checked |

**Variable 3: Date Range — To**

| Field | Value |
|---|---|
| Type | Date |
| Order | 300 |
| Question | Audit Period End Date |
| Name | audit_to_date |
| Mandatory | Checked |

**Variable 4: Scope**

| Field | Value |
|---|---|
| Type | Multi Line Text |
| Order | 400 |
| Question | Audit Scope Description |
| Name | audit_scope |
| Mandatory | Checked |
| Tooltip | Describe the systems, processes, and data in scope for this audit |

#### Step 4.5.3: Fulfillment

Create a single fulfillment task:

| Field | Value |
|---|---|
| Short description | Generate and deliver compliance audit report |
| Order | 100 |
| Assignment group | NOC |
| Instructions | Generate the requested compliance report from the NPCI Compliance Database. Validate data completeness for the specified date range. Format per the selected audit framework template. Deliver via secure internal document share. |

> **Note:** In a production implementation, this could be automated using Flow Designer to trigger a scheduled report generation job — no human task needed.

---

### Catalog Item 6: "Request Team Member Access"

#### Step 4.6.1: Create the Catalog Item

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Items**
2. Click **New**

   | Field | Value |
   |---|---|
   | Name | Request Team Member Access |
   | Catalogs | Service Catalog |
   | Category | Access & Onboarding |
   | Short description | Request system access or role assignment for a team member |
   | Description | Request access to ServiceNow and UPI platform systems for a team member. Access requests require manager approval and are provisioned within 1 business day. |
   | Delivery time | 1 Day |
   | Active | Checked |

3. Click **Submit** and reopen

#### Step 4.6.2: Add Variables

**Variable 1: User**

| Field | Value |
|---|---|
| Type | Reference |
| Order | 100 |
| Question | User Requiring Access |
| Name | target_user |
| Reference | User (sys_user) |
| Mandatory | Checked |

**Variable 2: Role Requested**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 200 |
| Question | Role Requested |
| Name | role_requested |
| Mandatory | Checked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| ITIL User | itil | 100 |
| Admin | admin | 200 |
| Approver | approver_user | 300 |

**Variable 3: Access Duration**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 300 |
| Question | Access Duration |
| Name | access_duration |
| Mandatory | Checked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| Permanent | permanent | 100 |
| 30 Days | 30_days | 200 |
| 90 Days | 90_days | 300 |

**Variable 4: Manager for Approval**

| Field | Value |
|---|---|
| Type | Reference |
| Order | 400 |
| Question | Approving Manager |
| Name | approving_manager |
| Reference | User (sys_user) |
| Mandatory | Checked |
| Tooltip | Select the manager who will approve this access request |

#### Step 4.6.3: Dynamic Approval (Selected Manager)

For this item, the approval goes to whoever the requester selects in the "Approving Manager" variable. This requires a Flow Designer flow or a workflow that reads the variable value.

**Quick approach using Approval Definition:**

1. Navigate to **Approval Definitions** on the catalog item
2. Click **New**

   | Field | Value |
   |---|---|
   | Approval type | User |
   | User | Sanjay Manager |
   | When to approve | Before fulfillment |

> **Note:** For true dynamic approval (routing to the user selected in the `approving_manager` variable), you need to use Flow Designer. The approach above is a simplified version. In Part 7, we discuss how to build this with Flow Designer.

#### Step 4.6.4: Fulfillment Task

| Field | Value |
|---|---|
| Short description | Provision user access and role assignment |
| Order | 100 |
| Assignment group | Service Desk |
| Instructions | Assign the requested role to the specified user. If access duration is not permanent, set a calendar reminder to revoke access on the expiration date. Notify the user and their manager of the provisioned access. |

---

## Part 5: Variables & Variable Sets — Deep Dive

### 5.1: Create a Reusable Variable Set — "UPI Common Info"

Some variables are needed across multiple catalog items. Instead of recreating them, build a Variable Set.

1. Navigate to **Service Catalog > Catalog Definitions > Variable Sets**
2. Click **New**
3. Select **Single-Row Variable Set** (not Multi-Row)

   | Field | Value |
   |---|---|
   | Title | UPI Common Info |
   | Internal name | upi_common_info |
   | Description | Common fields for UPI service requests: Transaction ID, Service Name, Environment |
   | Order | 50 |

4. Click **Submit** and reopen

5. Add the following variables to this Variable Set:

**Variable 1: UPI Transaction ID**

| Field | Value |
|---|---|
| Type | Single Line Text |
| Order | 100 |
| Question | UPI Transaction ID |
| Name | upi_txn_id |
| Mandatory | Unchecked |
| Tooltip | Optional: enter if this request relates to a specific transaction |

**Variable 2: Related UPI Service**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 200 |
| Question | Related UPI Service |
| Name | related_upi_service |
| Mandatory | Unchecked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| UPI Core Switch | core_switch | 100 |
| Settlement Engine | settlement | 200 |
| Dispute Manager | dispute | 300 |
| Merchant Portal | merchant_portal | 400 |
| Analytics Platform | analytics | 500 |

**Variable 3: Environment**

| Field | Value |
|---|---|
| Type | Select Box |
| Order | 300 |
| Question | Environment |
| Name | common_environment |
| Mandatory | Unchecked |

Question Choices:

| Text | Value | Order |
|---|---|---|
| Production | production | 100 |
| Staging | staging | 200 |
| UAT | uat | 300 |
| Development | dev | 400 |

### 5.2: Attach Variable Set to Catalog Items

1. Open **Request Merchant Onboarding** catalog item
2. Scroll to the **Variable Sets** related list
3. Click **Edit**
4. Move "UPI Common Info" from Available to Selected
5. Click **Save**

Repeat for "Request API Access" and "Request Compliance Audit Report."

> **Result:** All three items now show the UPI Common Info variables (Transaction ID, Service Name, Environment) in addition to their own item-specific variables.

### 5.3: Variable Ordering and Mandatory Settings

Variables display in order based on their **Order** field. Best practices:

- Use increments of 100 (100, 200, 300) to leave room for future additions
- Variable Set order is relative to item variables — a Variable Set with Order 50 appears before item variables starting at 100
- Group related variables together with **Label** type variables as section headers
- Mark only truly required fields as **Mandatory** — over-mandating frustrates users

**Example ordering for "Request Merchant Onboarding":**

```
Order 50:  [Variable Set: UPI Common Info]
             - UPI Transaction ID (optional)
             - Related UPI Service (optional)
             - Environment (optional)
Order 100: Merchant Name (mandatory)
Order 200: Business Type (mandatory)
Order 300: Merchant ID (mandatory)
Order 400: Integration Type (mandatory)
Order 500: Expected TPS (mandatory)
Order 600: Go-live Date (mandatory)
```

---

## Part 6: Catalog Client Scripts & UI Policies

### 6.1: Catalog Client Script — Production Environment Warning

When a user selects "Production" as the environment on "Request API Access," display a warning.

1. Open the **Request API Access** catalog item
2. Scroll to the **Catalog Client Scripts** related list
3. Click **New**

   | Field | Value |
   |---|---|
   | Name | Warn on Production Selection |
   | UI Type | Both (Desktop and Mobile / Service Portal) |
   | Type | onChange |
   | Variable name | target_environment |
   | Active | Checked |

4. Enter the following script:

```javascript
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }

    if (newValue === 'production') {
        // Show warning message
        g_form.showFieldMsg(
            'target_environment',
            'Production API access requires Technical Lead approval and takes additional time.',
            'warning'
        );

        // Show an alert dialog
        alert('WARNING: You are requesting Production API access.\n\n' +
              'This request requires approval from the Technical Lead (Ravi Kumar).\n' +
              'Please ensure you have tested your integration in Sandbox/UAT first.');
    } else {
        // Clear the warning when switching away from Production
        g_form.hideFieldMsg('target_environment');
    }
}
```

5. Click **Submit**

### 6.2: Catalog UI Policy — Make Checkbox Mandatory for API Integration

When "Integration Type" = "API" on the "Request Merchant Onboarding" item, make an acknowledgment checkbox mandatory.

**Step 1: Add the acknowledgment checkbox variable first:**

1. Open **Request Merchant Onboarding**
2. Add a new variable:

   | Field | Value |
   |---|---|
   | Type | Check Box |
   | Order | 450 |
   | Question | I acknowledge that I have reviewed the API documentation |
   | Name | api_doc_acknowledged |
   | Mandatory | Unchecked (the UI Policy will control this) |
   | Default value | false |

**Step 2: Create the Catalog UI Policy:**

1. On the catalog item, scroll to **Catalog UI Policies** related list
2. Click **New**

   | Field | Value |
   |---|---|
   | Short description | Make API doc acknowledgment mandatory when Integration Type is API |
   | Catalog item | Request Merchant Onboarding |
   | Applies on a catalog item view | Checked |
   | On load | Checked |
   | Reverse if false | Checked |

3. In the **Conditions** section, set:
   - **Variable:** integration_type | **is** | **api**

4. Click **Submit** and reopen

5. In the **Catalog UI Policy Actions** related list, click **New**:

   | Field | Value |
   |---|---|
   | Variable | api_doc_acknowledged |
   | Mandatory | Yes |
   | Visible | Yes |

6. Click **Submit**

> **How it works:**
> - When Integration Type = API: the checkbox becomes mandatory and visible
> - When Integration Type = SDK or Plugin: the checkbox reverts to optional (Reverse if false)

### 6.3: Catalog Client Script — Show/Hide Variables

Create a script that shows additional fields only when needed.

1. Open **Request New UPI Service Environment**
2. Add a new variable:

   | Field | Value |
   |---|---|
   | Type | Check Box |
   | Order | 150 |
   | Question | This environment requires High Availability (HA) configuration |
   | Name | requires_ha |
   | Default value | false |

3. Add another variable:

   | Field | Value |
   |---|---|
   | Type | Select Box |
   | Order | 160 |
   | Question | HA Configuration Type |
   | Name | ha_config_type |

   Question Choices: Active-Active (active_active), Active-Passive (active_passive)

4. Create a Catalog Client Script:

   | Field | Value |
   |---|---|
   | Name | Toggle HA Config Visibility |
   | Type | onChange |
   | Variable name | requires_ha |

```javascript
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading) {
        return;
    }

    // newValue is 'true' or 'false' (string) for checkboxes
    if (newValue === 'true' || newValue === true) {
        g_form.setDisplay('ha_config_type', true);
        g_form.setMandatory('ha_config_type', true);
    } else {
        g_form.setDisplay('ha_config_type', false);
        g_form.setMandatory('ha_config_type', false);
        g_form.clearValue('ha_config_type');
    }
}
```

5. Create an **onLoad** script to hide the field initially:

   | Field | Value |
   |---|---|
   | Name | Hide HA Config on Load |
   | Type | onLoad |

```javascript
function onLoad() {
    var requiresHA = g_form.getValue('requires_ha');
    if (requiresHA !== 'true' && requiresHA !== true) {
        g_form.setDisplay('ha_config_type', false);
    }
}
```

---

## Part 7: Approval Workflows

### 7.1: Understanding Approval in ServiceNow

ServiceNow provides several mechanisms for catalog item approval:

| Method | Description | Complexity |
|---|---|---|
| Approval Definitions | Simple user/group approval on the item | Low |
| Workflow Editor | Legacy visual workflow with approval activities | Medium |
| Flow Designer | Modern low-code approval with conditions | Medium-High |

### 7.2: Configure Approval for "Request Merchant Onboarding"

We already set up a basic approval in Part 4. Now let us make it sequential (Manager then Technical Lead).

1. Open **Request Merchant Onboarding**
2. Navigate to **Approval Definitions**
3. Verify the existing approval for Sanjay Manager (Order 100)
4. Add a second approval:

   | Field | Value |
   |---|---|
   | Approval type | User |
   | User | Ravi Kumar |
   | Order | 200 |
   | When to approve | Before fulfillment |

> **Sequential flow:**
> 1. Request submitted
> 2. Sanjay Manager receives approval request (Order 100)
> 3. If Sanjay Manager approves, Ravi Kumar receives approval request (Order 200)
> 4. If Ravi Kumar approves, fulfillment tasks are created
> 5. If either rejects, the request is rejected

### 7.3: Test the Approval Flow

1. **Impersonate Priya Sharma** (the NOC analyst)
   - Click the user avatar (top right) > **Impersonate User** > search for "Priya Sharma"
2. Navigate to **Self-Service > Service Catalog**
3. Browse to **UPI Platform Services > Merchant Services**
4. Click **Request Merchant Onboarding**
5. Fill in the variables:

   | Variable | Value |
   |---|---|
   | Merchant Name | QuickPay Solutions |
   | Business Type | E-commerce |
   | Merchant ID | MERCH-QPS-2024-001 |
   | Integration Type | API |
   | Expected TPS | 500 |
   | Go-live Date | (pick a date 30 days from now) |
   | API Doc Acknowledged | Checked |

6. Click **Order Now**
7. Note the REQ number (e.g., REQ0010001)

8. **Switch to Sanjay Manager:**
   - Impersonate > "Sanjay Manager"
   - Navigate to **Self-Service > My Approvals**
   - Find the approval for REQ0010001
   - Review the request details
   - Click **Approve**

9. **Switch to Ravi Kumar:**
   - Impersonate > "Ravi Kumar"
   - Navigate to **Self-Service > My Approvals**
   - Find the approval
   - Click **Approve**

10. **Verify fulfillment tasks were created:**
    - Navigate to **Service Catalog > Requests**
    - Open the REQ
    - Open the RITM
    - Verify two SCTASKs exist:
      - SCTASK: "Verify merchant documents" (assigned to Service Desk)
      - SCTASK: "Configure merchant in UPI Switch" (assigned to Platform Engineering, not yet active)

### 7.4: Delegation of Approvals

When an approver is unavailable (e.g., Sanjay Manager is on vacation), approvals can be delegated.

1. Impersonate **Sanjay Manager**
2. Navigate to **Self-Service > My Profile**
3. Look for the **Delegate** related list or navigate to **Self-Service > Delegation**
4. Click **New**
5. Fill in:

   | Field | Value |
   |---|---|
   | Delegate | Ravi Kumar |
   | Starts | (today) |
   | Ends | (one week from today) |

6. Click **Submit**

> **Result:** Any approvals that come to Sanjay Manager during this period will also be visible to Ravi Kumar, who can approve on Sanjay's behalf.

---

## Part 8: Request Fulfillment (SCTASKs)

### 8.1: Complete Fulfillment Tasks

Continuing from Part 7, let us complete the fulfillment tasks for the "QuickPay Solutions" merchant onboarding.

#### Step 8.1.1: Complete Task 1 — Verify Merchant Documents

1. Impersonate **Meera Joshi** (Service Desk)
2. Navigate to **Service Catalog > Catalog Tasks** (or filter for SCTASK)
3. Find the task: "Verify merchant documents"
4. Open it and observe:
   - **State:** Open
   - **Assignment group:** Service Desk
   - **Request item:** (linked to the RITM)
5. Add a **Work Note:**
   ```
   Verified merchant documents for QuickPay Solutions:
   - GST Certificate: Valid (GSTIN: 27AABCQ1234A1Z5)
   - PAN: Valid (AABCQ1234A)
   - Bank Account: Verified with ICICI Bank
   - Business Registration: Valid MCA registration
   All documents verified and compliant.
   ```
6. Change **State** to **Closed Complete**
7. Click **Update**

#### Step 8.1.2: Complete Task 2 — Configure Merchant in UPI Switch

1. Impersonate **Ravi Kumar** (Platform Engineering)
2. Navigate to **Service Catalog > Catalog Tasks**
3. Find the task: "Configure merchant in UPI Switch"
   - **Note:** This task should now be **Open** because Task 1 is complete (sequential execution)
4. Add a **Work Note:**
   ```
   Merchant QuickPay Solutions configured in UPI Switch:
   - MCC Code: 5411 (E-commerce)
   - Transaction limit: 500 TPS
   - Settlement account: ICICI Bank - configured
   - Sandbox testing: PASSED (50/50 test transactions successful)
   - Production activation: Ready for go-live on scheduled date
   ```
5. Change **State** to **Closed Complete**
6. Click **Update**

### 8.2: Verify the Lifecycle

After both SCTASKs are completed:

1. Navigate to the **RITM** record
   - **Expected state:** Closed Complete
   - All SCTASKs completed, so the RITM automatically closes

2. Navigate to the **REQ** record
   - **Expected state:** Closed Complete
   - All RITMs completed, so the REQ automatically closes

3. Check the **Activity Log** on the REQ to see the full timeline:
   ```
   REQ created → RITM created → Approval requested (Sanjay) →
   Approved (Sanjay) → Approval requested (Ravi) →
   Approved (Ravi) → SCTASK 1 created → SCTASK 1 completed →
   SCTASK 2 created → SCTASK 2 completed → RITM closed → REQ closed
   ```

### 8.3: SLA on Catalog Tasks

You can apply SLAs to catalog tasks to ensure timely fulfillment.

1. Navigate to **Service Level Management > SLA Definitions**
2. Click **New**

   | Field | Value |
   |---|---|
   | Name | Catalog Task - 2 Business Day Resolution |
   | Table | Catalog Task (sc_task) |
   | Type | SLA |
   | Duration | 2 Business Days |
   | Start condition | State = Open |
   | Stop condition | State = Closed Complete OR State = Closed Incomplete |
   | Target | 100% completed within 2 business days |

3. Click **Submit**

---

## Part 9: Test End-to-End

### 9.1: Scenario — Priya Sharma Requests API Access

This walkthrough demonstrates the complete self-service experience.

#### Step 9.1.1: Submit the Request

1. **Impersonate Priya Sharma**
2. Navigate to **Self-Service > Service Catalog**
3. Browse to **UPI Platform Services > Access & Onboarding**
4. Click **Request API Access**
5. Fill in:

   | Variable | Value |
   |---|---|
   | API Name | Transaction API |
   | Target Environment | Production |
   | Purpose / Use Case | Need Production Transaction API access to implement real-time transaction monitoring dashboard for the NOC team. |
   | Requestor Team | NOC |

6. **Observe:** The warning message appears because you selected "Production"
7. Click **Order Now**
8. Note the REQ number

#### Step 9.1.2: Approve the Request

1. **Impersonate Ravi Kumar**
2. Navigate to **Self-Service > My Approvals**
3. Find and open the approval
4. Review the details — confirm it is a Production API access request
5. Click **Approve**

#### Step 9.1.3: Fulfill the Request

1. **Stay as Ravi Kumar** (Platform Engineering)
2. Navigate to **Service Catalog > Catalog Tasks**
3. Find "Provision API credentials"
4. Add work notes:
   ```
   API credentials provisioned:
   - API: Transaction API
   - Environment: Production
   - API Key: Generated and stored in vault
   - Rate limit: 100 req/sec (NOC tier)
   - Documentation link sent to requestor
   ```
5. Close the task

#### Step 9.1.4: Verify Completion

1. **Impersonate Priya Sharma**
2. Navigate to **Self-Service > My Requests**
3. Confirm the request shows as **Closed Complete**
4. Verify the REQ > RITM > SCTASK chain is fully closed

### 9.2: Scenario — Report UPI Payment Issue (Record Producer)

1. **Impersonate Amit Verma**
2. Navigate to **Self-Service > Service Catalog**
3. Browse to **UPI Platform Services > Report an Issue**
4. Click **Report UPI Payment Issue**
5. Fill in:

   | Variable | Value |
   |---|---|
   | UPI Transaction ID | UPI202409151430ABCD |
   | Transaction Amount (INR) | 15000.50 |
   | UPI Error Code | U28 - Transaction timed out |
   | Transaction Timestamp | (yesterday at 14:30) |
   | Remitter Bank | State Bank of India |

6. Click **Submit**
7. **Observe:** You are redirected to an **Incident** record (not an RITM)
8. Verify on the Incident:
   - **Category:** Software
   - **Subcategory:** UPI
   - **Assignment group:** Platform Engineering
   - **Short description:** Contains the Transaction ID
   - **Description:** Contains all the variable values

> This demonstrates the key difference between a Record Producer and a regular Catalog Item. The user experience is the same (they go through the Service Catalog), but the backend creates an Incident instead of a Request.

---

## Practice Exercises

### Exercise 1: Create "Request UPI Transaction Limit Increase"

Create a new catalog item with the following specifications:

- **Category:** Merchant Services
- **Variables:**
  - Merchant ID (string, mandatory)
  - Current Transaction Limit (integer, read-only if possible)
  - Requested New Limit (integer, mandatory)
  - Justification (multi-line text, mandatory)
  - Effective Date (date, mandatory)
- **Approval:** Sanjay Manager
- **Fulfillment:** 1 SCTASK — "Update transaction limit in UPI Switch"

**Validation:** Submit a request, approve it, and complete the fulfillment task. Verify the REQ > RITM > SCTASK lifecycle.

---

### Exercise 2: Create an Order Guide — "New Team Member Setup"

An Order Guide bundles multiple catalog items into a single ordering experience.

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Order Guides**
2. Click **New**

   | Field | Value |
   |---|---|
   | Name | New Team Member Setup |
   | Catalogs | Service Catalog |
   | Category | Access & Onboarding |
   | Short description | Complete onboarding package: system access and API credentials |
   | Two step | Checked |

3. Click **Submit** and reopen
4. In the **Order Guide Items** related list, add:
   - Request Team Member Access
   - Request API Access

5. **Rule Base (optional):** Add a rule that includes "Request API Access" only when a certain variable is selected

6. **Test:** Order the guide, observe that a single REQ is created with two RITMs (one for each bundled item)

---

### Exercise 3: Validate Transaction ID Format

Create a Catalog Client Script that validates the UPI Transaction ID format on the "Report UPI Payment Issue" Record Producer.

1. Open the Record Producer
2. Add a Catalog Client Script:

   | Field | Value |
   |---|---|
   | Name | Validate Transaction ID Format |
   | Type | onChange |
   | Variable name | transaction_id |

```javascript
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }

    // UPI Transaction IDs must start with "UPI"
    if (newValue.substring(0, 3) !== 'UPI') {
        g_form.showFieldMsg(
            'transaction_id',
            'Transaction ID must start with "UPI" (e.g., UPI202409151430ABCD)',
            'error'
        );
    } else if (newValue.length < 10) {
        g_form.showFieldMsg(
            'transaction_id',
            'Transaction ID appears too short. Please verify.',
            'warning'
        );
    } else {
        g_form.hideFieldMsg('transaction_id');
    }
}
```

**Test:** Enter an invalid Transaction ID (e.g., "TXN12345") and verify the error appears. Enter a valid one (e.g., "UPI202409151430ABCD") and verify the error clears.

---

### Exercise 4: Record Producer — "Report Settlement Discrepancy"

Create a Record Producer that creates a **Problem** record.

1. Navigate to **Service Catalog > Catalog Definitions > Record Producers**
2. Click **New**

   | Field | Value |
   |---|---|
   | Name | Report Settlement Discrepancy |
   | Table name | Problem (problem) |
   | Category | Report an Issue |
   | Short description | Report a settlement amount mismatch for root cause analysis |

3. Add Variables:
   - Settlement Batch ID (string, mandatory)
   - Expected Amount (decimal, mandatory)
   - Actual Amount (decimal, mandatory)
   - Discrepancy Amount (decimal — ideally calculated, but can be manual)
   - Affected Banks (multi-line text)
   - Settlement Date (date, mandatory)

4. Add the Record Producer Script:

```javascript
// Record Producer Script - Report Settlement Discrepancy
current.category = 'software';
current.subcategory = 'UPI';
current.impact = 2;
current.urgency = 2;
current.assignment_group.setDisplayValue('Platform Engineering');

current.short_description = 'Settlement Discrepancy - Batch: ' + producer.settlement_batch_id;

var desc = 'Settlement Discrepancy Report\n';
desc += '=============================\n';
desc += 'Batch ID: ' + producer.settlement_batch_id + '\n';
desc += 'Expected Amount: INR ' + producer.expected_amount + '\n';
desc += 'Actual Amount: INR ' + producer.actual_amount + '\n';
desc += 'Discrepancy: INR ' + producer.discrepancy_amount + '\n';
desc += 'Settlement Date: ' + producer.settlement_date + '\n';
desc += 'Affected Banks:\n' + producer.affected_banks + '\n';

current.description = desc;
```

5. **Test:** Submit the form and verify a Problem record is created with the correct field mappings.

---

### Exercise 5: Build a Report — Top 10 Most Requested Catalog Items

1. Navigate to **Reports > Create New**
2. Configure:

   | Field | Value |
   |---|---|
   | Report name | Top 10 Most Requested Catalog Items |
   | Source type | Table |
   | Table | Requested Item (sc_req_item) |
   | Type | Bar chart |
   | Group by | Catalog Item |
   | Aggregation | Count |
   | Sort by | Count (descending) |
   | Limit | 10 |

3. Add filters if needed:
   - Created on: Last 90 days
   - State: is not Cancelled

4. Run the report and save it
5. **Bonus:** Add this report to a dashboard alongside your existing ITSM reports

---

## Appendix: Background Scripts for Bulk Setup

The following scripts can be run from **System Definition > Scripts - Background** to automatically create the catalog structure, categories, and items. This is useful for lab setup or demo environment preparation.

> **WARNING:** Background scripts execute server-side code with full admin privileges. Only run these in a development/PDI environment. Never run untested scripts in production.

### Script 1: Create Catalog Categories

```javascript
// ============================================================
// Script: Create UPI Platform Service Catalog Categories
// Run from: System Definition > Scripts - Background
// ============================================================

var catalogGR = new GlideRecord('sc_catalog');
catalogGR.addQuery('title', 'Service Catalog');
catalogGR.query();
var catalogSysId = '';
if (catalogGR.next()) {
    catalogSysId = catalogGR.sys_id.toString();
    gs.info('Found Service Catalog: ' + catalogSysId);
}

// Create parent category
var parentCat = new GlideRecord('sc_category');
parentCat.initialize();
parentCat.title = 'UPI Platform Services';
parentCat.sc_catalog = catalogSysId;
parentCat.description = 'Self-service catalog for NPCI UPI Payment Platform';
parentCat.active = true;
var parentSysId = parentCat.insert();
gs.info('Created parent category: ' + parentSysId);

// Sub-categories
var subCategories = [
    { title: 'Access & Onboarding', desc: 'Request access to systems, APIs, and onboard new team members' },
    { title: 'Merchant Services', desc: 'Merchant onboarding, configuration, and lifecycle management' },
    { title: 'Report an Issue', desc: 'Report payment issues, settlement discrepancies, and system problems' },
    { title: 'Infrastructure Requests', desc: 'Request new environments, infrastructure changes, and resources' },
    { title: 'Compliance & Security', desc: 'Request compliance audit reports and security reviews' }
];

for (var i = 0; i < subCategories.length; i++) {
    var subCat = new GlideRecord('sc_category');
    subCat.initialize();
    subCat.title = subCategories[i].title;
    subCat.sc_catalog = catalogSysId;
    subCat.parent = parentSysId;
    subCat.description = subCategories[i].desc;
    subCat.active = true;
    var subSysId = subCat.insert();
    gs.info('Created sub-category: ' + subCategories[i].title + ' (' + subSysId + ')');
}

gs.info('=== Category creation complete ===');
```

### Script 2: Create Catalog Items with Variables

```javascript
// ============================================================
// Script: Create UPI Catalog Items with Variables
// Run from: System Definition > Scripts - Background
// Prerequisites: Run Script 1 first (categories must exist)
// ============================================================

// Helper function to find a category by title
function getCategorySysId(title) {
    var gr = new GlideRecord('sc_category');
    gr.addQuery('title', title);
    gr.query();
    if (gr.next()) {
        return gr.sys_id.toString();
    }
    gs.warn('Category not found: ' + title);
    return '';
}

// Helper function to find the Service Catalog sys_id
function getServiceCatalogSysId() {
    var gr = new GlideRecord('sc_catalog');
    gr.addQuery('title', 'Service Catalog');
    gr.query();
    if (gr.next()) {
        return gr.sys_id.toString();
    }
    return '';
}

// Helper function to add a variable to a catalog item
function addVariable(catItemSysId, type, order, question, name, mandatory, tooltip) {
    var v = new GlideRecord('item_option_new');
    v.initialize();
    v.cat_item = catItemSysId;
    v.type = type;          // 6=Single Line, 5=Select Box, 8=Reference, etc.
    v.order = order;
    v.question_text = question;
    v.name = name;
    v.mandatory = mandatory || false;
    if (tooltip) v.tooltip = tooltip;
    return v.insert();
}

// Helper function to add question choices
function addChoice(variableSysId, text, value, order) {
    var c = new GlideRecord('question_choice');
    c.initialize();
    c.question = variableSysId;
    c.text = text;
    c.value = value;
    c.order = order;
    c.insert();
}

var catalogSysId = getServiceCatalogSysId();
var merchantSvcCat = getCategorySysId('Merchant Services');
var accessCat = getCategorySysId('Access & Onboarding');
var infraCat = getCategorySysId('Infrastructure Requests');
var complianceCat = getCategorySysId('Compliance & Security');

// ---- Item 1: Request Merchant Onboarding ----
var item1 = new GlideRecord('sc_cat_item');
item1.initialize();
item1.name = 'Request Merchant Onboarding';
item1.sc_catalogs = catalogSysId;
item1.category = merchantSvcCat;
item1.short_description = 'Request onboarding of a new merchant to the UPI payment platform';
item1.delivery_time = '5 00:00:00';   // 5 days
item1.active = true;
var item1SysId = item1.insert();
gs.info('Created: Request Merchant Onboarding (' + item1SysId + ')');

// Variables for Item 1
var v1 = addVariable(item1SysId, 6, 100, 'Merchant Name', 'merchant_name', true, 'Registered business name');
var v2 = addVariable(item1SysId, 5, 200, 'Business Type', 'business_type', true);
addChoice(v2, 'Retail', 'retail', 100);
addChoice(v2, 'E-commerce', 'ecommerce', 200);
addChoice(v2, 'Government', 'government', 300);
addChoice(v2, 'Education', 'education', 400);

addVariable(item1SysId, 6, 300, 'Merchant ID', 'merchant_id', true, 'Unique NPCI merchant identifier');

var v4 = addVariable(item1SysId, 5, 400, 'Integration Type', 'integration_type', true);
addChoice(v4, 'SDK', 'sdk', 100);
addChoice(v4, 'API', 'api', 200);
addChoice(v4, 'Plugin', 'plugin', 300);

addVariable(item1SysId, 14, 500, 'Expected TPS', 'expected_tps', true, 'Peak transactions per second');
addVariable(item1SysId, 10, 600, 'Planned Go-live Date', 'golive_date', true);

// ---- Item 2: Request API Access ----
var item2 = new GlideRecord('sc_cat_item');
item2.initialize();
item2.name = 'Request API Access';
item2.sc_catalogs = catalogSysId;
item2.category = accessCat;
item2.short_description = 'Request access credentials for UPI platform APIs';
item2.delivery_time = '2 00:00:00';
item2.active = true;
var item2SysId = item2.insert();
gs.info('Created: Request API Access (' + item2SysId + ')');

var v5 = addVariable(item2SysId, 5, 100, 'API Name', 'api_name', true);
addChoice(v5, 'Transaction API', 'transaction', 100);
addChoice(v5, 'Settlement API', 'settlement', 200);
addChoice(v5, 'Dispute API', 'dispute', 300);
addChoice(v5, 'Reporting API', 'reporting', 400);

var v6 = addVariable(item2SysId, 5, 200, 'Target Environment', 'target_environment', true);
addChoice(v6, 'Sandbox', 'sandbox', 100);
addChoice(v6, 'UAT', 'uat', 200);
addChoice(v6, 'Production', 'production', 300);

addVariable(item2SysId, 2, 300, 'Purpose / Use Case', 'purpose', true);
addVariable(item2SysId, 8, 400, 'Requestor Team', 'requestor_team', true);

// ---- Item 3: Request New UPI Service Environment ----
var item3 = new GlideRecord('sc_cat_item');
item3.initialize();
item3.name = 'Request New UPI Service Environment';
item3.sc_catalogs = catalogSysId;
item3.category = infraCat;
item3.short_description = 'Request provisioning of a new UPI service environment';
item3.delivery_time = '10 00:00:00';
item3.active = true;
var item3SysId = item3.insert();
gs.info('Created: Request New UPI Service Environment (' + item3SysId + ')');

var v7 = addVariable(item3SysId, 5, 100, 'Environment Type', 'env_type', true);
addChoice(v7, 'Development', 'dev', 100);
addChoice(v7, 'QA / Testing', 'qa', 200);
addChoice(v7, 'Staging / Pre-Production', 'staging', 300);
addChoice(v7, 'Disaster Recovery', 'dr', 400);

addVariable(item3SysId, 2, 200, 'Business Justification', 'justification', true);
addVariable(item3SysId, 6, 300, 'Project Code', 'project_code', true, 'e.g., UPI-2024-PROJ-001');

// ---- Item 4: Request Compliance Audit Report ----
var item4 = new GlideRecord('sc_cat_item');
item4.initialize();
item4.name = 'Request Compliance Audit Report';
item4.sc_catalogs = catalogSysId;
item4.category = complianceCat;
item4.short_description = 'Request generation of a compliance audit report';
item4.delivery_time = '3 00:00:00';
item4.active = true;
var item4SysId = item4.insert();
gs.info('Created: Request Compliance Audit Report (' + item4SysId + ')');

var v8 = addVariable(item4SysId, 5, 100, 'Audit Framework', 'audit_type', true);
addChoice(v8, 'PCI-DSS', 'pci_dss', 100);
addChoice(v8, 'SOC 2 Type II', 'soc2', 200);
addChoice(v8, 'RBI IT Framework', 'rbi_it', 300);
addChoice(v8, 'ISO 27001', 'iso27001', 400);

addVariable(item4SysId, 10, 200, 'Audit Period Start Date', 'audit_from_date', true);
addVariable(item4SysId, 10, 300, 'Audit Period End Date', 'audit_to_date', true);
addVariable(item4SysId, 2, 400, 'Audit Scope Description', 'audit_scope', true);

// ---- Item 5: Request Team Member Access ----
var item5 = new GlideRecord('sc_cat_item');
item5.initialize();
item5.name = 'Request Team Member Access';
item5.sc_catalogs = catalogSysId;
item5.category = accessCat;
item5.short_description = 'Request system access or role assignment for a team member';
item5.delivery_time = '1 00:00:00';
item5.active = true;
var item5SysId = item5.insert();
gs.info('Created: Request Team Member Access (' + item5SysId + ')');

addVariable(item5SysId, 8, 100, 'User Requiring Access', 'target_user', true);

var v9 = addVariable(item5SysId, 5, 200, 'Role Requested', 'role_requested', true);
addChoice(v9, 'ITIL User', 'itil', 100);
addChoice(v9, 'Admin', 'admin', 200);
addChoice(v9, 'Approver', 'approver_user', 300);

var v10 = addVariable(item5SysId, 5, 300, 'Access Duration', 'access_duration', true);
addChoice(v10, 'Permanent', 'permanent', 100);
addChoice(v10, '30 Days', '30_days', 200);
addChoice(v10, '90 Days', '90_days', 300);

addVariable(item5SysId, 8, 400, 'Approving Manager', 'approving_manager', true);

gs.info('=== Catalog item creation complete ===');
gs.info('Items created: 5 catalog items with variables');
gs.info('Note: Record Producer for "Report UPI Payment Issue" must be created manually');
```

### Script 3: Create Record Producer

```javascript
// ============================================================
// Script: Create Record Producer - Report UPI Payment Issue
// Run from: System Definition > Scripts - Background
// ============================================================

function getCategorySysId(title) {
    var gr = new GlideRecord('sc_category');
    gr.addQuery('title', title);
    gr.query();
    if (gr.next()) return gr.sys_id.toString();
    return '';
}

function getServiceCatalogSysId() {
    var gr = new GlideRecord('sc_catalog');
    gr.addQuery('title', 'Service Catalog');
    gr.query();
    if (gr.next()) return gr.sys_id.toString();
    return '';
}

var catalogSysId = getServiceCatalogSysId();
var issueCat = getCategorySysId('Report an Issue');

var rp = new GlideRecord('sc_cat_item_producer');
rp.initialize();
rp.name = 'Report UPI Payment Issue';
rp.sc_catalogs = catalogSysId;
rp.category = issueCat;
rp.table_name = 'incident';
rp.short_description = 'Report a UPI payment transaction issue for investigation';
rp.active = true;

// Record Producer script
rp.script = "current.category = 'software';\n" +
    "current.subcategory = 'UPI';\n" +
    "current.contact_type = 'self-service';\n" +
    "current.impact = 2;\n" +
    "current.urgency = 2;\n" +
    "current.assignment_group.setDisplayValue('Platform Engineering');\n" +
    "current.short_description = 'UPI Payment Issue - Transaction: ' + producer.transaction_id;\n" +
    "var desc = 'UPI Payment Issue Report\\n';\n" +
    "desc += 'Transaction ID: ' + producer.transaction_id + '\\n';\n" +
    "desc += 'Amount (INR): ' + producer.transaction_amount + '\\n';\n" +
    "desc += 'Error Code: ' + producer.error_code + '\\n';\n" +
    "desc += 'Timestamp: ' + producer.txn_timestamp + '\\n';\n" +
    "desc += 'Remitter Bank: ' + producer.bank_name + '\\n';\n" +
    "current.description = desc;\n";

var rpSysId = rp.insert();
gs.info('Created Record Producer: ' + rpSysId);

// Add variables to the record producer
function addRPVariable(rpSysId, type, order, question, name, mandatory, tooltip) {
    var v = new GlideRecord('item_option_new');
    v.initialize();
    v.cat_item = rpSysId;
    v.type = type;
    v.order = order;
    v.question_text = question;
    v.name = name;
    v.mandatory = mandatory || false;
    if (tooltip) v.tooltip = tooltip;
    return v.insert();
}

function addChoice(varSysId, text, value, order) {
    var c = new GlideRecord('question_choice');
    c.initialize();
    c.question = varSysId;
    c.text = text;
    c.value = value;
    c.order = order;
    c.insert();
}

addRPVariable(rpSysId, 6, 100, 'UPI Transaction ID', 'transaction_id', true, 'e.g., UPI202409151430ABCD');
addRPVariable(rpSysId, 4, 200, 'Transaction Amount (INR)', 'transaction_amount', true);

var errVar = addRPVariable(rpSysId, 5, 300, 'UPI Error Code', 'error_code', true);
addChoice(errVar, 'U30 - Device fingerprint mismatch', 'u30', 100);
addChoice(errVar, 'U16 - Risk threshold exceeded', 'u16', 200);
addChoice(errVar, 'U28 - Transaction timed out', 'u28', 300);
addChoice(errVar, 'U09 - Duplicate request', 'u09', 400);
addChoice(errVar, 'U67 - Account frozen', 'u67', 500);
addChoice(errVar, 'U78 - PSP not available', 'u78', 600);
addChoice(errVar, 'U69 - NPCI system error', 'u69', 700);
addChoice(errVar, 'Other', 'other', 800);

addRPVariable(rpSysId, 11, 400, 'Transaction Timestamp', 'txn_timestamp', true);
addRPVariable(rpSysId, 6, 500, 'Remitter Bank Name', 'bank_name', true);

gs.info('=== Record Producer creation complete ===');
```

---

## Quick Reference

### Key Tables

| Table | Label | Prefix | Module Path |
|---|---|---|---|
| sc_catalog | Service Catalog | — | Catalog Definitions > Maintain Catalogs |
| sc_category | Category | — | Catalog Definitions > Maintain Categories |
| sc_cat_item | Catalog Item | SC | Catalog Definitions > Maintain Items |
| sc_cat_item_producer | Record Producer | — | Catalog Definitions > Record Producers |
| sc_cat_item_guide | Order Guide | — | Catalog Definitions > Maintain Order Guides |
| item_option_new | Variable | — | (related list on catalog item) |
| item_option_new_set | Variable Set | — | Catalog Definitions > Variable Sets |
| sc_request | Request | REQ | Service Catalog > Requests |
| sc_req_item | Requested Item | RITM | (related list on REQ) |
| sc_task | Catalog Task | SCTASK | Service Catalog > Catalog Tasks |

### Variable Type Numbers (for scripts)

| Type Number | Type Name |
|---|---|
| 1 | Yes / No |
| 2 | Multi Line Text |
| 3 | Multiple Choice |
| 4 | Numeric Scale |
| 5 | Select Box |
| 6 | Single Line Text |
| 7 | Check Box |
| 8 | Reference |
| 9 | Date |
| 10 | Date/Time |
| 11 | Label |
| 14 | Integer |
| 15 | Lookup Select Box |
| 21 | List Collector |
| 24 | Multi Row Variable Set |

### Request Lifecycle States

```
REQ States:        Open → Approved → Closed Complete / Closed Incomplete
RITM States:       Open → Approved → Work in Progress → Closed Complete / Closed Incomplete
SCTASK States:     Open → Work in Progress → Closed Complete / Closed Incomplete / Closed Skipped
Approval States:   Requested → Approved / Rejected
```

### Catalog-Specific Scripting APIs

```javascript
// In Catalog Client Scripts:
g_form.getValue('variable_name');           // Get variable value
g_form.setValue('variable_name', 'value');   // Set variable value
g_form.setDisplay('variable_name', true);   // Show/hide variable
g_form.setMandatory('variable_name', true); // Make mandatory
g_form.showFieldMsg('var', 'msg', 'type');  // Show field message (info/warning/error)
g_form.hideFieldMsg('variable_name');       // Hide field message
g_form.addOption('var', 'value', 'label');  // Add choice option
g_form.removeOption('var', 'value');        // Remove choice option

// In Record Producer Scripts:
producer.variable_name    // Access variable value
current.field_name        // Set target record field

// In Server Scripts (Business Rules on sc_req_item):
current.variables.variable_name    // Access RITM variable value
```

---

## Summary

In this lab, you built a complete Service Catalog for the NPCI UPI Payment Platform:

| Component | What You Created |
|---|---|
| Category Structure | 1 parent + 5 sub-categories |
| Catalog Items | 5 standard catalog items |
| Record Producer | 1 (creates Incident from catalog) |
| Variables | 25+ variables across all items |
| Variable Sets | 2 (UPI Common Info + Environment Resources MRVS) |
| Catalog Client Scripts | 3 (warning, validation, show/hide) |
| Catalog UI Policies | 1 (conditional mandatory field) |
| Approval Definitions | Multiple (simple, sequential, conditional) |
| Fulfillment Tasks | Multi-stage SCTASK execution plans |
| End-to-End Tests | 2 complete request lifecycle walkthroughs |

**Key takeaways:**
- Service Requests are pre-defined, low-risk, and follow standard fulfillment models
- The REQ > RITM > SCTASK hierarchy provides structured fulfillment tracking
- Record Producers bridge the gap between self-service and other ITSM processes
- Variables, Client Scripts, and UI Policies create dynamic, user-friendly forms
- Approval definitions support simple, sequential, and conditional approval patterns
- Variable Sets promote reuse and consistency across catalog items

**Next Lab:** Lab 12 continues with Event Management and operational monitoring integration for the UPI platform.

---

*Lab 11 of 22 | NPCI UPI Payment Platform — ITIL 4 ServiceNow Lab Series*
