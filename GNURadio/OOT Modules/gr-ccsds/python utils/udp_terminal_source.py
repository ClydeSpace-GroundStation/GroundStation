import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while 1:

	message = raw_input("Enter text to send: ")

	while(len(message)<128):
		message += '\0';

	sock.sendto(message, (UDP_IP, UDP_PORT))
