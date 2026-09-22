# Lab 08: Problem Management

**Level:** Intermediate | **Duration:** 60 minutes | **Prerequisites:** Lab 07 completed

---

## Objective

By the end of this lab, you will:
- Create problems manually and from incidents
- Link multiple incidents to a problem
- Perform Root Cause Analysis (RCA) and document findings
- Create Known Error records
- Manage the problem lifecycle

---

## Part 1: Understanding Problems vs Incidents

```
Incident = "Something is broken RIGHT NOW. Fix it fast."
Problem  = "WHY does it keep breaking? Find the root cause."

Example:
  Incident INC001: "Email down for Marketing team" → Fix: restart mail server
  Incident INC005: "Email down for Sales team" → Fix: restart mail server
  Incident INC009: "Email down again - HR team" → Fix: restart mail server

  Problem PRB001: "Mail server crashes repeatedly"
  Root Cause: "Memory leak in mail service version 3.2"
  Fix: "Upgrade to version 3.3" → Creates a Change Request
```

---

## Part 2: Create a Problem

### Step 2.1: Create a Problem Manually

1. Navigate to **Problem > Create New** (or type `problem.do` in Filter Navigator)
2. Fill in the form:

   | Field | Value |
   |---|---|
   | Short description | Recurring email service outages |
   | Description | Multiple incidents reported over the past week for email service going down. Each time, restarting the mail server temporarily fixes the issue, but it recurs within 24-48 hours. |
   | Category | Software |
   | Subcategory | Email |
   | Impact | 2 - Medium |
   | Urgency | 2 - Medium |
   | Assignment group | Software (or Service Desk) |
   | Assigned to | (pick a user) |

3. Click **Submit**
4. Note the problem number (e.g., PRB0040001)

### Step 2.2: Create a Problem from an Incident

1. Navigate to **Incident > All**
2. Open one of the email-related incidents you created in Lab 07
3. Look for a **Create Problem** button or related link on the form
4. Click it
5. A new problem form opens pre-filled with information from the incident:
   - Short description copied from incident
   - Category/subcategory copied
   - The incident is automatically linked
6. Modify the short description to be more generic: "Root cause investigation - email service failures"
7. Click **Submit**

---

## Part 3: Link Incidents to Problems

### Step 3.1: Link Existing Incidents

1. Open the problem you created (PRB0040001)
2. Scroll down to the **Related Incidents** related list
3. Click **Edit** or **Add**
4. Search for and add 2-3 incidents that are related to email issues
5. Click **Save**

### Step 3.2: Verify Incident-Problem Link

1. Open one of the linked incidents
2. Find the **Problem** field on the incident form
3. It should now show the problem number (PRB0040001)
4. This two-way link means:
   - From the problem, you can see all affected incidents
   - From any incident, you can see the related problem

### Step 3.3: Impact Assessment

On the problem form, note:
- How many incidents are linked? This shows the **impact** of the problem
- What users/groups are affected? This helps prioritize the investigation

---

## Part 4: Root Cause Analysis (RCA)

### Step 4.1: Investigation Phase

1. Open the problem
2. Change **State** to: **Open** (or **Assess** depending on your version)
3. Add a **Work note**:
   ```
   Starting root cause investigation.

   Investigation plan:
   1. Review mail server logs for crash patterns
   2. Check memory and CPU utilization trends
   3. Review recent changes to the mail server
   4. Check vendor advisories for known issues
   ```
4. Click **Update**

### Step 4.2: Document the Investigation

1. Reopen the problem
2. Add another work note:
   ```
   Investigation findings:

   1. Mail server logs show OutOfMemoryError at the time of each crash
   2. Memory utilization graph shows steady increase over 24-48 hours
      until the server runs out of heap space and crashes
   3. Change log shows mail server was upgraded to v3.2 two weeks ago
      -- this is when the incidents started
   4. Vendor advisory SA-2026-045 confirms memory leak in v3.2
      affecting installations with >1000 mailboxes
   ```
3. Click **Update**

### Step 4.3: Document Root Cause

1. Reopen the problem
2. Find the **Root Cause** field (or **Cause Notes** / **RCA** section)
3. Enter:
   ```
   Root Cause: Memory leak in Mail Server version 3.2

   Details:
   - Vendor advisory SA-2026-045 confirms a memory leak in the IMAP
     connection handler introduced in version 3.2
   - Affects installations with more than 1000 active mailboxes
   - Memory consumption grows by approximately 50MB per hour under
     normal load, leading to OOM crash within 24-48 hours
   - Our installation has 2,400 mailboxes, well above the threshold

   Resolution path:
   - Short-term: Automated restart of mail service every 12 hours (workaround)
   - Long-term: Upgrade to Mail Server v3.3 which fixes the leak (permanent fix)
   ```
4. Click **Update**

### Step 4.4: Update Problem State

1. Change **State** to: **Root Cause Analysis** or **Known Error** (depending on version)
2. This indicates that the root cause has been identified
3. Click **Update**

---

## Part 5: Known Errors

### Step 5.1: Mark as Known Error

