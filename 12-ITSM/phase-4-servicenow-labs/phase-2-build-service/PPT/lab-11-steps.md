# Lab 11: Service Catalog & Request Management -- Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-11-service-catalog-request-management.md`

---

## Pre-check

- [ ] Labs 07-10 done (users ravi.kumar, amit.verma, priya.sharma, meera.joshi, sanjay.mgr exist)
- [ ] Groups exist: Platform Engineering, NOC, Service Desk
- [ ] UPI Operations Knowledge Base exists (Lab 10)
- [ ] Logged into PDI as admin

---

## Step 1: Verify the Default Service Catalog

Navigate: **Service Catalog > Catalog Definitions > Maintain Catalogs**

Open the **Service Catalog** record. Confirm it is **Active**. Note the sys_id.

---

## Step 2: Create Parent Category -- "UPI Platform Services"

Navigate: **Service Catalog > Catalog Definitions > Maintain Categories** > **New**

| Field | Value |
|-------|-------|
| Title | UPI Platform Services |
| Catalog | Service Catalog |
| Description | Self-service catalog for NPCI UPI Payment Platform. Request access, onboarding, infrastructure, and compliance services. |
| Active | Checked |
| Parent | (leave empty -- top-level category) |

> Submit.

---

## Step 3: Create 5 Sub-Categories

Navigate: **Maintain Categories** > **New** for each:

| # | Title | Parent | Description |
|---|-------|--------|-------------|
| 1 | Access & Onboarding | UPI Platform Services | Request access to systems, APIs, and onboard new team members or merchants |
| 2 | Merchant Services | UPI Platform Services | Merchant onboarding, configuration, and lifecycle management |
| 3 | Report an Issue | UPI Platform Services | Report payment issues, settlement discrepancies, and system problems |
| 4 | Infrastructure Requests | UPI Platform Services | Request new environments, infrastructure changes, and resource provisioning |
| 5 | Compliance & Security | UPI Platform Services | Request compliance audit reports, security reviews, and regulatory documentation |

All: **Catalog** = Service Catalog, **Active** = Checked.

---

## Checkpoint A

Navigate: **Maintain Categories** > filter: Parent = UPI Platform Services

Expected: **5 sub-categories**. Plus the parent = **6 total**.

---

## Step 4: Create Catalog Item -- "Request Merchant Onboarding"

### 4.1: Create the Item

Navigate: **Service Catalog > Catalog Definitions > Maintain Items** > **New**

| Field | Value |
|-------|-------|
| Name | Request Merchant Onboarding |
| Catalogs | Service Catalog |
| Category | Merchant Services |
| Short description | Request onboarding of a new merchant to the UPI payment platform |
| Description | Use this form to request merchant onboarding to the NPCI UPI Payment Platform. Includes document verification, technical configuration, and sandbox testing. Expected: 5 business days. |
| Delivery time | 5 Days |
| Active | Checked |

> Submit, then reopen the record.

### 4.2: Add 6 Variables

Open the catalog item > scroll to **Variables** related list > **New** for each:

**Variable 1: Merchant Name**

| Field | Value |
|-------|-------|
| Type | Single Line Text |
| Order | 100 |
| Question | Merchant Name |
| Name | merchant_name |
| Mandatory | Checked |

**Variable 2: Business Type**

| Field | Value |
|-------|-------|
| Type | Select Box |
| Order | 200 |
| Question | Business Type |
| Name | business_type |
| Mandatory | Checked |

After submit, reopen and add **Question Choices**:

| Text | Value | Order |
|------|-------|-------|
| Retail | retail | 100 |
| E-commerce | ecommerce | 200 |
| Government | government | 300 |
| Education | education | 400 |

**Variable 3: Merchant ID**

| Field | Value |
|-------|-------|
| Type | Single Line Text |
| Order | 300 |
| Question | Merchant ID |
| Name | merchant_id |
| Mandatory | Checked |

**Variable 4: Integration Type**

| Field | Value |
|-------|-------|
| Type | Select Box |
| Order | 400 |
| Question | Integration Type |
| Name | integration_type |
| Mandatory | Checked |

Question Choices: SDK (sdk, 100), API (api, 200), Plugin (plugin, 300)

**Variable 5: Expected TPS**

| Field | Value |
|-------|-------|
| Type | Integer |
| Order | 500 |
| Question | Expected TPS (Transactions Per Second) |
| Name | expected_tps |
| Mandatory | Checked |

**Variable 6: Go-live Date**

| Field | Value |
|-------|-------|
| Type | Date |
| Order | 600 |
| Question | Planned Go-live Date |
| Name | golive_date |
| Mandatory | Checked |

---

## Step 5: Create Catalog Item -- "Request API Access"

Navigate: **Maintain Items** > **New**

| Field | Value |
|-------|-------|
| Name | Request API Access |
| Catalogs | Service Catalog |
| Category | Access & Onboarding |
| Short description | Request access credentials for UPI platform APIs |
| Delivery time | 2 Days |
| Active | Checked |

