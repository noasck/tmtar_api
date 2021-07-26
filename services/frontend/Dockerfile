FROM node:slim

WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json package-lock.json ./
RUN npm install
RUN npm install -g @angular/cli@7.3.9

COPY . /app
RUN pwd
RUN ls
RUN npm run build