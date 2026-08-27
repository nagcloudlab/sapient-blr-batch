# Step 3: Install Apache

## Objective
Install Apache HTTP Server and verify it is running.

---

## Install

```bash
sudo apt update
sudo apt install -y apache2
```

## Verify Installation

```bash
# Check version
apache2 -v

# Check if running
sudo systemctl status apache2

# Check port 80 -- now apache2 is listening
sudo ss -tlnp | grep :80
```

## Test

```bash
# From the VM
curl http://localhost

# From your local machine (replace IP)
curl -I http://<EXTERNAL_IP>
```

Open `http://<EXTERNAL_IP>` in your browser -- you'll see the default Ubuntu Apache page.

## What Just Happened

```
apt install apache2
    |
    v
Installs binary   --> /usr/sbin/apache2
Creates config    --> /etc/apache2/
Creates docroot   --> /var/www/html/
Creates logs      --> /var/log/apache2/
Creates service   --> /lib/systemd/system/apache2.service
Auto-starts       --> systemd starts apache2 immediately
Listens           --> port 80 on all interfaces (0.0.0.0:80)
Serves            --> /var/www/html/index.html (default page)
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `sudo systemctl start apache2` | Start Apache |
| `sudo systemctl stop apache2` | Stop Apache |
| `sudo systemctl restart apache2` | Restart (drops connections) |
| `sudo systemctl reload apache2` | Reload config (graceful, no downtime) |
| `sudo systemctl status apache2` | Check if running |
| `apache2 -v` | Show version |
| `apache2 -t` | Test config syntax before restart |

---

## Key Takeaway

One command installs Apache, and it starts serving the default page immediately on port 80. In production, Apache is typically pre-installed as part of the server image.
