import os, sys, time
from hop_count import HopCount
from latency import LatencyTools

# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com
#
# USAGE: sudo python main.py <TYPE IP/LINK ADDRESS HERE>
#
# Coded using Python 2.7

def printer(status, outputFile):
	print status
	outputFile.write(status+"\n")

if not os.path.exists("./logs/"):
	os.makedirs("./logs/")

localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d%H%M%S", localtime)

output = open("./logs/"+timeString+".out","w")

timeString = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
printer("Started at "+timeString,output)

printer("\n***WARNING: You must have root permissions as this script uses raw packets.***\n",output)

dest_name = sys.argv[1]

printer("I) Running traceroute...\n",output)
c = HopCount()
k = c.counter(dest_name, output)
printer("\nDone!",output)

group_1 = LatencyTools()
group_2 = LatencyTools()

# DO NOT ALTER THE VALUES FOR PACKET SIZE
PACKET_TYPE1_SIZE = 1500 # This packet MUST have MTU size
GROUP1_PACKET_TYPE2_SIZE = 500 # This packet MUST be greater than the one from group 2
GROUP2_PACKET_TYPE2_SIZE = 50 # This packet MUST be smaller than the one from group 1
PACKET_TYPE3_SIZE = 0 # This packet MUST have size ZERO
NUMBER_OF_PACKET_TRAINS = 100
NUMBER_OF_PACKETS_PER_TRAIN = 102 # MUST be greater than or equal to 3. E.g.: 102 = 1 packet of type 1, 100 packets of type 2, and 1 packet of type 3.

printer("\nII) Sending groups of packet trains...",output)

printer("\n==================== Group #1 ====================",output)
printer("\nPACKET TYPE 1 --> Length = "+str(PACKET_TYPE1_SIZE)+"B | TTL = "+str(k-1)+" hops",output)
printer("PACKET TYPE 2 --> Length = "+str(GROUP1_PACKET_TYPE2_SIZE)+"B | TTL = "+str(k)+" hops",output)
printer("PACKET TYPE 3 --> Length = "+str(PACKET_TYPE3_SIZE)+"B | TTL = "+str(k)+" hops\n",output)
rtt1 = group_1.latency_tester(dest_name, PACKET_TYPE1_SIZE, k-1, GROUP1_PACKET_TYPE2_SIZE, k, PACKET_TYPE3_SIZE, k, NUMBER_OF_PACKET_TRAINS, NUMBER_OF_PACKETS_PER_TRAIN, output)

printer("\n==================== Group #2 ====================",output)
printer("\nPACKET TYPE 1 --> Length = "+str(PACKET_TYPE1_SIZE)+"B | TTL = "+str(k-1)+" hops",output)
printer("PACKET TYPE 2 --> Length = "+str(GROUP2_PACKET_TYPE2_SIZE)+"B | TTL = "+str(k)+" hops",output)
printer("PACKET TYPE 3 --> Length = "+str(PACKET_TYPE3_SIZE)+"B | TTL = "+str(k)+" hops\n",output)
rtt2 = group_2.latency_tester(dest_name, PACKET_TYPE1_SIZE, k-1, GROUP2_PACKET_TYPE2_SIZE, k, PACKET_TYPE3_SIZE, k, NUMBER_OF_PACKET_TRAINS, NUMBER_OF_PACKETS_PER_TRAIN, output)

if rtt1 > rtt2:
	cap = (NUMBER_OF_PACKETS_PER_TRAIN-2)*(GROUP1_PACKET_TYPE2_SIZE-GROUP2_PACKET_TYPE2_SIZE)*8/(rtt1-rtt2)
	printer("\nEnd-link capacity = "+str(cap)+" bps",output)
else:
	printer("\n**Unable to calculate end-link capacity as unexpected values for RTT were obtained. Please try running again.",output)

printer("\nDone!",output)
output.close()
