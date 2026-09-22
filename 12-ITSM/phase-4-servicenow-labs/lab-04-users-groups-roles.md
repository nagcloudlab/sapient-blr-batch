# Lab 04: Users, Groups & Roles

**Level:** Beginner | **Duration:** 60 minutes | **Prerequisites:** Lab 01-03 completed

---

## Objective

By the end of this lab, you will:
- Create new users in ServiceNow
- Create groups and add members
- Assign roles to users and groups
- Understand role inheritance
- Impersonate a user to test permissions

---

## Part 1: Understanding Users

### Step 1.1: View Existing Users

1. Navigate to **User Administration > Users** (or type `sys_user.list` in Filter Navigator)
2. You'll see a list of demo users pre-loaded in your PDI
3. Click on any user (e.g., **Abel Tuter**) to see their profile
4. Note the key fields:
   ```
   User ID:        abel.tuter
   First name:     Abel
   Last name:      Tuter
   Email:          abel.tuter@example.com
   Title:          IT Specialist
   Department:     IT
   Active:         true
   Roles:          itil
   Groups:         Service Desk, Hardware
   ```

### Step 1.2: Create a New User

1. Navigate to **User Administration > Users**
2. Click **New** (top-left)
3. Fill in the form:

   | Field | Value |
   |---|---|
   | User ID | ravi.kumar |
   | First name | Ravi |
   | Last name | Kumar |
   | Email | ravi.kumar@example.com |
   | Title | Platform Engineer |
   | Department | IT |
   | Active | Checked (true) |
   | Password | `ServiceNow@123` (set via "Set Password" if available) |

4. Click **Submit**

### Step 1.3: Create More Users

Create these additional users (repeat Step 1.2 for each):

| User ID | First Name | Last Name | Title | Department |
|---|---|---|---|---|
| priya.sharma | Priya | Sharma | NOC Operator | IT |
| amit.verma | Amit | Verma | Junior Engineer | IT |
| meera.joshi | Meera | Joshi | Service Desk Lead | IT |
| vijay.admin | Vijay | Admin | System Administrator | IT |
| sanjay.mgr | Sanjay | Manager | VP Engineering | Engineering |

**Checkpoint:** You should now have 6 new users plus the existing demo users.

### Step 1.4: Set Passwords

For each new user:
1. Open the user record
2. Click **Set Password** (button or related link at the bottom)
3. Set password to: `ServiceNow@123` (or any password meeting complexity rules)
4. Click **Save Password**

---

## Part 2: Creating Groups

### Step 2.1: View Existing Groups

1. Navigate to **User Administration > Groups** (or type `sys_user_group.list`)
2. Browse the existing demo groups
3. Click on any group to see its details

### Step 2.2: Create a New Group

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | Platform Engineering |
   | Manager | Ravi Kumar (search and select) |
   | Description | Handles UPI platform infrastructure |
   | Type | (leave default) |
   | Active | Checked |

3. Click **Submit**

### Step 2.3: Add Members to the Group

1. Open the **Platform Engineering** group (search for it in the list)
2. Scroll down to the **Group Members** related list
3. Click **Edit** (or **New** in the Group Members related list)
4. In the member selection dialog:
   - Search for and add: **Ravi Kumar**
   - Search for and add: **Amit Verma**
5. Click **Save**

### Step 2.4: Create More Groups and Add Members

Create these groups and assign members:

| Group Name | Manager | Members |
|---|---|---|
| Platform Engineering | Ravi Kumar | Ravi Kumar, Amit Verma |
| NOC | Priya Sharma | Priya Sharma |
| Service Desk | Meera Joshi | Meera Joshi |
| IT Management | Sanjay Manager | Sanjay Manager |
| IT Administration | Vijay Admin | Vijay Admin |

**Checkpoint:** You have 5 new groups with members assigned.

---

## Part 3: Understanding and Assigning Roles

### Step 3.1: View Available Roles

1. Navigate to **User Administration > Roles** (or type `sys_user_role.list`)
2. Browse the available roles
3. Key roles to know:

   | Role | Purpose |
   |---|---|
   | `admin` | Full system administration |
   | `itil` | Core ITSM user -- create/edit incidents, problems, changes |
   | `catalog_admin` | Manage service catalog |
   | `knowledge_admin` | Manage knowledge base |
   | `sn_change_mgr` | Change management |
   | `approver_user` | Can approve requests and changes |
   | `asset` | IT asset management |

### Step 3.2: Assign Roles to Individual Users

1. Open user **Ravi Kumar** (navigate to Users, find Ravi)
2. Scroll down to the **Roles** related list
3. Click **Edit**
4. In the role collection dialog:
   - Find `itil` in the available list
   - Move it to the selected list (click >> or drag)
5. Click **Save**
6. Ravi now has the `itil` role

### Step 3.3: Assign Roles to All Users

Assign roles as follows:

| User | Roles to Assign |
|---|---|
| Ravi Kumar | `itil` |
| Priya Sharma | `itil` |
| Amit Verma | `itil` |
| Meera Joshi | `itil`, `sn_change_mgr` |
| Vijay Admin | `admin` |
| Sanjay Manager | `approver_user` |

For each user:
1. Open the user record
2. Go to **Roles** related list > **Edit**
3. Add the specified roles
4. **Save**

