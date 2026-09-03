# Module 20: Linux -- Lab Setup

## Prerequisites

- Bash shell: WSL2 on Windows (Ubuntu recommended), or native terminal on macOS/Linux.
- No additional packages needed beyond a standard Linux installation.

## Running the Starter Code

```bash
cd Labs/starter-code
bash deploy.sh
```

The script will fail with errors -- this is expected. Each failure corresponds to a bug in
`lab-exercises.md`. Fix the script and re-run after each change.

For the log analysis exercise:
```bash
bash analyze-logs.sh /var/log/syslog    # or specify the log file path
```

## Verifying Your Fixes

After each fix, re-run the affected script and check:

```bash
bash deploy.sh               # Should complete all steps without error
bash health-check.sh         # Should print "PASS" for each service check
bash disk-cleanup.sh --dry-run  # Should list files to be removed, not crash
```

Compare actual output against the expected output block in each bug description.

## Expected Behavior

- `deploy.sh` runs all deployment steps and prints a success summary.
- Log analysis script counts ERROR lines correctly and outputs a summary table.
- Health check script exits with code 0 when all services are up, code 1 otherwise.
- Disk cleanup script removes files older than the configured retention period.
- No `command not found` or `permission denied` errors in normal operation.

## Troubleshooting

**Permission denied on scripts:** Run `chmod +x *.sh` in the `starter-code/` directory to make all
shell scripts executable.

**Script runs on Windows line endings:** If you see `^M` in error messages, convert the file with
`dos2unix deploy.sh` (install via `apt install dos2unix` if needed).