> Submit and reopen. Add 4 variables:

| # | Type | Order | Question | Name | Mandatory |
|---|------|-------|----------|------|-----------|
| 1 | Select Box | 100 | API Name | api_name | Yes |
| 2 | Select Box | 200 | Target Environment | target_environment | Yes |
| 3 | Multi Line Text | 300 | Purpose / Use Case | purpose | Yes |
| 4 | Reference | 400 | Requestor Team | requestor_team | Yes |

Variable 1 choices: Transaction API (transaction), Settlement API (settlement), Dispute API (dispute), Reporting API (reporting)

Variable 2 choices: Sandbox (sandbox), UAT (uat), Production (production)

Variable 4: **Reference** = Group (sys_user_group)

---

## Step 6: Create Catalog Item -- "Request Compliance Audit Report"

Navigate: **Maintain Items** > **New**

| Field | Value |
|-------|-------|
| Name | Request Compliance Audit Report |
| Catalogs | Service Catalog |
| Category | Compliance & Security |
| Short description | Request generation of a compliance audit report |
| Delivery time | 3 Days |
| Active | Checked |

> Submit and reopen. Add 4 variables:

| # | Type | Order | Question | Name | Mandatory |
|---|------|-------|----------|------|-----------|
| 1 | Select Box | 100 | Audit Framework | audit_type | Yes |
| 2 | Date | 200 | Audit Period Start Date | audit_from_date | Yes |
| 3 | Date | 300 | Audit Period End Date | audit_to_date | Yes |
| 4 | Multi Line Text | 400 | Audit Scope Description | audit_scope | Yes |

Variable 1 choices: PCI-DSS (pci_dss, 100), SOC 2 Type II (soc2, 200), RBI IT Framework (rbi_it, 300), ISO 27001 (iso27001, 400)

---

## Step 7: Create Catalog Item -- "Request Team Member Access"

Navigate: **Maintain Items** > **New**

| Field | Value |
|-------|-------|
| Name | Request Team Member Access |
| Catalogs | Service Catalog |
| Category | Access & Onboarding |
| Short description | Request system access or role assignment for a team member |
| Delivery time | 1 Day |
| Active | Checked |

> Submit and reopen. Add 4 variables:

| # | Type | Order | Question | Name | Mandatory |
|---|------|-------|----------|------|-----------|
| 1 | Reference | 100 | User Requiring Access | target_user | Yes |
| 2 | Select Box | 200 | Role Requested | role_requested | Yes |
| 3 | Select Box | 300 | Access Duration | access_duration | Yes |
| 4 | Reference | 400 | Approving Manager | approving_manager | Yes |

Variable 1: Reference = User (sys_user). Variable 4: Reference = User (sys_user).

Variable 2 choices: ITIL User (itil, 100), Admin (admin, 200), Approver (approver_user, 300)

Variable 3 choices: Permanent (permanent, 100), 30 Days (30_days, 200), 90 Days (90_days, 300)

---

## Checkpoint B

Navigate: **Maintain Items** > filter by Category starts with "UPI" or search for "Request"

Expected: **4 catalog items** created with variables.

---

## Step 8: Create Record Producer -- "Report UPI Payment Issue"

Navigate: **Service Catalog > Catalog Definitions > Record Producers** > **New**

| Field | Value |
|-------|-------|
| Name | Report UPI Payment Issue |
| Catalogs | Service Catalog |
| Category | Report an Issue |
| Table name | Incident (incident) |
| Short description | Report a UPI payment transaction issue for investigation |
| Active | Checked |

> Submit and reopen.

### 8.1: Add 5 Variables

| # | Type | Order | Question | Name | Mandatory |
|---|------|-------|----------|------|-----------|
| 1 | Single Line Text | 100 | UPI Transaction ID | transaction_id | Yes |
| 2 | Decimal | 200 | Transaction Amount (INR) | transaction_amount | Yes |
| 3 | Select Box | 300 | UPI Error Code | error_code | Yes |
| 4 | Date/Time | 400 | Transaction Timestamp | txn_timestamp | Yes |
| 5 | Single Line Text | 500 | Remitter Bank Name | bank_name | Yes |

Variable 3 choices:

| Text | Value | Order |
|------|-------|-------|
| U30 - Device fingerprint mismatch | u30 | 100 |
| U16 - Risk threshold exceeded | u16 | 200 |
| U28 - Transaction timed out | u28 | 300 |
| U09 - Duplicate request | u09 | 400 |
| U67 - Account frozen | u67 | 500 |
| U78 - PSP not available | u78 | 600 |
| U69 - NPCI system error | u69 | 700 |
| Other | other | 800 |

### 8.2: Add Record Producer Script

Open the Record Producer record. In the **Script** field, enter:

