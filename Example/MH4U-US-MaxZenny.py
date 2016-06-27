# PyNTR Demo Program 2
#
#	Name: 	MH4U-US-MaxZenny.py
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
# TODO: Simplify this
client.send_read_memory_packet(0x08369410, 0x4)
zenny = int.from_bytes(client.read_packet(), byteorder='little')

# Print it out
print("%08x -> %i" % (zenny, zenny))

# Write a new value
client.send_write_memory_packet(0x08369410, 0x4, 7777777)
