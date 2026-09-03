#!/bin/bash
# FoodExpress MySQL Container Run Script

echo "Starting FoodExpress MySQL container..."

# BUG: Volume mount missing the container path (should be -v mysql-data:/var/lib/mysql)
# BUG: Wrong data directory -- /data/mysql is not where MySQL stores data
# BUG: No restart policy -- container won't restart after host reboot
# BUG: MYSQL_ROOT_PASSWORD not set -- MySQL refuses to start without it
# BUG: No init SQL script mounted -- database won't be created on first run

docker run -d \
  --name fe-mysql \
  -p 3306:3306 \
  -v mysql-data:/data/mysql \
  mysql:8.0

echo "MySQL container started."
echo "Connect with: docker exec -it fe-mysql mysql -uroot"
