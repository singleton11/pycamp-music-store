#!/usr/bin/bash

### Generate robots.txt
echo "Configure environment: $APP_ENV"
case $APP_ENV in
    development|staging)
        echo -e "User-agent: *\nDisallow: /" > /home/www/app/robots.txt
        ;;
    production)
        ;;
esac

# owning filex by nginx
chown -R nginx:nginx /home/www/app

# sync DB changes
python3 manage.py migrate --noinput

# update CSS/JS in static folder
python3 manage.py collectstatic --noinput

# Store the build date and release version
echo `date` >> /home/www/builds
echo "__builddate__ = '`date`'" >> /home/www/app/__version__.py

### Starting supervisord services


echo "Starting Celery worker..."
supervisorctl start celery_worker

echo "Starting Celery beat..."
supervisorctl start celery_beat


echo "Starting NGINX..."
supervisorctl start nginx

echo "Starting UWSGI..."
supervisorctl start api

echo "Exiting bootstrap script"
exit 0
