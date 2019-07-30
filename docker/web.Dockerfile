FROM node

RUN npm install -g @vue/cli

WORKDIR /root

COPY web web
CMD node web/app.js
