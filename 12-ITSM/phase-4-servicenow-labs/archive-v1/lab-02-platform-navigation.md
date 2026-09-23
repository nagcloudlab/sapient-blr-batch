# Lab 02: Platform Navigation

**Level:** Beginner | **Duration:** 45 minutes | **Prerequisites:** Lab 01 completed

---

## Objective

By the end of this lab, you will:
- Master the Application Navigator and Filter Navigator
- Use Favorites, History, and Tabs for efficient navigation
- Perform Global Search across the entire platform
- Customize your homepage
- Understand URL patterns for direct navigation

---

## Part 1: Application Navigator Deep Dive

### Step 1.1: Browse Applications

1. Log in to your PDI
2. Look at the **left sidebar** -- this is the Application Navigator
3. Scroll through and note the major application groups:
   ```
   Self-Service
   Incident
   Problem
   Change
   Service Catalog
   Configuration (CMDB)
   Knowledge
   Service Level Management
   System Administration
   System Definition
   System Security
   ...
   ```
4. Click the **arrow (>)** next to **Incident** to expand it
5. You'll see modules like: Create New, All, My Incidents, Open, etc.

### Step 1.2: Filter Navigator Techniques

The Filter Navigator (text box at top of left sidebar) supports several patterns:

| What You Type | What Happens |
|---|---|
| `incident` | Filters to show all modules containing "incident" |
| `incident.list` | Directly opens the Incident list view |
| `incident.do` | Opens a new/blank Incident form |
| `sys_user.list` | Opens the User list |
| `sys_properties.list` | Opens System Properties list |
| `nav_to.do?uri=incident.do` | Advanced direct URL navigation |

