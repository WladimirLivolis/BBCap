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
	# packet (locomotive) and the response to the last packet (caboose). At the end, returns the smallest RTT. 
	# TTL1 is the TTL for LOCOMOTIVE packets and is supposed to be the number of hops till destination minus one. 
	# TTL2 is the TTL for CAR packets and is supposed to be the number of hops till destination.
	# TTL3 is the TTL for CABOOSE packets and is supposed to be the number of hops till destination.
	# LOCOMOTIVE_SIZE is the size for LOCOMOTIVE packets and is supposed to be MTU size.
	# CAR_SIZE is the size for CAR packets and is supposed to be either 500 bytes for GROUP1 or 50 bytes for GROUP2.
	# CABOOSE_SIZE is the size for CABOOSE packets and is supposed to be 44 bytes.
	# NUMBER_OF_TRAINS is the number of packet trains to be sent.
	# NUMBER_OF_CARS is the number of cars per train to be sent.
	def latency_tester(self, destination_name, LOCOMOTIVE_SIZE, TTL1, CAR_SIZE, TTL2, CABOOSE_SIZE, TTL3, NUMBER_OF_TRAINS, NUMBER_OF_CARS, output_file):
		dest_addr = socket.gethostbyname(destination_name)
		icmp = socket.getprotobyname('icmp')
		i = 1
		while i <= NUMBER_OF_TRAINS:
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.bind(("", self.port))
			recv_socket.settimeout(self.timeout)
			# LOCOMOTIVE
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL1)
			ICMPLib().send_icmp_packet(send_socket, destination_name, self.port, LOCOMOTIVE_SIZE, 'reply')
			t0 = time.time()
			# CARS
			j = 1
			while j <= NUMBER_OF_CARS:
				send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL2)
				ICMPLib().send_icmp_packet(send_socket, destination_name, self.port, CAR_SIZE, 'reply')
				j += 1
			# CABOOSE
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL3)
			ICMPLib().send_icmp_packet(send_socket, destination_name, self.port, CABOOSE_SIZE, 'request')
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