### Step 3.4: Assign Roles to Groups (Role Inheritance)

Instead of assigning roles to each user individually, you can assign roles to a group -- all members inherit the role.

1. Open the **Platform Engineering** group
2. Scroll to the **Roles** related list
3. Click **Edit**
4. Add the `itil` role
5. Click **Save**

Now **all members** of Platform Engineering (Ravi and Amit) inherit the `itil` role through the group.

```
Role Inheritance Flow:
  Group: Platform Engineering
    Role: itil
    Members: Ravi, Amit

    --> Ravi has itil (from group membership)
    --> Amit has itil (from group membership)

  If you add a new member to the group, they automatically get itil too.
```

---

## Part 4: Impersonation (Testing Permissions)

### Step 4.1: What is Impersonation?

Impersonation lets an admin "become" another user to see what they see and test their permissions -- without needing their password.

### Step 4.2: Impersonate a User

1. Click your **User icon** (top-right, currently shows "System Administrator")
2. Select **Impersonate User** (or **Impersonate Another User**)
3. Search for: **Ravi Kumar**
4. Select Ravi Kumar
5. The page reloads -- you are now seeing ServiceNow as Ravi would see it

### Step 4.3: Test Ravi's Permissions

As Ravi (impersonated):
1. Navigate to **Incident > All** -- Can Ravi see incidents? (Yes, because of `itil` role)
2. Click **Incident > Create New** -- Can Ravi create incidents? (Yes)
3. Navigate to **System Definition > Tables** -- Can Ravi access system admin pages? (No -- should be restricted)
4. Note what Ravi CAN and CANNOT do

### Step 4.4: Impersonate Another User

1. While impersonating Ravi, go back to **User icon > Impersonate User**
2. Search for: **Sanjay Manager**
3. Select Sanjay Manager
4. Test: Can Sanjay create incidents? (No -- he only has `approver_user`, not `itil`)
5. Test: Can Sanjay see the Approval module? (Yes)

### Step 4.5: Stop Impersonating

1. Click the **User icon** (top-right)
2. Select **Impersonate User** and choose **System Administrator** (admin)
3. Or look for **End Impersonation** option
4. You're back to being the admin

---

## Part 5: Role Testing Matrix

### Step 5.1: Verify Access for Each User

Impersonate each user and test these actions:

| Action | Ravi (itil) | Priya (itil) | Amit (itil) | Meera (itil+change_mgr) | Vijay (admin) | Sanjay (approver) |
|---|---|---|---|---|---|---|
| View incidents | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Create incidents | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| View changes | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Approve changes | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Access System Admin | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

Fill in this matrix as you test. Some results may vary depending on your PDI's configuration.

---

## Part 6: User Administration Tasks

### Step 6.1: Deactivate a User

1. Stop impersonating (back to admin)
2. Open user **Amit Verma**
3. Uncheck the **Active** checkbox
4. Click **Update**
5. Amit is now deactivated -- he can't log in, but his records are preserved
6. **Re-activate** Amit (check Active again, Update)

### Step 6.2: View a User's Access

1. Open user **Ravi Kumar**
2. Look at the **Roles** related list -- shows directly assigned roles
3. Look for a **Groups** related list -- shows group memberships
4. Note: Ravi has `itil` from both:
   - Direct role assignment (Step 3.2)
   - Group inheritance (Step 3.4 -- Platform Engineering group)

---

## Part 7: Practice Exercises

### Exercise 1: Create a Security Team

1. Create a new group called **Security Operations**
2. Create a new user: `security.analyst` / Rajan / Nair / Security Analyst
3. Add Rajan to the Security Operations group
4. Assign the `itil` and `sn_change_mgr` roles to the Security Operations group
5. Impersonate Rajan -- verify he can create incidents AND view change management

### Exercise 2: Role Investigation

1. Navigate to **User Administration > Roles** (`sys_user_role.list`)
2. Find these roles and note what they grant:
   - `catalog_admin` → ___________
   - `knowledge_admin` → ___________
   - `asset` → ___________
3. Assign `catalog_admin` to Meera Joshi
4. Impersonate Meera -- can she now manage catalog items?

### Exercise 3: Group Manager Permissions

1. Open the Platform Engineering group
2. Verify Ravi Kumar is the manager
3. Impersonate Ravi
4. Navigate to **My Groups' Work** or **Team Dashboard** (if available)
5. Can Ravi see his team's incidents? Document what you find.

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created users | Users are the foundation -- everyone needs an account |
| Created groups | Groups represent teams -- used for assignment routing |
| Assigned roles | Roles control what each user can see and do |
| Role inheritance via groups | Efficient permission management at scale |
| Impersonation testing | Verify permissions without sharing passwords |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **User** | An individual person with a ServiceNow account |
| **Group** | A collection of users representing a team |
| **Role** | A permission set that controls access to features |
| **Role Inheritance** | Group members automatically inherit the group's roles |
| **Impersonation** | Admin ability to "become" another user for testing |
| **Active/Inactive** | Deactivating a user prevents login but preserves data |

---

## What's Next

In **Lab 05**, you'll explore tables and columns -- the database structure behind everything in ServiceNow. You'll create a custom table and add fields to it.
