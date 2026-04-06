FROM node:20-alpine

WORKDIR /app

# Copy only package files first for caching
COPY package.json package-lock.json ./
RUN npm install

# Copy React source and public folder explicitly
COPY public/ ./public/
COPY src/ ./src/

CMD ["npm", "start"]