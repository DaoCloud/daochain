FROM daocloud.io/node:4.3.0-slim

ENV NGINX_VERSION 1.9.11-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
  && echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
  && apt-get update \
  && apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base git libpng-dev \
  && rm -rf /var/lib/apt/lists/* \
  && ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log \
#  && npm install -g -q npm && npm install -g -q gulp
  && npm install -g cnpm --registry=https://registry.npm.taobao.org && cnpm install -g -q gulp


WORKDIR /app

COPY ./package.json /app/
#RUN npm install -q
RUN cnpm install -q

COPY . /app/

ENV APP_DEBUG=true
ENV NODE_ENV=production
RUN gulp build

EXPOSE 80

CMD mkdir -p /usr/share/nginx/html/dist && \
 cp -r ./dist/* /usr/share/nginx/html/dist/ && \
 nginx -g 'daemon off;'
