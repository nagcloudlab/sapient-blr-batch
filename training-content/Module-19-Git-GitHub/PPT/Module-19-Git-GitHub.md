# Git & GitHub
## Module 19 | Sustain Engineering Training | Day 20

---

## Agenda

| # | Topic |
|---|-------|
| 01 | Version Control: Why It Matters |
| 02 | Git Fundamentals: Init, Clone, Status |
| 03 | Working Directory, Staging, Commits |
| 04 | Push, Pull, Remote Repositories |
| 05 | Undo & Fix Mistakes |
| 06 | Common Git Errors & Solutions |
| 07 | Branching & Merging |
| 08 | Branch Naming & Strategy |
| 09 | Collaboration: PRs, Reviews, Conflicts |
| 10 | README & Documentation |
| 11 | MCQ Quiz |
| 12 | Agile Role Play & Wrap-up |

---

## What Is Version Control?

### The Problem

Without version control:
- "Which file is the latest?"
- "Who changed this and why?"
- "Can we go back to last week's version?"
- "How do we work on the same file simultaneously?"

### The Solution

> **Version Control System (VCS):** Software that tracks changes to files over time, enabling collaboration, history, and rollback.

---

## Types of Version Control

| Type | Description | Examples |
|------|-------------|---------|
| **Local VCS** | Changes tracked on local machine only | RCS |
| **Centralized VCS** | Single server holds all versions | SVN, CVS |
| **Distributed VCS** | Every developer has full history | **Git**, Mercurial |

### Why Distributed?

```
Centralized (SVN):              Distributed (Git):
                                Dev A ←→ Dev B
Server ←→ Dev A                    ↕       ↕
  ↕                              Remote Server
Dev B                              ↕
                                Dev C
```

- Work offline, full history on every machine
- No single point of failure

---

## Git: The Basics

### What Is Git?

- Created by Linus Torvalds (2005) for Linux kernel development
- **Distributed** version control system
- Tracks content changes, not files
- Uses SHA-1 hashes for integrity
- Incredibly fast and efficient

### Git vs GitHub

| Git | GitHub |
|-----|--------|
| Version control tool | Hosting platform for Git repos |
| Runs locally | Runs in the cloud |
| Command-line based | Web-based UI + API |
| Free, open source | Free tier + paid plans |

---

## Git Installation & Setup

### First-Time Configuration

```bash
# Set your identity
git config --global user.name "Priya Sharma"
git config --global user.email "priya.sharma@foodexpress.in"

# Set default branch name
git config --global init.defaultBranch main

# Set default editor
git config --global core.editor "code --wait"

# View all settings
git config --list

# View specific setting
git config user.name
```

---

## Creating a Repository

### Two Ways to Start

```bash
# Option 1: Initialize a new repo
mkdir foodexpress-menu-service
cd foodexpress-menu-service
git init
# Creates .git/ directory (hidden)

# Option 2: Clone an existing repo
git clone https://github.com/foodexpress/menu-service.git
cd menu-service
# Already has .git/ with full history
```

### What's Inside .git/?

```
.git/
├── HEAD            # Points to current branch
├── config          # Repository settings
├── objects/        # All content (blobs, trees, commits)
├── refs/           # Branch and tag pointers
├── hooks/          # Pre/post commit scripts
└── index           # Staging area
```

---

## The Three Areas of Git

```
┌──────────────┐    git add     ┌──────────────┐   git commit   ┌──────────────┐
│   Working    │ ──────────────>│   Staging     │ ─────────────>│  Repository  │
│  Directory   │                │  Area (Index) │               │   (.git/)    │
│              │<───────────────│               │               │              │
│  Your files  │   git restore  │ Next commit   │               │  All commits │
└──────────────┘                └──────────────┘               └──────────────┘
```

