#FT CLIENT
#JAMES OBOYLE 

import socket
import threading
import os
import sys
import binascii

SERVER_HOST = '0.0.0.0'
SERVER_PORT =  47699# use one of your assigned ports instead
SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

class HandlerThread(threading.Thread):
    """ This class is a sub-class of the threading.Thread class

        There is a constructor and a function called run()
        This class is used for threading multiple connections to the server
        so that concurrency in the application is allowed.

    """

    def __init__(self, client, address):
        """constructor"""
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def run(self):
        """thread code"""

        #Receive the filename
        fileExist = False
        fileName = str(self.client.recv(512),'utf-8').strip()
        
        print("Receiving: ", fileName)
        

        if(os.path.isfile(fileName)):
        	fileExist = True
        	print("Error: File already Exists")
        else:
        	self.client.send("OK".encode())

        if(fileExist == False):
	        #receive the file
	        file = b''
	        while(True):
	        	data = self.client.recv(4096)
	        	if not data:
	        		break
	        	file = file + data
	        
	        #convert to string 
	        file = str(file,'utf-8').strip()
	        #Write the file
	        f = open(fileName, 'w+')
	        f.write(file)
	        f.close()
	        print("Transfer Complete")

        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()


def recvID(args):

	#Gets only important info i.e. 'vcf3:4760'
	print("Asking " + args[1] + " about an identification number")
	args = args[1].split(":")

	#Get the host
	host = args[0]

	#Get the port
	port = int(args[1])

	#address is the host and the port
	address = (host,port)

	#Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	#Connect the socket to the server
		sock.connect(address)
		#Sends the query
		sock.send(b'0')
		#Get the response
		data = sock.recv(4096)
		data = str(data,'utf-8').strip()
	finally:
		#Close the socket
		sock.close()

	recvID = data
	return recvID

def runRecvServer():
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	connection.bind(SERVER_ADDR)
	connection.listen(10)

	try:
		while True:
		    client, address = connection.accept()
		    th = HandlerThread(client, address)
		    th.start()
	except KeyboardInterrupt:
		print(" \nEveryting is finished...exiting program")

def sendMode(args):
	#Gets only important info i.e. 'vcf3:4760'
	print("Asking " + args[1] + " about " + args[3])
	
	#id to ask the server for
	ID = args[3]

	#file name of the file to send 
	fileName = args[4]

	serverInfo = args[1].split(":")
	#Get the host
	host = serverInfo[0]
	#Get the port
	port = int(serverInfo[1])
	#address is the host and the port
	address = (host,port)

	#Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	#Connect the socket to the ftserver
		sock.connect(address)
		#Sends the query
		message = '1' + ID
		sock.send(message.encode())
		#Get the response
		data = sock.recv(4096)
		data = str(data,'utf-8').strip()
	finally:
		#Close the socket
		sock.close()

	if(data == "NOID"):
		print("ERROR: NO ID WAS FOUND ON SERVER")
		sys.exit()
	else:
		print("Found client at ", data)
		info = data.split(":")
		ip = info[0]
		port = int(info[1])

	#we are going to assume that the file exists 
	fo = open(fileName, 'rb')
	sendFile = fo.read()
	fo.close()

	#Address of the receive server
	address = (ip, port)
	
	

	#Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#Send the file
	try:
		#Connect to the recieve server
		sock.connect(address)

		print("Sending: ", fileName)
		#Send the fileName
		sock.send(fileName.encode())

		#Confirmation
		confirm = str(sock.recv(512),'utf-8').strip()
		
		if(confirm == 'OK'):
			sock.sendall(sendFile)
			print("Transfer Complete")
		else:
			print("Could not send file")
	finally:
		#Close the socket
		sock.close()
	

if __name__ == "__main__":
	
	#Get the command line input
	args = sys.argv[1:]

	if(len(args) == 3):
		recvID = recvID(args)
		print("Issued " + recvID + " for identification...")
		runRecvServer()
	elif(len(args) == 5):
		sendMode(args)

	else:
		print("ERROR IN COMMAND SYNTAX")