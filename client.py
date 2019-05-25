from PyQt5 import QtCore, uic, QtWidgets
from socket import *
from threading import *
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

        # need to show the first tab using QWidget

        self.joinButton.clicked.connect(self.joinChat) # connect the join button to enter the chat room with username entered

        # need to show the second tab using QWidget

        self.userInput.setPlaceholderText("Enter your messages here")

        # Create and start thread of sending and receiving message - **** IS THIS RIGHT? MAYBE USE QTHREAD?? ***
        inMessage = Thread(target=self.receiveMessage, args=(clientSocket,))
        outMessage = Thread(target=self.sendMessage, args=(clientSocket,))
        inMessage.start()
        outMessage.start()

        # ADD more setup code for GUI if needed...


    # Function to set the username and join the chat room
    def joinChat (self, sock):
        # First page to get the username
        username = self.userNameInput.toPlainText()
        clientSocket.send(username.encode('utf-8'))

    # Function to send message to the server
    def sendMessage(self, sock):
        while 1:
            if self.sendButton.clicked: # if send button is clicked, send the message to the server
                # Send message to server
                message = self.userInput.toPlainText()
                sock.send(message.encode('utf-8'))

                # Display the sent message in chat window
                self.chatWindow.addItem("YOU SENT >> " + message) # delete this and let the server handle it?

    # Function to receive and display the messages from the server
    def receiveMessage(self, sock):
        while 1:
            try:
                # Receive message from server and print it
                incomingMessage = sock.recv(1024).decode('utf-8')
                if incomingMessage:
                    self.chatWindow.addItem(incomingMessage)
            except:
                continue

        sock.close()


app = QtWidgets.QApplication(sys.argv)
window = ChatGUI()
window.show()
sys.exit(app.exec_())




