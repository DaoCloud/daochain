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

ENV NODE_ENV production
ENV RPC_HOST geth
ENV RPC_PORT 8545
ENV LISTENING_PORT 30303
ENV INSTANCE_NAME ethstats
ENV WS_SERVER ws://blockchain.daocloud.io:3000
ENV WS_SECRET daocloud-eth-net-stats-secret
ENV VERBOSITY 2