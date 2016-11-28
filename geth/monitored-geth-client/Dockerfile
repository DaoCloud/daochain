FROM node:alpine

MAINTAINER DCS <dao@daocloud.io>

ENV GETH_VER v1.5.4
RUN apk add --no-cache --virtual .build-deps  \
	    go git make gcc musl-dev && \
    git clone https://github.com/ethereum/go-ethereum /go-ethereum && \
    cd go-ethereum && git checkout $GETH_VER && make geth && \
    cp /go-ethereum/build/bin/geth /usr/bin/geth && \
    apk del .build-deps && rm -rf ~/.cache && \
    rm -rf /go-ethereum

RUN apk add --no-cache --virtual .build-deps  \
	    git && \
	cd /root && \
    git clone https://github.com/cubedro/eth-net-intelligence-api && \
    cd eth-net-intelligence-api && \
    npm install && \
    npm install -g pm2 && \
    apk del .build-deps && rm -rf ~/.cache

ADD start.sh /root/start.sh
ADD app.json /root/eth-net-intelligence-api/app.json
ADD genesis.json /root/genesis.json
RUN chmod +x /root/start.sh

VOLUME /root/.ethereum/keystore

EXPOSE 30303 30303/udp 8545

ENTRYPOINT /root/start.sh

ENV WS_SERVER ws://blockchain.daocloud.io:3000
ENV WS_SECRET daocloud-eth-net-stats-secret