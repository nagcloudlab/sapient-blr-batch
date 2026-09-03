# Git & GitHub -- Submission Checklist
## Module 19 | Day 20

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | .gitignore: `node_modules/` ignored | [ ] |
| 2 | .gitignore: `.env` ignored, `.env.example` NOT ignored | [ ] |
| 3 | .gitignore: `package-lock.json` NOT ignored | [ ] |
| 4 | .gitignore: Source `.js` files NOT ignored | [ ] |
| 5 | .gitignore: Test files NOT ignored | [ ] |
| 6 | .gitignore: OS files (`.DS_Store`, `Thumbs.db`) ignored | [ ] |
| 7 | Commit messages follow `<type>(<scope>): <subject>` convention | [ ] |
| 8 | All 4 merge conflicts resolved with no conflict markers remaining | [ ] |
| 9 | Merged code combines both developers' intent | [ ] |
| 10 | All 5 branch names fixed to follow naming conventions | [ ] |
| 11 | Agile role play: at least 2 PRs created and merged | [ ] |
| 12 | Code reviews include meaningful comments | [ ] |

---

## Self-Check Questions

1. **If you add `.env` to `.gitignore` after it was already committed, is it removed from Git?** No -- you need `git rm --cached .env` first.
2. **What happens if you `git push --force` to main?** You overwrite remote history and may destroy teammates' work.
3. **Can you recover a commit after `git reset --hard`?** Yes, within a short window, using `git reflog`.
4. **What does `git stash` do?** Saves uncommitted changes temporarily so you can switch branches cleanly.
5. **Why use `git revert` instead of `git reset` on shared branches?** Revert preserves history; reset rewrites it.
6. **What is a fast-forward merge?** When the target branch has no new commits since the feature branch diverged.
7. **Should you commit generated files (e.g., `dist/`, `build/`)?** No -- they can be regenerated from source.
8. **What is the purpose of `package-lock.json`?** It locks exact dependency versions for reproducible installs.
9. **How do you check what will be committed before committing?** `git diff --staged`
10. **What does HEAD~2 mean?** The commit two steps before the current HEAD (grandparent commit).
