# Lab 17: Client Scripts

**Level:** Advanced | **Duration:** 90 minutes | **Prerequisites:** Lab 16 completed, JavaScript knowledge

---

## Objective

By the end of this lab, you will:
- Create all four types of Client Scripts (onLoad, onChange, onSubmit, onCellEdit)
- Use the g_form API to manipulate form fields
- Use GlideAjax to call server-side scripts from the client
- Access g_scratchpad data set by Display Business Rules
- Debug client scripts using browser developer tools

---

## Part 1: Client Script Types

```
Client Scripts run in the USER'S BROWSER (not the server).

Types:
  onLoad    → Runs when the form first loads
  onChange  → Runs when a specific field's value changes
  onSubmit  → Runs when the user clicks Save/Update/Submit
  onCellEdit → Runs when a cell is edited in list view
```

---

## Part 2: onLoad Client Script

### Step 2.1: Display Info Message on Load

1. Navigate to **System Definition > Client Scripts** (or type `sys_script_client.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | Show CI Incident Count on Load |
   | Table | Incident [incident] |
   | Type | onLoad |
   | Active | Checked |

4. **Script**:
   ```javascript
   function onLoad() {
       // Use g_scratchpad data from Display Business Rule (Lab 16)
       var count = g_scratchpad.ci_incident_count;
       var ciName = g_scratchpad.ci_name;

       if (count > 0) {
           g_form.addInfoMessage('Note: There are ' + count +
               ' other open incidents for CI "' + ciName + '".');
       }
   }
   ```

5. Click **Submit**
6. **Test:** Open an incident that has a CI with other open incidents -- you should see the info message

### Step 2.2: Set Default Values on Load

1. Create a new Client Script:

   | Field | Value |
   |---|---|
   | Name | Set Defaults for New Incidents |
   | Table | Incident [incident] |
   | Type | onLoad |

2. **Script**:
   ```javascript
   function onLoad() {
       // Only for new records (no sys_id yet)
       if (g_form.isNewRecord()) {
           // Set default assignment group
           g_form.setValue('assignment_group', '');  // clear first
           g_form.setValue('contact_type', 'phone'); // default contact type

           // Add a helpful message
           g_form.addInfoMessage('Please fill in all required fields. ' +
               'Priority will be auto-calculated from Impact and Urgency.');
       }
   }
   ```

3. Click **Submit**

---

## Part 3: onChange Client Script

### Step 3.1: Auto-Fill Based on Category

1. Create a new Client Script:

   | Field | Value |
   |---|---|
   | Name | Auto-set Assignment Group from Category |
   | Table | Incident [incident] |
   | Type | onChange |
   | Field name | Category |

2. **Script**:
   ```javascript
   function onChange(control, oldValue, newValue, isLoading) {
       // Don't run on initial form load
       if (isLoading) return;

       // Map categories to assignment groups
       var groupMap = {
           'network': 'Network',
           'hardware': 'Hardware',
           'software': 'Software',
           'database': 'Database',
           'inquiry': 'Service Desk'
       };

       var groupName = groupMap[newValue];
       if (groupName) {
           // Look up the group sys_id using GlideRecord on the client
           // Note: For better performance, use GlideAjax (see Part 5)
           g_form.setValue('assignment_group', '');

           // Show info message
           g_form.addInfoMessage('Assignment group suggestion: ' + groupName +
               '. Please verify before saving.');
       }
   }
   ```

3. Click **Submit**

### Step 3.2: Dynamic Field Behavior on Change

1. Create:

   | Field | Value |
   |---|---|
   | Name | Show Major Incident Fields |
   | Table | Incident [incident] |
   | Type | onChange |
   | Field name | Priority |

2. **Script**:
   ```javascript
   function onChange(control, oldValue, newValue, isLoading) {
       if (isLoading) return;

       // If priority is 1 (Critical), show major incident fields
       if (newValue == 1) {
           g_form.setDisplay('business_impact', true);
           g_form.setMandatory('business_impact', true);
           g_form.addWarningMessage('P1 Critical incident! ' +
               'Business Impact field is now required.');

           // Add visual indicator
           g_form.setLabelOf('short_description',
               'Short description (P1 - CRITICAL)');
       } else {
           g_form.setDisplay('business_impact', false);
           g_form.setMandatory('business_impact', false);
           g_form.setLabelOf('short_description', 'Short description');
       }
   }
   ```

### Step 3.3: Confirmation on State Change

1. Create:

   | Field | Value |
   |---|---|
   | Name | Confirm State Change to Closed |
   | Table | Incident [incident] |
   | Type | onChange |
   | Field name | State |

2. **Script**:
   ```javascript
   function onChange(control, oldValue, newValue, isLoading) {
       if (isLoading) return;

       // State 7 = Closed
       if (newValue == 7) {
           var confirmed = confirm(
               'Are you sure you want to close this incident?\n\n' +
               'Please verify:\n' +
               '- Resolution notes are complete\n' +
               '- Customer has been notified\n' +
               '- All related tasks are closed'
           );

           if (!confirmed) {
               // Revert to previous state
               g_form.setValue('state', oldValue);
           }
       }
   }
   ```

---

## Part 4: onSubmit Client Script

### Step 4.1: Validate Before Save

1. Create:

   | Field | Value |
   |---|---|
   | Name | Validate Incident Before Submit |
   | Table | Incident [incident] |
   | Type | onSubmit |

2. **Script**:
   ```javascript
   function onSubmit() {
       var priority = g_form.getValue('priority');
       var assignGroup = g_form.getValue('assignment_group');
       var shortDesc = g_form.getValue('short_description');

       // P1 incidents must have an assignment group
       if (priority == 1 && assignGroup == '') {
           g_form.addErrorMessage('P1 Critical incidents must have ' +
               'an Assignment Group before saving.');
           return false; // Prevent save
       }

       // Short description must be at least 10 characters
       if (shortDesc.length < 10) {
           g_form.addErrorMessage('Short description must be at least ' +
               '10 characters long.');
           return false; // Prevent save
       }

       // All validations passed
       return true; // Allow save
   }
   ```

3. Click **Submit**
4. **Test:** Try to save a P1 incident without an assignment group -- save should be blocked

### Step 4.2: Confirmation Before Save

1. Create:

   | Field | Value |
   |---|---|
   | Name | Confirm P1 Incident Creation |
   | Table | Incident [incident] |
   | Type | onSubmit |

2. **Script**:
   ```javascript
   function onSubmit() {
       var priority = g_form.getValue('priority');

       if (priority == 1 && g_form.isNewRecord()) {
           return confirm(
               'You are about to create a P1 CRITICAL incident.\n\n' +
               'This will:\n' +
               '- Trigger immediate notifications to on-call team\n' +
               '- Start a 30-minute SLA timer\n' +
               '- Alert management\n\n' +
               'Are you sure this is a P1?'
           );
       }

       return true;
   }
   ```

---

## Part 5: g_form API Reference

### Step 5.1: Key g_form Methods

| Method | Description | Example |
|---|---|---|
| `getValue(field)` | Get field value | `g_form.getValue('priority')` |
| `setValue(field, value)` | Set field value | `g_form.setValue('state', 2)` |
| `setDisplay(field, bool)` | Show/hide field | `g_form.setDisplay('notes', true)` |
| `setVisible(field, bool)` | Show/hide (with space) | `g_form.setVisible('notes', false)` |
| `setMandatory(field, bool)` | Make required | `g_form.setMandatory('group', true)` |
| `setReadOnly(field, bool)` | Make read-only | `g_form.setReadOnly('number', true)` |
| `setLabelOf(field, label)` | Change label text | `g_form.setLabelOf('desc', 'Details')` |
| `addInfoMessage(msg)` | Blue info banner | `g_form.addInfoMessage('Saved!')` |
| `addWarningMessage(msg)` | Yellow warning | `g_form.addWarningMessage('Check!')` |
| `addErrorMessage(msg)` | Red error banner | `g_form.addErrorMessage('Error!')` |
| `clearMessages()` | Remove all banners | `g_form.clearMessages()` |
| `isNewRecord()` | Check if new/unsaved | `if (g_form.isNewRecord()) {...}` |
| `save()` | Save the form | `g_form.save()` |
| `submit()` | Submit the form | `g_form.submit()` |
| `addOption(field, val, label)` | Add dropdown option | `g_form.addOption('state', 9, 'Custom')` |
| `removeOption(field, val)` | Remove dropdown option | `g_form.removeOption('state', 8)` |
| `getReference(field, callback)` | Get referenced record | See Step 5.2 |
| `flash(field, color, count)` | Flash a field | `g_form.flash('priority', '#ff0000', 3)` |

### Step 5.2: getReference Example

```javascript
// Get the caller's details (async -- must use callback)
g_form.getReference('caller_id', function(callerRecord) {
    var callerName = callerRecord.name;
    var callerEmail = callerRecord.email;
    var callerVIP = callerRecord.vip;

    if (callerVIP == 'true') {
        g_form.addInfoMessage('VIP Caller: ' + callerName +
            ' (' + callerEmail + ')');
    }
});
```

---

## Part 6: GlideAjax -- Call Server Scripts from Client

### Step 6.1: Why GlideAjax?

Client Scripts run in the browser. They can't directly query the database. GlideAjax bridges this gap:

```
Client Script (browser) --GlideAjax call--> Script Include (server)
                         <--JSON response--
```

### Step 6.2: Create a Script Include (Server Side)

1. Navigate to **System Definition > Script Includes** (or type `sys_script_include.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | IncidentUtils |
   | Client callable | Checked (IMPORTANT!) |
   | Active | Checked |

4. **Script**:
   ```javascript
   var IncidentUtils = Class.create();
   IncidentUtils.prototype = Object.extendsObject(AbstractAjaxProcessor, {

       // Get count of open incidents for a given CI
       getOpenIncidentCount: function() {
           var ciSysId = this.getParameter('sysparm_ci_sys_id');
           var gr = new GlideRecord('incident');
           gr.addQuery('cmdb_ci', ciSysId);
           gr.addQuery('state', 'NOT IN', '6,7,8');
           gr.query();
           return gr.getRowCount();
       },

       // Check if a user is VIP
       isUserVIP: function() {
           var userId = this.getParameter('sysparm_user_id');
           var gr = new GlideRecord('sys_user');
           if (gr.get(userId)) {
               return gr.vip.toString();
           }
           return 'false';
       },

       type: 'IncidentUtils'
   });
   ```

5. Click **Submit**

### Step 6.3: Call Script Include from Client Script

1. Create a new Client Script:

   | Field | Value |
   |---|---|
   | Name | Check CI Open Incidents via Ajax |
   | Table | Incident [incident] |
   | Type | onChange |
   | Field name | Configuration item |

2. **Script**:
   ```javascript
   function onChange(control, oldValue, newValue, isLoading) {
       if (isLoading || newValue == '') return;

       // Call server-side Script Include via GlideAjax
       var ga = new GlideAjax('IncidentUtils');
       ga.addParam('sysparm_name', 'getOpenIncidentCount');
       ga.addParam('sysparm_ci_sys_id', newValue);
       ga.getXMLAnswer(function(answer) {
           var count = parseInt(answer);
           if (count > 0) {
               g_form.addWarningMessage('Warning: There are ' + count +
                   ' other open incidents for this CI. ' +
                   'This may be a recurring issue.');
           }
       });
   }
   ```

3. Click **Submit**
4. **Test:** Open an incident form, select a CI that has other open incidents

---

## Part 7: Debugging Client Scripts

### Step 7.1: Browser Developer Tools

1. Open your browser's Developer Tools (F12 or Ctrl+Shift+I)
2. Go to the **Console** tab
3. Client script errors appear here in red

### Step 7.2: Using console.log()

Add `console.log()` statements to your scripts for debugging:

```javascript
function onChange(control, oldValue, newValue, isLoading) {
    console.log('onChange fired! Field: ' + control.fieldName);
    console.log('Old value: ' + oldValue);
    console.log('New value: ' + newValue);
    console.log('Is loading: ' + isLoading);
    // ... your logic
}
```

### Step 7.3: Using jslog()

ServiceNow provides `jslog()` for client-side logging:

```javascript
jslog('My client script is running');
```

View jslog output: Append `?sysparm_log=true` to the URL, or enable JavaScript Log via the gear icon.

### Step 7.4: Common Client Script Errors

| Error | Cause | Fix |
|---|---|---|
| "g_form is not defined" | Script running outside a form context | Ensure script is on correct table |
| "getReference is not a function" | Using wrong API | Use `g_form.getReference(field, callback)` |
| Ajax returns empty | Script Include not client-callable | Check "Client callable" checkbox |
| Script doesn't fire | Wrong type or field name | Verify type (onChange, onLoad) and field name |
| Changes not persisting | Setting values in onLoad for existing record | Check if `isLoading` guard is blocking |

---

## Part 8: Practice Exercises

### Exercise 1: VIP Caller Handling

Create a Client Script (onChange on Caller field):
1. When a caller is selected, check if they're a VIP (use GlideAjax)
2. If VIP:
   - Flash the Priority field red
   - Set Impact to 1-High
   - Add warning: "VIP Caller! Impact elevated."

### Exercise 2: Dynamic Subcategory

Create onChange scripts:
1. When Category changes, populate the Subcategory dropdown with relevant options:
   - Network: DNS, VPN, WiFi, Firewall
   - Hardware: Laptop, Desktop, Printer, Monitor
   - Software: Email, CRM, ERP, Custom App

### Exercise 3: Form Validation Suite

Create onSubmit scripts that validate:
1. Description must be at least 20 characters
2. If Impact = 1, Configuration Item must be filled
3. If state = Resolved, resolution notes must be at least 50 characters
4. Show specific error messages for each validation failure

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created onLoad scripts | Initialize form state and show messages |
| Created onChange scripts | React to user input in real-time |
| Created onSubmit scripts | Validate before saving |
| Used g_form API | Control form fields programmatically |
| Used GlideAjax | Server queries from client without page reload |
| Debugged in browser | Essential for client-side troubleshooting |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Client Script** | JavaScript running in the user's browser |
| **onLoad** | Fires when the form loads |
| **onChange** | Fires when a specific field value changes |
| **onSubmit** | Fires when form is saved; return false to prevent save |
| **g_form** | Client-side API for form manipulation |
| **GlideAjax** | Client-to-server communication bridge |
| **g_scratchpad** | Data passed from Display Business Rules to Client Scripts |
| **Client Callable** | Script Include property enabling GlideAjax calls |

---

## What's Next

In **Lab 18**, you'll learn **Script Includes** -- reusable server-side scripts, advanced GlideRecord patterns, and debugging techniques.