| Area | Description | Analogy |
|------|-------------|---------|
| Working Directory | Files you're editing | Your desk |
| Staging Area (Index) | Files marked for next commit | Shopping cart |
| Repository | Committed history | Receipt/record |

---

## Git Status: Know Where You Are

```bash
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/menu.js          # Staged (green)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   src/cart.js           # Modified (red)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/ratings.js                    # New file (red)
```

### Short Status

```bash
$ git status -s
M  src/menu.js       # M in first column = staged
 M src/cart.js       # M in second column = modified
?? src/ratings.js    # ?? = untracked
```

---

## Git Add: Staging Changes

```bash
# Stage a specific file
git add src/menu.js

# Stage multiple files
git add src/menu.js src/cart.js

# Stage all changes in current directory
git add .

# Stage all changes in the repo
git add -A

# Stage parts of a file (interactive)
git add -p src/menu.js

# Unstage a file (keep changes in working dir)
git restore --staged src/menu.js
```

**FoodExpress best practice:** Stage specific files, not `git add .` to avoid accidentally staging debug files or secrets.

---

## Git Commit: Save a Snapshot

```bash
# Commit with a message
git commit -m "Add combo meal pricing to menu service"

# Commit with multi-line message
git commit -m "Fix price calculation bug

- Handle currency prefix in parseFloat
- Add fallback for NaN values
- Ref: FE-001"

# Amend the last commit (change message or add files)
git commit --amend -m "Updated commit message"

# View commit history
git log
git log --oneline
git log --oneline --graph --all
```

---

## Writing Good Commit Messages

### The 7 Rules

| Rule | Example |
|------|---------|
| 1. Separate subject from body with blank line | ✓ |
| 2. Limit subject to 50 characters | `Fix price NaN bug in checkout` |
| 3. Capitalize the subject line | `Fix`, not `fix` |
| 4. Do not end subject with a period | `Fix bug`, not `Fix bug.` |
| 5. Use imperative mood | `Fix`, not `Fixed` or `Fixes` |
| 6. Wrap body at 72 characters | Use editor, not `-m` for long messages |
| 7. Body explains what and why, not how | Code shows how; message explains why |

### FoodExpress Convention

```
<type>(<scope>): <subject>

fix(menu): Correct price display for combo meals
feat(order): Add order tracking notification
refactor(cart): Extract price formatter utility
docs(api): Update endpoint documentation
```

---

## Git Push & Pull

### Connecting to Remote

```bash
# Add a remote repository
git remote add origin https://github.com/foodexpress/menu-service.git

# View remotes
git remote -v

# Push to remote (first time)
git push -u origin main

# Push subsequent commits
git push

# Pull latest changes from remote
git pull

# Fetch without merging
git fetch origin
```

---

## Push & Pull Workflow

```
Local Repository                    Remote Repository (GitHub)
┌──────────────┐                   ┌──────────────┐
│   main       │ ── git push ────> │   main       │
│   a1b2c3d    │                   │   a1b2c3d    │
│              │ <── git pull ──── │              │
│              │    (fetch+merge)  │   d4e5f6a    │
└──────────────┘                   └──────────────┘
```

### Push Rejected?

```bash
$ git push
! [rejected]  main -> main (non-fast-forward)

# Solution: Pull first, then push
git pull --rebase origin main
git push
```

---

## Undoing Changes

### Different Levels of Undo

| Scenario | Command | What It Does |
|----------|---------|-------------|
| Discard working directory changes | `git restore <file>` | Reverts file to last commit |
| Unstage a file | `git restore --staged <file>` | Moves from staging to working dir |
| Undo last commit (keep changes) | `git reset --soft HEAD~1` | Moves commit back to staging |
| Undo last commit (discard changes) | `git reset --hard HEAD~1` | Destroys the commit and changes |
| Create a new "undo" commit | `git revert <commit>` | Safest option for shared branches |

```bash
# FoodExpress example: Accidentally committed debug logs
# Safe undo (creates a new commit):
git revert abc1234

# View what would be reverted:
git show abc1234
```

