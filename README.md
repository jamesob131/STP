James O'Boyle

# Simple Transfer Protocol 

-- Description -- 

This program is a simple transfer protocol application. ftserver.py is the server
that assigns the receive client it's unique ID and store the ip/port of the client server
so that when the send mode of the client server talks to the server it can get the needed
information. 

The file you are sending must exist, it will not give an error. 

The ftclient protocol works by sending a query to the ftserver. If it is requesting an ID
the query will be a 0. If it is requesting info about an ID the query will begin with a 1
followed by the ID it is inquiring about. 

-- Virtual Environment -- 
To activate virtual environment type: source bin/active

-- Server -- 
python3 ftserver.py

-- Receive Mode -- 
python3 ftclient.py --server vcf0:47698 --receive

-- Send Mode -- 
python3 ftclient.py --server vcf0:47698 --send ID filename.txt
