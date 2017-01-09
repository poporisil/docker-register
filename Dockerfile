FROM python:2-onbuild

ENTRYPOINT [ "python" ]
CMD [ "./docker-register.py" ]