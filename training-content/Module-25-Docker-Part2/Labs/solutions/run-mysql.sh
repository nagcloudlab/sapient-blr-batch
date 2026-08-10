#!/bin/bash
# FoodExpress MySQL Container Run Script

echo "Starting FoodExpress MySQL container..."

# Create volume if it doesn't exist
docker volume create mysql-data 2>/dev/null

# FIX: Corrected volume mount path to /var/lib/mysql
# FIX: Added MYSQL_ROOT_PASSWORD environment variable
# FIX: Added restart policy for auto-restart after host reboot
# FIX: Added init SQL script mount for database creation on first run
docker run -d \
  --name fe-mysql \
  -p 3306:3306 \
  -v mysql-data:/var/lib/mysql \
  -v "$(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql" \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=foodexpress \
  --restart unless-stopped \
  mysql:8.0

echo "MySQL container started."
echo "Connect with: docker exec -it fe-mysql mysql -uroot -psecret"
echo "Data persists in volume: mysql-data"
