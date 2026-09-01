# Git & GitHub -- Lab Exercises
## Module 19 | Day 20

---

## Client Email

```
From: amit.verma@foodexpress.in
To: sustain-engineering@team.com
Subject: Git Repository Cleanup Needed
Date: 2026-07-30

Team,

Our FoodExpress menu-service Git repository has several problems
that are blocking our workflow:

1. The .gitignore is missing entries, and someone committed
   node_modules and .env files
2. Several commit messages are unclear or wrong
3. There are merge conflicts in a pending PR
4. Branch naming doesn't follow our conventions

Please fix these issues and document the correct Git workflow
for new team members.

-- Amit Verma, Tech Lead, FoodExpress
```

---

## Lab 1: Fix the .gitignore (6 bugs)

### Buggy .gitignore

```bash
# FoodExpress Menu Service .gitignore

# Bug 1: node_modules not ignored (missing entry)

# Bug 2: .env file not ignored
.env.example

# Dependencies
package-lock.json          # Bug 3: This file SHOULD be tracked

# Build output
dist/

# Bug 4: Ignoring all .js files (way too broad!)
*.js

# IDE files
.idea/

# Bug 5: Missing OS-specific files
# (no .DS_Store or Thumbs.db entries)

# Bug 6: Ignoring test files -- tests should be tracked!
__tests__/
*.test.js
*.spec.js
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | `node_modules/` is missing from .gitignore, so the entire directory (thousands of files) gets committed | Bloated repo, slow clones, version conflicts |
| 2 | `.env.example` is ignored but `.env` is not -- it's backwards. `.env` has secrets; `.env.example` is a template | Database passwords and API keys exposed in Git history |
| 3 | `package-lock.json` should be tracked -- it ensures reproducible builds | Different developers get different dependency versions |
| 4 | `*.js` ignores ALL JavaScript files, including source code | No JavaScript source code would ever be committed |
| 5 | OS-specific files like `.DS_Store` (Mac) and `Thumbs.db` (Windows) are not ignored | Unnecessary files cluttering the repository |
| 6 | Test files (`__tests__/`, `*.test.js`, `*.spec.js`) should NOT be ignored -- tests are code | Tests not tracked means they can be lost |

### Fixed .gitignore

```bash
# FoodExpress Menu Service .gitignore

# Dependencies
node_modules/

# Environment files (secrets!)
.env
.env.local
.env.production

# Build output
dist/
build/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Coverage reports
coverage/
```

### Checkpoint
- [ ] `node_modules/` is ignored
- [ ] `.env` is ignored but `.env.example` is NOT
- [ ] `package-lock.json` is NOT ignored
- [ ] Source `.js` files are NOT ignored
- [ ] OS files (`.DS_Store`, `Thumbs.db`) are ignored
- [ ] Test files are NOT ignored

### Bonus: Remove already-committed files

```bash
# If node_modules was already committed:
git rm -r --cached node_modules/
git commit -m "Remove node_modules from tracking"

# If .env was already committed:
git rm --cached .env
git commit -m "Remove .env from tracking

IMPORTANT: Rotate all credentials in .env immediately.
Git history still contains the old values."
```

---

## Lab 2: Fix the Commit Messages (5 bugs)

### Buggy Git Log

```
$ git log --oneline

a1b2c3d stuff
d4e5f6a fixed it.
g7h8i9j WIP
k0l1m2n CHANGES TO MENU AND CART AND ORDER AND PAYMENT AND EVERYTHING
p3q4r5s update file
```

### Bugs to Find and Fix

| # | Original | Problem | Better Message |
|---|----------|---------|----------------|
| 1 | `stuff` | Completely meaningless; no one knows what changed | `feat(menu): Add vegetarian filter to menu page` |
| 2 | `fixed it.` | No context on what was fixed; ends with period | `fix(cart): Correct quantity calculation for combo meals` |
| 3 | `WIP` | Work-in-progress committed to main branch; should have been squashed | `refactor(order): Extract price formatter to utility module` |
| 4 | `CHANGES TO MENU AND...` | All caps; too many changes in one commit (should be split) | Split into separate commits per feature/fix |
| 5 | `update file` | Doesn't say which file or why it was updated | `docs(api): Update menu endpoint documentation with new fields` |

### FoodExpress Commit Convention

```
<type>(<scope>): <subject>

Types: feat, fix, refactor, docs, test, chore, style
Scope: menu, cart, order, payment, auth, config
Subject: imperative mood, no period, max 50 chars

