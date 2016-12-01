FROM node:alpine

MAINTAINER DCS <dao@daocloud.io>

ADD https://github.com/cubedro/eth-netstats/archive/master.zip /root/

RUN cd /root && \
    unzip -q master.zip && \
    cd eth-netstats-master && \
    npm install -q && \
    npm install -q -g grunt-cli && \
    grunt

WORKDIR /root/eth-netstats-master

EXPOSE 3000

CMD ["npm", "start"]

ENV WS_SECRET daocloud-eth-net-stats-secret
