# Module 16: Jira & Confluence -- Lab Setup

## Prerequisites

- Jira and Confluence access provided by the trainer (cloud instance URL and login credentials).
- No local software installation required.
- A modern browser (Chrome recommended).

## Running the Starter Code

This lab is performed entirely in the browser-based Jira/Confluence instance.

1. Log in with the credentials provided by the trainer.
2. Read `Project/BRIEF.md` for the full exercise instructions.
3. The `Labs/starter-code/` folder contains the flawed JQL queries, board configuration notes,
   and Confluence page drafts to review and fix.

## Verifying Your Fixes

Compare your work against `Project/CHECKLIST.md`:

- Jira issues: correct issue type, priority, component, label, and linked epic.
- JQL queries: each query returns the correct issue count shown in `lab-exercises.md`.
- Confluence pages: follow the standard template structure (summary, details, action items).
- Board design: columns map correctly to the team workflow states.

## Expected Behavior

- JQL queries run without syntax errors and return the expected issue sets.
- Jira board columns reflect the full lifecycle: Backlog > In Progress > In Review > Done.
- Confluence pages are structured, linked to the relevant Jira epic, and readable by non-engineers.
- Labels and components are consistent across all created issues.

## Troubleshooting

**JQL syntax error:** JQL is case-insensitive for keywords but field names must match exactly. Use the
autocomplete suggestions in the Jira query bar to confirm field names.

**Cannot create issues:** Check that you are working in the correct project key (shown in `BRIEF.md`).
If permissions are missing, ask the trainer to grant the "Create Issues" role.
