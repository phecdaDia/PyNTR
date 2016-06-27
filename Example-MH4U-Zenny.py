# PyNTR Demo Program 2
#
#	Name: 	Example-MH4U-Zenny.py
#	Author:	imthe666st
#

# Import PyNTR
from PyNTR import PyNTR

# Create the client
client = PyNTR('192.168.0.11')

# Connect
client.start_connection()

# Get the pid
client.set_game_name('redgiant')

# Get current Zenny
zenny = client.ReadU32(0x08369410)

# Print it out
print("%08x -> %i" % (zenny, zenny))

# Write a new value
client.WriteU32(0x08369410, 7777777)
