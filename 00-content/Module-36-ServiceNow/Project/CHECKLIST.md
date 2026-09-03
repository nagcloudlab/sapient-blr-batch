# ServiceNow -- Submission Checklist
## Module 36 | Days 43-44

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | SLA: P1 start condition checks Priority = 1 | [ ] |
| 2 | SLA: P1 duration is 4 hours | [ ] |
| 3 | SLA: Stop condition triggers on Resolved or Closed | [ ] |
| 4 | SLA: Pause condition triggers on Pending (not In Progress) | [ ] |
| 5 | SLA: P2 uses 24x7 schedule | [ ] |
| 6 | SLA: Warning notifications at 50% and 75% (not just 100%) | [ ] |
| 7 | SLA: Name correctly identifies P1 Incident Resolution | [ ] |
| 8 | Email: P1 notification has meaningful subject line | [ ] |
| 9 | Email: Variables use ${} syntax | [ ] |
| 10 | Email: P1 notification has recipients (groups and users) | [ ] |
| 11 | Email: SLA breach notification fires for all priorities | [ ] |
| 12 | Email: Change approval sent to approver (not requester) | [ ] |
| 13 | Email: Reply action is "Add to work notes" (not Delete) | [ ] |
| 14 | Config: Admin uses SSO/MFA (not weak password) | [ ] |
| 15 | Config: ACLs are enabled | [ ] |
| 16 | Config: Session timeout is 30 minutes | [ ] |
| 17 | Config: Named update set (not Default) | [ ] |
| 18 | Config: CMDB discovery uses data center IP range | [ ] |
| 19 | Config: Integration credentials reference secrets vault | [ ] |
| 20 | MCQ: Assessment completed with >= 70% score | [ ] |
| 21 | Role Play: Participated in Round 1 (Major Incident) | [ ] |
| 22 | Role Play: Participated in Round 2 (Change + Problem) | [ ] |

---

## Self-Check Questions

1. **Why does Priority=5 in the start condition break P1 SLAs?** Priority 5 is "Planning" -- the SLA would attach to trivial issues and never attach to real P1 incidents.
2. **What happens if you pause the SLA during "In Progress"?** The SLA timer stops every time someone starts working. Engineers could manipulate the timer by toggling states.
3. **Why use ${variable} not {variable}?** ServiceNow's template engine requires the dollar sign prefix. Without it, the literal text "{number}" appears in the email.
4. **Why must credentials go in a vault, not config files?** Config files can be accidentally shared, committed to version control, or accessed by unauthorized users. Vaults provide access control, rotation, and audit trails.
5. **What is the "Default" update set problem?** Changes in Default cannot be exported, tracked, or promoted. If you need to move configurations from Dev to Prod, you cannot extract Default changes.
