from PyQt5 import QtCore, uic, QtWidgets
from socket import *
from threading import *
import time
import sys

UIClass, QtBaseClass = uic.loadUiType("mainwindow.ui")


class MyApp(UIClass, QtBaseClass):  # load the GUI
    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chat Program')  # set the title of the program window

    def sendMessage(sock):  # function to send message
        while 1:
            # gather and send message to server
            message = input()
            sock.send(message.encode('utf-8'))

    def receiveMessage(sock):   # function to receive the message
        while 1:
            try:
                # receive message from server and print it
                incomingMessage = sock.recv(1024).decode('utf-8')
                if incomingMessage:
                    print(">> " + incomingMessage)
                    if incomingMessage == "Farewell! May the force be with you.":
                        break
            except:
                continue

        sock.close()
        print("Disconnected from the server. Please exit the program.")


app = QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())

window.lineEdit_3.setPlaceholderText("Hello there")

# setup socket to connect to server
serverName = input("Enter the server IP address: ")  # localhost is 127.0.0.1
serverPort = input("Enter the server port (43500 - 43505): ")
clientSocket = socket(AF_INET, SOCK_STREAM)  # TCP socket
clientSocket.connect((serverName, int(serverPort)))

# prompt user to enter a username with a welcome message
welcomeMessage = clientSocket.recv(1024).decode('utf-8')
username = input(welcomeMessage)
clientSocket.send(username.encode('utf-8'))

# create and start thread of sending and receiving message
inMessage = Thread(target=receiveMessage, args=(clientSocket,))
outMessage = Thread(target=sendMessage, args=(clientSocket,))
inMessage.start()
outMessage.start()



while 1:  # go on loop until the user enters /quit to exit
    time.sleep(1)  # prevent overload in the processor
    pass
