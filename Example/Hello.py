# PyNTR Demo Program 1
#
#	Name: 	Hello.py
#	Author:	imthe666st
#

# Import PyNTR
from PyNTR import PyNTR

# Create the client
print("Starting the programm..")
client = PyNTR('192.168.0.11')

# Connect
print("Starting the connection..")
client.start_connection()

# Send the packet
print("Sending a 'hello' packet..")
client.send_hello_packet()