```javascript
current.category = 'software';
current.subcategory = 'UPI';
current.contact_type = 'self-service';
current.impact = 2;
current.urgency = 2;
current.assignment_group.setDisplayValue('Platform Engineering');
current.short_description = 'UPI Payment Issue - Transaction: ' + producer.transaction_id;

var desc = 'UPI Payment Issue Report\n';
desc += '========================\n';
desc += 'Transaction ID: ' + producer.transaction_id + '\n';
desc += 'Amount (INR): ' + producer.transaction_amount + '\n';
desc += 'Error Code: ' + producer.error_code + '\n';
desc += 'Timestamp: ' + producer.txn_timestamp + '\n';
desc += 'Remitter Bank: ' + producer.bank_name + '\n';
current.description = desc;
```

> Update.

---

## Checkpoint C

You should now have:
- 1 parent category + 5 sub-categories = **6 categories**
- 4 catalog items + 1 record producer = **5 requestable items**

---

## Step 9: Test -- Submit a Catalog Request

### 9.1: Impersonate and Order

1. Click user avatar (top right) > **Impersonate User** > search for **Priya Sharma**
2. Navigate: **Self-Service > Service Catalog**
3. Browse to **UPI Platform Services > Merchant Services**
4. Click **Request Merchant Onboarding**
5. Fill in the variables:

| Variable | Value |
|----------|-------|
| Merchant Name | QuickPay Solutions |
| Business Type | E-commerce |
| Merchant ID | MERCH-QPS-2024-001 |
| Integration Type | API |
| Expected TPS | 500 |
| Go-live Date | (pick a date 30 days from now) |

6. Click **Order Now**
7. Note the REQ number (e.g., REQ0010001)

### 9.2: Verify the REQ > RITM > SCTASK Chain

1. **Stop impersonating** (return to admin)
2. Navigate: `sc_request.list` > find the REQ
3. Open it > look at the **Requested Items** related list
4. Open the RITM > verify:
   - Variables are populated with the values you entered
   - State is Open or Approved
5. Check the **Catalog Tasks** related list on the RITM for SCTASKs

---

## Step 10: Test -- Record Producer (Creates Incident)

1. **Impersonate Amit Verma**
2. Navigate: **Self-Service > Service Catalog > UPI Platform Services > Report an Issue**
3. Click **Report UPI Payment Issue**
4. Fill in:

| Variable | Value |
|----------|-------|
| UPI Transaction ID | UPI202409151430ABCD |
| Transaction Amount (INR) | 15000.50 |
| UPI Error Code | U28 - Transaction timed out |
| Transaction Timestamp | (yesterday at 14:30) |
| Remitter Bank Name | State Bank of India |

5. Click **Submit**
6. **Observe:** You are redirected to an **Incident** record (not an RITM)
7. Verify on the Incident:
   - **Category:** Software
   - **Assignment group:** Platform Engineering
   - **Short description:** Contains "UPI Payment Issue - Transaction: UPI202409151430ABCD"
   - **Description:** Contains all variable values

> This demonstrates the key difference: Record Producer creates an Incident, not a Request.

---

## Step 11: Verify Catalog Structure

### 11.1: Browse the Catalog

Navigate: **Self-Service > Service Catalog** > click **UPI Platform Services**

Verify all 5 sub-categories appear with their items.

### 11.2: Check Tables

| Table | Navigate | Expected Count |
|-------|----------|---------------|
| sc_category | `sc_category.list` filter Title starts with "UPI" or parent = UPI Platform Services | 6 (1 parent + 5 sub) |
| sc_cat_item | `sc_cat_item.list` filter Category in UPI sub-categories | 4 items |
| sc_cat_item_producer | `sc_cat_item_producer.list` filter Name = Report UPI Payment Issue | 1 record producer |
| sc_request | `sc_request.list` | At least 1 REQ from testing |

---

## Quick Verification Checklist

- [ ] 1 parent category "UPI Platform Services" created
- [ ] 5 sub-categories created under parent
- [ ] Catalog item "Request Merchant Onboarding" with 6 variables
- [ ] Catalog item "Request API Access" with 4 variables
- [ ] Catalog item "Request Compliance Audit Report" with 4 variables
- [ ] Catalog item "Request Team Member Access" with 4 variables
- [ ] Record Producer "Report UPI Payment Issue" with 5 variables + script
- [ ] Test request submitted and REQ > RITM chain verified
- [ ] Record Producer creates an Incident (not RITM)
- [ ] Catalog browsable via Self-Service > Service Catalog

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run Scripts 1, 2, and 3 from the Appendix in `lab-11-service-catalog-request-management.md`. Script 1 creates categories, Script 2 creates catalog items with variables, Script 3 creates the Record Producer.

---

*For detailed ITIL theory, approval workflows, Catalog Client Scripts, UI Policies, variable sets, fulfillment tasks, and full end-to-end test walkthroughs, see the full lab doc.*
