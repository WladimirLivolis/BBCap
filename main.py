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

PACKET1_SIZE = 1500
GROUP1_PACKET2_SIZE = 500
GROUP2_PACKET2_SIZE = 50
PACKET3_SIZE = 0
SAMPLE_SIZE = 50

printer("\nII) Sending groups of packet triples...",output)

printer("\n==================== Group #1 ====================",output)
printer("\nPacket 1 --> Length = "+str(PACKET1_SIZE)+"B | TTL = "+str(k-1)+" hops",output)
printer("Packet 2 --> Length = "+str(GROUP1_PACKET2_SIZE)+"B | TTL = "+str(k)+" hops",output)
printer("Packet 3 --> Length = "+str(PACKET3_SIZE)+"B | TTL = "+str(k)+" hops\n",output)
rtt1 = group_1.latency_tester(dest_name, PACKET1_SIZE, k-1, GROUP1_PACKET2_SIZE, k, PACKET3_SIZE, k, SAMPLE_SIZE, output)

printer("\n==================== Group #2 ====================",output)
printer("\nPacket 1 --> Length = "+str(PACKET1_SIZE)+"B | TTL = "+str(k-1)+" hops",output)
printer("Packet 2 --> Length = "+str(GROUP2_PACKET2_SIZE)+"B | TTL = "+str(k)+" hops",output)
printer("Packet 3 --> Length = "+str(PACKET3_SIZE)+"B | TTL = "+str(k)+" hops\n",output)
rtt2 = group_2.latency_tester(dest_name, PACKET1_SIZE, k-1, GROUP2_PACKET2_SIZE, k, PACKET3_SIZE, k, SAMPLE_SIZE, output)

if rtt1 > rtt2:
	cap = (GROUP1_PACKET2_SIZE-GROUP2_PACKET2_SIZE)*8/(rtt1-rtt2)
	printer("\nEnd-link capacity = "+str(cap)+" bps",output)
else:
	printer("\n**Unable to calculate end-link capacity as unexpected values for RTT were obtained. Please try running again.",output)

printer("\nDone!",output)
output.close()
