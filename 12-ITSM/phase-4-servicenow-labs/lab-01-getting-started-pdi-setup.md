# Lab 01: Getting Started -- Personal Developer Instance (PDI) Setup

**Level:** Beginner | **Duration:** 30 minutes | **Prerequisites:** None

---

## Objective

By the end of this lab, you will:
- Create a free ServiceNow developer account
- Request and activate a Personal Developer Instance (PDI)
- Log in and explore the ServiceNow homepage
- Understand instance URLs and versioning

---

## Part 1: Create Your Developer Account

### Step 1.1: Sign Up

1. Open your browser and go to **developer.servicenow.com**
2. Click **Sign Up** (top-right corner)
3. Fill in the registration form:
   - First Name
   - Last Name
   - Email (use your professional or personal email)
   - Password (must meet complexity requirements)
   - Country
4. Accept the Terms of Use
5. Click **Sign Up**
6. Check your email for a verification link and click it

### Step 1.2: Verify Your Account

1. Open the verification email from ServiceNow
2. Click the verification link
3. You'll be redirected to the developer portal
4. Log in with your credentials

**Checkpoint:** You should now see the ServiceNow Developer Portal dashboard.

---

## Part 2: Request a Personal Developer Instance

### Step 2.1: Request Instance

1. After logging in to developer.servicenow.com, click your **profile icon** (top-right)
2. Select **Manage instance password** or go to the **Instance** section
3. Click **Request Instance**
4. Select the **latest release version** (e.g., "Xanadu" or whichever is current)
   - Always pick the latest GA (General Availability) release for learning
5. Click **Request**

### Step 2.2: Wait for Provisioning

1. Instance provisioning takes **5-15 minutes**
2. You'll see a progress indicator
3. When ready, you'll see:
   - **Instance URL:** `https://devXXXXXX.service-now.com`
   - **Admin Username:** `admin`
   - **Admin Password:** (auto-generated, shown on screen)

### Step 2.3: Save Your Credentials

```
Write these down -- you'll need them for every lab:

Instance URL:  https://dev_______.service-now.com
Username:      admin
Password:      ___________________________

IMPORTANT: PDIs are reclaimed after 10 days of inactivity.
           Log in at least once every 10 days to keep your instance alive.
           If reclaimed, you can request a new one (but you lose all data).
```

**Checkpoint:** You have an instance URL, username, and password.

---

## Part 3: First Login

### Step 3.1: Log In

1. Open a new browser tab
2. Navigate to your instance URL: `https://devXXXXXX.service-now.com`
3. Enter:
   - Username: `admin`
   - Password: (the password from Step 2.2)
4. Click **Log in**

### Step 3.2: First-Time Setup

On first login, you may see:
- A **guided setup wizard** -- you can skip this for now (click "Close" or "Skip")
- A **welcome dialog** -- close it
- The **System Administrator** homepage/dashboard

### Step 3.3: Understand What You See

```
+------------------------------------------------------------------+
| Banner (top bar)                                                   |
| [All] [Favorites★] [History⟲] [Search🔍]      [User👤] [?Help]  |
+------------------------------------------------------------------+
|                    |                                                |
| Application        |  Content Frame                                |
| Navigator          |                                                |
| (left sidebar)     |  (This is where all content appears)         |
|                    |                                                |
| Filter navigator   |  Currently showing: Homepage / Dashboard      |
| [____________]     |                                                |
|                    |                                                |
| > Self-Service     |                                                |
| > Incident         |                                                |
| > Problem          |                                                |
| > Change           |                                                |
| > ...              |                                                |
+------------------------------------------------------------------+
```

**Key Areas:**
| Area | Location | Purpose |
|---|---|---|
| **Banner** | Top | Global search, favorites, history, user menu |
| **All Menu** | Top-left | Access all applications and modules |
| **Navigator** | Left sidebar | Browse applications and modules |
| **Filter Navigator** | Top of left sidebar | Type to quickly find any module |
| **Content Frame** | Center/right | Where forms, lists, dashboards appear |

