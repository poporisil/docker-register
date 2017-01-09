docker-register
========
Register docker container to ETCD

How to start
--------------------

```
usage: docker-register.py [-h] [-e ETCD_URL] [-d DOCKER_URL]
                          [--docker-api-ver DOCKER_API_VER] [-t TTL]
                          [-l LOG_PATH]
```

Options
--------------------
```
  -h, --help            show this help message and exit
  -e ETCD_URL           etcd url (default: http://localhost:4001)
  -d DOCKER_URL         docker url (default: unix://var/run/docker.sock)
  --docker-api-ver DOCKER_API_VER   docker api version (default: 1.23)
  -t TTL                register ttl (default: 15)
  -l LOG_PATH           log path (default: .)
```