**Practice:**
1. Type `incident.list` and press **Enter** -- you go directly to the incident list
2. Clear it, type `problem.list` and press **Enter** -- you go to the problem list
3. Clear it, type `change` -- notice it filters the navigator (doesn't navigate)
4. Click **Change > All** from the filtered results

### Step 1.3: Using .do and .list Shortcuts

```
Pattern:          <table_name>.list     --> Opens list of all records
                  <table_name>.do       --> Opens a new/empty form
                  <table_name>.do?sys_id=<id>  --> Opens a specific record

Common shortcuts:
  incident.list          --> All incidents
  incident.do            --> New incident form
  sys_user.list          --> All users
  sys_user_group.list    --> All groups
  change_request.list    --> All changes
  sc_cat_item.list       --> All catalog items
  kb_knowledge.list      --> All KB articles
  cmdb_ci.list           --> All CIs
  task.list              --> All tasks (parent table)
```

**Practice:**
1. Type `sys_user_group.list` in Filter Navigator, press Enter
2. You should see a list of groups
3. Try `sc_cat_item.list` -- you'll see catalog items

---

## Part 2: Favorites

### Step 2.1: Add a Favorite

1. Navigate to **Incident > All** (type `incident` in Filter Navigator, click All)
2. In the content frame header, click the **star icon** (☆) next to "Incidents"
3. The star turns filled (★) -- this page is now a favorite
4. Alternatively: right-click on **Incident > All** in the navigator and select **Add to Favorites**

### Step 2.2: Add More Favorites

Add these as favorites (you'll use them frequently):
1. **Incident > All** (if not already done)
2. **Change > All**
3. **Problem > All**
4. **Service Catalog > Catalog Definitions > Maintain Items**
5. **System Definition > Tables**

### Step 2.3: Access Favorites

1. Click the **Favorites** icon (★) in the top banner
2. You'll see all your favorited modules
3. Click any favorite to navigate directly to it

### Step 2.4: Organize Favorites

1. Click the **Favorites** icon (★) in the banner
2. Click **Edit Favorites** (pencil icon or gear icon)
3. You can:
   - Reorder favorites (drag and drop)
   - Remove favorites (click X)
   - Create favorite groups/folders

---

## Part 3: History

### Step 3.1: View Navigation History

1. Click the **History** icon (⟲ clock icon) in the top banner
2. You'll see a list of recently visited pages
3. This shows your navigation history for the current session
4. Click any item to go back to that page

### Step 3.2: Practice Using History

1. Navigate to these pages in order:
   - Incident > All
   - Problem > All
   - Change > All
   - sys_user.list (type in Filter Navigator)
2. Now click the **History** icon
3. You should see all four pages listed
4. Click "All Incidents" in history to go back

---

## Part 4: Global Search

### Step 4.1: Basic Search

1. Click the **Search** icon (🔍) in the top banner (or press Ctrl+Alt+G)
2. Type: `email`
3. Press **Enter**
4. Results appear grouped by table:
   ```
   Incidents (3 results)
     - INC0000001: Unable to access email
     - ...
   Knowledge (2 results)
     - KB0000005: How to configure email
     - ...
   Users (5 results)
     - ...
   ```
5. Click any result to open that record

### Step 4.2: Search Specific Tables

1. Open Global Search
2. In the search bar, you can prefix with a table name:
   - Type: `incident: email` -- searches only the incident table
   - Type: `user: admin` -- searches only the user table
3. Try searching: `kb: password reset`

### Step 4.3: Search Tips

| Technique | Example | What It Does |
|---|---|---|
| Plain search | `network outage` | Searches across all tables |
| Table-scoped | `incident: network` | Searches only incidents |
| Wildcard | `net*` | Matches "network", "netflix", etc. |
| Exact phrase | `"network outage"` | Matches the exact phrase |

---

## Part 5: Tabs and Multi-Window

### Step 5.1: Working with Tabs (Next Experience)

In the Next Experience UI (modern ServiceNow):
1. Navigate to **Incident > All**
2. Open any incident by clicking its number
3. Notice a **tab** appears at the top of the content frame
4. Navigate to **Problem > All** -- another tab appears
5. You can switch between tabs without losing your place
6. Close a tab by clicking the **X** on it

### Step 5.2: Opening in New Tabs/Windows

1. Navigate to **Incident > All**
2. **Right-click** on any incident number
3. Select **Open in new tab** (browser tab)
4. This is useful when you need to compare records or work on multiple things

---

## Part 6: URL Patterns

### Step 6.1: Understanding ServiceNow URLs

Every page in ServiceNow has a predictable URL pattern:

```
Base URL: https://devXXXXXX.service-now.com

List view:
  /incident_list.do                    --> All incidents (old UI)
  /now/nav/ui/classic/params/target/incident_list.do  --> (Next Experience)

Form view:
  /incident.do?sys_id=abc123           --> Specific incident record

Direct navigation:
  /nav_to.do?uri=incident.list         --> Navigate to incident list
  /nav_to.do?uri=sys_user.list         --> Navigate to user list

System pages:
  /stats.do                            --> Instance statistics
  /cache.do                            --> Cache management
  /xmlstats.do                         --> XML statistics
```

### Step 6.2: Practice URL Navigation

1. In your browser address bar, append to your instance URL:
   - `/stats.do` -- view instance stats
   - `/nav_to.do?uri=incident.list` -- go to incident list
   - `/nav_to.do?uri=sys_user.list` -- go to user list
2. Bookmark useful URLs for quick access

---

## Part 7: Customizing Your Homepage

### Step 7.1: Explore the Default Homepage

1. Click the **ServiceNow logo** or **Home** to go to the homepage
2. Observe the default widgets/dashboard:
   - Welcome message
   - Quick links
   - Reports or gauges (if any)

### Step 7.2: Homepage Administration

1. Type `sys_home_page.list` in the Filter Navigator
2. This shows configurable homepages
3. As admin, you can modify what users see on their homepage

---

## Part 8: Practice Exercises

### Exercise 1: Speed Navigation Challenge

Complete these navigations as fast as possible (use Filter Navigator shortcuts):

1. Open the Incident list → ___ seconds
2. Open the User list → ___ seconds
3. Open a new Change form → ___ seconds
4. Open System Properties → ___ seconds
5. Open the Knowledge Base → ___ seconds

**Target:** Each navigation in under 5 seconds using Filter Navigator

### Exercise 2: Favorites Setup

Create a "Daily Work" set of favorites:
1. Incident > All
2. Problem > All
3. Change > All
4. My Approvals (type `approval` in Filter Navigator)
5. System Logs > System Log > All

### Exercise 3: Global Search

Use Global Search to find:
1. Any incident related to "network"
2. Any user named "Abel"
3. Any knowledge article about "VPN"

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Mastered Filter Navigator | Navigate 10x faster than clicking through menus |
| Set up Favorites | One-click access to your most-used pages |
| Used History | Quickly return to recently visited pages |
| Performed Global Search | Find any record across the entire platform |
| Learned URL patterns | Direct navigation and bookmarking |

---

## Key Shortcuts Cheat Sheet

| Action | Shortcut |
|---|---|
| Filter Navigator | Click left sidebar search box |
| Open list directly | Type `<table>.list` in Filter Navigator |
| Open new form | Type `<table>.do` in Filter Navigator |
| Global Search | Click 🔍 or Ctrl+Alt+G |
| Favorites | Click ★ in banner |
| History | Click ⟲ in banner |
| Instance stats | Type `stats.do` in Filter Navigator |

---

## What's Next

In **Lab 03**, you'll work with lists and forms -- the two most common UI elements in ServiceNow. You'll learn to read, edit, sort, filter, and personalize them.
