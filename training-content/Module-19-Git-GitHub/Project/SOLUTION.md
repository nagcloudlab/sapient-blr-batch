# Git & GitHub -- Trainer Solutions & Hints
## Module 19 | Day 20

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix .gitignore | Add `node_modules/`, `.env`; remove `*.js`, test ignores; keep `package-lock.json` | Students forget that `.gitignore` doesn't retroactively remove already-committed files. Need `git rm --cached` | Ask: "If .env was already committed, is adding it to .gitignore enough?" (No -- history still has it) |
| 2 | Commit Messages | Use `<type>(<scope>): <subject>` format, imperative mood, under 50 chars | Students write past tense ("Fixed") instead of imperative ("Fix"). Some over-explain in subject line | Ask: "If I read only the commit message, do I know what changed and why?" |
| 3 | Merge Conflicts | Combine both developers' intent, not just pick one side. Use environment variables for config | Students delete one side entirely instead of merging intent. Conflict 1 (config) is where most struggle | Ask: "How do you handle values that differ between dev and production?" (Environment variables) |
| 4 | Branch Names | Use lowercase, hyphens, prefixes (`feature/`, `fix/`), include ticket numbers | Students create overly long branch names or forget to update the remote | Remind: Branch names should be readable in a `git log --oneline` output |
| 5 | Agile Role Play | Full cycle: Issue -> Branch -> Code -> PR -> Review -> Merge -> Close | Teams skip code review or merge without approval. Some forget to close issues | This exercise reveals workflow gaps. Debrief: "What was the bottleneck?" |

---

## Key Discussion Points

1. Why should `package-lock.json` be tracked but `node_modules/` ignored?
2. What should you do if secrets were committed to Git history? (Rotate immediately, use `git filter-branch` or BFG Repo-Cleaner)
3. When is `git revert` preferred over `git reset`? (When commits are already pushed/shared)
4. What's the difference between `git merge` and `git rebase`? When to use each?
5. How do branch protection rules prevent bad merges to main?

---

## MCQ Answer Key

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | B | `git add .` stages all changes in current directory and subdirectories |
| 2 | B | `git revert` creates a new undo commit, preserving history safely |
| 3 | C | HEAD points to current branch/commit |
| 4 | C | Never rebase commits that have been pushed and shared |
| 5 | B | `.gitignore` tells Git which file patterns to not track |
