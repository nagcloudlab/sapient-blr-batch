# Contributing to FoodExpress

## Branch Naming Conventions

Use the following prefixes for branch names:

| Type | Prefix | Example |
|------|--------|---------|
| Feature | `feature/` | `feature/add-payment-gateway` |
| Bug Fix | `bugfix/` | `bugfix/fix-order-total` |
| Hotfix | `hotfix/` | `hotfix/payment-timeout` |
| Release | `release/` | `release/v1.2.0` |
| Chore | `chore/` | `chore/update-dependencies` |

### Rules
- Branch names must be lowercase
- Use hyphens (-) to separate words, not underscores
- Include the Jira ticket number when applicable: `feature/FE-123-add-search`

---

## Commit Message Format

```
<type>(<scope>): <short description>

<body - optional>

<footer - optional>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code restructuring (no feature/fix)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(order): add discount code validation
fix(cart): correct total calculation for multiple items
docs(readme): update setup instructions
```

---

## Pull Request Template

When creating a PR, include the following:

### Title
`[FE-XXX] Brief description of changes`

### Description
```
## What
TODO: Describe what this PR does.

## Why
TODO: Explain why this change is needed.

## How
TODO: Describe the approach taken.

## Testing
TODO: Describe how this was tested.
- [ ] Unit tests pass
- [ ] Manual testing done
- [ ] No regressions

## Screenshots (if UI changes)
TODO: Add before/after screenshots.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated (if needed)
- [ ] No new warnings introduced
```

---

## Code Review Guidelines

### As a Reviewer
- Be constructive and specific
- Approve when satisfied, don't block on minor style issues
- Check for: correctness, readability, test coverage, security

### As an Author
- Keep PRs small (< 400 lines of changes)
- Respond to all comments
- Request re-review after making changes
