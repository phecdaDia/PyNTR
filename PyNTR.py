# PyNTR
#	
#	Credits:  
#	Cell9 - Creating NTR CFW
#	Seth VanHeulen - https://github.com/svanheulen - Python NTR Example
#	
#	Haifischbecken Team - <3
#	

import socket
from enum import Enum
from array import array
from time import sleep
import re

# class PacketTypes(Enum):
# 	General = 0
# 	GeneralMemory = 1

# class PacketCommands(Enum):
# 	Heartbeat = 0
#	Hello = 3
# 	Reload = 4
# 	ListProcesses = 5

# 	ListAddresses = 8
# 	Read = 9
# 	Write = 10

class PyNTR:
	def __init__(self, host):
		self.sequence = 0
		self.host = host
		self.pid = -1
		self.game_name = None

	def set_game_name(self, name):
		self.game_name = name
		self.send_processes_packet()
		self.send_heartbeat_packet()
		self.read_packet()

	def read_packet(self):
		packet_header = self.socket.recv(84)
		if len(packet_header) == 0:
			return None

		while len(packet_header) < 84:
			packet_header += self.socket.recv(84 - len(packet_header))

		packet_header = array('I', packet_header)
		packet_data = b''
		while len(packet_data) < packet_header[20]:
			packet_data += self.socket.recv(packet_header[20] - len(packet_data))

		if packet_header[3] == 0:
			if self.game_name is not None:
				m = re.search('pid: 0x([0-9a-f]{8}), pname: %s' % self.game_name, packet_data.decode())
				if m:
					self.pid = int(m.group(1), 16)
					print("Setting pid to %x" % self.pid)

			return 0
		elif packet_header[3] == 9:
			return packet_data
		else:
			return 0xDEADC0DE

	def send_packet(self, packet_type, command, args=[], data=-1):
		self.sequence += 1000
		if ((len(args)) >= 3) and (data is not -1):
			data = data.to_bytes(args[2], 'little')
		else:
			data = b''

		#print(data)
		packet_header = array('I', (0x12345678, self.sequence, packet_type, command))
		packet_header.extend(args)
		packet_header.extend([0] * (16 - len(args)))
		packet_header.append(len(data)) # len(data)
		self.socket.sendall(packet_header.tostring() + data)

	def start_connection(self):
		print("Connecting to %s" % self.host)
		self.socket = socket.create_connection((self.host, 8000))
		self.send_heartbeat_packet()
		packet = self.read_packet()

	# Sending packets

	def send_heartbeat_packet(self):
		print("Sending Heartbeat Packet")
		self.send_packet(0, 0)

	def send_hello_packet(self):
		print("Sending Hello Packet")
		self.send_packet(0, 3)

	def send_reload_packet(self):
		print("Sending Reload Packet")
		self.send_packet(0, 4)

	def send_processes_packet(self):
		print("Sending Processes Packet")
		self.send_packet(0, 5)

	def send_addresses_packet(self):
		print("Sending Addresses Packet")
		self.send_packet(0, 8)

	def send_read_memory_packet(self, addr, length):
		print("Sending RMemory Packet")
		print("%02x\t%08x\t%x" % (self.pid, addr, length))
		self.send_packet(0, 9, [self.pid, addr, length])

	def send_write_memory_packet(self, addr, length, data):
		print("Sending WMemory Packet")
		print("%02x\t%08x\t%x" % (self.pid, addr, length))
		print("%x" % data)
		self.send_packet(0, 10, [self.pid, addr, length], data)


