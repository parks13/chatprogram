from socket import *
from threading import *
import time

clientsList = []  # list of clients for multiple connection
indexKeeper = []  # list of names for accessing

# Receive clients and append its info into the list
def connectClient ():
   while 1:
        connectionSocket, addr = serverSocket.accept()  # accept connection from the client
        connectionSocket.send(b"SERVER MESSAGE: Hello there! Please enter your username before you start!")
        username = connectionSocket.recv(1024).decode('utf-8')  # save the user name from the client
        clientsList.append(connectionSocket)  # append the client to the list
        indexKeeper.append(username)   # append the name to the list

        print("Client", username, "[", addr, "]", "has connected.")  # inform the host

        serverMessage(username, " JOINED THE CHAT.") # broadcast to chat room

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
            if message: # broadcast the message to the clients in the server
                serverMessage(username, message)

            else: # remove client if message is not received
                print("Client", username, "has disconnected.")  # inform the host
                serverMessage(username, " DISCONNECTED.")
                clientsList.remove(connectionSocket)
                indexKeeper.remove(username)

        except:
            continue


# Sends out message to all clients
def serverMessage (username, message):
    for user in clientsList:  # loop through connected clients
        to_send = username + ": " + message # parse the message with username of the sender
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
