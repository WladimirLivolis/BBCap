import socket, sys, time
from ICMP import ICMPLib

# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com

class LatencyTools:

	def __init__(self):
		self.port = 33434 # port
		self.timeout = 2 # timeout for socket receive

	# Prints to screen and to file
	def printer(self, status, outputFile):
		print status
		outputFile.write(status+"\n")

	# Returns the minimum of a array of rtts
	def minimum(self, rtt_array):
		min = rtt_array[0]
		for i in range(1,len(rtt_array)):
			rtt = rtt_array[i]
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
		dest_addr = socket.gethostbyname(destination_name) # destination address
		icmp = socket.getprotobyname('icmp')  # get the number assigned to ICMP protocol (1)
		i = 1 # number of trains initial value
		rtt_array = []
		while i <= NUMBER_OF_TRAINS:
			# Create a socket for receiving data
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.bind(("", self.port)) # set port
			recv_socket.settimeout(self.timeout) # set timeout
			# Create a socket for sending LOCOMOTIVE packet
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL1) # set ttl
			ICMPLib().send_icmp_packet(send_socket, destination_name, self.port, LOCOMOTIVE_SIZE, 'reply') # send LOCOMOTIVE packet to destination
			t0 = time.time() # register initial time
			# Set socket for sending CARS packets
			j = 1 # number of cars initial value
			while j <= NUMBER_OF_CARS:
				send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL2) # set ttl
				ICMPLib().send_icmp_packet(send_socket, destination_name, self.port, CAR_SIZE, 'reply') # send CAR packet to destination
				j += 1
			# Set socket for sending CABOOSE packet
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL3) # set ttl
			ICMPLib().send_icmp_packet(send_socket, destination_name, self.port, CABOOSE_SIZE, 'request') # send CABOOSE packet to destination
			try:
				data = recv_socket.recv(1024) # Receive packet reply
				t1 = time.time() # register receiving time
				rtt = t1 - t0 # calculate rtt
				rtt_array.append(rtt)
			except:
				print sys.exc_info()[0]
				rtt = -1
				pass
			finally: # close sockets
				send_socket.close()
				recv_socket.close()
			self.printer("*Packet Train #"+str(i)+" --> RTT = "+str(rtt)+"s",output_file)
			i += 1
		rtt = self.minimum(rtt_array) # get the smallest rtt
		self.printer("\nSmallest RTT = "+str(rtt)+"s",output_file)
		return rtt

	# Reads rrt values from local file.
	# Returns the smallest rtt for each group.
	# NUMBER_OF_TRAINS: number of packet trains per group.
	# NUMBER_OF_CARS: number of packet cars per train.
	# NUMBER_OF_GROUPS: number of packet train groups.
	def latency_reader(self, input_file, NUMBER_OF_TRAINS, NUMBER_OF_CARS, NUMBER_OF_GROUPS, output_file):
		self.printer("\nI-II) Reading RTT values from file...\n",output_file)
		in_file = open(input_file) # Open file 
		i = 1 # number of groups initial value
		rtt_array = []
		while i <= NUMBER_OF_GROUPS: # for each group
			self.printer("\n ========== GROUP #"+str(i)+" - RTTs: ========== \n",output_file)
			aux_array = []
			j = 1 # number of trains initial value
			while j <= NUMBER_OF_TRAINS: # for each packet train
				rtt = float(in_file.readline()) # read line (rtt) from file
				self.printer("*Packet Train #"+str(j)+" --> RTT = "+str(rtt)+"s",output_file)
				aux_array.append(rtt)
				j += 1
			rtt_min = self.minimum(aux_array) # get the smallest rtt for this group
			self.printer("\nSmallest RTT = "+str(rtt_min)+"s",output_file)
			rtt_array.append(rtt_min)
			i += 1
		return rtt_array
			
