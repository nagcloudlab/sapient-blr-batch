# Lab 09: SLA, SLO & SLI — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-09-sla-slo-sli-service-levels.md`

---

## Pre-check

- [ ] Labs 07-08 done (CMDB CIs + Business/Technical Services exist)
- [ ] Business Service "UPI Payment Processing" exists
- [ ] Users exist: Ravi Kumar, Priya Sharma, Sanjay Manager
- [ ] Group exists: Platform Engineering
- [ ] Logged into PDI as admin

---

## Step 1: Create 2 Schedules

### Schedule #1: NPCI 24x7 Critical Support

Navigate: **System Scheduler > Schedules** > **New**

| Field | Value |
|-------|-------|
| Name | NPCI 24x7 Critical Support |
| Time zone | Asia/Kolkata |
| Type | Standard |

> Save. Then add **7 Schedule Entries** (one per day):

| Entry Name | Type | Day | Start | End |
|------------|------|-----|-------|-----|
| Sunday | Time range | Sunday | 00:00:00 | 23:59:59 |
| Monday | Time range | Monday | 00:00:00 | 23:59:59 |
| Tuesday | Time range | Tuesday | 00:00:00 | 23:59:59 |
| Wednesday | Time range | Wednesday | 00:00:00 | 23:59:59 |
| Thursday | Time range | Thursday | 00:00:00 | 23:59:59 |
| Friday | Time range | Friday | 00:00:00 | 23:59:59 |
| Saturday | Time range | Saturday | 00:00:00 | 23:59:59 |

> Alternatively, use the built-in "24x7" schedule if available in your PDI.

---

### Schedule #2: NPCI Business Hours

Navigate: **System Scheduler > Schedules** > **New**

| Field | Value |
|-------|-------|
| Name | NPCI Business Hours |
| Time zone | Asia/Kolkata |
| Type | Standard |

> Save. Then add **6 Schedule Entries** (Mon-Sat, no Sunday):

| Entry Name | Type | Day | Start | End |
|------------|------|-----|-------|-----|
| Monday | Time range | Monday | 08:00:00 | 20:00:00 |
| Tuesday | Time range | Tuesday | 08:00:00 | 20:00:00 |
| Wednesday | Time range | Wednesday | 08:00:00 | 20:00:00 |
| Thursday | Time range | Thursday | 08:00:00 | 20:00:00 |
| Friday | Time range | Friday | 08:00:00 | 20:00:00 |
| Saturday | Time range | Saturday | 08:00:00 | 20:00:00 |

---

## Checkpoint

Navigate: `cmn_schedule.list` > filter: **Name starts with NPCI**

Expected: **2 schedules** — NPCI 24x7 Critical Support (7 entries), NPCI Business Hours (6 entries).

---

## Step 2: Create 7 SLA Definitions

Navigate: **Service Level Management > SLA > SLA Definitions** > **New** (create 7 records)

### SLA #1: P1 Critical Response (30 min)

| Field | Value |
|-------|-------|
| Name | NPCI UPI - P1 Critical Response |
| Type | SLA |
| Table | Incident [incident] |
| Duration | 30 Minutes |
| Schedule | 24x7 (or NPCI 24x7 Critical Support) |
| Timezone | Asia/Kolkata |
| Active | Checked |

**Start Conditions:** `Priority is 1 - Critical AND State is New`

**Pause Conditions:** `State is Awaiting User Info`

**Stop Conditions:** `State is In Progress OR State is Resolved OR State is Closed`

> Save.

---

### SLA #2: P1 Critical Resolution (1 hour)

| Field | Value |
|-------|-------|
| Name | NPCI UPI - P1 Critical Resolution |
| Type | SLA |
| Table | Incident [incident] |
| Duration | 1 Hour |
| Schedule | 24x7 (or NPCI 24x7 Critical Support) |
| Timezone | Asia/Kolkata |
| Active | Checked |

**Start Conditions:** `Priority is 1 - Critical AND State is In Progress`

