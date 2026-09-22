# Lab 12: CMDB & Configuration Management

**Level:** Intermediate | **Duration:** 90 minutes | **Prerequisites:** Lab 07-11 completed

---

## Objective

By the end of this lab, you will:
- Understand the CMDB class hierarchy
- Create Configuration Items (CIs) manually
- Define relationships between CIs (dependency maps)
- Link CIs to incidents, changes, and problems
- Use the CMDB dependency view
- Understand CI lifecycle and attributes

---

## Part 1: Explore the CMDB

### Step 1.1: Browse CI Classes

1. Navigate to **Configuration > CI Class Manager** (or type `cmdb_ci.list`)
2. The CMDB is organized into a class hierarchy:

```
cmdb_ci (base class)
  ├── cmdb_ci_computer
  │   ├── cmdb_ci_server
  │   │   ├── cmdb_ci_linux_server
  │   │   ├── cmdb_ci_win_server
  │   │   └── cmdb_ci_unix_server
  │   └── cmdb_ci_pc_hardware
  ├── cmdb_ci_netgear (network devices)
  │   ├── cmdb_ci_ip_router
  │   ├── cmdb_ci_ip_switch
  │   └── cmdb_ci_ip_firewall
  ├── cmdb_ci_service
  │   ├── cmdb_ci_service_auto
  │   └── cmdb_ci_service_manual
  ├── cmdb_ci_appl (applications)
  │   ├── cmdb_ci_app_server
  │   └── cmdb_ci_db_instance
  └── cmdb_ci_storage_device
```

### Step 1.2: View Existing CIs

1. Navigate to **Configuration > Servers** (or type `cmdb_ci_server.list`)
2. Browse demo server CIs
3. Click on any server to see its attributes:
   ```
   Name:              web-server-01
   Class:             Linux Server
   Status:            Operational
   Environment:       Production
   IP Address:        10.0.1.50
   Operating System:  Ubuntu 22.04
   RAM:               16 GB
   CPU:               4 cores
   Location:          Data Center A
   Managed by:        Platform Engineering
   Supported by:      Platform Engineering
   ```

### Step 1.3: Browse Different CI Types

Try these navigation paths:
- **Configuration > Servers** → Server CIs
- **Configuration > Network > Routers** → Router CIs
- **Configuration > Applications** → Application CIs
- **Configuration > All** → All CIs regardless of type

---

## Part 2: Create Configuration Items

### Step 2.1: Create Server CIs

1. Navigate to **Configuration > Servers > Linux** (or `cmdb_ci_linux_server.do`)
2. Click **New**
3. Create these servers:

**Server 1: Web Application Server**
| Field | Value |
|---|---|
| Name | app-web-01 |
| Class | Linux Server |
| Status | Operational |
| Environment | Production |
| IP Address | 10.0.1.100 |
| Operating System | Ubuntu 22.04 LTS |
| RAM (MB) | 16384 |
| CPU count | 4 |
| Serial number | SRV-WEB-001 |
| Location | Data Center A |
| Managed by | Platform Engineering |
| Supported by | Platform Engineering |

Click **Submit**

**Server 2: Database Server**
| Field | Value |
|---|---|
| Name | db-primary-01 |
| Class | Linux Server |
| Status | Operational |
| Environment | Production |
| IP Address | 10.0.2.50 |
| Operating System | Ubuntu 22.04 LTS |
| RAM (MB) | 65536 |
| CPU count | 8 |
| Serial number | SRV-DB-001 |
| Location | Data Center A |
| Managed by | Database Team |
| Supported by | Database Team |

Click **Submit**

**Server 3: Mail Server**
| Field | Value |
|---|---|
| Name | mail-server-01 |
| Class | Linux Server |
| Status | Operational |
| Environment | Production |
| IP Address | 10.0.1.200 |
| Operating System | Ubuntu 22.04 LTS |
| RAM (MB) | 32768 |
| CPU count | 4 |
| Serial number | SRV-MAIL-001 |
| Location | Data Center A |

Click **Submit**

### Step 2.2: Create Application CIs

