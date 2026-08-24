# Section 6: Job Control -- "Run it in the background"

## Day 20 | Linux OS (Day 2) | Time: ~20 minutes

---

## The Scenario

> "You need to run a long backup while still working on other things. You need to monitor logs AND restart a service at the same time. You can't just stare at one command and wait."

---

## 6.1 -- Running a command in the background: &

Add `&` at the end of any command to run it in the background.

```bash
sleep 60 &
```

**Output:**
```
[1] 12345
```

`[1]` = job number. `12345` = process ID (PID). The command runs in the background and you get your prompt back immediately.

**Real example:**
```bash
# Run a backup in the background while you continue working
tar -czvf /tmp/backup.tar.gz /var/log/ &

# Watch logs in the background
tail -f /var/log/foodexpress/app.log &
```

---

## 6.2 -- jobs: See what's running in the background

```bash
jobs
```

**Output:**
```
[1]+  Running    sleep 60 &
[2]-  Running    tail -f /var/log/foodexpress/app.log &
```

| Symbol | Meaning |
|--------|---------|
| `[1]` | Job number |
| `+` | Most recent job |
| `-` | Second most recent job |
| `Running` | Currently running |
| `Stopped` | Paused (Ctrl+Z) |
| `Done` | Finished |

---

## 6.3 -- Ctrl+Z: Pause a running command

You're running `top` or `tail -f` and want to pause it temporarily:

1. Press **Ctrl+Z** -- the command pauses (stops)
2. You get your prompt back
3. The command is NOT killed -- it's just frozen

**Output:**
```
[1]+  Stopped    top
```

---

## 6.4 -- bg: Resume a paused command in the background

After pressing Ctrl+Z, the command is stopped. Resume it in the background:

```bash
bg
```

`bg` = **b**ack**g**round. Resumes the most recently stopped job in the background.

```bash
bg %1    # Resume job number 1 specifically
```

---

## 6.5 -- fg: Bring a background command to the foreground

```bash
fg
```

`fg` = **f**ore**g**round. Brings the most recent background job back to your screen.

```bash
fg %2    # Bring job number 2 to the foreground
```

---

## 6.6 -- The Complete Flow

```
Command running (foreground)
    │
    ├── Ctrl+Z ──> Stopped (paused)
    │                  │
    │                  ├── bg ──> Running (background)
    │                  │              │
    │                  │              └── fg ──> Running (foreground)
    │                  │
    │                  └── fg ──> Running (foreground)
    │
    └── & (at end) ──> Running (background) from the start
```

### Practical example:

```bash
# Step 1: Start watching logs
tail -f ~/foodexpress-server/var/log/foodexpress/app.log

# Step 2: Oh wait, I need to run another command. Press Ctrl+Z
# Output: [1]+  Stopped    tail -f ...

# Step 3: Put it in the background
bg
# Output: [1]+ tail -f ... &

# Step 4: Now run your other command
grep -c "ERROR" ~/foodexpress-server/var/log/foodexpress/app.log

# Step 5: Bring tail back to foreground when done
fg
```

---

## 6.7 -- nohup: Keep running after you log out

When you SSH out, all your background jobs die. `nohup` prevents that.

```bash
nohup java -jar /opt/app.jar &
```

| Part | Stands For | What It Does |
|------|-----------|-------------|
| `nohup` | **no** **h**ang **up** | Don't kill this process when I log out |
| `&` | background | Run it in the background |

**Output goes to `nohup.out`** by default. Or redirect it:

```bash
nohup java -jar /opt/app.jar > /var/log/app.log 2>&1 &
#                               │                 │
#                               │                 └── 2>&1 = send errors to same file
#                               └── redirect output to this log file
```

**Sustain context:** You deploy a Java app on the server and need it to keep running after you close your SSH session. Without `nohup`, the app dies when you disconnect.

---

## Practice Exercises

| # | Task | Commands |
|---|------|---------|
| 1 | Start a sleep 120 in the background | `sleep 120 &` |
| 2 | Check running background jobs | `jobs` |
| 3 | Start `top`, pause it, put it in background | `top` → Ctrl+Z → `bg` |
| 4 | Bring it back to foreground | `fg` |
| 5 | Run a command that survives logout | `nohup sleep 300 &` |
| 6 | Kill a background job | `kill %1` (kill job number 1) |
