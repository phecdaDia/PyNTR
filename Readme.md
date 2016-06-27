# PyNTR  
___
### What is PyNTR?  
PyNTR is similar to PyGecko, a Python program that allows you to communicate with your 3DS and read / write RAM.   
___
### Current Features
Feature | Status | Note
---|---|---
Connecting | Done | 
Raw packet sending | Nearly Done | Remoteplay is still missing
Reading Memory | Done | UI Library still missing
Writing Memory | Nearly Done | UI Library still missing / Writing as int, not bytes
PyNTR Plugin Support | In Development | PyNTR Plugins aren't NTR Plugins.
___
### Examples
```Python
# Importing the PyNTR Class
from PyNTR import PyNTR

# Creating a client || PyNTR(IP)
client = PyNTR('192.168.0.11')

# Testing the connection with a "Hello" packet || client.send_hello_packet()
client.send_hello_packet()

# Get the PID of a process by name || client.set_game_name(GameName) ; returns Integer ( Pid )
# 'redgiant' is Monster Hunter 4 Ultimate
client.set_game_name('redgiant')

# Reading a WORD
# IMPORTANT: This will be simplified. This is just for debugging for now.
# Sending the Read Packet || client.ReadU32(Address) ; returns Integer ( Data )
data = client.ReadU32(0x08369410)

# Writing a new value || client.WriteU32(Address, Data)
client.WriteU32(0x08369410, 7777777)

# This would set the Zenny to 7777777 in MH4U (US)
```
___
### Credits  
- Cell9 - Creating NTR CFW  
- imthe666st  
- [Svanheulen](https://github.com/svanheulen) - Basic Python-NTR script  
- Haifischbecken - Distracting me while working. 