---

## Common Git Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `fatal: not a git repository` | Not in a git repo directory | `cd` to repo or `git init` |
| `error: failed to push` | Remote has changes you don't | `git pull --rebase` then push |
| `CONFLICT (content)` | Two people edited same lines | Manually resolve, then commit |
| `fatal: refusing to merge unrelated histories` | Repos have no common ancestor | `git pull origin main --allow-unrelated-histories` |
| `error: Your local changes would be overwritten` | Uncommitted changes conflict with pull | `git stash`, pull, then `git stash pop` |
| `detached HEAD` | Checked out a commit, not a branch | `git checkout main` or create branch |

---

## Git Stash: Temporary Storage

```bash
# Save current changes temporarily
git stash
# or with a message
git stash save "WIP: menu price formatting"

# List stashes
git stash list
# stash@{0}: WIP: menu price formatting
# stash@{1}: On main: cart fix in progress

# Apply most recent stash
git stash pop

# Apply specific stash (keep it in stash list)
git stash apply stash@{1}

# Drop a stash
git stash drop stash@{0}
```

**Use case:** You're fixing a menu bug but an urgent production issue comes in. Stash your work, fix the urgent bug, then pop your stash.

---

## Branching: Parallel Development

### What Is a Branch?

> A **branch** is a lightweight, movable pointer to a commit. Creating a branch is instant and costs almost nothing.

```
main:     A──B──C──D
                    \
feature:             E──F──G

A, B, C = shared history
D = latest on main
E, F, G = feature branch commits
```

---

## Branch Commands

```bash
# Create a new branch
git branch feature/add-ratings

# Switch to a branch
git checkout feature/add-ratings
# or (newer syntax)
git switch feature/add-ratings

# Create AND switch in one command
git checkout -b feature/add-ratings
# or
git switch -c feature/add-ratings

# List all branches
git branch          # local branches
git branch -r       # remote branches
git branch -a       # all branches

# Delete a branch
git branch -d feature/add-ratings     # safe delete
git branch -D feature/add-ratings     # force delete
```

---

## Branch Naming Conventions

### FoodExpress Branch Strategy

| Prefix | Purpose | Example |
|--------|---------|---------|
| `main` | Production-ready code | `main` |
| `develop` | Integration branch | `develop` |
| `feature/` | New feature | `feature/add-combo-meals` |
| `fix/` | Bug fix | `fix/FE-001-price-nan` |
| `hotfix/` | Urgent production fix | `hotfix/payment-crash` |
| `release/` | Release preparation | `release/v2.3.0` |

### Rules

- Use lowercase with hyphens (not underscores or camelCase)
- Include Jira ticket number when applicable
- Keep names descriptive but concise
- Delete branches after merging

---

## Master, Main, and HEAD

### Terminology

| Term | Meaning |
|------|---------|
| `main` (or `master`) | The default branch; typically represents production |
| `HEAD` | Pointer to the current branch/commit you're on |
| `origin` | The default name for the remote repository |
| `HEAD~1` | The commit before HEAD (parent) |
| `HEAD~2` | Two commits before HEAD (grandparent) |

```bash
# Where is HEAD pointing?
$ cat .git/HEAD
ref: refs/heads/main

# After switching branches:
$ git checkout feature/add-ratings
$ cat .git/HEAD
ref: refs/heads/feature/add-ratings
```

---

## Merging Branches

### Fast-Forward Merge

```bash
# When feature branch is ahead of main with no divergence
git checkout main
git merge feature/add-ratings
# Result: main pointer moves forward (no merge commit)

main:     A──B──C──D──E──F
                          ^
                   feature/add-ratings (merged)
```

### Three-Way Merge

```bash
# When both branches have new commits
git checkout main
git merge feature/add-ratings
# Result: new merge commit created

main:     A──B──C──D──────M (merge commit)
                    \     /
feature:             E──F
```

