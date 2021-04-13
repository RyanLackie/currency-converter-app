# Currency Converter

## Project setup
This project will need 3 seperate terminals based in the projects root directory with the following code:

Terminal 1
```
npm install
npm run serve
(Watch for the console output to see the local address the project will be viewable at)
```

Terminal 2
```
cd server_py
docker-compose up --build
```

Terminal 3
```
cd server_js
docker-compose up --build
```

## About This Project
This application was made to play around with client to server side connections 🥳

In the app you can enter an amount and a currency, and then see the amount it is equal to in another currency using the http://exchangeratesapi.io/ api.

Down at the bottom there is a switch that will display the python or javascript icon. You can use this to switch between the 2 servers (Node and Flask) you started during setup.

