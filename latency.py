import socket, sys, time
from ICMP import ICMPLib

# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com

class LatencyTools:

	def __init__(self):
		self.port = 33434
		self.timeout = 2
		self.array = []

	# Prints to screen and to file
	def printer(self, status, outputFile):
		print status
		outputFile.write(status+"\n")

	# Returns the minimum of a array of rtts
	def minimum(self):
		min = self.array[0]
		for i in range(1,len(self.array)):
			rtt = self.array[i]
			if rtt < min:
				min = rtt
		return min

	# Sends packet trains to destination and counts the time (RTT) between the sending of the first
	# packet and the response to the last packet. At the end, returns the smallest RTT. 
	# TTL1 is the TTL for PACKET_TYPE1 and is supposed to be the number of hops till destination minus one. 
	# TTL2 is the TTL for PACKET_TYPE2 and is supposed to be the number of hops till destination.
	# TTL3 is the TTL for PACKET_TYPE3 and is supposed to be the number of hops till destination.
	# packet_size1 should be the desired size for PACKET_TYPE1.
	# packet_size2 should be the desired size for PACKET_TYPE2.
	# packet_size3 should be the desired size for PACKET_TYPE3.
	# number_of_packet_trains is the number of packet trains to be sent.
	# number_of_packets_per_train is the number of packets per train and must be at least 3.
	def latency_tester(self, destination_name, packet_size1, TTL1, packet_size2, TTL2, packet_size3, TTL3, number_of_packet_trains, number_of_packets_per_train, output_file):
		dest_addr = socket.gethostbyname(destination_name)
		icmp = socket.getprotobyname('icmp')
		i = 1
		while i <= number_of_packet_trains:
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.bind(("", self.port))
			recv_socket.settimeout(self.timeout)
			# PACKET_TYPE_1
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL1)
			send_socket.sendto(abs(packet_size1-36)*"J", (destination_name, self.port))
			t0 = time.time()
			# PACKET_TYPE_2
			j = 2 # counting first and last packets
			while j < number_of_packets_per_train:
				send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL2)
				send_socket.sendto(abs(packet_size2-36)*"J", (destination_name, self.port))
				j += 1
			# PACKET_TYPE_3
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL3)
			ICMPLib().send_icmp_packet(send_socket, destination_name, self.port, packet_size3)
			try:
				data = recv_socket.recv(1024)
				t1 = time.time()
				rtt = t1 - t0
				self.array.append(rtt)
			except:
				print sys.exc_info()[0]
				rtt = -1
				pass
			finally:
				send_socket.close()
				recv_socket.close()
			self.printer("*Packet Train #"+str(i)+" --> RTT = "+str(rtt)+"s",output_file)
			i += 1
		rtt = self.minimum()
		self.printer("\nSmallest RTT = "+str(rtt)+"s",output_file)
		return rtt		