---

## Merge Conflicts

### When Conflicts Happen

Two developers edited the same lines in the same file.

```
<<<<<<< HEAD
  const TAX_RATE = 0.18;    // Your change (current branch)
=======
  const TAX_RATE = 0.12;    // Their change (incoming branch)
>>>>>>> feature/update-tax
```

### How to Resolve

1. Open the conflicted file
2. Choose which change to keep (or combine both)
3. Remove the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
4. Stage and commit

```bash
git add src/config.js
git commit -m "Resolve tax rate conflict: use 18% GST rate"
```

---

## Rebasing vs Merging

### Merge (preserves history)

```
main:     A──B──C──D──────M
                    \     /
feature:             E──F
```

### Rebase (linear history)

```
# Before rebase:
main:     A──B──C──D
feature:       E──F

# After rebase:
main:     A──B──C──D
feature:             E'──F'
```

```bash
git checkout feature/add-ratings
git rebase main
# Replays feature commits on top of main
```

**Rule:** Never rebase commits that have been pushed and shared with others.

---

## Collaboration: Pull Requests

### Pull Request (PR) Workflow

```
1. Create feature branch
   git checkout -b feature/add-ratings

2. Make changes and push
   git push -u origin feature/add-ratings

3. Open PR on GitHub
   Compare: feature/add-ratings → main

4. Code review
   Teammates review, comment, request changes

5. Address feedback
   Push additional commits to the same branch

6. Merge PR
   Squash and merge, or merge commit

7. Delete feature branch
   git branch -d feature/add-ratings
```

---

## Code Review Best Practices

### As a Reviewer

| Do | Don't |
|----|-------|
| Focus on logic and design | Nitpick formatting (use linters) |
| Ask questions to understand | Be condescending |
| Suggest alternatives | Just say "wrong" |
| Review promptly (< 24 hours) | Block PRs for days |
| Approve when "good enough" | Demand perfection |

### As an Author

| Do | Don't |
|----|-------|
| Keep PRs small (< 400 lines) | Submit 2000-line PRs |
| Write a clear description | Leave description empty |
| Self-review before requesting | Push and hope for the best |
| Respond to all comments | Ignore feedback |

---

## README: Project Documentation

### Essential Sections

```markdown
# FoodExpress Menu Service

## Overview
Node.js/Express service for managing restaurant menu items.

## Prerequisites
- Node.js 18+
- MySQL 8.0
- npm 9+

## Setup
git clone https://github.com/foodexpress/menu-service.git
cd menu-service
npm install
cp .env.example .env
npm run dev

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/menu/items | List all menu items |
| GET | /api/menu/search?q= | Search menu items |
| POST | /api/menu/items | Add a menu item |

## Running Tests
npm test

## Contributing
See CONTRIBUTING.md for guidelines.
```

---

## .gitignore: What NOT to Track

```bash
# .gitignore for FoodExpress

# Dependencies
node_modules/
target/

# Environment files (NEVER commit secrets)
.env
.env.local
*.pem

# Build output
dist/
build/
*.jar

# IDE files
.idea/
.vscode/
*.swp

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

**Critical rule:** NEVER commit `.env` files, API keys, passwords, or certificates to Git.

---

## Git Log: Exploring History

```bash
# Basic log
git log

# Compact one-line format
git log --oneline

# Graph view with branches
git log --oneline --graph --all

# Filter by author
git log --author="Priya"

# Filter by date
git log --since="2026-07-01" --until="2026-07-27"

# Filter by file
git log -- src/menu.js

# Search commit messages
git log --grep="price"

# Show changes in each commit
git log -p

# Last 5 commits
git log -5
```

---

## Git Diff: Comparing Changes

```bash
# Changes in working directory (not staged)
git diff

# Changes staged for next commit
git diff --staged

# Compare two branches
git diff main..feature/add-ratings

