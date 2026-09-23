# Lab 11: Knowledge Management

**Level:** Intermediate | **Duration:** 60 minutes | **Prerequisites:** Lab 07-10 completed

---

## Objective

By the end of this lab, you will:
- Create a Knowledge Base and categories
- Author knowledge articles with rich formatting
- Configure article lifecycle and approval workflows
- Attach KB articles to incidents
- Search and use the knowledge base effectively

---

## Part 1: Create a Knowledge Base

### Step 1.1: View Existing Knowledge Bases

1. Navigate to **Knowledge > Knowledge Bases** (or type `kb_knowledge_base.list`)
2. Browse existing knowledge bases (demo data)

### Step 1.2: Create a New Knowledge Base

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Title | IT Operations Knowledge Base |
   | Description | Central repository for IT operations procedures, troubleshooting guides, and known issue documentation. |
   | Owner | (select your admin user) |
   | Active | Checked |

3. Click **Submit**

---

## Part 2: Create Categories

### Step 2.1: Add Categories to Your Knowledge Base

1. Navigate to **Knowledge > Categories** (or type `kb_category.list`)
2. Click **New** for each category:

| Category Name | Parent | Description |
|---|---|---|
| Troubleshooting | (top level) | Step-by-step troubleshooting guides |
| How-To Guides | (top level) | Procedures and instructions |
| Known Issues | (top level) | Documented known issues and workarounds |
| FAQs | (top level) | Frequently asked questions |
| Network | Troubleshooting | Network-related troubleshooting |
| Email | Troubleshooting | Email service troubleshooting |
| VPN | Troubleshooting | VPN connection troubleshooting |

For each:
1. Set the **Knowledge base** to: "IT Operations Knowledge Base"
2. Click **Submit**

---

## Part 3: Author Knowledge Articles

### Step 3.1: Create a Troubleshooting Article

1. Navigate to **Knowledge > Create New** (or type `kb_knowledge.do`)
2. Fill in:

   | Field | Value |
   |---|---|
   | Knowledge base | IT Operations Knowledge Base |
   | Category | Email (under Troubleshooting) |
   | Short description | How to fix email sync issues on mobile devices |
   | Article type | How-To |

3. In the **Article body**, write:

   ```
   # Email Sync Issues on Mobile Devices

   ## Symptoms
   - Email not syncing on iPhone or Android
   - New emails not appearing on mobile
   - "Cannot connect to server" error on mobile email app

   ## Applies To
   - iPhone (iOS 15+)
   - Android (12+)
   - Microsoft Outlook mobile app
   - Native mail clients

   ## Resolution Steps

   ### Step 1: Check Network Connection
   1. Ensure WiFi or cellular data is active
   2. Try opening a website to confirm internet connectivity
   3. If no connection, troubleshoot network first

   ### Step 2: Verify Account Settings
   1. Go to Settings > Mail > Accounts
   2. Select your email account
   3. Verify server settings:
      - Incoming: mail.company.com (Port 993, SSL)
      - Outgoing: smtp.company.com (Port 587, TLS)

   ### Step 3: Remove and Re-add Account
   1. Go to Settings > Mail > Accounts
   2. Select the problematic account
   3. Tap "Delete Account"
   4. Re-add the account with correct credentials

   ### Step 4: Check Server Status
   1. Contact IT Service Desk to verify mail server status
   2. Check the IT Status Page: status.company.com

   ## Related Known Issues
   - KI-2026-045: Mail Server v3.2 memory leak (see PRB0040001)

   ## Contact
   If these steps don't resolve the issue, contact the Service Desk
   at ext. 5555 or create an incident.
   ```

4. Click **Submit**

### Step 3.2: Create a Known Issue Article

1. Navigate to **Knowledge > Create New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Knowledge base | IT Operations Knowledge Base |
   | Category | Known Issues |
   | Short description | Known Issue: Mail Server v3.2 Memory Leak |
   | Article type | Known Error |

3. Article body:

   ```
   # Known Issue: Mail Server v3.2 Memory Leak

   ## Issue ID: KI-2026-045
   ## Status: Workaround Available
   ## Related Problem: PRB0040001

   ## Summary
   Mail Server version 3.2 has a memory leak in the IMAP connection
   handler that causes the service to crash every 24-48 hours.

   ## Impact
   - Affects all organizations running Mail Server v3.2 with 1000+
     active mailboxes
   - Results in intermittent email service outages
   - Approximately 2,400 users affected in our environment

   ## Root Cause
   Vendor advisory SA-2026-045 confirms a memory leak in the IMAP
   connection handler. Memory grows by ~50MB/hour under normal load.

   ## Workaround
   Configure scheduled restarts of the mail service every 12 hours:
   - 2:00 AM: systemctl restart mailservice
   - 2:00 PM: systemctl restart mailservice

   ## Permanent Fix
   Upgrade to Mail Server v3.3 (Change Request CHG0030001 scheduled)

   ## Timeline
   - Sep 10: First incident reported
   - Sep 15: Root cause identified
   - Sep 17: Workaround implemented
   - Oct 5: Planned upgrade to v3.3
   ```

4. Click **Submit**

