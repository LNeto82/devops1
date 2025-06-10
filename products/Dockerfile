FROM node:16

WORKDIR /app

COPY index.js .

RUN npm init -y && npm install express

EXPOSE 3001

CMD ["node", "index.js"]
