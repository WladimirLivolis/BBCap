import socket
from ICMP import ICMPLib

# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com

class HopCount:

	def __init__(self):
		self.port = 33434 # port
		self.max_hops = 30 # hop limit
		self.timeout = 0.5 # timeout for socket receive

	# Prints to screen and to file
	def printer(self, status, outputFile):
		print status
		outputFile.write(status+"\n")	
	
	# Returns the number of hops till destination. It's a variation of traceroute.
	def counter(self, dest_name, outputFile):
		dest_addr = socket.gethostbyname(dest_name) # destination address
		icmp = socket.getprotobyname('icmp') # get the number assigned to ICMP protocol (1)
		ttl = 1 # ttl initial value
		destinationReached = False
		hopCountExceeded = False
		while not (destinationReached or hopCountExceeded):
			# Create a socket for receiving data
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.bind(("", self.port)) # set port
			recv_socket.settimeout(self.timeout) # set timeout
			# Create a socket for sending data
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl) # set ttl
			ICMPLib().send_icmp_packet(send_socket, dest_name, self.port, 0, 'request') # send packet to destination
			curr_addr = None
			try: # Get the address from receiving messages
				_, curr_addr = recv_socket.recvfrom(512)
				curr_addr = curr_addr[0]
			except socket.error:
				pass
			finally: # Close sockets
				send_socket.close()
				recv_socket.close()
			if curr_addr == dest_addr: # check whether the address from current receiving message is actually the destination address
				destinationReached = True # destination reached
			else:
				ttl += 1
				if ttl > self.max_hops: # check whether hop count exceeded
					hopCountExceeded = True
		if destinationReached: # destination was successfully reached
			self.printer(str(ttl)+" hops till "+dest_name,outputFile)
			return ttl
		else: # destination could not be reached
			self.printer("Hop Count Exceeded!",outputFile)
			return -1