### Step 3.3: Create a How-To Article

1. Create another article:

   | Field | Value |
   |---|---|
   | Knowledge base | IT Operations Knowledge Base |
   | Category | How-To Guides |
   | Short description | How to reset your Active Directory password |

2. Write step-by-step instructions in the article body
3. Click **Submit**

---

## Part 4: Article Lifecycle

### Step 4.1: Article Workflow States

Knowledge articles go through a lifecycle:

```
Draft --> Review --> Published --> Retired/Archived
           |
        (Rejected --> back to Draft)
```

### Step 4.2: Publish an Article

1. Open one of your draft articles
2. Change **Workflow state** to: **Review** (or look for a **Publish** or **Submit for Review** button)
3. If an approval workflow is configured:
   - An approver reviews the article
   - If approved, state moves to **Published**
   - If rejected, state goes back to **Draft** with feedback
4. If no approval workflow, change state directly to **Published**
5. Click **Update**

### Step 4.3: Configure Article Approval

1. Navigate to **Knowledge > Administration > Knowledge Bases**
2. Open "IT Operations Knowledge Base"
3. Look for **Approval** settings:
   - Enable approval: Yes
   - Approver: (select a user or group, e.g., Meera Joshi)
4. Save

Now, when an author submits an article for review, the approver is notified.

### Step 4.4: Retire an Article

1. Open a published article
2. Change **Workflow state** to **Retired**
3. Set a **Valid to** date (expiration date)
4. Click **Update**
5. Retired articles are hidden from search results but preserved in the system

---

## Part 5: Using Knowledge in Incident Resolution

### Step 5.1: Search Knowledge from an Incident

1. Open any incident
2. Look for a **Knowledge** panel or icon on the incident form
3. ServiceNow auto-suggests KB articles based on the incident's:
   - Short description
   - Category
   - Keywords
4. If you see matching articles, click one to view it

### Step 5.2: Attach a KB Article to an Incident

1. Open an email-related incident
2. Find the Knowledge section
3. Search for your "email sync" article
4. Click to attach or link it to the incident
5. Add a work note: "Resolved using KB article: How to fix email sync issues on mobile devices"
6. Resolve the incident

### Step 5.3: Create an Article from an Incident

1. Open a resolved incident with useful resolution notes
2. Look for a **Create Knowledge** button or link
3. Click it -- a new KB article form opens pre-filled with incident information
4. Edit and enhance the article
5. Submit for review/publish

---

## Part 6: Knowledge Base Settings

### Step 6.1: Configure KB Properties

1. Navigate to **Knowledge > Administration > Properties** (or type `kb_properties`)
2. Key settings:

   | Property | Description | Recommended |
   |---|---|---|
   | Article rating | Allow users to rate articles | Enable |
   | Article feedback | Allow comments on articles | Enable |
   | Auto-suggest | Suggest articles when creating incidents | Enable |
   | Search behavior | Full-text search vs keyword match | Full-text |

### Step 6.2: Article Versioning

1. Open a published article
2. Click **Checkout** (or **Edit** if versioning is enabled)
3. Make changes to the article
4. Click **Publish** -- a new version is created
5. The previous version is preserved in version history

---

## Part 7: Practice Exercises

### Exercise 1: Build a Knowledge Category Tree

Create a complete category structure:
```
IT Operations Knowledge Base
  ├── Troubleshooting
  │   ├── Network
  │   ├── Email
  │   ├── VPN
  │   └── Printing
  ├── How-To Guides
  │   ├── Account Management
  │   ├── Software Installation
  │   └── Remote Access
  ├── Known Issues
  └── FAQs
```

### Exercise 2: Create 5 Articles

Write articles for each category:
1. Troubleshooting: "VPN connection drops every 10 minutes"
2. How-To: "How to install approved software from the Software Center"
3. Known Issue: "WiFi instability on Floor 3 (firmware bug)"
4. FAQ: "How do I request a new laptop?"
5. How-To: "How to set up VPN on a personal device"

### Exercise 3: Knowledge-Driven Incident Resolution

1. Create 3 incidents with symptoms matching your KB articles
2. For each incident, use the knowledge panel to find matching articles
3. Resolve each incident by referencing the KB article
4. Track: How much faster is resolution when a KB article exists?

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created knowledge base and categories | Organized knowledge repository |
| Authored articles with rich content | Reusable troubleshooting and procedural guides |
| Configured article lifecycle | Quality control through review and approval |
| Linked KB to incidents | Faster incident resolution using existing knowledge |
| Created articles from incidents | Capture tribal knowledge for future use |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Knowledge Base** | A container for a collection of knowledge articles |
| **Category** | Organizational grouping within a knowledge base |
| **Article** | A document containing troubleshooting, how-to, or reference information |
| **Workflow State** | Article lifecycle: Draft → Review → Published → Retired |
| **Article Versioning** | Tracking changes across multiple versions of an article |
| **Knowledge-Centered Service** | Practice of capturing and reusing knowledge during incident resolution |

---

## What's Next

In **Lab 12**, you'll work with **CMDB** -- creating configuration items, defining relationships, and visualizing dependencies.
