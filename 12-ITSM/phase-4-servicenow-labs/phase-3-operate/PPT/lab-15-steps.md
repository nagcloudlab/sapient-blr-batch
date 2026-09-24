# Lab 15: Change Management — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-15-change-management.md`

---

## Pre-check

- [ ] Labs 12-14 done (Incidents, Problems exist; CMDB from Lab 07 populated)
- [ ] Users exist: ravi.kumar, amit.verma, priya.sharma, sanjay.mgr
- [ ] Groups exist: Platform Engineering, NOC
- [ ] Logged into PDI as admin

---

## Step 1: Create a Normal Change (PostgreSQL Separation)

This change addresses the SPOF finding from Lab 07 (both PostgreSQL instances on same DB Server 01) and the Problem from Lab 14.

Navigate: `change_request.do` > **New**

| Field | Value |
|-------|-------|
| Type | Normal |
| Short description | Separate PostgreSQL instances to dedicated servers — eliminate SPOF |
| Description | Move PostgreSQL Replica to a dedicated server (UPI DB Server 02) to eliminate the single point of failure identified in CMDB Lab 07. Both primary and replica currently run on UPI DB Server 01. Root cause contributor to Problem PRB from Lab 14. |
| Category | Hardware |
| Risk | High |
| Impact | 1 - High |
| Priority | 2 - High |
| Assignment group | Platform Engineering |
| Assigned to | Amit Verma |

Click **Submit**. Note the CHG number.

---

## Step 2: Fill in Planning Details

Open the Normal Change > navigate to **Planning** tab.

| Field | Value |
|-------|-------|
| Planned start date | (Next Sunday, 02:00 AM) |
| Planned end date | (Next Sunday, 06:00 AM) |
| Justification | Eliminate SPOF: both PostgreSQL Primary and Replica run on UPI DB Server 01. If the server fails, all UPI transaction and settlement data is lost. Identified in CMDB Lab 07 service map analysis. |

**Implementation plan** (paste into field):
```
1. Pre-implementation (02:00 AM):
   - Notify operations and NOC team
   - Full backup of PostgreSQL Primary and Replica
   - Provision UPI DB Server 02 (already staged)

2. Stop replication (02:30 AM):
   - Pause streaming replication on Replica
   - Verify Primary is unaffected

3. Migrate Replica to DB Server 02 (02:45 AM):
   - pg_basebackup from Primary to new server
   - Configure streaming replication to new host
   - Update connection strings in Settlement Service

4. Verify replication (03:30 AM):
   - Confirm replication lag < 1 second
   - Run read queries against new Replica
   - Verify Settlement Service connects to new Replica

5. Update CMDB (04:00 AM):
   - Change Replica "Runs on" relationship to DB Server 02
   - Update service map

6. Monitor (04:15 - 06:00 AM):
   - Watch replication lag, query latency, settlement processing
```

**Rollback plan** (paste into field):
```
1. Stop new Replica on DB Server 02
2. Restart original Replica on DB Server 01
3. Re-establish replication from Primary
4. Revert connection strings in Settlement Service
5. Estimated rollback time: 20 minutes
```

**Test plan** (paste into field):
```
1. Tested in staging with production-equivalent data volume
2. Replication established within 15 minutes
3. Read query performance identical on new server
4. Settlement batch processing verified against new Replica
5. Failover tested: promote Replica on DB Server 02 successfully
```

Click **Update**.

---

## Step 3: Add Affected CIs

Open the Normal Change > scroll to **Affected CIs** related list > click **Edit/Add**.

| CI to Add |
|-----------|
| UPI PostgreSQL Primary |
| UPI PostgreSQL Replica |
| UPI DB Server 01 |
| UPI Settlement Service |
| UPI Payment Platform |

Click **Save**.

---

## Step 4: Walk Normal Change Through All States

### 4a: New to Assess

1. Open the change
2. Click **Assess** (or set State = Assess)
3. Add work note: "Planning complete. Implementation, rollback, and test plans verified. All affected CIs identified. Submitting for CAB review."
4. Click **Update**

### 4b: Assess to Authorize

1. Click **Authorize** (or set State = Authorize)
2. Add work note: "Assessment complete. Risk: High (database migration). Submitting for CAB approval."
3. Click **Update**

### 4c: CAB Approval Simulation

**Add approver:**

1. Scroll to **Approvers** related list > click **New**
2. Approver: **Sanjay Manager**
3. State: Requested
4. Click **Save**

**Approve the change:**

