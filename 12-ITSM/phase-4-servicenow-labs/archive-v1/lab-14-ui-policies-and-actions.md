# Lab 14: UI Policies & UI Actions

**Level:** Advanced | **Duration:** 60 minutes | **Prerequisites:** Lab 07-13 completed

---

## Objective

By the end of this lab, you will:
- Create UI Policies to dynamically control field behavior (visibility, mandatory, read-only)
- Build UI Actions (buttons, links, context menu items) on forms and lists
- Use UI Policy actions with reverse conditions
- Understand when to use UI Policies vs Client Scripts

---

## Part 1: UI Policies

### What Are UI Policies?

UI Policies dynamically change the form based on conditions -- **without writing code**.

```
Examples:
- When Priority = 1-Critical, make "Assignment group" mandatory
- When State = Resolved, make "Resolution notes" mandatory and visible
- When Category = Hardware, show "Hardware type" field
- When VIP = true, highlight the caller field in a special color
```

### Step 1.1: View Existing UI Policies

1. Navigate to **System UI > UI Policies** (or type `sys_ui_policy.list`)
2. Browse existing policies -- note the table, conditions, and actions

### Step 1.2: Create UI Policy -- Mandatory Resolution Notes

When an incident is resolved, resolution notes should be mandatory.

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Table | Incident [incident] |
   | Short description | Make resolution notes mandatory when resolved |
   | Active | Checked |
   | Order | 100 |
   | On load | Checked |
   | Reverse if false | Checked |
   | Inherit | Checked |

3. **Conditions**:
   ```
   State is Resolved
   ```

4. Click **Submit**
5. Reopen the UI Policy

6. In the **UI Policy Actions** related list, click **New**:

   | Field | Value |
   |---|---|
   | Field name | Resolution notes |
   | Mandatory | True |
   | Visible | True |
   | Read only | False |

7. Click **Submit**

### Step 1.3: Test the UI Policy

1. Open any incident
2. Change **State** to **Resolved**
3. Observe: "Resolution notes" field should now:
   - Be visible (if it was hidden)
   - Be marked as mandatory (red asterisk)
4. Try to save without resolution notes -- you should get a validation error
5. Change State back to **In Progress**
6. Observe: "Resolution notes" should revert to non-mandatory (because of **Reverse if false**)

### Step 1.4: Create UI Policy -- Show Hardware Fields

1. Create a new UI Policy:

   | Field | Value |
   |---|---|
   | Table | Incident [incident] |
   | Short description | Show hardware fields when category is Hardware |
   | Conditions | Category is Hardware |
   | On load | Checked |
   | Reverse if false | Checked |

2. Add UI Policy Actions:

   | Field Name | Mandatory | Visible | Read Only |
   |---|---|---|---|
   | Subcategory | True | True | -- |
   | Configuration item | True | True | -- |

3. Click **Submit**

### Step 1.5: Create UI Policy -- Read-Only When Closed

1. Create a new UI Policy:

   | Field | Value |
   |---|---|
   | Table | Incident [incident] |
   | Short description | Make all fields read-only when closed |
   | Conditions | State is Closed |
   | On load | Checked |
   | Reverse if false | Checked |

2. Add UI Policy Actions -- make key fields read-only:

   | Field Name | Read Only |
   |---|---|
   | Short description | True |
   | Description | True |
   | Priority | True |
   | Category | True |
   | Assignment group | True |
   | Assigned to | True |

3. Test: open a closed incident -- fields should be read-only
4. Open an open incident -- fields should be editable

### Step 1.6: Create UI Policy -- P1 Mandatory Fields

1. Create:

   | Field | Value |
   |---|---|
   | Table | Incident [incident] |
   | Short description | Additional mandatory fields for P1 incidents |
   | Conditions | Priority is 1 - Critical |
   | Reverse if false | Checked |

2. Actions:

   | Field Name | Mandatory |
   |---|---|
   | Assignment group | True |
   | Configuration item | True |
   | Description | True |

---

## Part 2: UI Policy with Scripting

### Step 2.1: Scripted UI Policy

For more complex logic, you can add a script to a UI Policy:

1. Create a new UI Policy
2. Check **Run scripts**
3. Two script fields appear:
   - **Execute if true** -- runs when condition is met
   - **Execute if false** -- runs when condition is not met (reverse)

4. Example script (Execute if true):
   ```javascript
   // Highlight the caller field when VIP
   g_form.setLabelOf('caller_id', 'Caller (VIP)');
   g_form.addDecoration('caller_id', 'icon-star', 'VIP Customer');
   ```

5. Example script (Execute if false):
   ```javascript
   // Remove VIP highlighting
   g_form.setLabelOf('caller_id', 'Caller');
   g_form.removeDecoration('caller_id', 'icon-star', 'VIP Customer');
   ```

---

## Part 3: UI Actions

### What Are UI Actions?

UI Actions add **buttons, links, and context menu items** to forms and lists.

```
Examples:
- "Escalate" button on the incident form
- "Assign to Me" button in the form header
- "Create Problem" link on the incident form
- "Close All Selected" action on the incident list
```

### Step 3.1: View Existing UI Actions

1. Navigate to **System Definition > UI Actions** (or type `sys_ui_action.list`)
2. Filter by Table = Incident
3. Browse existing UI actions -- note the names, positions, and scripts

### Step 3.2: Create a "Mark as VIP" Button

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | Mark as VIP |
   | Table | Incident [incident] |
   | Show insert | Unchecked |
   | Show update | Checked |
   | Client | Unchecked |
   | Form button | Checked |
   | Form context menu | Unchecked |
   | Form link | Unchecked |
   | List banner button | Unchecked |
   | Active | Checked |
   | Order | 200 |

