# Module 19: Git & GitHub -- Lab Setup

## Prerequisites

- Git 2.40 or higher (`git --version` to confirm)
- A terminal / command prompt
- GitHub account (for the remote exercise; URL provided by trainer)

## Running the Starter Code

```bash
cd Labs/starter-code
git init
git add .
git commit -m "initial: starter code"
```

Then follow the step-by-step instructions in `lab-exercises.md`. Each exercise builds on the
previous state of the repository, so work through them in order.

## Verifying Your Fixes

Use standard Git inspection commands after each fix:

```bash
git log --oneline --graph    # Check commit history and branch structure
git status                   # Confirm no unintended files are staged
git diff HEAD~1              # Review what changed in the last commit
cat .gitignore               # Verify ignored file patterns
```

For the merge conflict exercise, confirm the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) are
completely removed before committing.

## Expected Behavior

- `.gitignore` excludes `node_modules/`, `*.log`, `.env`, and build artefacts.
- Commit messages follow the `type: short description` convention (feat, fix, chore, docs).
- Feature branch merges into `main` cleanly with no conflict markers left in files.
- `git log` shows a clean, readable history -- no "WIP" or empty commit messages.
- No secrets or credentials appear in the commit history.

## Troubleshooting

**Merge conflict not resolving:** Open the conflicted file, manually choose which lines to keep,
remove all `<<<<<<<` / `=======` / `>>>>>>>` markers, save, then `git add <file>` and `git commit`.

**`.gitignore` not taking effect on already-tracked files:** Run `git rm --cached <file>` to untrack
the file first, then the `.gitignore` rule will apply on the next commit.