1. Top-right User icon > **Impersonate User** > search **Sanjay Manager**
2. Navigate: `sysapproval_approver.list`
3. Find the approval for your Change > open it > click **Approve**
4. Top-right User icon > **End Impersonation** (back to admin)

### 4d: Authorize to Scheduled

1. Open the change (should show Approved)
2. Set State = **Scheduled**
3. Add work note: "CAB approved. Scheduled for Sunday maintenance window 02:00-06:00 AM."
4. Click **Update**

### 4e: Scheduled to Implement

1. Set State = **Implement**
2. Add work note:
   ```
   02:00 AM - Pre-implementation started
   - NOC team notified, dashboards active
   - Full PostgreSQL backup completed (Primary + Replica)
   - DB Server 02 provisioned and ready
   ```
3. Add another work note:
   ```
   03:30 AM - Migration complete
   - Replica running on DB Server 02
   - Replication lag: 0.3 seconds
   - Settlement Service connected to new Replica
   - All read queries responding normally
   ```
4. Click **Update**

### 4f: Implement to Review

1. Set State = **Review**
2. Add work note:
   ```
   06:00 AM - Monitoring period complete
   - Replication stable for 2 hours
   - Zero errors, zero failed transactions
   - CMDB updated: Replica now "Runs on" DB Server 02
   - SPOF eliminated — Primary and Replica on separate servers
   - Change declared SUCCESSFUL
   ```
3. Click **Update**

### 4g: Review to Closed

1. Set State = **Closed**
2. Close code: **Successful**
3. Close notes:
   ```
   PostgreSQL Replica successfully migrated to dedicated DB Server 02.
   - SPOF from Lab 07 CMDB analysis eliminated
   - Replication lag stable at < 0.5 seconds
   - Settlement Service verified on new Replica
   - CMDB relationships updated
   - Service map now shows proper server separation
   ```
4. Click **Update**

---

## Checkpoint

Navigate: `change_request.list` > find your Normal Change.

Expected: State = Closed, Close code = Successful. Check **Activity** tab for all work notes across state transitions.

---

## Step 5: Create a Standard Change (Certificate Renewal)

Navigate: `change_request.do` > **New**

| Field | Value |
|-------|-------|
| Type | Standard |
| Short description | Renew UPI payment gateway SSL certificate — quarterly rotation |
| Description | Standard pre-approved procedure: Renew SSL certificate for UPI payment gateway. Certificate expires in 30 days. Quarterly rotation per security policy. |
| Category | Network |
| Risk | Low |
| Impact | 3 - Low |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar |

**Implementation plan**:
```
1. Obtain new SSL certificate from internal CA
2. Install certificate on payment gateway (HAProxy)
3. Reload HAProxy configuration (zero-downtime reload)
4. Verify HTTPS handshake with openssl s_client
5. Update certificate expiry monitoring in Prometheus
```

**Rollback plan**: "Restore previous certificate from backup, reload HAProxy"

Click **Submit**.

**Walk through Standard Change lifecycle** (no CAB needed):

1. Open the Standard Change
2. Set State = **Scheduled** > add work note: "Pre-approved standard change. Scheduled for next maintenance window." > Update
3. Set State = **Implement** > add work note: "Certificate renewed and installed. HAProxy reloaded. HTTPS verified." > Update
4. Set State = **Review** > add work note: "Certificate valid for 90 days. Monitoring alert configured for 30-day warning." > Update
5. Set State = **Closed** > Close code: Successful > Close notes: "SSL certificate renewed. Next renewal due in 90 days." > Update

---

## Step 6: Create an Emergency Change (Security Patch)

Navigate: `change_request.do` > **New**

| Field | Value |
|-------|-------|
| Type | Emergency |
| Short description | EMERGENCY: Critical RCE vulnerability in UPI Transaction Service — CVE-2026-XXXX |
| Description | Remote Code Execution vulnerability discovered in Spring Boot dependency used by UPI Transaction Service. CVSS score 9.8. Active exploitation detected in the wild. Immediate patching required. Verbal approval from VP Engineering (Sanjay) at 10:15 PM. |
| Category | Software |
| Risk | High |
| Impact | 1 - High |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar |
| Justification | Critical security vulnerability with active exploitation. RCE allows unauthenticated remote attackers to execute arbitrary code. All UPI transaction data at risk. Verbal approval obtained from Sanjay Manager at 10:15 PM. |

Click **Submit**.

**Walk through Emergency Change lifecycle** (fast-track):

1. Set State = **Implement**
2. Add work note:
   ```
   10:30 PM - Emergency patching started
   - Updated Spring Boot dependency to patched version
   - Rolling restart of UPI Transaction Service (2 servers)
   - Verified vulnerability scan shows CVE-2026-XXXX resolved
   - Transaction processing restored and healthy at 10:50 PM
   ```
