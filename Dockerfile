FROM python:2-onbuild

# runtime env
ENV ETCD_URL	http://localhost:4001
ENV DOCKER_URL	unix://var/run/docker.sock
ENV DOCKER_API_VER	1.23
ENV TTL			15

CMD [ "python", "./docker-register.py", "-e $ETCD_URL", "-d $DOCKER_URL", "--docker-api-ver $DOCKER_API_VER", "-t $TTL" ]