3. **Condition** (when to show the button):
   ```
   current.priority == 1
   ```
   (Only show for P1 incidents)

4. **Script** (server-side -- what happens when clicked):
   ```javascript
   // Add VIP tag to the work notes
   current.work_notes = "*** MARKED AS VIP ***\nThis incident has been flagged as VIP priority.";
   current.update();
   action.setRedirectURL(current);
   ```

5. Click **Submit**

### Step 3.3: Test the Button

1. Open a P1 incident
2. Look for the "Mark as VIP" button in the form header
3. Click it
4. The work note should be added
5. Open a P2 incident -- the button should NOT appear (condition: priority == 1)

### Step 3.4: Create an "Assign to Me" Button

1. Create a new UI Action:

   | Field | Value |
   |---|---|
   | Name | Assign to Me |
   | Table | Incident [incident] |
   | Form button | Checked |
   | Show update | Checked |
   | Order | 100 |

2. **Script**:
   ```javascript
   current.assigned_to = gs.getUserID();
   current.state = 2; // In Progress
   current.work_notes = "Assigned to myself: " + gs.getUserDisplayName();
   current.update();
   action.setRedirectURL(current);
   ```

3. Click **Submit**
4. Test: open an incident, click "Assign to Me" -- it should assign to you and set state to In Progress

### Step 3.5: Create a Form Link

UI Actions can also appear as links below the form buttons.

1. Create a new UI Action:

   | Field | Value |
   |---|---|
   | Name | View CI Details |
   | Table | Incident [incident] |
   | Form link | Checked |
   | Form button | Unchecked |
   | Condition | `!current.cmdb_ci.nil()` |

2. **Script**:
   ```javascript
   action.setRedirectURL('cmdb_ci.do?sys_id=' + current.cmdb_ci);
   ```

3. Test: open an incident with a CI linked -- the "View CI Details" link appears and navigates to the CI

### Step 3.6: Create a List UI Action

1. Create a new UI Action:

   | Field | Value |
   |---|---|
   | Name | Bulk Assign to Service Desk |
   | Table | Incident [incident] |
   | List banner button | Checked |
   | Form button | Unchecked |
   | Show update | Unchecked |
   | Client | Checked |
   | List choice | Checked |

2. **Client script** (onClick):
   ```javascript
   function onClick(g_list) {
       var selectedSysIds = g_list.getChecked();
       if (selectedSysIds == '') {
           alert('Please select at least one incident.');
           return false;
       }
       if (!confirm('Assign selected incidents to Service Desk?')) {
           return false;
       }
       // Call server-side script
       return true;
   }
   ```

3. **Script** (server-side):
   ```javascript
   // Get the Service Desk group sys_id
   var grp = new GlideRecord('sys_user_group');
   grp.addQuery('name', 'Service Desk');
   grp.query();
   if (grp.next()) {
       var ids = request.getParameter('sysparm_checked_items');
       var idArray = ids.split(',');
       for (var i = 0; i < idArray.length; i++) {
           var inc = new GlideRecord('incident');
           if (inc.get(idArray[i].replace('sys_id:', ''))) {
               inc.assignment_group = grp.sys_id;
               inc.update();
           }
       }
   }
   ```

---

## Part 4: UI Policies vs Client Scripts

| Feature | UI Policy | Client Script |
|---|---|---|
| **Code required** | No (declarative) | Yes (JavaScript) |
| **Complexity** | Simple show/hide/mandatory/readonly | Complex logic, API calls |
| **When to use** | Field visibility, mandatory, read-only | Calculations, validations, alerts |
| **Reverse logic** | Built-in "Reverse if false" | Must code manually |
| **Performance** | Better (optimized by platform) | Depends on script quality |
| **Recommendation** | Use FIRST -- covers most needs | Use when UI Policy is not enough |

---

## Part 5: Practice Exercises

### Exercise 1: Change Management UI Policies

Create these UI Policies on the Change Request table:

1. When Type = Emergency, make these mandatory: Justification, Backout plan
2. When State = Closed, make all fields read-only
3. When Risk = High, show the "Risk mitigation plan" field and make it mandatory

### Exercise 2: Custom Buttons

Create these UI Actions:

1. **"Escalate to L3"** button on the Incident form:
   - Changes assignment group to a specific L3 group
   - Adds work note: "Auto-escalated to L3"
   - Only visible when Priority is 1 or 2

2. **"Quick Close"** button on the Incident form:
   - Sets state to Closed
   - Sets close code to "Solved"
   - Adds close notes with current date/time
   - Only visible when State is Resolved

### Exercise 3: Conditional Field Behavior

Create a UI Policy that:
1. When Impact = 1 (High) AND Urgency = 1 (High):
   - Make "Major incident" checkbox visible
   - Make "Business impact" field visible and mandatory
   - Show a special section called "Major Incident Details"

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created UI Policies | Dynamic forms without writing code |
| Used Reverse if false | Automatic reversal when conditions no longer match |
| Created UI Actions (buttons) | Custom actions on forms and lists |
| Created form links and list actions | Extend ServiceNow functionality |
| Understood UI Policy vs Client Script | Choose the right tool for the job |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **UI Policy** | Declarative rule that controls field visibility, mandatory, and read-only state |
| **UI Policy Action** | Specific field behavior set by a UI Policy |
| **Reverse if false** | Automatically undo the policy when conditions no longer match |
| **UI Action** | Custom button, link, or context menu item on forms/lists |
| **Form button** | Button in the form header area |
| **Form link** | Link below the form buttons |
| **List banner button** | Button on the list view header |
| **Condition** | Server-side condition controlling when a UI Action is visible |

---

## What's Next

In **Lab 15**, you'll learn **Flow Designer** -- building automated workflows with visual drag-and-drop, including approval flows, notifications, and subflows.
