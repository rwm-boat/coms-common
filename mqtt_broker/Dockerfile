FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install mosquitto -y 

COPY ./mosquitto.conf /etc/mosquitto/mosquitto.conf

EXPOSE 1883
