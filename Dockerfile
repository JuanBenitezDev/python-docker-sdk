FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y python3 \
    && apt-get install -y gcc \
    && apt-get install -y g++ \
    && apt-get install -y default-jre \
    && apt-get install -y nodejs \
    && apt-get install -y ruby \
    && apt-get install -y php \
    && apt-get install -y golang 

WORKDIR /home/

