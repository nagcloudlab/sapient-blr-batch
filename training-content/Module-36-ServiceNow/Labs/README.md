# Module 36: ServiceNow -- Lab Setup

## Prerequisites

- ServiceNow Personal Developer Instance (PDI) -- provided by the trainer or request at
  developer.servicenow.com (instance provisioning takes 10-15 minutes).
- Google Chrome (recommended browser for ServiceNow).
- No local software installation required.

## Running the Starter Code

This lab is performed in the browser-based ServiceNow PDI.

1. Log in to your PDI with the admin credentials.
2. Read `Project/BRIEF.md` for the full exercise instructions.
3. Open the configuration documents in `Labs/starter-code/`:
   - `sla-policies.md` -- 7 bugs to fix
   - `email-notifications.md` -- 6 bugs to fix
   - `instance-config.md` -- 6 bugs to fix
4. Replicate the buggy configurations in your PDI, then apply the fixes.

## Verifying Your Fixes

Compare each fixed configuration against `Project/CHECKLIST.md`:

- SLA policies: correct conditions trigger each SLA, durations match ITIL response targets,
  breach notifications are configured, schedules exclude non-business hours where appropriate.
- Email notifications: subject line uses correct field variables, recipient list correct,
  trigger condition is specific (not "always"), body template is readable.
- Instance config: session timeout is 30 minutes or less, ACLs restrict sensitive tables, admin
  password meets complexity requirements, default passwords are changed.

## Expected Behavior

- SLA records are created and auto-attached to incidents based on the correct conditions.
- Email notifications fire at the right trigger points and contain the correct field values.
- Instance security settings follow ServiceNow hardening guidelines.
- No "Can't find SLA" or missing notification errors in the system log.

## Troubleshooting

**PDI not accessible:** Developer instances hibernate after inactivity. Log in to
developer.servicenow.com and click "Wake Up" to restart your instance (takes 2-3 minutes).

**SLA not attaching to incidents:** Check the SLA condition script -- if the filter uses a field
that does not exist on your PDI's incident table, the SLA will silently not attach.
