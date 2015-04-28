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

	# Sends packet triples to destination and counts the time between the sending of the first
	# packet and the response to the third packet. TTL1 is first packet's ttl and is supposed
	# to be the number of hops till destination minus one. TTL2 is second packet's ttl and is
	# supposed to be the number of hops till destination. TTL3 is third packet's ttl and is
	# supposed to be the number of hops till destination. packet_size1 should be the desired size
	# for the first packet. packet_size2 should be the desired size for the second packet.
	# packet_size3 should be the desired size for the third packet.
	def latency_tester(self, dest_name, packet_size1, TTL1, packet_size2, TTL2, packet_size3, TTL3, outputFile):
		dest_addr = socket.gethostbyname(dest_name)
		icmp = socket.getprotobyname('icmp')
		count = 1
		while count <= 50:
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.bind(("", self.port))
			recv_socket.settimeout(self.timeout)
			# Packet 1
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL1)
			send_socket.sendto(abs(packet_size1-36)*"J", (dest_name, self.port))
			t0 = time.time()
			# Packet 2
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL2)
			send_socket.sendto(abs(packet_size2-36)*"J", (dest_name, self.port))
			# Packet 3
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL3)
			icmp_sender = ICMPLib()
			icmp_sender.send_icmp_packet(send_socket, dest_name, self.port, packet_size3)
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
			self.printer("*Packet Triple #"+str(count)+" --> RTT = "+str(rtt)+"s",outputFile)
			count += 1
		self.printer("\nSmallest RTT = "+str(numpy.min(self.array))+"s",outputFile)			
