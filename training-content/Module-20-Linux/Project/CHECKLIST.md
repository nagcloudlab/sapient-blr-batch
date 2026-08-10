# Linux OS -- Submission Checklist
## Module 20 | Days 21-22

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Log Analysis: All 6 buggy commands fixed | [ ] |
| 2 | Log Analysis: All 5 analysis questions answered with commands | [ ] |
| 3 | Deploy Script: `set -euo pipefail` added | [ ] |
| 4 | Deploy Script: Variable assignment has no spaces around `=` | [ ] |
| 5 | Deploy Script: VERSION argument validated | [ ] |
| 6 | Deploy Script: All variables quoted | [ ] |
| 7 | Deploy Script: Script exits on errors | [ ] |
| 8 | Deploy Script: Rollback implemented | [ ] |
| 9 | Disk Cleanup: Correct `du`, `find` commands | [ ] |
| 10 | Disk Cleanup: Crontab entry targets only `.log` files | [ ] |
| 11 | Health Check: curl has timeout | [ ] |
| 12 | Health Check: Variables quoted in comparisons | [ ] |
| 13 | Health Check: Logging and alerting added | [ ] |
| 14 | Health Check: Non-zero exit code on failure | [ ] |

---

## Self-Check Questions

1. **What does `grep -w` do differently from `grep`?** It matches whole words only, preventing partial matches.
2. **Why do we use `set -euo pipefail` in scripts?** `e` exits on error, `u` errors on undefined variables, `pipefail` catches failures in piped commands.
3. **What is the difference between `find -mtime 30` and `find -mtime +30`?** Without `+`, it means exactly 30 days ago. With `+`, it means more than 30 days ago.
4. **Why should you archive before deleting old logs?** Compliance requirements, debugging historical incidents, legal holds.
5. **What is the difference between a hard link and a symbolic link?** Hard link shares the inode (same file); symbolic link is a pointer (breaks if original is deleted).
6. **How do you follow a log file in real-time?** `tail -f filename.log`
7. **What does `du -sh` do?** Shows total size of a directory in human-readable format.
8. **Why quote variables in `if [ "$VAR" = "value" ]`?** Without quotes, if `$VAR` is empty, the command becomes `[ = "value" ]` which is a syntax error.
9. **What does `crontab -l` show?** Lists the current user's scheduled cron jobs.
10. **How do you compress a tar archive with gzip?** Add the `-z` flag: `tar -czvf archive.tar.gz directory/`
