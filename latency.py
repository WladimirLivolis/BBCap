import socket, sys, time, numpy
from ICMP import ICMPLib

# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com

class LatencyTools:

	def __init__(self):
		self.port = 33434
		self.timeout = 2
		self.array = []

	def printer(self, status, outputFile):
		print status
		outputFile.write(status+"\n")
	
	# Sends packet pairs to destination and counts the time between the sending of the first
	# packet and the response to the second packet. TTL1 is first packet's ttl and is supposed
	# to be the number of hops till destination minus one. TTL2 is second packet's ttl and is
	# supposed to be the number of hops till destination. data_size1 should be the desired size
	# for the first packet. data_size2 should be the desired size for the second packet.
	def latency_tester(self, dest_name, data_size1, TTL1, data_size2, TTL2, outputFile):
		dest_addr = socket.gethostbyname(dest_name)
		icmp = socket.getprotobyname('icmp')
		count = 1
		while count <= 50:
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.bind(("", self.port))
			recv_socket.settimeout(self.timeout)
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL1)
			send_socket.sendto(abs(data_size1-34)*"J", (dest_name, self.port))
			t0 = time.time()
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL2)
			icmp_sender = ICMPLib()
			icmp_sender.send_icmp_packet(send_socket, dest_name, self.port, data_size2)
			try:
				data = recv_socket.recv(1024)
				t1 = time.time()
				rtt = t1 - t0
				self.array.append(rtt)
			except:
				print sys.exc_info()[0]
				rtt = -1
				self.array.append(1)
				pass
			finally:
				send_socket.close()
				recv_socket.close()
			self.printer("*Packet Pair #"+str(count)+" --> RTT = "+str(rtt)+"s",outputFile)
			count += 1
		self.printer("\nSmallest RTT = "+str(numpy.min(self.array))+"s",outputFile)
		self.printer("Biggest RTT = "+str(numpy.max(self.array))+"s",outputFile)
		self.printer("Average RTT = "+str(numpy.average(self.array))+"s",outputFile)			
