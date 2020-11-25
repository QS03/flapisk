#!/bin/bash

sudo su


cd /var/www/flapisk/backend/

echo "Install requirements..."
. /var/www/flapisk/backend/env/bin/activate

pip install -r /var/www/flapisk/backend/requirements.txt
chown -R www-data:www-data /var/www/flapisk/

echo "Main service reload..."
service flapisk stop
cp -f /var/www/flapisk/backend/scripts/flapisk.service /etc/systemd/system/
systemctl daemon-reload
service flapisk restart

echo "Nginx reload..."
cp -f /var/www/flapisk/backend/scripts/flapisk.conf /etc/nginx/sites-available/
ln -s -f /etc/nginx/sites-available/flapisk.conf /etc/nginx/sites-enabled/
service nginx restart

echo "Celery reload..."
cp -f /var/www/flapisk/backend/scripts/celery-worker.conf /etc/supervisor/conf.d/
supervisorctl reload
