# Lab 10: Service Catalog & Request Management

**Level:** Intermediate | **Duration:** 90 minutes | **Prerequisites:** Lab 07-09 completed

---

## Objective

By the end of this lab, you will:
- Create catalog categories and catalog items
- Add variables (form fields) to catalog items
- Configure approval workflows for catalog items
- Submit requests and track REQ/RITM/SCTASK lifecycle
- Customize the self-service portal

---

## Part 1: Explore the Existing Service Catalog

### Step 1.1: View as End User

1. Navigate to **Self-Service > Service Catalog** (or type `sc_homepage`)
2. Browse the existing catalog categories and items
3. Note the structure:
   ```
   Service Catalog
     > Can We Help You?
     > Hardware
     > Software
     > Services
     > Peripherals
   ```
4. Click into a category and browse the catalog items

### Step 1.2: View as Admin

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Categories** (or type `sc_category.list`)
2. View all categories
3. Navigate to **Service Catalog > Catalog Definitions > Maintain Items** (or type `sc_cat_item.list`)
4. View all catalog items

---

## Part 2: Create a New Category

### Step 2.1: Create the Category

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Categories**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Title | IT Access Management |
   | Description | Request access to IT systems, databases, and tools |
   | Icon | (choose an icon, e.g., a lock or key icon) |
   | Active | Checked |
   | Parent | Service Catalog (the main catalog) |

4. Click **Submit**

---

## Part 3: Create a Catalog Item

### Step 3.1: Create the Item

1. Navigate to **Service Catalog > Catalog Definitions > Maintain Items**
2. Click **New**
3. Fill in the basic details:

   | Field | Value |
   |---|---|
   | Name | Database Access Request |
   | Short description | Request read or read-write access to a production database |
   | Description | Use this form to request access to any production database. All requests require manager and DBA team approval. Access will be provisioned within 4 business hours of final approval. |
   | Category | IT Access Management (the category you just created) |
   | Catalogs | Service Catalog |
   | Active | Checked |
   | Icon | (choose a database icon) |

4. Click **Submit** (this saves the item and lets you add more details)

### Step 3.2: Reopen and Configure

1. Reopen the "Database Access Request" catalog item
2. You'll now see additional tabs and related lists

---

## Part 4: Add Variables (Form Fields)

### Step 4.1: Understand Variables

Variables are the form fields that users fill in when ordering a catalog item. Think of them as the "order form."

### Step 4.2: Add Variables to Your Catalog Item

1. On the "Database Access Request" item, find the **Variables** related list
2. Click **New** to add each variable:

**Variable 1: Database Name**
| Field | Value |
|---|---|
| Type | Select Box |
| Question | Which database do you need access to? |
| Name | u_database_name |
| Mandatory | Yes |
| Order | 100 |
| Choice values | Add these choices: |

Choices:
- `prod_app_db` → Production Application Database
- `prod_reporting_db` → Production Reporting Database
- `prod_analytics_db` → Analytics Database
- `prod_audit_db` → Audit Database

Click **Submit**

**Variable 2: Access Type**
| Field | Value |
|---|---|
| Type | Radio Buttons |
| Question | What type of access do you need? |
| Name | u_access_type |
| Mandatory | Yes |
| Order | 200 |
| Choice values | |

Choices:
- `read_only` → Read-Only
- `read_write` → Read-Write

Click **Submit**

**Variable 3: Duration**
| Field | Value |
|---|---|
| Type | Select Box |
| Question | How long do you need access? |
| Name | u_duration |
| Mandatory | Yes |
| Order | 300 |
| Choice values | |

Choices:
- `24h` → 24 Hours
- `1week` → 1 Week
- `1month` → 1 Month
- `permanent` → Permanent

Click **Submit**

**Variable 4: Justification**
| Field | Value |
|---|---|
| Type | Multi Line Text |
| Question | Business justification for this access request |
| Name | u_justification |
| Mandatory | Yes |
| Order | 400 |
| Help text | Please explain why you need this access and what you will use it for. |

Click **Submit**

**Variable 5: Requested For**
| Field | Value |
|---|---|
| Type | Reference |
| Question | Who needs this access? |
| Name | u_requested_for |
| Reference | User [sys_user] |
| Mandatory | Yes |
| Order | 50 |
| Default value | (current user) |

Click **Submit**

### Step 4.3: Preview the Catalog Item

1. Navigate to **Self-Service > Service Catalog**
2. Find the **IT Access Management** category
3. Click **Database Access Request**
4. You should see the order form with all your variables:
   ```
   Database Access Request
   ─────────────────────────────────────
   Who needs this access?      [Current User  🔍]
   Which database?             [Select one ▼]
   What type of access?        ○ Read-Only  ○ Read-Write
   How long?                   [Select one ▼]
   Business justification:     [                         ]
                               [                         ]
                               [                         ]

                               [Order Now]  [Add to Cart]
   ```

---

## Part 5: Submit a Request

### Step 5.1: Order the Catalog Item

1. On the "Database Access Request" form, fill in:
   | Variable | Value |
   |---|---|
   | Who needs this access? | Abel Tuter |
   | Which database? | Production Application Database |
   | What type of access? | Read-Only |
   | How long? | 1 Week |
   | Business justification | Need to investigate a data discrepancy reported by the QA team. Will be querying customer order tables for audit purposes. |

2. Click **Order Now**

### Step 5.2: Understand REQ / RITM / SCTASK

After submitting, ServiceNow creates a chain of records:

```
REQ (Request)             = The shopping cart / overall request
  └── RITM (Request Item) = Each item ordered
        └── SCTASK (Task) = Fulfillment tasks for teams to complete
```

