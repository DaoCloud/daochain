FROM ubuntu:latest

MAINTAINER DCS <dao@daocloud.io> 

ADD website

WORKDIR website

RUN apt-get install -y npm
RUN npm install -g gulp karma karma-cli webpack
RUN npm install

#ENV GETH

VOLUME /var/run/docker.sock

EXPOSE 3000
CMD ["bash", "start.sh"]