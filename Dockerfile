FROM alpine:3.6
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
RUN pip3 install celery flask flask-sqlalchemy flower 
COPY . /code
WORKDIR /code
RUN pip install -r requirements-dev.txt
EXPOSE 5580
CMD ["celery", "-A", "stalks.tasks", "worker", "-B", "-l", "DEBUG", "-c", "2"]
