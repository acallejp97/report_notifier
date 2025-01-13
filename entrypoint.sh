#!/bin/sh

echo "Configuring cron job..."

echo "$CRON_PARKING python3 /usr/src/app/main.py parking has_changes>> /var/log/cron.log 2>&1" > /etc/cron.d/cron_parking
echo "$CRON_ESTER python3 /usr/src/app/main.py ester>> /var/log/cron.log 2>&1" > /etc/cron.d/cron_ester
echo "$CRON_WEBPAGE python3 /usr/src/app/main.py webpage>> /var/log/cron.log 2>&1" > /etc/cron.d/cron_webpage

chmod 0644 /etc/cron.d/cron_parking
chmod 0644 /etc/cron.d/cron_ester
chmod 0644 /etc/cron.d/cron_webpage

cat /etc/cron.d/cron_parking
cat /etc/cron.d/cron_ester
cat /etc/cron.d/cron_webpage

echo "Starting cron..."
crond -l 2 && tail -f /var/log/cron.log
