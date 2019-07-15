* Author: Jason Park & Bomin Kim


## About
This is a simple chat program on a user-friendly GUI from PyQT that allows multiple users to receive and send messages simultaneously through secure TCP connection.
It also has a feature that shows currently connected clients, so that user is aware of how he/she is chatting with.
The server also has a very nice notification feature, which is broadcasted to all the clients whenever another client is connected or disconnected.
The UDP file transfer feature was to be implemented, but as we focused more on researching the use of PyQT tool and design of how client list feature works with the server, the file transfer feature was not implemented in this build. Through the research, it was found that UDP file transfer would work on small files due to its unstable connection, so it would have to be implemented using more secure TCP connection for its reliability.


## How to use
You may use a compiler of your choice or a command prompt to run this program in the following order.
1. Start server.py
2. Enter the port to be used with the server (43500 by default)
3. Start client.py
4. Type in the port of the server (43500 by default). The IP address is your local address 127.0.0.1 but it can be easily changed in client file.
5. Enter your username to join the chat
6. Enjoy the chat


## Known Bugs
The chat server uses threading. We believe because of threading's possble delay for each clients, the client list randomly gets parsed in the wrong order. This occurs when there is 3 or more clients in which server has to take care of multiple clients.


## Note
This program was tested on Windows 10 PC using PyCharm IDE.
