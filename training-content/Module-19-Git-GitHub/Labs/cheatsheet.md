# Git Commands Quick Reference

> Single-page reference for everyday Git usage. Replace `<branch>`, `<file>`, `<remote>` with actual values.

---

## Setup

| Command | Example | Description |
|---|---|---|
| `git config --global user.name "Name"` | `git config --global user.name "Nagabhushanam"` | Set commit author name |
| `git config --global user.email "email"` | `git config --global user.email "naga@sapient.com"` | Set commit author email |
| `git config --global core.editor "code --wait"` | `git config --global core.editor "vim"` | Set default editor |
| `git config --list` | `git config --list` | View all config values |
| `git init` | `git init foodexpress` | Initialise new local repo |
| `git clone <url>` | `git clone https://github.com/org/foodexpress.git` | Clone remote repo locally |
| `git clone <url> <dir>` | `git clone https://github.com/org/foodexpress.git fe-app` | Clone into named directory |

---

## Basic Workflow

| Command | Example | Description |
|---|---|---|
| `git status` | `git status` | Show working tree and staging state |
| `git add <file>` | `git add src/app.js` | Stage a specific file |
| `git add .` | `git add .` | Stage all changes in current directory |
| `git add -p` | `git add -p` | Interactively stage hunks |
| `git commit -m "message"` | `git commit -m "feat: add order tracking endpoint"` | Commit with inline message |
| `git commit --amend` | `git commit --amend` | Modify the last commit (message or content) |
| `git diff` | `git diff` | Show unstaged changes |
| `git diff --staged` | `git diff --staged` | Show staged changes vs last commit |
| `git diff <branch1> <branch2>` | `git diff main feature/payment` | Compare two branches |
| `git log` | `git log` | Full commit history |
| `git log --oneline` | `git log --oneline` | Compact one-line history |
| `git log --oneline --graph --all` | `git log --oneline --graph --all` | Visual branch graph |
| `git log --author="Name"` | `git log --author="Naga"` | Filter commits by author |
| `git show <commit>` | `git show a3f9b12` | Show changes in a commit |

---

## Branching

| Command | Example | Description |
|---|---|---|
| `git branch` | `git branch` | List local branches |
| `git branch -a` | `git branch -a` | List local and remote branches |
| `git branch <name>` | `git branch feature/order-history` | Create new branch |
| `git checkout <branch>` | `git checkout feature/order-history` | Switch to branch |
| `git checkout -b <branch>` | `git checkout -b feature/payment-gateway` | Create and switch in one step |
| `git switch <branch>` | `git switch main` | Switch branch (modern syntax) |
| `git switch -c <branch>` | `git switch -c hotfix/menu-bug` | Create and switch (modern syntax) |
| `git branch -d <branch>` | `git branch -d feature/order-history` | Delete branch (safe, merged only) |
| `git branch -D <branch>` | `git branch -D feature/abandoned` | Force-delete branch |
| `git merge <branch>` | `git merge feature/payment-gateway` | Merge branch into current |
| `git merge --no-ff <branch>` | `git merge --no-ff feature/login` | Merge with merge commit (no fast-forward) |
| `git merge --squash <branch>` | `git merge --squash feature/cleanup` | Squash all commits into one before merging |

---

## Remote

| Command | Example | Description |
|---|---|---|
| `git remote -v` | `git remote -v` | List remotes with URLs |
| `git remote add <name> <url>` | `git remote add origin https://github.com/org/foodexpress.git` | Add a remote |
| `git remote remove <name>` | `git remote remove old-origin` | Remove a remote |
| `git fetch <remote>` | `git fetch origin` | Download remote changes without merging |
| `git fetch --all` | `git fetch --all` | Fetch all remotes |
| `git pull` | `git pull` | Fetch + merge current branch from remote |
| `git pull --rebase` | `git pull --rebase` | Fetch + rebase instead of merge |
| `git push <remote> <branch>` | `git push origin feature/payment-gateway` | Push branch to remote |
| `git push -u origin <branch>` | `git push -u origin feature/payment-gateway` | Push and set upstream tracking |
| `git push --force-with-lease` | `git push --force-with-lease` | Safe force-push (fails if remote changed) |
| `git push origin --delete <branch>` | `git push origin --delete feature/old-feature` | Delete remote branch |

---

## Undoing

| Command | Example | Description |
|---|---|---|
| `git restore <file>` | `git restore src/app.js` | Discard unstaged changes in file |
| `git restore --staged <file>` | `git restore --staged src/app.js` | Unstage a file |
| `git reset HEAD~1` | `git reset HEAD~1` | Undo last commit, keep changes staged |
| `git reset --soft HEAD~1` | `git reset --soft HEAD~1` | Undo last commit, keep changes staged |
| `git reset --mixed HEAD~1` | `git reset --mixed HEAD~1` | Undo last commit, unstage changes |
| `git reset --hard HEAD~1` | `git reset --hard HEAD~1` | Undo last commit, discard all changes |
| `git revert <commit>` | `git revert a3f9b12` | Create new commit that undoes a prior commit (safe for shared history) |
| `git stash` | `git stash` | Save working changes temporarily |
| `git stash push -m "message"` | `git stash push -m "WIP: order filter"` | Stash with description |
| `git stash list` | `git stash list` | List all stashes |
| `git stash pop` | `git stash pop` | Apply latest stash and remove it |
| `git stash apply stash@{n}` | `git stash apply stash@{1}` | Apply specific stash, keep it in list |
| `git stash drop stash@{n}` | `git stash drop stash@{0}` | Delete a specific stash |
| `git clean -fd` | `git clean -fd` | Remove untracked files and directories |

---

## Advanced

| Command | Example | Description |
|---|---|---|
| `git rebase <branch>` | `git rebase main` | Replay current branch commits on top of `main` |
| `git rebase -i HEAD~n` | `git rebase -i HEAD~3` | Interactive rebase: squash, reorder, edit last n commits |
| `git cherry-pick <commit>` | `git cherry-pick a3f9b12` | Apply a single commit onto current branch |
| `git cherry-pick <c1>..<c2>` | `git cherry-pick a3f9b12..d8e0c45` | Apply a range of commits |
| `git tag <name>` | `git tag v1.0.0` | Create lightweight tag |
| `git tag -a <name> -m "msg"` | `git tag -a v1.0.0 -m "Production release"` | Create annotated tag |
| `git push origin <tag>` | `git push origin v1.0.0` | Push tag to remote |
| `git push origin --tags` | `git push origin --tags` | Push all tags |
| `git bisect start` | `git bisect start` | Start binary search for regression |
| `git bisect good <commit>` | `git bisect good v0.9.0` | Mark commit as good |
| `git bisect bad` | `git bisect bad` | Mark current commit as bad |
| `git blame <file>` | `git blame src/order.js` | Show who last modified each line |
| `git shortlog -sn` | `git shortlog -sn` | Commit count per author |

---

## .gitignore Patterns

| Pattern | Matches |
|---|---|
| `node_modules/` | The `node_modules` directory anywhere |
| `*.log` | All `.log` files |
| `!important.log` | Exception: do not ignore `important.log` |
| `dist/` | The `dist` directory |
| `.env` | The `.env` file (keep secrets out of repo) |
| `**/*.class` | All `.class` files in any subdirectory |

---

*FoodExpress Training | Module 19: Git & GitHub | Publicis Sapient Sustain Eng 2026*
