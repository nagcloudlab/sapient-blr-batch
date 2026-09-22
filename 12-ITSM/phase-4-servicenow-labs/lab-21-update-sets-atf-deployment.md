# Lab 21: Update Sets, ATF & Deployment

**Level:** Expert | **Duration:** 90 minutes | **Prerequisites:** All previous labs completed

---

## Objective

By the end of this lab, you will:
- Capture configuration changes in Update Sets
- Preview, commit, and back out Update Sets
- Create and run Automated Test Framework (ATF) tests
- Understand the development-to-production deployment pipeline
- Follow best practices for managing ServiceNow across instances

---

## Part 1: Understanding Update Sets

### What Are Update Sets?

Update Sets capture **configuration changes** made in ServiceNow so they can be moved between instances.

```
Development Instance → (Update Set XML) → Test Instance → (Verified) → Production Instance

What Update Sets capture:
  ✅ Business Rules, Client Scripts, Script Includes
  ✅ UI Policies, UI Actions
  ✅ Flows, Subflows
  ✅ SLA Definitions, Notifications
  ✅ Form layouts, List layouts
  ✅ Catalog Items, Variables
  ✅ System Properties

What Update Sets do NOT capture:
  ❌ Data (incident records, user records, CI data)
  ❌ Attachments (by default)
  ❌ Scheduled Jobs (sometimes)
  ❌ Homepage configurations
```

---

## Part 2: Working with Update Sets

### Step 2.1: View the Current Update Set

1. Look at the top-right of the ServiceNow banner
2. You should see the current Update Set name (often "Default")
3. Click on it to see details or change it

### Step 2.2: Create a New Update Set

