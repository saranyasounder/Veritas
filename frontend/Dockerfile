# stage 1 — build the React app
FROM node:20-slim AS builder

WORKDIR /app

# copy and install dependencies first
COPY package.json package-lock.json ./
RUN npm install

# copy source code and build
COPY . .
RUN npm run build

# stage 2 — serve with nginx
FROM nginx:alpine

# copy built files from stage 1 into nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# expose port 80 — standard HTTP port
EXPOSE 80

# nginx starts automatically
CMD ["nginx", "-g", "daemon off;"]