1. After clicking "Order Now", you'll see a confirmation with the REQ number
2. Click the REQ number to open it
3. Look at the related lists:
   - **Requested Items** -- shows the RITM for "Database Access Request"
   - Click the RITM to open it
   - On the RITM, look for **Catalog Tasks** -- shows the SCTASK

### Step 5.3: Track the Request

1. Navigate to **Self-Service > My Requests** (or type `sc_request.list`)
2. Find your request
3. Open it and note the stages:
   ```
   Stage:       Waiting for Approval → Fulfillment → Complete → Closed
   ```

---

## Part 6: Configure Approvals

### Step 6.1: Add Approval to the Catalog Item

1. Open the "Database Access Request" catalog item (admin view)
2. Find the **Process Engine** or **Flow** tab
3. You have two options for approvals:

**Option A: Simple Approval (via Catalog Item settings)**
1. On the catalog item form, scroll to the **Process Engine** section
2. Look for **Flow** or **Workflow** field
3. You can select a pre-built approval flow

**Option B: Create Approval via Flow Designer (more control)**
We'll cover this in detail in Lab 15 (Flow Designer). For now, use the simpler approach.

### Step 6.2: Manual Approval Setup

If flow designer isn't configured yet, set up approvals manually:

1. Open your RITM (Request Item)
2. Look for the **Approval** tab or related list
3. Click **New** to add an approver:
   - Approver: Sanjay Manager
   - State: Requested
4. Save

### Step 6.3: Approve the Request

1. Impersonate **Sanjay Manager**
2. Navigate to **Self-Service > My Approvals**
3. Find the approval for the Database Access Request
4. Open it and click **Approve**
5. Stop impersonating

### Step 6.4: Fulfill the Request

1. As admin, open the RITM
2. The stage should now be **Fulfillment** (after approval)
3. Open the SCTASK (catalog task)
4. Assign it to a DBA group or user
5. Add work notes: "Database access provisioned for Abel Tuter. Read-only access to prod_app_db granted."
6. Change the SCTASK state to **Closed Complete**
7. Go back to the RITM -- it should now be closed/complete
8. Go back to the REQ -- it should also update

---

## Part 7: Create Another Catalog Item

### Step 7.1: Build a "New Laptop Request"

1. Create a new catalog item:
   | Field | Value |
   |---|---|
   | Name | New Laptop Request |
   | Category | Hardware (existing category) |
   | Short description | Request a new laptop for a team member |

2. Add variables:
   - **Laptop Type** (Select Box): Standard, Developer, Executive
   - **Operating System** (Radio): Windows 11, macOS
   - **Needed By** (Date): When the laptop is needed
   - **Employee Name** (Reference to sys_user): Who the laptop is for
   - **Special Requirements** (Multi Line Text): Any specific software or hardware needs

3. Preview and test by submitting a request

---

## Part 8: Variable Sets (Reusable Variable Groups)

### Step 8.1: Create a Variable Set

Variable sets let you reuse the same group of variables across multiple catalog items.

1. Navigate to **Service Catalog > Catalog Definitions > Variable Sets** (or type `item_option_new_set.list`)
2. Click **New**
3. Fill in:
   | Field | Value |
   |---|---|
   | Title | Standard Access Request Fields |
   | Internal name | standard_access_fields |
   | Type | Single Row |
4. Click **Submit**

5. Open the variable set
6. Add variables:
   - Justification (Multi Line Text, mandatory)
   - Duration (Select Box: 24h, 1 Week, 1 Month, Permanent)
   - Manager Approval Required (Yes/No, default: Yes)

### Step 8.2: Apply Variable Set to Catalog Items

1. Open any catalog item that needs these fields
2. Find the **Variable Sets** related list
3. Click **Edit** or **New**
4. Add "Standard Access Request Fields"
5. Save

Now those variables appear on the catalog item form without being redefined.

---

## Part 9: Practice Exercises

### Exercise 1: Build a Complete Catalog Item

Create a catalog item: **VPN Access Request**
- Category: IT Access Management
- Variables: User, VPN Profile (dropdown: Standard, Developer, Admin), Start Date, End Date, Justification
- Submit a request and walk through the full lifecycle: Order → Approve → Fulfill → Close

### Exercise 2: Multi-Item Request

1. Add 2 items to the cart (don't click "Order Now" -- click "Add to Cart" instead)
2. Go to the cart
3. Checkout with 2 items
4. Observe: 1 REQ is created with 2 RITMs

### Exercise 3: Request Tracking Dashboard

1. Create 5+ requests across different catalog items
2. Navigate to **Self-Service > My Requests**
3. Note the different stages and statuses
4. Try filtering: show only "Waiting for Approval" requests

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created catalog categories | Organized catalog for easy browsing |
| Built catalog items with variables | Self-service forms for users to request services |
| Submitted and tracked requests | REQ → RITM → SCTASK lifecycle |
| Configured approvals | Governance and authorization for service requests |
| Created variable sets | Reusable form fields across multiple items |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Catalog Item** | A requestable service or product in the service catalog |
| **Variable** | A form field on a catalog item (dropdown, text, reference, etc.) |
| **Variable Set** | Reusable group of variables shared across items |
| **REQ** | Request -- the overall order (shopping cart) |
| **RITM** | Request Item -- one specific item being requested |
| **SCTASK** | Catalog Task -- a fulfillment task assigned to a team |
| **Approval** | Authorization step before fulfillment begins |
| **Self-Service Portal** | User-facing catalog interface |

---

## What's Next

In **Lab 11**, you'll create a **Knowledge Base** with articles, categories, and approval workflows.
