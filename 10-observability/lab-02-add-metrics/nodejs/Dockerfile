FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY order-service.js .
EXPOSE 8080
CMD ["node", "order-service.js"]
