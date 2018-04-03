FROM docker.saritasa.com/centos7-python361-nginx-uwsgi
### https://gitblit.saritasa.com/blob/?r=saritasa/docker/images.git&f=centos7-python361-nginx-uwsgi/Dockerfile&h=development

### Setup run parameters
EXPOSE 80
WORKDIR /home/www/app
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

### Argument for sets django environment
ARG DJANGO_ENV
ARG MUSIC_STORE_EXERCISE_ENVIRONMENT

### Environment variables
### If you want project related environment to be pushed into Docker container
### CRM_ENVIRONMENT=${CRM_ENVIRONMENT:-dev}
ENV APP_ENV=${DJANGO_ENV:-development} \
    DJANGO_SETTINGS_MODULE=config.settings.${DJANGO_ENV:-development} \
    TERM=xterm LC_ALL=en_US.UTF-8 \
    C_FORCE_ROOT=True


### Install dependencies
COPY requirements /home/www/app/requirements
RUN /bin/bash -c "pip3 install --src=/src -r /home/www/app/requirements/${APP_ENV}.txt"

### Add config files to container
ADD .docker/rootfs /

### Add source code to container
ADD . /home/www/app/