# Compare specific file between branches
git diff main..feature/add-ratings -- src/menu.js

# Compare with a specific commit
git diff abc1234

# Show stats (files changed, lines added/removed)
git diff --stat
```

---

## GitHub Features for Collaboration

| Feature | Purpose | FoodExpress Use |
|---------|---------|-----------------|
| **Issues** | Track bugs, features, tasks | Bug reports from customers |
| **Pull Requests** | Code review workflow | All changes reviewed before merge |
| **Actions** | CI/CD workflows | Automated testing on every PR |
| **Projects** | Kanban/sprint boards | Sprint planning |
| **Wiki** | Team documentation | Runbooks, architecture docs |
| **Releases** | Version tagging | `v2.3.0` with changelog |
| **Branch Protection** | Enforce rules on branches | Require PR review before merge to main |
| **CODEOWNERS** | Auto-assign reviewers | `src/payment/ @payment-team` |

---

## MCQ Quiz (Sample Questions)

### Question 1
What does `git add .` do?

- A) Commits all changes
- B) Stages all changes in the current directory and subdirectories
- C) Pushes all changes to remote
- D) Creates a new branch

**Answer: B**

### Question 2
What is the safest way to undo a commit that has been pushed?

- A) `git reset --hard HEAD~1`
- B) `git revert <commit>`
- C) Delete the commit on GitHub
- D) `git push --force`

**Answer: B** -- `git revert` creates a new commit that undoes the changes, preserving history.

---

## MCQ Quiz (continued)

### Question 3
What does HEAD point to?

- A) The remote repository
- B) The first commit
- C) The current branch or commit you're on
- D) The latest tag

**Answer: C**

### Question 4
When should you NOT rebase?

- A) Before pushing a feature branch
- B) When working on your own local branch
- C) After commits have been pushed and shared with others
- D) When resolving merge conflicts

**Answer: C** -- Rebasing rewrites history; shared commits should never be rewritten.

### Question 5
What does `.gitignore` do?

- A) Deletes files from the repository
- B) Tells Git which files/patterns to NOT track
- C) Hides files from other developers
- D) Encrypts sensitive files

**Answer: B**

---

## Agile Role Play Exercise

### Scenario: FoodExpress Sprint

**Setup:** Teams of 4-5 simulate a mini sprint using Git & GitHub.

| Role | Responsibility |
|------|---------------|
| Product Owner | Write 3 user stories as GitHub Issues |
| Scrum Master | Create sprint board (GitHub Project), run stand-up |
| Developer 1 | Pick issue, create branch, implement, submit PR |
| Developer 2 | Pick issue, create branch, implement, submit PR |
| Reviewer | Review both PRs, leave comments, approve/request changes |

### Steps

1. **PO:** Create 3 issues (e.g., "Add vegetarian filter", "Fix search bug", "Update footer")
2. **SM:** Assign issues, set priorities
3. **Devs:** Create feature branches, make changes, push, open PRs
4. **Reviewer:** Review PRs, leave at least 2 comments each
5. **Devs:** Address feedback, get approval
6. **SM:** Merge PRs, close issues, update board
7. **All:** 5-minute retrospective

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Version control | Git tracks every change; nothing is ever truly lost |
| Three areas | Working directory -> Staging (add) -> Repository (commit) |
| Branching | Lightweight, instant; use feature branches for all work |
| Merging | Fast-forward or three-way; resolve conflicts manually |
| Push/Pull | Push shares your work; pull gets others' work |
| Undo | `revert` for shared history; `reset` for local only |
| Collaboration | PRs for code review; small PRs, clear descriptions |
| Branch naming | Use prefixes: `feature/`, `fix/`, `hotfix/` |
| .gitignore | Never commit secrets, dependencies, or build artifacts |
| README | Every repo needs setup instructions and API docs |

> **Next: Module 20 -- Linux OS**
