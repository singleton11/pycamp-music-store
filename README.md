README
==================================================================================
Generate actual docs with fab docs.sphinx after all instructions below
----------------------------------------------------------------------------------

You have to have the following tools installed prior initalizing the project:
    * [docker](https://docs.docker.com/engine/installation/)
    * [docker-compose](https://docs.docker.com/v1.8/compose/install/)
    * [fabric3](https://github.com/mathiasertl/fabric/)
    * [rancherssh](https://github.com/fangli/rancherssh)
    * [pip-tools](https://github.com/jazzband/pip-tools)
    * [pyenv](https://github.com/pyenv/pyenv)
    * [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

To develop frontend solution you will need to have latest node.js with npm/npx
installed
    * [node](https://nodejs.org/en/download/current/)

==================================================================================
Installation of node.js
----------------------------------------------------------------------------------

```bash
wget -cqO- https://nodejs.org/dist/v8.7.0/node-v8.7.0-linux-x64.tar.xz | tar -xJv
sudo cp -a node-v8.7.0-linux-x64/{bin,include,lib,share} /usr/
```

More info: https://fusion809.github.io/howto-install-nodejs/, if you dare you can
just run `sudo npm install npm -g` to update to latest npm with npx included, on
Fedora26 with LTS node 6.x it totally broke and destroyed node/npm and I had to
reinstall non-LTS from scratch

[why npx is cool](https://medium.com/@maybekatz/introducing-npx-an-npm-package-runner-55f7d4bd282b)

==================================================================================
Required linux packages
----------------------------------------------------------------------------------

You also need to install sqlite3 (including develop package) so you can use ipython
properly

```bash
sudo dnf install sqlite
sudo dnf install sqlite-devel sqlite-tcl sqlite-jdbc
```

if you're on Ubuntu, then

```bash
sudo apt-get install sqlite3 libsqlite3-dev
```


==================================================================================
Build project and start coding
----------------------------------------------------------------------------------

Also you should be logged in Saritasa docker registry, i.e.
run ``docker login docker.saritasa.com`` (use LDAP credentials), you need to authenticate
again docker.saritasa.com, so docker can pull images from our own docker registry


Then run:

```bash

$ fab project.init
$ fab docs.sphinx
$ npm install
$ npm run start
$ MUSIC_STORE_EXERCISE_ENVIRONMENT=local fab django.run
```

Once you run ``project.init`` initially you can start web server with ``fab django.run`` command without
executing ``project.init`` call. Also keep in mind that my-music_store_exercise-network should be created only once through docker cli

If you develop frontend you should run
```bash
$ npm run start
$ MUSIC_STORE_EXERCISE_ENVIRONMENT=local fab django.run
```

If you run into the error similar to this one:
```bash
(ck1) ➜  ck1 livereload '.ui, templates'
Starting LiveReload v0.6.2 for /home/dmitry/Projects/tests/ck1/.ui,/home/dmitry/Projects/tests/ck1/templates on port 35729.
events.js:160
      throw er; // Unhandled 'error' event
      ^

Error: listen EADDRINUSE :::35729
    at Object.exports._errnoException (util.js:1020:11)
    at exports._exceptionWithHostPort (util.js:1043:20)
    at Server._listen2 (net.js:1262:14)
    at listen (net.js:1298:10)
    at Server.listen (net.js:1394:5)
    at Server.listen (/usr/lib/node_modules/livereload/lib/livereload.js:66:28)
    at Object.exports.createServer (/usr/lib/node_modules/livereload/lib/livereload.js:224:14)
    at Object.runner [as run] (/usr/lib/node_modules/livereload/lib/command.js:70:25)
    at Object.<anonymous> (/usr/lib/node_modules/livereload/bin/livereload.js:2:27)
    at Module._compile (module.js:570:32)

```

just kill the process holding port 35729 opened with
```bash
kill -9 $(lsof -t -i :35729)
```

In some cases sublime plugin consumes this port. You may need to remove such plugin from the sublime

==================================================================================
Local development
----------------------------------------------------------------------------------

You can develop inside docker container, or using local python interpeter,
if you prefer local python, then create .fabric file in the root with the following content

```
[Project]
interpreter = local
```

By default we assume you will develop inside docker container, but if you need
good old django approach, just create virtualenv and then (once activated)

```bash
pip install -r requirements/development.txt
```


==================================================================================
Async celery
----------------------------------------------------------------------------------

If you plan to develop and debug async tasks with celery, pls create virtualhost
inside rabbitmq container and grant user permissions as shown below

```bash
$ docker-compose run rabbitmq
$ docker-compose exec rabbitmq rabbitmqctl add_vhost "music_store_exercise-development"
$ docker-compose exec rabbitmq rabbitmqctl add_user music_store_exercise_user manager
$ docker-compose exec rabbitmq rabbitmqctl set_permissions -p "music_store_exercise-development" music_store_exercise_user ".*" ".*" ".*"
```

 If however you started the development with ``fab project.init`` these operations are already completed

You may need to adjust CELERY settings in config/settings/development.py as needed

==================================================================================
CLI
----------------------------------------------------------------------------------

There are bunch of commands available for your using ``fab`` command, just type

```bash
$ fab l
```

to list all available commands.

Happy Coding!
