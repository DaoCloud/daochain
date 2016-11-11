FROM ubuntu:latest

MAINTAINER DCS <dao@daocloud.io> 

ADD . app

WORKDIR app/cli

RUN apt-get update
RUN apt-get install -y npm python python-pip
RUN npm install -g gulp karma karma-cli webpack
RUN npm install
RUN gulp webpack

RUN pip install -r cli/requirements.pip

ENV ETH_RPC_ENDPOINT=localhost:8545
ENV HUB_ENDPOINT=http://api.daocloud.co

VOLUME /var/run/docker.sock

EXPOSE 8000
CMD [ "python", "server/gunicorn_runner.py" ]