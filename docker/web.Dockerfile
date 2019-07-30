FROM node

WORKDIR /root

COPY web web
CMD node web/app.js