3. Set State = **Review**
4. Add work note:
   ```
   Post-implementation review:
   - Vulnerability patched within 35 minutes of approval
   - No service disruption during rolling restart
   - Action item: Add automated dependency vulnerability scanning to CI/CD
   - Action item: Create Standard Change template for dependency security patches
   ```
5. Set State = **Closed** > Close code: Successful > Update

---

## Step 7: Create a Failed Change with Rollback

Navigate: `change_request.do` > **New**

| Field | Value |
|-------|-------|
| Type | Normal |
| Short description | Upgrade UPI Settlement Service database connection pool from HikariCP 4 to 5 |
| Description | Upgrade HikariCP connection pool library to version 5 for improved performance and connection leak detection. |
| Category | Software |
| Risk | Moderate |
| Impact | 2 - Medium |
| Assignment group | Platform Engineering |
| Assigned to | Amit Verma |

Click **Submit**.

**Walk through states until failure:**

1. Set State = **Assess** > Update
2. Set State = **Authorize** > Update
3. Add approver (Sanjay Manager) > Impersonate > Approve > End impersonation
4. Set State = **Scheduled** > Update
5. Set State = **Implement**
6. Add work note:
   ```
   02:30 AM - Deployment started
   - HikariCP 5 deployed to Settlement Service
   - Service restarted successfully

   02:45 AM - FAILURE DETECTED
   - Connection pool exhaustion after 15 minutes
   - HikariCP 5 changed default maxLifetime behavior
   - Settlement batch jobs timing out
   - Error rate: 12% and climbing

   02:50 AM - INITIATING ROLLBACK
   - Reverting to HikariCP 4
   - Restarting Settlement Service

   03:00 AM - ROLLBACK COMPLETE
   - HikariCP 4 restored, connection pool stable
   - Settlement processing resumed normally
   - Error rate back to 0%
   ```
7. Click **Update**
8. Set State = **Review**
9. Add work note:
   ```
   Post-mortem: HikariCP 5 changed default maxLifetime from 30min to 10min.
   Our batch jobs run up to 20 minutes — connections were being killed mid-batch.
   Remediation: Update batch job configuration to use shorter-lived connections
   before re-attempting upgrade.
   ```
10. Set State = **Closed**
11. Close code: **Unsuccessful**
12. Close notes: "Rollback executed. HikariCP 5 incompatible with current batch job configuration. Remediation plan created." > Update

---

## Step 8: Change Calendar and Blackout Period

### 8a: View the Change Calendar

1. Navigate: **Change > Change Calendar** (or type `change_calendar`)
2. Verify your scheduled changes appear on the calendar
3. Click on any change to see details

### 8b: Create a Blackout Period

Navigate: **Change > Administration > Blackout Schedule** (or `change_blackout.list`) > **New**

| Field | Value |
|-------|-------|
| Name | UPI Year-End Settlement Freeze |
| Type | Blackout |
| Begin date | Dec 28, 2026 00:00 |
| End date | Jan 3, 2027 23:59 |
| Description | No changes permitted during year-end settlement reconciliation. UPI settlement volumes peak. Any failure impacts 350+ banks. |

Click **Submit**.

Create a second blackout:

| Field | Value |
|-------|-------|
| Name | Diwali Festival — Transaction Peak Freeze |
| Type | Blackout |
| Begin date | Oct 19, 2026 00:00 |
| End date | Oct 26, 2026 23:59 |
| Description | UPI transaction volumes surge 300-400% during Diwali. No changes permitted. All hands on monitoring. |

Click **Submit**.

---

## Quick Verification Checklist

- [ ] Normal Change created (PostgreSQL separation) and walked through all 7 states
- [ ] Affected CIs linked (5 CIs from CMDB Lab 07)
- [ ] CAB approval simulated via impersonation
- [ ] Standard Change created (certificate renewal) and closed successfully
- [ ] Emergency Change created (security patch) and closed successfully
- [ ] Failed Change created with rollback work notes, closed as Unsuccessful
- [ ] Change Calendar viewed with scheduled changes visible
- [ ] 2 Blackout periods created (Year-End, Diwali)

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the script from the Appendix in `lab-15-change-management.md`. Creates all change records with planning details pre-filled. You still need to walk through state transitions, CAB approval simulation, and blackout periods manually.

---

*For detailed ITIL theory, state flow diagrams, exercises, and background script code, see the full lab doc.*
