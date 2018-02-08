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
		return self.pid

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
				m = re.search('pid: 0x([0-9a-f]{8}), pname:\s+%s' % self.game_name, packet_data.decode())
				if m:
					self.pid = int(m.group(1), 16)
					print("Setting pid to %x" % self.pid)

			return 0
		elif packet_header[3] == 9:
			return packet_data
		else:
			return 0xDEADC0DE

	def send_packet(self, packet_type, command, args=[], data=b''):
		self.sequence += 1000
		# if ((len(args)) >= 3) and (data is not -1):
		# 	data = data.to_bytes(args[2], 'little')
		# else:
		# 	data = b''

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
		#print("Data: "+data)
		self.send_packet(0, 10, [self.pid, addr, length], data)

	# Improved UI Commands

	# Writing

	def WriteCustom(self, addr, data, length, isSigned=False):
		# Safety checks and stuff
		t = type(data)
		if t == type(0):
			if ((data >= 0x00) and (data < (0x100 ** length))):
				data = data.to_bytes(length, 'little', signed=isSigned)
			else:
				raise Exception("WriteU%i: Invalid Data, must be in range 0-%i" % (8*length, ((0x100 * length)-1)))
		self.send_write_memory_packet(addr, length, data)

	def WriteU8(self, addr, data):
		self.WriteCustom(addr, data, 1)
	def WriteU16(self, addr, data):
		self.WriteCustom(addr, data, 2)
	def WriteU32(self, addr, data):
		self.WriteCustom(addr, data, 4)
	def WriteU64(self, addr, data):
		self.WriteCustom(addr, data, 8)

	def Write8(self, addr, data):
		self.WriteCustom(addr, data, 1, isSigned=True)
	def Write16(self, addr, data):
		self.WriteCustom(addr, data, 2, isSigned=True)
	def Write32(self, addr, data):
		self.WriteCustom(addr, data, 4, isSigned=True)
	def Write64(self, addr, data):
		self.WriteCustom(addr, data, 8, isSigned=True)

	# Reading

	def ReadCustom(self, addr, length, isSigned=False):
		self.send_read_memory_packet(addr, length)
		return int.from_bytes(self.read_packet(), byteorder='little', signed=isSigned)

	def ReadU8(self, addr):
		return self.ReadCustom(addr, 1)
	def ReadU16(self, addr):
		return self.ReadCustom(addr, 2)
	def ReadU32(self, addr):
		return self.ReadCustom(addr, 4)
	def ReadU64(self, addr):
		return self.ReadCustom(addr, 8)

	def Read8(self, addr):
		return self.ReadCustom(addr, 1, isSigned=True)
	def Read16(self, addr):
		return self.ReadCustom(addr, 2, isSigned=True)
	def Read32(self, addr):
		return self.ReadCustom(addr, 4, isSigned=True)
	def Read64(self, addr):
		return self.ReadCustom(addr, 8, isSigned=True)
