FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY *.js ./
EXPOSE 8080 8081 8082
CMD ["node", "order-service-v3.js"]
