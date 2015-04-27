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

	def printer(self, status, outputFile):
		print status
		outputFile.write(status+"\n")	

	def counter(self, dest_name, outputFile):
		dest_addr = socket.gethostbyname(dest_name)
		icmp = socket.getprotobyname('icmp')
		ttl = 1
		done = False
		destinationReached = False
		hopCountExceeded = False
		while not done:
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
			recv_socket.bind(("", self.port))
			icmp_sender = ICMPLib()
			icmp_sender.send_icmp_packet(send_socket, dest_name, self.port, "")
			recv_socket.settimeout(self.timeout)
			curr_addr = None
			curr_name = None
			try:
				_, curr_addr = recv_socket.recvfrom(512)
				curr_addr = curr_addr[0]
				try:
					curr_name = socket.gethostbyaddr(curr_addr)[0]
				except socket.error:
					curr_name = curr_addr
			except socket.error:
				pass
			finally:
				send_socket.close()
				recv_socket.close()
			#if curr_addr is not None:
			#	curr_host = "%s (%s)" % (curr_name, curr_addr)
			#else:
			#	curr_host = "*"
			#print "%d\t%s" % (ttl, curr_host)
			ttl += 1
			destinationReached = (curr_addr == dest_addr)
			hopCountExceeded = (ttl > self.max_hops)
			done = (destinationReached or hopCountExceeded)
		if destinationReached:
			self.printer(str(ttl-1)+" hops till "+dest_name,outputFile)
			return ttl-1
		else:
			self.printer("Hop Count Exceeded!",outputFile)
			return -1