**Pause Conditions:** `State is Awaiting User Info OR State is Awaiting Vendor`

**Stop Conditions:** `State is Resolved`

> Save.

---

### SLA #3: P2 High Response (1 hour)

| Field | Value |
|-------|-------|
| Name | NPCI UPI - P2 High Response |
| Type | SLA |
| Table | Incident [incident] |
| Duration | 1 Hour |
| Schedule | 24x7 (or NPCI 24x7 Critical Support) |
| Timezone | Asia/Kolkata |
| Active | Checked |

**Start Conditions:** `Priority is 2 - High AND State is New`

**Pause Conditions:** `State is Awaiting User Info`

**Stop Conditions:** `State is In Progress OR State is Resolved OR State is Closed`

> Save.

---

### SLA #4: P2 High Resolution (4 hours)

| Field | Value |
|-------|-------|
| Name | NPCI UPI - P2 High Resolution |
| Type | SLA |
| Table | Incident [incident] |
| Duration | 4 Hours |
| Schedule | 24x7 (or NPCI 24x7 Critical Support) |
| Timezone | Asia/Kolkata |
| Active | Checked |

**Start Conditions:** `Priority is 2 - High AND State is In Progress`

**Pause Conditions:** `State is Awaiting User Info OR State is Awaiting Vendor`

**Stop Conditions:** `State is Resolved`

> Save.

---

### SLA #5: P3 Moderate Response (4 hours)

| Field | Value |
|-------|-------|
| Name | NPCI UPI - P3 Moderate Response |
| Type | SLA |
| Table | Incident [incident] |
| Duration | 4 Hours |
| Schedule | NPCI Business Hours |
| Timezone | Asia/Kolkata |
| Active | Checked |

**Start Conditions:** `Priority is 3 - Moderate AND State is New`

**Pause Conditions:** `State is Awaiting User Info`

**Stop Conditions:** `State is In Progress OR State is Resolved OR State is Closed`

> Save.

---

### SLA #6: P3 Moderate Resolution (24 hours)

| Field | Value |
|-------|-------|
| Name | NPCI UPI - P3 Moderate Resolution |
| Type | SLA |
| Table | Incident [incident] |
| Duration | 24 Hours |
| Schedule | NPCI Business Hours |
| Timezone | Asia/Kolkata |
| Active | Checked |

**Start Conditions:** `Priority is 3 - Moderate AND State is In Progress`

**Pause Conditions:** `State is Awaiting User Info OR State is Awaiting Vendor`

**Stop Conditions:** `State is Resolved`

> Save.

---

### SLA #7: P4 Low Resolution (72 hours)

| Field | Value |
|-------|-------|
| Name | NPCI UPI - P4 Low Resolution |
| Type | SLA |
| Table | Incident [incident] |
| Duration | 72 Hours |
| Schedule | NPCI Business Hours |
| Timezone | Asia/Kolkata |
| Active | Checked |

**Start Conditions:** `Priority is 4 - Low AND State is In Progress`

**Pause Conditions:** `State is Awaiting User Info OR State is Awaiting Vendor`

**Stop Conditions:** `State is Resolved`

> Save.

---

## Checkpoint

Navigate: `contract_sla.list` > filter: **Name starts with NPCI UPI**

Expected: **7 SLA Definitions** — all Active = true.

| Priority | SLA Name | Duration | Schedule |
|----------|----------|----------|----------|
| P1 | P1 Critical Response | 30 min | 24x7 |
| P1 | P1 Critical Resolution | 1 hour | 24x7 |
| P2 | P2 High Response | 1 hour | 24x7 |
| P2 | P2 High Resolution | 4 hours | 24x7 |
| P3 | P3 Moderate Response | 4 hours | Business Hours |
| P3 | P3 Moderate Resolution | 24 hours | Business Hours |
| P4 | P4 Low Resolution | 72 hours | Business Hours |

---

## Step 3: Test SLA — Create a P1 Incident

Navigate: **Incident > Create New**

