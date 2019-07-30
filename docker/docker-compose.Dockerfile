FROM alpine:latest

RUN apk add docker-compose

WORKDIR /root

COPY docker-compose.yml docker-compose.yml
ENTRYPOINT [ "docker-compose" ]
