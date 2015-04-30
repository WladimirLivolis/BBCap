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

printer("\nII) Sending groups of packet triples...",output)

printer("\n==================== Group #1 ====================",output)
printer("\nPacket 1 --> Length = 1.5KB | TTL = "+str(k-1)+" hops",output)
printer("Packet 2 --> Length = 500B  | TTL = "+str(k)+" hops",output)
printer("Packet 3 --> Length = 0B    | TTL = "+str(k)+" hops\n",output)
rtt1 = group_1.latency_tester(dest_name, 1500, k-1, 500, k, 0, k, output)

printer("\n==================== Group #2 ====================",output)
printer("\nPacket 1 --> Length = 1.5KB | TTL = "+str(k-1)+" hops",output)
printer("Packet 2 --> Length = 50B   | TTL = "+str(k)+" hops",output)
printer("Packet 3 --> Length = 0B    | TTL = "+str(k)+" hops\n",output)
rtt2 = group_2.latency_tester(dest_name, 1500, k-1, 50, k, 0, k, output)

if rtt1 > rtt2:
	cap = (500-50)*8/(rtt1-rtt2)
	printer("\nEnd-link capacity = "+str(cap)+" bps",output)
else:
	printer("\n**Unable to calculate end-link capacity as unexpected values for RTT were obtained. Please try running again.",output)

printer("\nDone!",output)
output.close()
