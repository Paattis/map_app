FROM node:20-alpine3.17

WORKDIR /src/frontend/

# install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install


# copy app files
COPY ./ ./
