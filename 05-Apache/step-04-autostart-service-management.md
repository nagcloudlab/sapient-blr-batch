# Step 4: Auto-start & Service Management

## Objective
Control Apache's lifecycle: start, stop, restart, reload, enable/disable auto-start on boot.

---

## Check Auto-start Status

```bash
sudo systemctl is-enabled apache2
```

Ubuntu enables it by default on install.

## Full Lifecycle Practice

### Stop Apache

```bash
sudo systemctl stop apache2
sudo systemctl status apache2
curl http://localhost              # Fails -- Connection refused
sudo ss -tlnp | grep :80          # Empty -- nothing listening
```

### Start Apache

```bash
sudo systemctl start apache2
sudo systemctl status apache2
curl -I http://localhost           # 200 OK -- back up
```

## Restart vs Reload -- Critical Difference

### Restart (drops all connections)

```bash
cat /var/run/apache2/apache2.pid           # Note the PID
sudo systemctl restart apache2
cat /var/run/apache2/apache2.pid           # PID changed -- new process
```

### Reload (graceful -- no downtime)

```bash
cat /var/run/apache2/apache2.pid           # Note the PID
sudo systemctl reload apache2
cat /var/run/apache2/apache2.pid           # PID stays same -- config re-read
```

| Command | When to Use | Production Safe? |
|---------|------------|-----------------|
| `reload` | Changed config files | **Yes** -- no downtime |
| `restart` | Added/removed modules | **No** -- drops connections |
| `stop/start` | Troubleshooting | **No** -- server goes down |

## Config Test Before Reload (Build This Habit)

```bash
sudo apache2ctl configtest
```

Should say `Syntax OK`. Always run this before `reload` or `restart` in production.

### Break it on purpose

```bash
echo "GARBAGE" | sudo tee -a /etc/apache2/apache2.conf
sudo apache2ctl configtest           # Shows error!
```

Fix it:

```bash
sudo sed -i '/GARBAGE/d' /etc/apache2/apache2.conf
sudo apache2ctl configtest           # Syntax OK again
```

## Enable / Disable Auto-start

```bash
# Disable -- won't start on reboot
sudo systemctl disable apache2
sudo systemctl is-enabled apache2    # disabled

# Re-enable -- starts on reboot
sudo systemctl enable apache2
sudo systemctl is-enabled apache2    # enabled
```

---

## Why This Matters in Sustain Engineering

> If the server reboots after a patch or crash, Apache must come back automatically. If you forget `enable`, your website goes down until someone manually starts it. This is a real production incident cause.

**Golden rule:** `apache2ctl configtest` --> then `reload`. Never reload without testing first.

---

## Key Takeaway

- Use `reload` for config changes (safe, no downtime)
- Use `restart` only for module changes
- Always `configtest` before reload/restart
- Always `enable` Apache on production servers
