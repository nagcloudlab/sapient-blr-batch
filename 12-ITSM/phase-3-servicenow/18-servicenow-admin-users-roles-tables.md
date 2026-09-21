# Section 18: ServiceNow Admin -- Users, Groups, Roles & Tables

## Purpose

Understand how ServiceNow is administered -- who can do what, and how data is organized.

---

## Users, Groups & Roles

Think of it as **access control** -- just like Linux permissions, but for ITSM.

```
User   = a person (e.g., Ravi, Priya)
Group  = a team (e.g., Platform Engineering, NOC, DBA)
Role   = a permission set (e.g., itil, admin, catalog_admin)

User --belongs to--> Group
User --has--> Role
Group --has--> Role (all members inherit it)
```

### UPI Example: NPCI's ServiceNow Setup

| User | Group | Role | What they can do |
|---|---|---|---|
| Ravi (L2 Engineer) | Platform Engineering | `itil` | Create/update incidents, changes, problems |
| Priya (NOC Operator) | NOC | `itil` | Create incidents, assign to groups |
| Amit (New Joiner) | Platform Engineering | `itil_lite` | View incidents, add comments (no edit) |
| Meera (Service Desk Lead) | Service Desk | `itil` + `sn_change_mgr` | Manage incidents + approve standard changes |
| Vijay (Admin) | IT Admin | `admin` | Configure ServiceNow itself -- forms, workflows, tables |
| Sanjay (VP Engineering) | Management | `approver_user` | Approve changes, view dashboards |

### Key Roles in ServiceNow

| Role | What it grants |
|---|---|
| `itil` | Core ITSM -- create/edit incidents, problems, changes, KB articles |
| `admin` | Full system administration -- configure anything |
| `catalog_admin` | Manage service catalog items |
| `knowledge_admin` | Manage knowledge base articles and categories |
| `sn_change_mgr` | Change management -- approve/reject changes |
| `approver_user` | Approve requests and changes |
| `asset` | IT asset management |

### Role Tagging (Elevated Privileges)

Some actions need **elevated roles** -- like sudo in Linux:

```
Normal:    Ravi (itil role) can create and update incidents
Elevated:  Ravi needs `security_admin` to view security incidents
           --> Ravi requests role elevation
           --> Manager approves
           --> Role granted for 8 hours (auto-expires)
```

---

## Tables & Columns

ServiceNow stores everything in **tables** -- just like a relational database.

### Core ITSM Tables

| Table Name | What it stores | Key Fields |
|---|---|---|
| `incident` | Incidents | number, short_description, priority, state, assigned_to |
| `problem` | Problems | number, short_description, root_cause, known_error |
| `change_request` | Changes | number, type, risk, state, cab_required |
| `sc_request` | Service Requests | number, requested_for, stage |
| `sc_cat_item` | Catalog Items | name, category, price, workflow |
| `cmdb_ci` | Configuration Items | name, class, status, environment |
| `kb_knowledge` | Knowledge Articles | number, title, workflow_state, category |
| `sys_user` | Users | user_name, email, active, department |
| `sys_user_group` | Groups | name, manager, type |
| `sla_definition` | SLA Definitions | name, target, type |

### Table Relationships

```
incident
  |-- caller_id        --> sys_user (who reported it)
  |-- assigned_to      --> sys_user (who's fixing it)
  |-- assignment_group --> sys_user_group (which team)
  |-- cmdb_ci          --> cmdb_ci (which CI is affected)
  |-- problem_id       --> problem (linked problem)
  |-- caused_by        --> change_request (which change caused it)

Everything links to everything. That's the power.
```

### UPI Example: Incident Record in the Table

```
incident table, row INC0010042:
+-------------------+------------------------------------------+
| Field             | Value                                    |
+-------------------+------------------------------------------+
| number            | INC0010042                               |
| short_description | Axis Bank transactions failing           |
| caller_id         | HDFC Bank Integration (sys_user)         |
| priority          | 1 - Critical                             |
| state             | In Progress                              |
| assigned_to       | Ravi (sys_user)                          |
| assignment_group  | Platform Engineering (sys_user_group)    |
| cmdb_ci           | CI-4001 PSP Gateway (cmdb_ci)            |
| sla_due           | 2026-09-21 08:33:00                      |
| work_notes        | "Checking Axis PSP node connectivity..." |
+-------------------+------------------------------------------+
```

---

## Auditing

ServiceNow tracks **who changed what, when** -- critical for compliance.

```
Audit trail for INC0010042:
+--------------------+----------+-------------------+------------------+
| Timestamp          | User     | Field Changed     | Old -> New       |
+--------------------+----------+-------------------+------------------+
| Sep 21 08:05:12    | Priya    | state             | New -> In Prog   |
| Sep 21 08:05:12    | Priya    | assigned_to       | (empty) -> Ravi  |
| Sep 21 08:10:33    | Ravi     | work_notes        | (added note)     |
| Sep 21 08:15:01    | Ravi     | state             | In Prog -> Resol |
| Sep 21 08:15:01    | Ravi     | resolution_code   | (empty) -> Fixed |
+--------------------+----------+-------------------+------------------+
```

**UPI relevance:** RBI audits require NPCI to show full audit trails for P1 incidents -- who did what, when, and why. ServiceNow provides this automatically.

---

## Key Takeaway

> ServiceNow admin is about **who can do what** (roles) and **where data lives** (tables).
>
> - **Users** = people
> - **Groups** = teams
> - **Roles** = permissions
> - **Tables** = data storage
> - **Auditing** = accountability
>
> If you understand these 5 concepts, you can navigate any ServiceNow instance.
