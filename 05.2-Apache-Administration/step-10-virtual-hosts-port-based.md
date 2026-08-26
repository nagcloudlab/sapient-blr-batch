# Step 10: Virtual Hosts -- Port-based

## Objective
Serve different websites on different ports from the same server.

---

## Concept

Instead of different domain names, use **different ports** on the same IP. Common in sustain engineering:
- Port 80 for the app
- Port 8080 for admin
- Port 8443 for API

```
http://IP          --> FoodExpress (port 80)
http://IP:8080     --> FoodTrack Admin (port 8080)
```

---

## Step 1: Tell Apache to Listen on Port 8080

```bash
cat /etc/apache2/ports.conf

echo "Listen 8080" | sudo tee -a /etc/apache2/ports.conf
cat /etc/apache2/ports.conf
```

## Step 2: Update FoodTrack Config to Use Port 8080

```bash
sudo nano /etc/apache2/sites-available/foodtrack.conf
```

Change to:

```apache
<VirtualHost *:8080>
    ServerName foodtrack.local
    DocumentRoot /var/www/foodtrack

    ErrorLog ${APACHE_LOG_DIR}/foodtrack-error.log
    CustomLog ${APACHE_LOG_DIR}/foodtrack-access.log combined
</VirtualHost>
```

## Step 3: Reload and Test

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Verify both ports:

```bash
sudo ss -tlnp | grep apache
```

You'll see `:80` and `:8080`.

```bash
curl http://localhost           # FoodExpress (port 80)
curl http://localhost:8080      # FoodTrack Admin (port 8080)
```

Different content on different ports.

## Step 4: Open Port 8080 in Firewalls

### UFW (if enabled)

```bash
sudo ufw allow 8080/tcp
sudo ufw status
```

### GCP Firewall

```bash
gcloud compute firewall-rules create allow-8080 \
  --allow tcp:8080 \
  --target-tags=http-server \
  --description="Allow port 8080"
```

## Step 5: Test from Outside

```bash
curl http://<EXTERNAL_IP>           # FoodExpress
curl http://<EXTERNAL_IP>:8080      # FoodTrack Admin
```

Or open both in browser.

## Step 6: Check Virtual Host Map

```bash
apache2ctl -S
```

Shows:

```
*:80    foodexpress.local (/etc/apache2/sites-enabled/foodexpress.conf)
*:80    _default_ (/etc/apache2/sites-enabled/000-default.conf)
*:8080  foodtrack.local (/etc/apache2/sites-enabled/foodtrack.conf)
```

## Step 7: Quick Exercise -- Add a Third Site on Port 9090

```bash
echo "Listen 9090" | sudo tee -a /etc/apache2/ports.conf
sudo mkdir -p /var/www/foodapi
echo '<h1>FoodExpress API v2</h1><p>Port 9090</p>' | sudo tee /var/www/foodapi/index.html
```

```bash
sudo nano /etc/apache2/sites-available/foodapi.conf
```

```apache
<VirtualHost *:9090>
    ServerName foodapi.local
    DocumentRoot /var/www/foodapi

    ErrorLog ${APACHE_LOG_DIR}/foodapi-error.log
    CustomLog ${APACHE_LOG_DIR}/foodapi-access.log combined
</VirtualHost>
```

```bash
sudo a2ensite foodapi.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Test all three:

```bash
curl http://localhost           # Port 80
curl http://localhost:8080      # Port 8080
curl http://localhost:9090      # Port 9090
```

Check the full map:

```bash
apache2ctl -S
sudo ss -tlnp | grep apache
```

### Clean Up Third Site

```bash
sudo a2dissite foodapi.conf
sudo rm /etc/apache2/sites-available/foodapi.conf
sudo rm -rf /var/www/foodapi
sudo sed -i '/Listen 9090/d' /etc/apache2/ports.conf
sudo systemctl reload apache2
```

---

## Name-based vs Port-based

| Approach | How It Works | When to Use |
|----------|-------------|-------------|
| Name-based | Same port, different `Host` header | Multiple public websites on one server |
| Port-based | Same domain, different port number | App vs admin vs API separation |
| Combined | Both techniques together | Real-world setups |

## Two Firewalls to Remember

```
GCP:  gcloud compute firewall-rules create ...
UFW:  sudo ufw allow <port>/tcp
```

Both must allow the port. If either blocks, traffic is dropped.

---

## Summary

```
Port-based Virtual Hosts:

  ports.conf: Listen <port>           <-- Apache must know about the port
  VirtualHost *:<port>                <-- Site config must match
  GCP firewall: allow tcp:<port>      <-- Cloud must allow
  UFW: allow <port>/tcp               <-- Host must allow

  http://IP        -->:80    --> FoodExpress
  http://IP:8080   -->:8080  --> FoodTrack Admin
  http://IP:9090   -->:9090  --> FoodExpress API
```

---

## Key Takeaway

Port-based virtual hosts are used to separate concerns (app, admin, API) on the same server. Always remember to open the port in both GCP firewall and UFW.
