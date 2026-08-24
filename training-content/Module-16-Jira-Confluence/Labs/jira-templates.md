# Jira Issue Templates for FoodExpress

Use these templates when creating Jira issues for FoodExpress sustain work.

---

## Bug Report Template

**Project:** FOOD (FoodExpress)
**Issue Type:** Bug
**Priority:** P1/P2/P3/P4

### Summary
[Service] Brief description of the issue

### Description
**Environment:** Production / Staging / Dev
**Service:** Restaurant Service / Cart Service / Order Service / Delivery Service / Frontend
**Browser/Client:** (if frontend)

**Steps to Reproduce:**
1.
2.
3.

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages/Logs:**
```
[Paste relevant logs]
```

**Screenshots:**
[Attach if applicable]

### Labels
`bug`, `[service-name]`, `[priority]`

### Acceptance Criteria
- [ ] Bug no longer reproducible
- [ ] Regression test added
- [ ] No performance degradation
- [ ] Documentation updated (if needed)

---

## Enhancement Request Template

**Issue Type:** Story/Enhancement

### Summary
As a [user type], I want [feature] so that [benefit]

### Description
[Detailed description of the enhancement]

### Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Tests written
- [ ] Documentation updated

### Technical Notes
[Implementation hints, affected files, dependencies]

---

## Incident Template

**Issue Type:** Incident
**Priority:** P1/P2/P3

### Summary
[INC] Brief description -- [Service] [Symptom]

### Description
**Detected:** [Time] via [Alert/Client/Manual]
**Impact:** [Users affected, business impact]
**Current Status:** Investigating / Mitigating / Resolved

### Linked Issues
- Related to: FOOD-XXX
- Caused by: FOOD-XXX (if known)

---

## Change Request Template

**Issue Type:** Change Request
**Change Type:** Standard / Normal / Emergency

### Summary
[CHG] Brief description of the change

### Description
**Service affected:** FoodExpress - [Component]
**Environment:** Production
**Scheduled date:** YYYY-MM-DD HH:MM

### Rollback Plan
[How to undo if it fails]

### Testing Completed
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Tested in staging

### Approvals Required
- [ ] Technical Lead
- [ ] CAB (for Normal/Emergency changes)
