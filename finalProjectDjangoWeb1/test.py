import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('10.0.0.6', 10001)
client.sendto('hello', addr)