1. Navigate to **System Update Sets > Local Update Sets** (or type `sys_update_set.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | Lab Exercise Changes |
   | Description | Contains all configuration changes made during lab exercises including Business Rules, Client Scripts, UI Policies, and Service Catalog items. |
   | State | In Progress |
   | Application | Global |

4. Click **Submit**

### Step 2.3: Set as Current Update Set

1. Click on the Update Set picker in the top-right banner
2. Select **Lab Exercise Changes**
3. Alternatively: open the Update Set record and click **Make This My Current Set**

Now, all configuration changes you make will be tracked in this Update Set.

### Step 2.4: Make Changes and Track Them

1. Create a simple Business Rule:
   - Name: "Test BR for Update Set"
   - Table: Incident
   - When: before
   - Script: `gs.info('Update Set test');`
   - Submit

2. Create a UI Policy:
   - Name: "Test UI Policy for Update Set"
   - Table: Incident
   - Condition: Priority = 1
   - Submit

3. Now check what's been captured:
   - Open **Lab Exercise Changes** Update Set
   - Scroll to the **Customer Updates** related list
   - You should see your Business Rule and UI Policy listed
   ```
   Customer Updates:
   +------------------+-------------------+--------+
   | Name             | Type              | Action |
   +------------------+-------------------+--------+
   | Test BR for US   | Business Rule     | Insert |
   | Test UI Policy   | UI Policy         | Insert |
   +------------------+-------------------+--------+
   ```

### Step 2.5: Complete the Update Set

1. Open the Update Set
2. Change **State** to: **Complete**
3. Click **Update**
4. A completed Update Set can no longer receive new changes
5. It's now ready for export

### Step 2.6: Export the Update Set

1. Open the completed Update Set
2. Click **Export to XML** (related link)
3. A file downloads: `sys_update_set_xml_XXXXXXXX.xml`
4. This XML file contains all captured changes

---

## Part 3: Import and Commit Update Sets

### Step 3.1: Import an Update Set (Simulated)

In a real workflow, you'd import the XML to another instance. On your PDI, simulate:

1. Navigate to **System Update Sets > Retrieved Update Sets** (or type `sys_remote_update_set.list`)
2. Click **Import Update Set from XML**
3. Upload the XML file you exported
4. The Update Set appears in the Retrieved list

### Step 3.2: Preview the Update Set

1. Open the retrieved Update Set
2. Click **Preview**
3. Preview checks for:
   - **Conflicts** -- does this change something that already exists differently?
   - **Missing references** -- does it reference records that don't exist here?
   - **Collisions** -- will it overwrite something another Update Set changed?
4. Review the preview log for warnings or errors

### Step 3.3: Commit the Update Set

1. If preview shows no critical issues, click **Commit**
2. This applies all changes to the current instance
3. Verify: check that your Business Rule and UI Policy exist

### Step 3.4: Back Out an Update Set

If a committed Update Set caused problems:

1. Navigate to **System Update Sets > Local Update Sets**
2. Find the committed Update Set
3. Click **Back Out**
4. This reverses all changes made by the Update Set
5. Use this as a rollback mechanism

---

## Part 4: Update Set Best Practices

### Step 4.1: Naming Convention

```
Format: [Project/Feature]-[Description]-[Version]

Examples:
  ITSM-Incident-AutoAssignment-v1.0
  CATALOG-DatabaseAccessRequest-v1.2
  SLA-P1ResolutionTimer-v2.0
  INTEGRATION-MonitoringAPI-v1.0
```

### Step 4.2: One Feature Per Update Set

```
GOOD:
  Update Set 1: "Incident VIP Auto-Priority"
    - Business Rule: Auto-set VIP Priority
    - Client Script: Show VIP indicator
    - UI Policy: VIP mandatory fields

  Update Set 2: "SLA P1 Definitions"
    - SLA Definition: P1 Response
    - SLA Definition: P1 Resolution
    - Notification: P1 SLA Warning

BAD:
  Update Set: "All September Changes"
    - Mixed: Business Rules + SLAs + Catalog Items + Random fixes
    - Can't selectively deploy or roll back
```

### Step 4.3: Development Pipeline

```
Instance Strategy:

Developer PDI → Dev Instance → Test Instance → Production
     |              |              |               |
  Prototype    Integrate      Test/QA          Go Live
  & Learn      changes       with users        deploy

Update Set Flow:
  1. Developer creates Update Set in Dev
  2. Completes and exports XML
  3. Imports to Test instance
  4. Preview → fix conflicts → Commit
  5. QA team tests all changes
  6. If approved, import to Production
  7. Preview → Commit → Verify
```

---

## Part 5: Automated Test Framework (ATF)

### Step 5.1: What is ATF?

ATF lets you create automated tests for your ServiceNow configurations:
- Test Business Rules
- Test Client Scripts (with browser-based testing)
- Test Workflows and Flows
- Regression testing after upgrades

### Step 5.2: Create a Test

1. Navigate to **Automated Test Framework > Tests** (or type `sys_atf_test.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | Test: P1 Incident Auto-Assignment |
   | Description | Verify that P1 incidents are automatically assigned to the Critical Response team |
   | Active | Checked |

4. Click **Submit**

### Step 5.3: Add Test Steps

Open the test and add steps:

**Step 1: Impersonate a User**
1. Click **Add Test Step**
2. Select: **Server > Impersonate**
3. User: ITIL User (or any user with itil role)

**Step 2: Create a Record**
1. Add step: **Server > Create a Record**
2. Configure:
   | Field | Value |
   |---|---|
   | Table | Incident |
   | Fields | |
   | short_description | ATF Test - P1 Auto-Assignment |
   | caller_id | Abel Tuter |
   | impact | 1 |
   | urgency | 1 |
   | category | network |

**Step 3: Verify Field Value**
1. Add step: **Server > Field Values Validation**
2. Configure:
   | Field | Value |
   |---|---|
   | Table | Incident |
   | Record | (use the record from Step 2) |
   | Expected values | |
   | priority | 1 |
   | assignment_group | Network (or your auto-assigned group) |

**Step 4: Verify Work Note**
1. Add step: **Server > Record Validation**
2. Check that work_notes contains "Auto-assigned"

**Step 5: Cleanup -- Delete the Test Record**
1. Add step: **Server > Delete a Record**
2. Delete the incident created in Step 2

### Step 5.4: Run the Test

1. Click **Run Test** (top-right)
2. The test executes each step sequentially
3. Results show:
   ```
   Step 1: Impersonate ITIL User .............. PASS ✅
   Step 2: Create P1 Incident ................. PASS ✅
   Step 3: Verify Auto-Assignment ............. PASS ✅ (or FAIL ❌)
   Step 4: Verify Work Note ................... PASS ✅
   Step 5: Delete Test Record ................. PASS ✅

   Overall: PASS ✅
   ```
4. If a step fails, click on it for details (expected vs actual)

### Step 5.5: Create a Test Suite

A Test Suite groups multiple tests:

1. Navigate to **ATF > Test Suites** (or type `sys_atf_test_suite.list`)
2. Click **New**
3. Name: **ITSM Regression Suite**
4. Add tests:
   - Test: P1 Incident Auto-Assignment
   - Test: Resolution Notes Required on Close
   - Test: VIP Priority Escalation
   - Test: SLA Timer Start/Stop
5. Click **Run Suite**
6. All tests run in sequence; report shows pass/fail for each

---

## Part 6: Client-Side ATF Testing

### Step 6.1: Test Client Scripts

ATF can also test client-side behavior:

1. Create a new test: **Test: P1 Mandatory Fields UI Policy**
2. Add steps:

**Step 1: Open a Form**
- Step type: **Client > Open a Form**
- Table: Incident
- Record: (pick any incident)

**Step 2: Set Field Value**
- Step type: **Client > Set Field Value**
- Field: Priority
- Value: 1 - Critical

**Step 3: Verify Field Attribute**
- Step type: **Client > Field Attribute Validation**
- Field: Assignment group
- Attribute: Mandatory
- Expected: true

This validates that your UI Policy correctly makes Assignment Group mandatory for P1 incidents.

---

## Part 7: Deployment Checklist

### Step 7.1: Pre-Deployment Checklist

Before deploying changes to production:

```
☐ All changes captured in a named Update Set
☐ Update Set is complete (state = Complete)
☐ ATF tests pass in the development instance
☐ Update Set previewed in test instance (no critical conflicts)
☐ Update Set committed in test instance
☐ QA testing completed in test instance
☐ ATF tests pass in test instance
☐ Change Request created and approved for production deployment
☐ Rollback plan documented (back out Update Set)
☐ Deployment window scheduled
```

### Step 7.2: Post-Deployment Verification

```
☐ Update Set committed in production
☐ Run ATF regression suite in production
☐ Verify critical functionality manually
☐ Check system logs for errors
☐ Monitor for new incidents related to the changes
☐ Post-Implementation Review completed
☐ Change Request closed as Successful
```

---

## Part 8: Application Scope (Bonus)

### Step 8.1: What Are Scoped Applications?

Instead of Update Sets, modern ServiceNow development uses **Scoped Applications**:

```
Update Sets (traditional):
  - Global scope
  - Manual XML export/import
  - Conflict-prone in large teams

Scoped Applications (modern):
  - Isolated namespace
  - Source control integration (Git)
  - App Repository (store apps)
  - Team development support
  - Better dependency management
```

### Step 8.2: Create a Scoped Application

1. Navigate to **System Applications > Studio** (or type `studio`)
2. Click **Create Application**
3. Fill in:
   | Field | Value |
   |---|---|
   | Name | My ITSM Customizations |
   | Scope | x_myorg_itsm_custom |
4. Click **Create**
5. Studio opens -- you can create all artifacts (Business Rules, Scripts, etc.) within this application scope

---

## Part 9: Practice Exercises

### Exercise 1: Full Deployment Simulation

1. Create a new Update Set: "Incident-VIP-Enhancement-v1.0"
2. Make these changes (with the Update Set active):
   - Create a Business Rule for VIP handling
   - Create a UI Policy for VIP fields
   - Create a Client Script for VIP notification
3. Complete the Update Set
4. Export to XML
5. Create a NEW Update Set (different name)
6. Import the XML
7. Preview and commit
8. Verify all changes work

### Exercise 2: ATF Test Suite

Create ATF tests for:
1. Incident creation with correct priority calculation
2. Problem creation from an incident
3. Change request approval workflow
4. Service catalog item submission
5. SLA timer start and stop

Run all as a suite and document results.

### Exercise 3: Rollback Practice

1. Create an Update Set with a Business Rule
2. Commit it
3. Verify the Business Rule works
4. Back out the Update Set
5. Verify the Business Rule is gone (rolled back)

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created and managed Update Sets | Track and transport configuration changes |
| Exported/imported Update Sets | Move changes between instances |
| Previewed and resolved conflicts | Prevent deployment issues |
| Created ATF tests | Automated verification of configurations |
| Built test suites | Regression testing before deployments |
| Practiced deployment pipeline | Real-world DevOps for ServiceNow |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Update Set** | Container that captures configuration changes for transport |
| **Customer Update** | A single change tracked within an Update Set |
| **Preview** | Pre-deployment check for conflicts and missing references |
| **Commit** | Apply an Update Set's changes to the current instance |
| **Back Out** | Reverse all changes made by a committed Update Set |
| **ATF** | Automated Test Framework for creating and running tests |
| **Test Suite** | A collection of ATF tests run together |
| **Scoped Application** | Modern alternative to Update Sets with isolation and Git support |
| **Deployment Pipeline** | Dev → Test → Prod workflow for changes |

---

## Course Complete!

Congratulations -- you've completed all 21 labs, progressing from **zero to expertise** in ServiceNow!

### Your Journey:

```
Beginner (Labs 01-06):
  ✅ PDI setup, navigation, lists, forms
  ✅ Users, groups, roles, tables
  ✅ Filters, views, list controls

Intermediate (Labs 07-12):
  ✅ Incident Management (full lifecycle)
  ✅ Problem Management (RCA, known errors)
  ✅ Change Management (normal, standard, emergency)
  ✅ Service Catalog (items, variables, REQ/RITM/SCTASK)
  ✅ Knowledge Management (articles, lifecycle)
  ✅ CMDB (CIs, relationships, dependencies)

Advanced (Labs 13-18):
  ✅ SLAs & Notifications (timers, escalation, email)
  ✅ UI Policies & UI Actions (dynamic forms, buttons)
  ✅ Flow Designer (visual automation)
  ✅ Business Rules (server-side scripting)
  ✅ Client Scripts (browser-side scripting)
  ✅ Script Includes (reusable server code)

Expert (Labs 19-21):
  ✅ Reporting & Dashboards (charts, PA, executive views)
  ✅ REST API & Integrations (Table API, Scripted REST, Import Sets)
  ✅ Update Sets, ATF & Deployment (configuration management, testing)
```

### What's Next for You:

1. **Get Certified:** ServiceNow Certified System Administrator (CSA)
2. **Specialize:** ITSM, ITOM, ITAM, SecOps, HRSD, or CSM
3. **Build:** Create real applications on your PDI
4. **Contribute:** Join the ServiceNow Community and share knowledge
5. **Stay Current:** Each ServiceNow release (twice per year) brings new features
