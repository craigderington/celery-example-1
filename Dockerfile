FROM alpine:latest
MAINTAINER Craig Derington <cderington@championsg.com>
RUN apk update && apk upgrade
RUN apk install screen
COPY . /code
WORKDIR /code
RUN pip3 install -r requirements-dev.txt
