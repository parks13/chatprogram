from socket import *
from threading import *
import time

clientsList = [] # list of clients for multiple connection
indexKeeper = [] # list of names for accessing

# Receive clients and append its info into the list
def connectClient ():
   while 1:
        connectionSocket, addr = serverSocket.accept() # accept connection from the client
        username = connectionSocket.recv(1024).decode('utf-8') # save the user name from the client
        clientsList.append(connectionSocket)  # append the client to the list
        indexKeeper.append(username)   # append the name to the list

        print("Client", username, "[", addr, "]", "has connected.") # inform the host

        serverMessage("[SERVER NOTIFICATION] '" + username + "' JOINED THE CHAT.") # broadcast to chat room

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
        try: # try to see if message is successfully received and verified
            message = connectionSocket.recv(1024).decode('utf-8') # receive and decode message
            if message != "//EXIT//" and message != "//JOIN//": # if it is not EXIT message nor JOIN message, broadcast to the clients
                print("RECEIVED -- " + username + ": " + message)
                serverMessage(username + ": " + message)

            elif message == "//JOIN//":
                for user in clientsList:  # loop through connected clients
                    user.send(message.encode('utf-8')) # send the command to the client side
                    for name in indexKeeper: # send all username that is active
                        user.send(name.encode('utf-8'))
                    done = "//..//"
                    user.send(done.encode('utf-8')) # indicate that it's done


            else: # remove client if message is not received
                clientsList.remove(connectionSocket)
                indexKeeper.remove(username)
                for user in clientsList:  # loop through connected clients
                    user.send(message.encode('utf-8')) # send the command to the client side
                    for name in indexKeeper: # send all username that is active
                        user.send(name.encode('utf-8'))
                    done = "//..//"
                    user.send(done.encode('utf-8')) # indicate that it's done
                print("Client", username, "has disconnected.") # inform the host
                serverMessage("[SERVER NOTIFICATION] '" + username + "' DISCONNECTED.")
        except:
            continue


# Sends out message to all clients
def serverMessage (message):
    for user in clientsList: # loop through connected clients
        user.send(message.encode('utf-8'))
        print("SENDING -- " + message)


# setup socket to wait for connections
serverPort = input("Choose a server port (43500 by default): ") # prompt host to choose a port
serverSocket = socket(AF_INET, SOCK_STREAM) # TCP (reliable)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # make port reusable
serverSocket.bind(('', int(serverPort)))
serverSocket.listen(1)

print('The server is now running! Use the provided client program to connect!')

# run threads for connecting clients, terminate the server if not
threadserver = Thread(target=connectClient()) # start threaded connection for each users
threadserver.start()

while 1: # run until the server is shut down manually
    time.sleep(1) # prevent overload in the processor
    pass