| Field | Value |
|-------|-------|
| Caller | Priya Sharma |
| Short description | UPI Real-time settlement failure -- all banks affected |
| Impact | 1 - High |
| Urgency | 1 - High |
| Priority | (auto: 1 - Critical) |
| Assignment Group | Platform Engineering |
| Configuration Item | UPI Settlement Service |
| Business Service | UPI Payment Processing |

> Click **Save** (stay on the form).

---

## Step 4: Verify SLA Auto-Attaches

1. Scroll down to **Task SLAs** related list
2. Expected: **1 Task SLA** record appears automatically

| SLA Definition | Stage | Planned End Time |
|---------------|-------|-----------------|
| NPCI UPI - P1 Critical Response | In Progress | (now + 30 min) |

> The Resolution SLA has NOT started yet (incident is still in New state).

---

## Step 5: Move to In Progress — Trigger Resolution SLA

1. Change **State** to `In Progress`
2. Set **Assigned to** to `Ravi Kumar`
3. Click **Save**

Check **Task SLAs** related list:

| SLA Definition | Stage |
|---------------|-------|
| NPCI UPI - P1 Critical Response | Achieved |
| NPCI UPI - P1 Critical Resolution | In Progress |

> Response SLA achieved (stop condition met). Resolution SLA clock now ticking (1 hour).

---

## Step 6: Pause the SLA

1. Change **State** to `Awaiting User Info`
2. Add Work note: "Requested transaction IDs from SBI"
3. Click **Save**

Check Resolution Task SLA: **Stage = Paused**, percentage stopped increasing.

---

## Step 7: Resume the SLA

1. Change **State** back to `In Progress`
2. Add Work note: "SBI provided transaction IDs. Resuming."
3. Click **Save**

Check Resolution Task SLA: **Stage = In Progress** (resumed), planned end time pushed forward.

---

## Step 8: Resolve the Incident — SLA Achieved

1. Change **State** to `Resolved`
2. Set **Close code** to `Solved (Permanently)`
3. Set **Close notes**: "Recycled stale DB connection pool. Reprocessed 50K pending transactions."
4. Click **Save**

Check **Task SLAs** related list:

| SLA Definition | Stage | Has Breached |
|---------------|-------|-------------|
| NPCI UPI - P1 Critical Response | Achieved | false |
| NPCI UPI - P1 Critical Resolution | Achieved | false |

---

## Step 9: Check Task SLA Record Details

1. Click on the Resolution Task SLA record
2. Verify these fields:
   - **Start time** — when incident moved to In Progress
   - **End time** — when incident was resolved
   - **Business elapsed percentage** — 100% (completed)
   - **Has breached** — false
   - **Pause duration** — shows time spent in Awaiting User Info

---

## Step 10: View SLA Timeline

1. On the incident form, look for the **SLA Timeline** visualization
2. Or click on a Task SLA record > **SLA Timeline** icon
3. Expected: color-coded bar showing elapsed (green), paused (flat), and completed status

---

## Checkpoint

Navigate: `task_sla.list` > filter: **Task = (your incident number)**

Expected: **2 Task SLA records** — both Stage = Achieved, Has Breached = false.

---

## Quick Verification Checklist

- [ ] 2 schedules created (24x7 + Business Hours)
- [ ] 7 SLA Definitions created in contract_sla (all Active)
- [ ] P1 test incident created
- [ ] Response SLA auto-attached when incident saved as New
- [ ] Resolution SLA started when moved to In Progress
- [ ] SLA paused when set to Awaiting User Info
- [ ] SLA resumed when set back to In Progress
- [ ] Both SLAs show Achieved after resolution
- [ ] Task SLA records visible with correct timestamps
- [ ] SLA Timeline visualization reviewed

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the script from Appendix A in `lab-09-sla-slo-sli-service-levels.md`. Creates all 7 SLA definitions programmatically.

---

*For detailed ITIL theory, SLO/SLI mapping, breach notifications, watermelon SLAs, and background script code, see the full lab doc.*
