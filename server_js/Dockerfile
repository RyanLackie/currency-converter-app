FROM node:14
# Create app directory
WORKDIR /server-js
# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json /server-js/
RUN npm install
# Bundle app source
COPY . /server-js
EXPOSE 8000
CMD [ "node", "index.js" ]