1. Navigate to **Configuration > Applications** (or `cmdb_ci_appl.do`)
2. Create:

**Application 1: Corporate Email Service**
| Field | Value |
|---|---|
| Name | Corporate Email Service |
| Class | Application |
| Status | Operational |
| Environment | Production |
| Version | 3.2 |
| Managed by | Software Team |

Click **Submit**

**Application 2: Internal Web Portal**
| Field | Value |
|---|---|
| Name | Internal Web Portal |
| Class | Application |
| Status | Operational |
| Version | 2.5 |
| Managed by | Platform Engineering |

Click **Submit**

### Step 2.3: Create a Business Service CI

1. Navigate to **Configuration > Business Services** (or `cmdb_ci_service.do`)
2. Create:

| Field | Value |
|---|---|
| Name | Email Service |
| Class | Business Service |
| Status | Operational |
| Environment | Production |
| Service classification | Business Service |
| Managed by | IT Management |

Click **Submit**

---

## Part 3: Create Relationships Between CIs

### Step 3.1: Understand Relationship Types

| Relationship | Meaning | Example |
|---|---|---|
| **Runs on** | Application runs on server | Email App runs on mail-server-01 |
| **Depends on** | CI depends on another CI | Web Portal depends on db-primary-01 |
| **Used by** | Reverse of "Depends on" | db-primary-01 is used by Web Portal |
| **Hosted on** | Virtual resource hosted on physical | VM hosted on Physical Server |
| **Contains** | Parent-child containment | Rack contains servers |
| **Connected to** | Network connectivity | Server connected to switch |

### Step 3.2: Add Relationships

1. Open the CI: **Corporate Email Service** (application)
2. Scroll to the **Relations** or **CI Relationships** related list
3. Click **New**
4. Add relationship:
   | Field | Value |
   |---|---|
   | Parent | Corporate Email Service |
   | Type | Runs on::Runs |
   | Child | mail-server-01 |
5. Click **Submit**

6. Add another relationship:
   | Field | Value |
   |---|---|
   | Parent | Email Service (business service) |
   | Type | Depends on::Used by |
   | Child | Corporate Email Service |

7. Add more relationships to build a dependency chain:

```
Email Service (Business Service)
  └── depends on → Corporate Email Service (Application)
        └── runs on → mail-server-01 (Server)
              └── depends on → db-primary-01 (Database Server)

Internal Web Portal (Application)
  ├── runs on → app-web-01 (Server)
  └── depends on → db-primary-01 (Database Server)
```

### Step 3.3: Create All Relationships

Add relationships so the full dependency looks like:

| Parent CI | Relationship | Child CI |
|---|---|---|
| Email Service | Depends on | Corporate Email Service |
| Corporate Email Service | Runs on | mail-server-01 |
| Corporate Email Service | Depends on | db-primary-01 |
| Internal Web Portal | Runs on | app-web-01 |
| Internal Web Portal | Depends on | db-primary-01 |
| app-web-01 | Connected to | (a network switch, if you created one) |

---

## Part 4: Dependency Views

### Step 4.1: View CI Dependencies

1. Open any CI (e.g., **Email Service**)
2. Look for a **Dependency Views** or **View Map** button/related link
3. Click it to see a graphical dependency map:

```
       Email Service
            |
            v
   Corporate Email Service
       |            |
       v            v
 mail-server-01   db-primary-01
                       ^
                       |
              Internal Web Portal
                       |
                       v
                  app-web-01
```

4. This visualization shows:
   - **Upstream** dependencies (what does this CI depend on?)
   - **Downstream** dependents (what depends on this CI?)

### Step 4.2: Impact Analysis

From the dependency view:
1. Click on **db-primary-01**
2. The view shows everything that depends on this database server:
   - Corporate Email Service
   - Internal Web Portal
   - And transitively: Email Service (business service)
3. This means: **if db-primary-01 goes down, both Email and Web Portal are affected**
4. This is critical for incident impact assessment

---

## Part 5: Link CIs to ITSM Records

### Step 5.1: Link CI to an Incident

