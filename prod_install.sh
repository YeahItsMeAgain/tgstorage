#!/usr/bin/env sh

docker-compose -f docker-compose.install.yml up -d nginx
docker-compose -f docker-compose.install.yml up certbot
docker-compose -f docker-compose.install.yml down

curl -L --create-dirs -o ./services/nginx/etc_letsencrypt/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
openssl dhparam -out ./services/nginx/etc_letsencrypt/ssl-dhparams.pem 2048

crontab ./services/nginx/crontab
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build