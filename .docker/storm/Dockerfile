FROM alpine:3.5

###############################################################
# Java / OpenJDK 8.121
###############################################################

# Default to UTF-8 file.encoding
ENV LANG C.UTF-8

# add a simple script that can auto-detect the appropriate JAVA_HOME value
# based on whether the JDK or only the JRE is installed
RUN { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
	&& chmod +x /usr/local/bin/docker-java-home
ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk/jre
ENV PATH $PATH:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin

ENV JAVA_VERSION 8u121
ENV JAVA_ALPINE_VERSION 8.121.13-r0

RUN set -x \
	&& apk add --no-cache \
		openjdk8-jre="$JAVA_ALPINE_VERSION" \
	&& [ "$JAVA_HOME" = "$(docker-java-home)" ]


###############################################################
# Python
###############################################################

RUN apk add --no-cache \
    linux-headers \
    the_silver_searcher \
    bash \
    python \
    su-exec \
    caddy

# Install python3
RUN apk add --no-cache python3 \
    python3-dev \
    build-base && \ 
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    pip3 install virtualenv


###############################################################
# Postgresql
###############################################################

RUN apk add --no-cache libpq \
    postgresql-client \
    postgresql \
    postgresql-dev \
    postgresql-contrib


###############################################################
# Apache Storm
###############################################################

ENV STORM_USER=storm \
    STORM_CONF_DIR=/conf \
    STORM_DATA_DIR=/data \
    STORM_LOG_DIR=/logs \
    GRPC_VERBOSITY=ERROR

# Add a user and make dirs
RUN set -x \
    && adduser -D "$STORM_USER" \
    && mkdir -p "$STORM_CONF_DIR" "$STORM_DATA_DIR" "$STORM_LOG_DIR" \
    && chown -R "$STORM_USER:$STORM_USER" "$STORM_CONF_DIR" "$STORM_DATA_DIR" "$STORM_LOG_DIR"

ARG DISTRO_NAME=apache-storm-1.0.2

# Download Apache Storm
RUN set -x \
    && apk add --no-cache --virtual .build-deps \
    && wget -q "http://www.apache.org/dist/storm/$DISTRO_NAME/$DISTRO_NAME.tar.gz" \
    && tar -xzf "$DISTRO_NAME.tar.gz" \
    && chown -R "$STORM_USER:$STORM_USER" "$DISTRO_NAME" \
    && rm -r "$DISTRO_NAME.tar.gz" \
    && apk del .build-deps


###############################################################
# Caddy
###############################################################

RUN echo -e "*:80\nbasicauth / storm sar1tas4\nproxy / localhost:8080" >> /etc/caddy/caddy.conf

###############################################################
# Working dir
###############################################################

WORKDIR $DISTRO_NAME

ENV PATH $PATH:/$DISTRO_NAME/bin

###############################################################
# Docker entrypoint
###############################################################

COPY docker-entrypoint.sh /
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]
