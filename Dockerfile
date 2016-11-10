FROM ubuntu:latest

MAINTAINER DCS <dao@daocloud.io> 

ADD website .

RUN apt-get install -y npm
RUN npm install -g gulp karma karma-cli webpack
RUN npm install

ENV ETH_RPC_ENDPOINT=localhost:8545
ENV HUB_ENDPOINT=http://api.daocloud.co

VOLUME /var/run/docker.sock

EXPOSE 3000
CMD ["bash", "start.sh"]