1. Navigate to **Incident > Create New**
2. Create an incident:
   | Field | Value |
   |---|---|
   | Short description | Email service slow - high latency |
   | Configuration item | Corporate Email Service (search and select) |
   | Category | Software |
   | Impact | 2 - Medium |
   | Urgency | 2 - Medium |
3. Click **Submit**

Now the incident is linked to the CI. From the CI's page, you can see all related incidents.

### Step 5.2: Link CI to a Change

1. Open a change request (or create a new one)
2. Set the **Configuration item** field to: **mail-server-01**
3. This shows which CI is being changed
4. From the CI, you can see all changes that affect it

### Step 5.3: View a CI's Related Records

1. Open the CI: **mail-server-01**
2. Scroll down to related lists:
   - **Incidents** -- all incidents affecting this CI
   - **Changes** -- all changes to this CI
   - **Problems** -- all problems related to this CI
   - **Relationships** -- all CI relationships
3. This single view shows the complete operational picture of a CI

---

## Part 6: CI Lifecycle and Attributes

### Step 6.1: CI Status Values

| Status | Meaning |
|---|---|
| **Operational** | CI is live and in use |
| **Non-Operational** | CI exists but is not currently active |
| **Repair in Progress** | CI is being repaired/maintained |
| **DR Standby** | Disaster recovery standby |
| **Retired** | CI has been decommissioned |
| **Stolen** | CI has been stolen (for assets) |
| **Absent** | CI location unknown |

### Step 6.2: Update CI Status

1. Open **mail-server-01**
2. Change Status to: **Repair in Progress** (simulating maintenance)
3. Add work notes explaining the maintenance
4. Click **Update**
5. Change it back to **Operational** after "maintenance"

### Step 6.3: CI Audit History

1. Open any CI
2. Look for an **Audit** or **History** related list
3. This shows all changes made to the CI record:
   - Who changed what field
   - When it was changed
   - Old value → New value

---

## Part 7: Practice Exercises

### Exercise 1: Build a Full Application Stack

Create CIs and relationships for a web application stack:

```
Business Service: Customer Portal
  └── Application: Customer Portal App (v4.2)
        ├── runs on → web-server-01 (Linux Server)
        ├── runs on → web-server-02 (Linux Server) [redundancy]
        ├── depends on → api-gateway-01 (Application)
        │     └── runs on → app-server-01 (Linux Server)
        └── depends on → customer-db (Database Instance)
              └── runs on → db-server-01 (Linux Server)
```

### Exercise 2: Impact Scenario

Using the CIs you created:
1. Simulate: **db-primary-01** has a hardware failure
2. Open db-primary-01's dependency view
3. List all CIs and services impacted
4. Create a P1 incident linked to db-primary-01
5. In the incident, document all affected services in the description

### Exercise 3: CMDB Report

1. Navigate to `cmdb_ci.list` (all CIs)
2. Filter to show only CIs where Status = Operational AND Environment = Production
3. Count by class: How many servers? Applications? Services?
4. Export the list to CSV

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created CIs across different classes | CMDB is the foundation of ITSM -- knowing what you have |
| Built relationships between CIs | Dependency maps enable impact analysis |
| Used dependency views | Visual understanding of how components connect |
| Linked CIs to incidents/changes | Connects operational events to infrastructure |
| Managed CI lifecycle | Track the state of every component |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Configuration Item (CI)** | Any component that needs to be managed to deliver an IT service |
| **CMDB** | Configuration Management Database -- stores all CIs and relationships |
| **CI Class** | Category/type of CI (server, application, network device, etc.) |
| **Relationship** | A defined connection between two CIs (depends on, runs on, etc.) |
| **Dependency Map** | Visual diagram showing upstream/downstream CI relationships |
| **Impact Analysis** | Using CMDB relationships to determine blast radius of an issue |
| **CI Lifecycle** | States a CI moves through: Operational → Repair → Retired |

---

## What's Next

Congratulations -- you've completed the **Intermediate** labs! You now know how to work with all core ITSM modules.

In **Lab 13**, you begin the **Advanced** labs, starting with **SLAs & Notifications** -- configuring time-based rules, escalation triggers, and automated alerts.
