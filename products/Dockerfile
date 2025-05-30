FROM node:20

WORKDIR /app

COPY index.js .

RUN npm init -y && npm install express

EXPOSE 4001

CMD ["node", "index.js"]
