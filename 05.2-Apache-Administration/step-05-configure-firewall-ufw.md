# Step 5: Configure Firewall (UFW)

## Objective
Configure the host-level firewall (UFW) to control which ports are accessible.

---

## Two Layers of Firewall

```
Internet --> GCP Firewall (cloud level) --> UFW (host level) --> Apache (port 80)
              tags: http-server              allow 'Apache'      listening 0.0.0.0:80
              rule: allow tcp:80             allow OpenSSH
```

Both must allow traffic. If either blocks, the request is dropped.

## Check Current Status

```bash
sudo ufw status
```

Should say `inactive`.

## Enable UFW

```bash
sudo ufw enable
```

Say `y` when warned about SSH disruption.

```bash
sudo ufw status verbose
```

Everything blocked by default. Test from outside:

```bash
# From local machine -- should timeout
curl -I http://<EXTERNAL_IP> --max-time 5
```

## Apache Profiles in UFW

```bash
sudo ufw app list
```

Three profiles:

| Profile | Ports |
|---------|-------|
| `Apache` | Port 80 only |
| `Apache Full` | Port 80 + 443 |
| `Apache Secure` | Port 443 only |

Inspect a profile:

```bash
sudo ufw app info 'Apache'
sudo ufw app info 'Apache Full'
```

## Allow HTTP

```bash
sudo ufw allow 'Apache'
sudo ufw status
```

Test from outside -- works now.

## Don't Forget SSH

```bash
sudo ufw allow OpenSSH
sudo ufw status numbered
```

**Critical:** If you forget to allow SSH before enabling UFW on a remote server, you're locked out.

## Practice Removing a Rule

```bash
sudo ufw status numbered
sudo ufw delete 1                   # Remove first rule
sudo ufw status                     # Rule gone
```

Add it back:

```bash
sudo ufw allow 'Apache Full'        # Both 80 and 443
sudo ufw status
```

## Block a Specific IP

```bash
sudo ufw deny from 203.0.113.50
sudo ufw status
```

## Rate-limit SSH (Brute Force Protection)

```bash
sudo ufw delete allow OpenSSH
sudo ufw limit OpenSSH
sudo ufw status
```

`limit` = allows 6 connections in 30 seconds, then blocks.

## Reset Everything

```bash
sudo ufw reset
```

Back to clean slate.

## Recommended Production Setup

```bash
sudo ufw enable
sudo ufw allow 'Apache Full'
sudo ufw limit OpenSSH
sudo ufw status
```

---

## UFW Command Reference

| Command | Purpose |
|---------|---------|
| `ufw enable` | Turn on firewall |
| `ufw disable` | Turn off (not recommended) |
| `ufw allow 'Apache'` | Open port 80 |
| `ufw allow 'Apache Full'` | Open 80 + 443 |
| `ufw limit OpenSSH` | SSH with brute-force protection |
| `ufw status numbered` | See all rules with numbers |
| `ufw delete N` | Remove rule by number |
| `ufw deny from IP` | Block specific IP |
| `ufw reset` | Remove all rules |

---

## Key Takeaway

Always configure both GCP firewall (cloud) and UFW (host). Open only the ports you need. Allow SSH first before enabling UFW on a remote server.
