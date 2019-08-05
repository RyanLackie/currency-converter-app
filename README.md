# Currency Converter Coding Assessment

This applciation can be viewed at http://165.22.11.241/  
It is responsive for various screen sizes.  

To run this application locally use the scripts:
* Terminal 1
  * (Requires npm and Node)
  * npm install
  * npm run serve

* Terminal 2
  * (Requires pip and Python3)
  * cd server_py/venv
  * pip install --requirement requirements.txt
  * npm run start_py

* Terminal 3
  * npm run start_js

The client side interfaces with 2 server side applciations.  
Both gather currency exchange rates from http://exchangeratesapi.io/ but use different languages and frameworks.  
The default is set to use Python and Flask and the secondary is JavaScript and Node.  

Labels of the parts of the applciation:

<img src="./assets/Application Overview.png" alt="Application Overview.png"/>
