from socket import *
from threading import *
import time
import random

clientsList = []  # list of clients for multiple connection
indexKeeper = []  # list of names for accessing

# Receive clients and save its info into the list
def connectClient ():
   while 1:
        # Accept client
        connectionSocket, addr = serverSocket.accept()  # accept connection from the client

        username = connectionSocket.recv(1024).decode('utf-8')  # save the user name from the client
        clientsList.append(connectionSocket)  # append the client to the list
        indexKeeper.append(username)   # append the name to the list

        print("Client", username, "[", addr, "]", "has connected.")  # inform the host

        serverMessage("[SERVER NOTIFICATION: " + username + " has joined the chat.]") # broadcast to chat room

        try:
            # create and starts messaging thread for this client
            messaging = Thread(target=receiveMessage, args=[username, connectionSocket])
            messaging.start()
        except:
            continue


# Verify if the user input is the command or message
# Execute command if the user input is correct command
# If user input is not command and there is only one user, warn about it
def receiveMessage(username, connectionSocket):
    while 1:
        try:  # try to see if message is successfully received and verified
            message = connectionSocket.recv(1024)  # receive and store message
            if message:  # verify if message is command or not
                clientsList.remove(connectionSocket)
                serverMessage("SERVER NOTIFICATION: " + username + " has lost connection.")
        except:
            continue


# Sends out message to all clients about server events
def serverMessage (message):
    for user in clientsList:  # loop through connected clients
        to_send = message
        user.send(to_send.encode('utf-8'))


# setup socket to wait for connections
serverPort = input("Choose a server port (43500 - 43505): ")  # prompt host to choose a port
serverSocket = socket(AF_INET, SOCK_STREAM)  # TCP (reliable)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # make port reusable
serverSocket.bind(('', int(serverPort)))
serverSocket.listen(1)

print('The server is now running! Use the provided client program to connect!')

# run threads for connecting clients, terminate the server if not
threadserver = Thread(target=connectClient())  # start threaded connection for each users
threadserver.start()

while 1:  # run until the server is shut down manually
    time.sleep(1)  # prevent overload in the processor
    pass
