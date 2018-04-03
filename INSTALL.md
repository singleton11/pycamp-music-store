# Prerequisites

You have to have following installed:
  * [docker](https://docs.docker.com/engine/installation/)
      Ensure you can run `docker` without `sudo`.
  * [docker-compose](https://docs.docker.com/v1.8/compose/install/)
  * [pip-tools](https://github.com/nvie/pip-tools)

Also you should be logged in Saritasa docker registry, i.e. run
``docker login docker.saritasa.com`` (use LDAP credentials)


Then run:

```
fab sphinx
```

and open [localhost:8001](http://localhost:8001)
