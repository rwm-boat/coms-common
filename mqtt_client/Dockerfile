FROM ubuntu:latest

RUN apt-get update -y 

RUN apt-get install -y python3 \
    python3-pip \
    python3-dev

RUN pip3 install paho-mqtt

COPY ./client.py /