Examples:
feat(menu): Add combo meal category
fix(cart): Handle empty cart checkout gracefully
test(order): Add unit tests for order total calculation
docs(readme): Add API endpoint table
chore(deps): Update Express to v4.18.3
```

### Checkpoint
- [ ] All 5 bad commit messages identified
- [ ] Rewritten messages follow the convention
- [ ] Each message uses imperative mood
- [ ] Messages are under 50 characters for subject line

---

## Lab 3: Resolve Merge Conflicts (4 conflicts)

### Scenario

Two developers on the FoodExpress team made conflicting changes. You need to resolve the merge conflicts.

### Conflict 1: config.js

```javascript
<<<<<<< HEAD
const config = {
  port: 3000,
  dbHost: 'localhost',
  dbPort: 3306,
  taxRate: 0.18,
=======
const config = {
  port: 8080,
  dbHost: 'db.foodexpress.in',
  dbPort: 3306,
  taxRate: 0.12,
>>>>>>> feature/production-config
};
```

**Resolution:** Use environment-specific configuration:

```javascript
const config = {
  port: process.env.PORT || 3000,
  dbHost: process.env.DB_HOST || 'localhost',
  dbPort: parseInt(process.env.DB_PORT) || 3306,
  taxRate: 0.18, // GST rate is fixed at 18%
};
```

### Conflict 2: menu.js

```javascript
<<<<<<< HEAD
function getMenuItems(category) {
  return db.query('SELECT * FROM menu_items WHERE category = ?', [category]);
}
=======
async function getMenuItems(category, isVegetarian) {
  const query = isVegetarian
    ? 'SELECT * FROM menu_items WHERE category = ? AND is_vegetarian = 1'
    : 'SELECT * FROM menu_items WHERE category = ?';
  return await db.query(query, [category]);
}
>>>>>>> feature/veg-filter
```

**Resolution:** Keep both changes (async + vegetarian filter):

```javascript
async function getMenuItems(category, isVegetarian = false) {
  let query = 'SELECT * FROM menu_items WHERE category = ?';
  const params = [category];
  if (isVegetarian) {
    query += ' AND is_vegetarian = 1';
  }
  return await db.query(query, params);
}
```

### Conflict 3: package.json

```json
<<<<<<< HEAD
  "version": "2.3.1",
  "description": "FoodExpress Menu Service",
=======
  "version": "2.4.0",
  "description": "FoodExpress Menu Service - with vegetarian filter",
>>>>>>> feature/veg-filter
```

**Resolution:** Use the higher version, keep description concise:

```json
  "version": "2.4.0",
  "description": "FoodExpress Menu Service",
```

### Conflict 4: README.md

```markdown
<<<<<<< HEAD
## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/menu/items | List all menu items |
| GET | /api/menu/search | Search menu items |
=======
## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/menu/items | List all menu items |
| GET | /api/menu/items?veg=true | List vegetarian items |
>>>>>>> feature/veg-filter
```

**Resolution:** Include all endpoints:

```markdown
## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/menu/items | List all menu items |
| GET | /api/menu/items?veg=true | List vegetarian items |
| GET | /api/menu/search | Search menu items |
```

### Checkpoint
- [ ] All 4 conflicts resolved correctly
- [ ] No conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) remain
- [ ] Merged code combines both developers' intent
- [ ] Resolution committed with a clear merge message

---

## Lab 4: Branch Naming Cleanup (5 bugs)

### Current Branches

```bash
$ git branch -a
* main
  MyFeature                    # Bug 1: No prefix, PascalCase
  bug_fix_123                  # Bug 2: Underscore, no description
  feature/ADD-NEW-MENU-ITEMS   # Bug 3: All caps
  f                            # Bug 4: Too short, meaningless
  test                         # Bug 5: Ambiguous, no prefix
```

### Bugs to Find and Fix

| # | Current Name | Problem | Correct Name |
|---|-------------|---------|-------------|
| 1 | `MyFeature` | No prefix, PascalCase | `feature/my-feature-description` |
| 2 | `bug_fix_123` | Underscores, no meaningful description | `fix/FE-123-price-display-nan` |
| 3 | `feature/ADD-NEW-MENU-ITEMS` | All uppercase | `feature/add-new-menu-items` |
| 4 | `f` | Too short, no context | `feature/add-vegetarian-filter` |
| 5 | `test` | Ambiguous (test what?), no prefix | `feature/add-menu-unit-tests` |

### Renaming a Branch

```bash
# Rename current branch
git branch -m old-name new-name

# Rename and update remote
git push origin -u new-name
git push origin --delete old-name
```

### Checkpoint
- [ ] All 5 branch naming issues identified
- [ ] Correct names follow `<prefix>/<description>` pattern
- [ ] Names use lowercase with hyphens
- [ ] Names are descriptive and include ticket numbers where applicable

---

## Bonus: Agile Role Play

### Instructions

1. Form teams of 4-5
2. Create a shared GitHub repository
3. Each person creates 1 issue (user story or bug)
4. Assign issues, create branches, make changes
5. Open pull requests, review each other's code
6. Resolve any conflicts, merge PRs
7. Close issues and update the project board
8. Run a 5-minute retrospective

**Time limit:** 30 minutes
