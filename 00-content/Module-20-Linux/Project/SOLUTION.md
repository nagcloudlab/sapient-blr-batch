# Linux OS -- Trainer Solutions & Hints
## Module 20 | Days 21-22

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Log Analysis | Use `grep -w` for word boundaries, `grep -c` for counting, `egrep` for extended regex, `awk` for field extraction | Students pipe everything through `cat` unnecessarily (`cat file \| grep` instead of `grep pattern file`). Teach "useless use of cat" | Ask: "How would you find the top 5 error types in a 10GB log file?" |
| 2 | Fix Deploy Script | `set -euo pipefail`, no spaces in assignment, quote all variables, validate args, add rollback | #1 pitfall: students don't understand why spaces around `=` break things (bash parses `APP_NAME` as a command). Demo this live | Ask: "What happens if you deploy and the health check fails at 2 AM?" |
| 3 | Disk Cleanup | `du -sh`, `find -size +100M`, `find -mtime +30`, `tar -czvf`, crontab targets `.log` only | Students use `find -mtime 30` (exactly 30 days) instead of `+30` (older than). Also deleting without archiving first | Ask: "What if legal needs logs from 3 months ago?" (Archive before delete) |
| 4 | Health Check | `curl --max-time 5`, quote `"$result"`, add logging and exit codes, handle curl failure | Students test with services running and never see the failure path. Have them test with a stopped service | Ask: "What if curl hangs forever because the network is down?" |
| 5 | Log Rotation | Combine `find`, `gzip`, `date`, functions; handle edge cases (no files to rotate) | Students forget to handle the case where no files match the criteria (empty loop) | Suggest: "Test with `echo` commands first before actually deleting anything" |

---

## Key Discussion Points

1. Why is `tail -f` the most important command for sustain engineers? (Real-time log monitoring)
2. When would you use `rsync` instead of `scp`? (Incremental sync, bandwidth efficiency)
3. Why `set -euo pipefail`? (e = exit on error, u = error on undefined vars, o pipefail = catch pipe failures)
4. Why quote variables in bash? (Prevent word splitting and globbing)
5. How does crontab differ from systemd timers? (Timers have better logging, dependency management)
