from PyQt5 import QtCore, uic, QtWidgets
from socket import *
from threading import *
import time
import sys

# Load the UI file
UIClass, QtBaseClass = uic.loadUiType("mainwindow.ui")

# **CHANGE IF NECESSARY**
# Server Address and Port
serverName = '127.0.0.1'   # localhost - 127.0.0.1
serverPort = '43500'  # 43500 - 43505 for luke.cs.spu.edu

# Setup the TCP connection to the server
clientSocket = socket(AF_INET, SOCK_STREAM)  # TCP socket
clientSocket.connect((serverName, int(serverPort)))

# Class to handle the GUI of the chat program
class ChatGUI(UIClass, QtBaseClass):
    # Constructs the GUI
    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chat Program') # set the title of the program window
        self.userInput.setPlaceholderText("Enter your messages here")
        self.sendButton.clicked.connect(self.sendMessage) # connect send button to a sendMessage function

        # ADD more setup code for GUI if needed...

        # Create and start thread of sending and receiving message - IS THIS RIGHT?
        inMessage = Thread(target=self.receiveMessage, args=(clientSocket,))
        outMessage = Thread(target=self.sendMessage, args=(clientSocket,))
        inMessage.start()
        outMessage.start()



    # Function to send message to the server
    def sendMessage(self, sock):
        while 1:
            # Send message to server
            message = self.userInput.toPlainText()
            sock.send(message.encode('utf-8'))

            # Display the sent message in chat window
            self.chatWindow.addItem("YOU SENT >> " + message)

    # Function to receive and display the messages from the server
    def receiveMessage(self, sock):
        while 1:
            try:
                # Receive message from server and print it
                incomingMessage = sock.recv(1024).decode('utf-8')
                if incomingMessage:
                    self.chatWindow.addItem("YOU RECEIVED >> " + incomingMessage)
                    if incomingMessage == "Farewell! May the force be with you.": # modify this properly
                        break
            except:
                continue

        sock.close()
        print("Disconnected from the server. Please exit the program.")




# Code below this line should be modified to fit into the GUI


app = QtWidgets.QApplication(sys.argv)
window = ChatGUI()
window.show()
sys.exit(app.exec_())


# prompt user to enter a username with a welcome message
welcomeMessage = clientSocket.recv(1024).decode('utf-8')
username = input(welcomeMessage)
clientSocket.send(username.encode('utf-8'))


# go on loop until the user enters /quit to exit
while 1:
    time.sleep(1)  # prevent overload in the processor
    pass