**Checkpoint:** You are logged in and can see the ServiceNow interface.

---

## Part 4: Explore the Homepage

### Step 4.1: Check Your Instance Info

1. Click the **User icon** (top-right, looks like a person)
2. Note your logged-in user: **System Administrator**
3. Click **About** or check the banner for the instance version

### Step 4.2: Try the Filter Navigator

The Filter Navigator is your best friend. It's the search box at the top of the left sidebar.

1. Click in the **Filter Navigator** text box
2. Type: `incident`
3. Watch the left sidebar filter to show only incident-related modules:
   ```
   > Incident
     - Create New
     - All
     - My Incidents
     - Open
     - Open - Unassigned
     - Resolved
     - ...
   ```
4. Click **Incident > All** to see the incident list
5. Clear the filter and type: `sys_properties` -- this shows system properties (admin settings)

### Step 4.3: Try the "All" Menu

1. Click **All** in the top-left of the banner
2. This opens a full-screen menu showing ALL applications
3. Browse the categories: Self-Service, Incident, Problem, Change, etc.
4. Click any item to navigate there
5. Press **Escape** or click elsewhere to close

### Step 4.4: Check System Settings

1. In the Filter Navigator, type: `system properties`
2. Click **System Properties > Basic Configuration**
3. Note the settings available:
   - Instance name
   - Page header/caption
   - Banner text
   - Date/time format
4. **Don't change anything yet** -- just observe

**Checkpoint:** You can navigate using the Filter Navigator and the All menu.

---

## Part 5: Quick Orientation Tasks

Complete these tasks to build muscle memory:

### Task 1: Find the Incident Module
1. Type `incident` in the Filter Navigator
2. Click **Incident > Create New**
3. Observe the empty incident form (don't fill it in yet)
4. Click the browser **Back** button or navigate away

### Task 2: Find the User Table
1. Type `sys_user.list` in the Filter Navigator and press Enter
2. This directly opens the User table list view
3. You'll see all users in the system (demo data)
4. Count how many users exist in your PDI

### Task 3: Check Your Instance Version
1. Type `stats.do` in the Filter Navigator and press Enter
2. This shows instance statistics:
   - Build name (release version)
   - Build date
   - Node info
   - Database info
3. Note your **Build name** -- this is the ServiceNow release you're on

### Task 4: Find the System Logs
1. Type `syslog` in the Filter Navigator
2. Click **System Logs > System Log > All**
3. This shows all system log entries -- useful for debugging later

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created developer account | Free access to ServiceNow for learning |
| Requested PDI | Your personal sandbox -- safe to experiment |
| Logged in as admin | Full admin access to configure anything |
| Used Filter Navigator | Fastest way to find anything in ServiceNow |
| Explored modules | Understanding the layout before diving deep |

---

## Key Concepts Introduced

| Concept | Definition |
|---|---|
| **PDI** | Personal Developer Instance -- free, full-featured sandbox |
| **Instance** | A single deployment of ServiceNow (has its own URL, data, config) |
| **Filter Navigator** | Search box in the left sidebar to find modules |
| **Module** | A menu item that opens a specific page (form, list, dashboard) |
| **Application** | A group of related modules (e.g., Incident Management) |
| **Content Frame** | The main area where content is displayed |

---

## Common Issues & Fixes

| Issue | Fix |
|---|---|
| PDI not provisioning | Wait 15 minutes. If stuck, cancel and re-request |
| Forgot password | Go to developer.servicenow.com > Manage instance password |
| PDI reclaimed | Request a new instance (data is lost) |
| Page looks different | Different ServiceNow versions have slightly different UIs -- concepts are the same |
| Can't find a module | Use Filter Navigator -- type the module name |

---

## What's Next

In **Lab 02**, you'll master platform navigation -- favorites, history, tabs, and the global search. This is the foundation for working efficiently in ServiceNow.
