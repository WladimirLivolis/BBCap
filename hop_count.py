import socket
from ICMP import ICMPLib

# Based upon the following Oracle's tutorial: https://blogs.oracle.com/ksplice/entry/learning_by_doing_writing_your
#
# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com

class HopCount:

	def __init__(self):
		self.port = 33434
		self.max_hops = 30
		self.timeout = 0.5

	# Prints to screen and to file
	def printer(self, status, outputFile):
		print status
		outputFile.write(status+"\n")	
	
	# Returns the number of hops till destination. Works exactly as traceroute.
	def counter(self, dest_name, outputFile):
		dest_addr = socket.gethostbyname(dest_name)
		icmp = socket.getprotobyname('icmp')
		ttl = 1
		destinationReached = False
		hopCountExceeded = False
		while not (destinationReached or hopCountExceeded):
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.bind(("", self.port))
			recv_socket.settimeout(self.timeout)
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
			ICMPLib().send_icmp_packet(send_socket, dest_name, self.port, 0)
			curr_addr = None
			try:
				_, curr_addr = recv_socket.recvfrom(512)
				curr_addr = curr_addr[0]
			except socket.error:
				pass
			finally:
				send_socket.close()
				recv_socket.close()
			if curr_addr == dest_addr:
				destinationReached = True
			else:
				ttl += 1
				if ttl > self.max_hops:
					hopCountExceeded = True
		if destinationReached:
			self.printer(str(ttl)+" hops till "+dest_name,outputFile)
			return ttl
		else:
			self.printer("Hop Count Exceeded!",outputFile)
			return -1
