FROM python:2.7-alpine

ENV WORK_DIR /usr/src/app
RUN mkdir -p $WORK_DIR
WORKDIR $WORK_DIR

ADD docker-register.py ./
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./docker-register.py

CMD [ "./docker-register.py" ]