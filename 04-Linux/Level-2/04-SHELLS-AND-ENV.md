# Section 8: Shells & Environment Variables

## Day 20 | Linux OS (Day 2) | Time: ~25 minutes

---

## The Scenario

> "The Java app won't start. Error: 'java: command not found'. But Java IS installed. The problem? The PATH environment variable doesn't include Java's directory. You need to understand how the shell finds commands."

---

## 8.1 -- What is a Shell?

A shell is the program that reads your commands and executes them. When you type `ls`, the shell finds and runs the `ls` program.

```bash
# What shell am I using?
echo $SHELL
```
**Output:** `/bin/bash`

### Common shells:

| Shell | Name | Notes |
|-------|------|-------|
| `bash` | **B**ourne **A**gain **Sh**ell | Most common. Default on Ubuntu. |
| `sh` | Bourne Shell | Original. Scripts use `#!/bin/sh` for portability. |
| `zsh` | Z Shell | Default on macOS. Similar to bash with extras. |
| `dash` | Debian Almquist Shell | Minimal, fast. Ubuntu uses it for `/bin/sh`. |

**For sustain engineering:** You'll almost always use `bash`. Scripts should start with `#!/bin/bash`.

---

## 8.2 -- Environment Variables: The Server's Settings

Environment variables are **key=value** pairs that configure how the system and applications behave.

### View all environment variables:

```bash
env
```

Shows ALL variables. It's a long list. Filter it:

```bash
env | grep -i java
env | grep PATH
env | grep HOME
```

### Important environment variables:

| Variable | What It Contains | Example |
|----------|-----------------|---------|
| `PATH` | Directories where shell looks for commands | `/usr/bin:/usr/local/bin:/opt/java/bin` |
| `HOME` | Your home directory | `/home/pappu` |
| `USER` | Your username | `pappu` |
| `SHELL` | Your default shell | `/bin/bash` |
| `PWD` | Current working directory | `/home/pappu/foodexpress-server` |
| `LANG` | Language/locale | `en_US.UTF-8` |
| `JAVA_HOME` | Where Java is installed | `/usr/lib/jvm/java-17-openjdk` |
| `TERM` | Terminal type | `xterm-256color` |

### Read a specific variable:

```bash
echo $HOME
# Output: /home/pappu

echo $PATH
# Output: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

echo $USER
# Output: pappu
```

**Note:** Use `$` before the variable name to read its value. Without `$`, it's just the literal text "HOME".

---

## 8.3 -- PATH: How the Shell Finds Commands

When you type `java`, the shell searches each directory in `PATH` from left to right until it finds a `java` executable.

```bash
echo $PATH
```
**Output:** `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`

Directories are separated by `:`. The shell checks:
1. `/usr/local/sbin/java` -- exists? No. Next.
2. `/usr/local/bin/java` -- exists? No. Next.
3. `/usr/sbin/java` -- exists? No. Next.
4. `/usr/bin/java` -- exists? **Yes!** Run it.

If none match: `java: command not found`

### Fix "command not found" by adding to PATH:

```bash
# Temporarily (current session only)
export PATH=$PATH:/opt/java/bin

# Verify
echo $PATH
# Now includes /opt/java/bin at the end
```

---

## 8.4 -- Setting Variables

### Local variable (current session only):

```bash
APP_NAME="order-service"
echo $APP_NAME
# Output: order-service
```

**Note:** No spaces around `=`. `APP_NAME = "value"` will FAIL (common mistake from Day 1 lab).

### Export variable (available to child processes):

```bash
export APP_NAME="order-service"
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
export PATH=$PATH:$JAVA_HOME/bin
```

| Keyword | Scope |
|---------|-------|
| `VAR=value` | Only in current shell (local) |
| `export VAR=value` | Current shell + any programs/scripts launched from it |

**Without `export`:** If you set `JAVA_HOME` without export, a script you run won't see it.

---

## 8.5 -- Making Variables Permanent: .bashrc and .profile

Variables set with `export` disappear when you log out. To make them permanent:

### Edit ~/.bashrc (runs every time you open a terminal):

```bash
nano ~/.bashrc
```

Add at the end:

```bash
# Custom environment variables
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
export PATH=$PATH:$JAVA_HOME/bin
export APP_ENV="production"
```

Save and reload:

```bash
source ~/.bashrc
```

`source` = re-read the file without logging out. Same as `. ~/.bashrc` (dot space filename).

### .bashrc vs .profile vs .bash_profile:

| File | When It Runs | Use For |
|------|-------------|---------|
| `~/.bashrc` | Every new terminal/SSH session | Aliases, custom PATH, variables |
| `~/.profile` | Login shells only | System-wide settings |
| `~/.bash_profile` | Login shells (bash-specific) | Same as .profile for bash |
| `/etc/environment` | All users, all shells | System-wide PATH, LANG |

**Rule of thumb:** Put your stuff in `~/.bashrc`. It always works.

---

## 8.6 -- Useful Variable Tricks

### Unset a variable:

```bash
unset APP_NAME
echo $APP_NAME
# Output: (empty)
```

### Default value if variable is not set:

```bash
echo ${DB_HOST:-localhost}
# If DB_HOST is set, prints its value
# If DB_HOST is NOT set, prints "localhost"
```

### Check if a variable exists:

```bash
if [ -z "$JAVA_HOME" ]; then
    echo "JAVA_HOME is NOT set"
else
    echo "JAVA_HOME = $JAVA_HOME"
fi
```

`-z` = is the string **z**ero length (empty)?

---

## 8.7 -- Aliases: Shortcuts for long commands

```bash
# Create an alias
alias ll='ls -lah'
alias grep='grep --color=auto'
alias errors='grep -c ERROR ~/foodexpress-server/var/log/foodexpress/app.log'
alias logs='tail -f /var/log/foodexpress/app.log'

# Use it
ll
errors
logs
```

### Make aliases permanent:

Add them to `~/.bashrc`:

```bash
echo "alias ll='ls -lah'" >> ~/.bashrc
echo "alias logs='tail -f /var/log/foodexpress/app.log'" >> ~/.bashrc
source ~/.bashrc
```

### Remove an alias:

```bash
unalias ll
```

---

## Practice Exercises

| # | Task | Command |
|---|------|---------|
| 1 | What shell are you using? | `echo $SHELL` |
| 2 | What is your home directory? | `echo $HOME` |
| 3 | Print your full PATH | `echo $PATH` |
| 4 | Where is `grep` installed? | `which grep` |
| 5 | Set a variable APP_NAME to "foodexpress" | `export APP_NAME="foodexpress"` |
| 6 | Verify it | `echo $APP_NAME` |
| 7 | Add /opt/scripts to your PATH | `export PATH=$PATH:/opt/scripts` |
| 8 | Create an alias `errors` for counting errors | `alias errors='grep -c ERROR ~/foodexpress-server/var/log/foodexpress/app.log'` |
| 9 | Make it permanent | `echo "alias errors='...'" >> ~/.bashrc && source ~/.bashrc` |
| 10 | Unset APP_NAME | `unset APP_NAME` |
