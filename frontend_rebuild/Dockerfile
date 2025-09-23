FROM node:18-alpine AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install --verbose
COPY ./ .
RUN npm run build

FROM nginx:latest AS production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf