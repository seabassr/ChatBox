# ChatBox
Solo project for Computer Networks

## Description
Both python scripts will display a basic GUI interface. Server.py will display the users currently in the server, and will handle broadcasting messages to all users. Client.py will require the user to type in public IP address to server, and will try to connect. If connection was successful, display the chatbox and allow user to send messages. If not, program will alert the user.

<img src="/Demo/Server.png" width="400" height="514"> <img src="/Demo/Client.png" width="400" height="496">


## Requirements
- Must setup router with port forward to your server
- ChatBoxUser.db needs to be on server
- Internet connection
- Python 3

## Run server
```
python3 server.py
````

## Run client
```
python3 client.py
```
