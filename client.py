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

# username has to be multiple values so this might not work

# Class to handle the GUI of the chat program
class ChatGUI(UIClass, QtBaseClass):
    # Constructs the GUI
    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chat Program') # set the title of the program window
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False) # disable windows maximize button
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False) # disable windows exit button
        self.userInput.setPlaceholderText("Enter your messages here")

        # Show login page and let the user join the chat with username
        self.stackedWidget.setCurrentIndex(0)
        self.joinButton.clicked.connect(self.joinChat)

        # Create and start thread of sending and receiving message
        inMessage = Thread(target=self.receiveMessage, args=())
        outMessage = Thread(target=self.sendMessage, args=())
        inMessage.start()
        outMessage.start()

        self.sendButton.clicked.connect(self.sendMessage) # connect sendButton to sendMessage
        self.exitButton.clicked.connect(self.exitChat) # connect exit button to exitChat

    # Function to join the chat with username
    def joinChat(self):
        message = self.userNameInput.text()
        clientSocket.send(message.encode('utf-8'))
        self.stackedWidget.setCurrentIndex(1) # show the chat page after join button is clicked
        joinMsg = "//JOIN//"
        clientSocket.send(joinMsg.encode('utf-8'))


    # Function to terminate the program, lets the server know it is terminating
    def exitChat(self):
        exitMsg = "//EXIT//"
        clientSocket.send(exitMsg.encode('utf-8'))
        self.close()

    # Function to send message to the server
    def sendMessage(self):
        # Send message to server and clear the text box
        message = self.userInput.text()
        clientSocket.send(message.encode('utf-8'))
        self.userInput.clear()

    # Function to receive and display the messages from the server
    def receiveMessage(self):
        while 1:
            try:
                # Receive message from server and print it
                incomingMessage = clientSocket.recv(1024).decode('utf-8')
                if incomingMessage:
                    if incomingMessage == "//JOIN//" or incomingMessage == "//EXIT//": # if a command is recvd from the server
                        usernameList=[]
                        incomingMessage = clientSocket.recv(1024).decode('utf-8')
                        while incomingMessage != "//..//": # get the usernames until there is a sign for done
                            substr = incomingMessage
                            if substr[-6:] != "//..//": # getting usernames
                                usernameList.append(substr) # put the username in the list
                                incomingMessage = clientSocket.recv(1024).decode('utf-8') # get next username
                            else: # getting the last username
                                usernameList.append(incomingMessage[:-6]) # put it in the list
                                break
                        self.listWidget.clear() # empty out the listWidget
                        for username in usernameList: # populate the listWidget with the usernames in the list
                            self.listWidget.addItem(username)
                    else: # normal chat function
                        self.chatWindow.addItem(incomingMessage)
            except:
                continue

        clientSocket.close()


app = QtWidgets.QApplication(sys.argv)
window = ChatGUI()
window.show()
sys.exit(app.exec_())
