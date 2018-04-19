#FT SERVER
#HW04 JAMES OBOYLE

import socket
import threading
import os
import sys
import binascii
import random

SERVER_HOST = '0.0.0.0'
SERVER_PORT =  47698# use one of your assigned ports instead
SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

class HandlerThread(threading.Thread):
    """ This class is a sub-class of the threading.Thread class

        There is a constructor and a function called run()
        This class is used for threading multiple connections to the server
        so that concurrency in the application is allowed.

    """

    def __init__(self, client, address, idDict):
        """constructor"""
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.idDict = idDict

    def run(self):
        """thread code"""
        
        requestString = str(self.client.recv(4096),'utf-8').strip()
        
        queryBit = requestString[0]
        if(queryBit == '0'):
            recvAddress, recvPort = self.address
            #hard code for now
            recvPort = 47699
            ID = str(random.randint(10,99))
            #insert ID into dictionary
            qString = recvAddress + ':' + str(recvPort)
            tempDict = {ID:qString}
            self.idDict.update(tempDict)

            #Send the ID to the recv client
            self.client.send(ID.encode())
        elif(queryBit == '1'):
            idLookup = requestString[1:]
            if(idLookup not in self.idDict):
                self.client.send("NOID".encode())
            else:
                recvInfo = self.idDict[idLookup]
                self.client.send(recvInfo.encode())
        else:
            print("Error in protocol syntax")

        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind(SERVER_ADDR)
connection.listen(10)

idDict = {'1':'address'}
print("Server is running")
try:
    while True:
        client, address = connection.accept()
        th = HandlerThread(client, address, idDict)
        th.start()
except KeyboardInterrupt:
    print("\nEverything is finished...exiting program")
sys.exit(0)