A **Known Error** = a problem with a documented root cause and a workaround or fix.

1. Open the problem
2. Check the **Known error** checkbox (or click **Mark as Known Error** button)
3. Fill in the **Workaround** field:
   ```
   Workaround: Configure a scheduled task to restart the mail service
   every 12 hours (at 2:00 AM and 2:00 PM). This prevents the memory
   from exceeding the threshold.

   Scheduled restart command: systemctl restart mailservice

   Note: This is a temporary workaround. The permanent fix is to
   upgrade to Mail Server v3.3 (Change Request to be created).
   ```
4. Click **Update**

### Step 5.2: Link to a Knowledge Article

1. Consider creating a Knowledge Article documenting this known error:
   - Navigate to **Knowledge > Create New**
   - Title: "Known Issue: Mail Server v3.2 Memory Leak"
   - Article body: Document the symptoms, root cause, and workaround
   - Submit the article

2. Link the KB article to the problem:
   - Open the problem
   - Find the related Knowledge section
   - Link the article

### Step 5.3: Known Error Database (KEDB)

1. Navigate to **Problem > Known Errors** (or filter problems where Known error = true)
2. This is the **Known Error Database** -- a list of all documented known errors
3. This is valuable because:
   - When a new incident comes in, agents can search KEDB for a matching workaround
   - Faster resolution: "We know about this issue. Here's the workaround."

---

## Part 6: Problem Resolution

### Step 6.1: Create a Fix Change

1. Open the problem
2. Look for a **Create Change** related link or button
3. Click it to create a change request:
   - Type: Normal
   - Short description: "Upgrade Mail Server from v3.2 to v3.3 to fix memory leak"
   - Justification: "Fixes memory leak causing recurring email outages (PRB0040001)"
4. Submit the change
5. The change is now linked to the problem

### Step 6.2: Resolve the Problem

After the change has been implemented:

1. Open the problem
2. Change **State** to: **Resolved** (or **Closed/Resolved**)
3. Fill in resolution fields:
   - **Fix notes**: "Upgraded Mail Server to v3.3. Memory leak fix confirmed by vendor. Monitoring shows stable memory usage over 72 hours post-upgrade."
   - **Resolution code**: Fix Applied
4. Click **Update**

### Step 6.3: Close Related Incidents

1. Open the problem
2. Review the **Related Incidents** list
3. For each related incident that's still open:
   - Open it
   - Change State to **Resolved**
   - Add resolution note: "Root cause identified and fixed via PRB0040001. Mail Server upgraded to v3.3."
   - Close it
4. Alternatively, some ServiceNow configurations allow **bulk-closing** related incidents from the problem

---

## Part 7: Problem Lifecycle Summary

```
Problem Lifecycle:

New --> Open/Assess --> Root Cause Analysis --> Known Error --> Resolved --> Closed
 |                           |                      |              |
 |                    (investigating)         (workaround    (permanent
 |                                            documented)    fix applied)
 |
 v
Closed (if determined to not be a real problem)
```

---

## Part 8: Practice Exercises

### Exercise 1: Network Problem

1. Create 3 incidents with similar symptoms:
   - "WiFi drops in Conference Room A"
   - "WiFi intermittent in Floor 3"
   - "Wireless connection unstable in cafeteria"
2. Create a problem: "Recurring WiFi instability across building"
3. Link all 3 incidents to the problem
4. Document RCA: "Wireless access points running firmware v2.1 have a known DHCP lease renewal bug"
5. Mark as Known Error with workaround: "Reset AP every 6 hours via scheduled task"
6. Create a change request to upgrade AP firmware

### Exercise 2: Problem from Pattern

1. Navigate to **Incident > All**
2. Filter: Category = Software AND Subcategory = Email
3. Look for patterns -- are multiple incidents about similar issues?
4. If yes, create a problem to investigate the pattern
5. Document your investigation steps

### Exercise 3: Known Error Search

1. Create 2-3 problems and mark them as Known Errors
2. Navigate to the Known Error list
3. Practice searching the KEDB by keyword
4. Simulate: a new incident comes in about "email not working"
5. Search the KEDB -- find the matching known error
6. Link the new incident to the existing problem

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created problems manually and from incidents | Problems capture the "why" behind recurring incidents |
| Linked incidents to problems | Shows impact and prevents duplicate investigations |
| Documented Root Cause Analysis | Structured RCA process for permanent fixes |
| Created Known Errors | Enables faster resolution of future incidents |
| Linked problems to changes | Connects the fix to the investigation |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Problem** | The underlying root cause of one or more incidents |
| **Root Cause Analysis (RCA)** | Investigation process to find why incidents occur |
| **Known Error** | A problem with documented root cause and workaround |
| **KEDB** | Known Error Database -- searchable list of documented known errors |
| **Workaround** | Temporary fix that reduces incident impact until permanent fix |
| **Fix** | Permanent resolution, typically implemented via a Change Request |

---

## What's Next

In **Lab 09**, you'll work with **Change Management** -- creating normal, standard, and emergency changes, going through CAB approval, and using the change calendar.
