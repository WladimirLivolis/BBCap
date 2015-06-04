import argparse, os, sys, textwrap, time
from hop_count import HopCount
from latency import LatencyTools
	 
# USAGE: sudo python main.py [-h] -d DESTINATION [-t PACKET_TRAINS] [-p PACKETS_PER_TRAIN]
#
# Coded using Python 2.7
#
# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com
#
# This software is distributed under the MIT License: http://www.opensource.org/licenses/mit-license.php

# GLOBAL CONSTANTS
# DO NOT ALTER THE VALUES FOR PACKET SIZE
PACKET_TYPE1_SIZE = 1500 # This packet MUST have MTU size
GROUP1_PACKET_TYPE2_SIZE = 500 # This packet MUST be greater than the one from group 2
GROUP2_PACKET_TYPE2_SIZE = 50 # This packet MUST be smaller than the one from group 1
PACKET_TYPE3_SIZE = 0 # This packet MUST have size ZERO

# Prints to screen and to file
def printer(status, outputFile):
	print status
	outputFile.write(status+"\n")

# Creates a log dir if needed
if not os.path.exists("./logs/"):
	os.makedirs("./logs/")

# Gets current time
localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d%H%M%S", localtime)

# Creates a log file
output = open("./logs/"+timeString+".out","w")

# Writes time to log file
timeString = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
printer("Started at "+timeString,output)

# Parses the arguments
parser = argparse.ArgumentParser(prog='sudo python main.py',
formatter_class=argparse.RawDescriptionHelpFormatter, 
description=textwrap.dedent(''' 
===================== END-LINK CAPACITY CALCULATOR =====================

Author: Wladimir Cabral
	wladimircabral@gmail.com

*This software is distributed under the MIT License: http://www.opensource.org/licenses/mit-license.php

**Coded using Python 2.7

***WARNING: You must have root permissions as this script uses ICMP packets.***

------------------------------------------------------------------------
ALGORITHM
------------------------------------------------------------------------
1. Runs traceroute to calculate the number of hops (K) till destination;
2. Sends 2 groups of packet trains to destination:
    2.1 GROUP_1:
        2.1.1 For each packet train of GROUP_1:
            2.1.1.1 ONE packet of TYPE1 is sent: SIZE = 1500 bytes (MTU) & TTL = K - 1;
            2.1.1.2 ONE or MORE packets of TYPE2 is/are sent: SIZE = 500 bytes & TTL = K;
            2.1.1.3 ONE packet of TYPE3 is sent: SIZE = ZERO & TTL = K;
            2.1.1.4 Returns RTT = time between the sending of the first packet and the response to the third packet;
        2.1.2 Returns the smallest RTT (RTT1).
    2.2 GROUP_2:
        2.2.1 For each packet train of GROUP_2:
            2.2.1.1 ONE packet of TYPE1 is sent: SIZE = 1500 bytes (MTU) & TTL = K - 1;
            2.2.1.2 ONE or MORE packets of TYPE2 is/are sent: SIZE = 50 bytes & TTL = K;
            2.2.1.3 ONE packet of TYPE3 is sent: SIZE = ZERO & TTL = K;
            2.2.1.4 Returns RTT = time between the sending of the first packet and the response to the third packet;
        2.2.2 Returns the smallest RTT (RTT2).
3. Calculates end-link capacity: C = N*(SIZE1-SIZE2)*8/(RTT1-RTT2),
				where N = NUMBER_OF_TYPE2_PACKETS_PER_TRAIN,
					SIZE1 = GROUP1_TYPE2_PACKET_SIZE,
					SIZE2 = GROUP2_TYPE2_PACKET_SIZE,
					RTT1 > RTT2.

*   Packets of TYPE1 do not cause response either because TTL < K or because they are malformed.
**  Packets of TYPE2 do not cause response as they are malformed.
*** Packets of TYPE3 have same size as their headers.
------------------------------------------------------------------------
'''))
parser.add_argument('-d','--destination', help='Destination IP address', required=True)
parser.add_argument('-t','--packet_trains',help='Number of packet trains (Default: 100)', default=100, type=int)
parser.add_argument('-p','--packets_per_train',help='Number of packets per train ***MUST be greater than or equal to 3*** E.g.: 102 = 1 packet of TYPE1, 100 packets of TYPE2, and 1 packet of TYPE3. (Default: 102)', default=102, type=int)
args = parser.parse_args()

DESTINATION_NAME = args.destination
NUMBER_OF_PACKET_TRAINS = args.packet_trains
NUMBER_OF_PACKETS_PER_TRAIN = args.packets_per_train

# Calculates number of hops till destination
printer("\nI) Running traceroute...\n",output)
K = HopCount().counter(DESTINATION_NAME, output)
printer("\nDone!",output) 

# Sends probes to destination
printer("\nII) Sending groups of packet trains...\n",output)

printer("# PACKET TRAINS: "+str(NUMBER_OF_PACKET_TRAINS),output)
printer("# PACKETS PER TRAIN: "+str(NUMBER_OF_PACKETS_PER_TRAIN),output)

printer("\n==================== Group #1 ====================",output)
printer("\nPACKET TYPE 1 --> Length = "+str(PACKET_TYPE1_SIZE)+"B | TTL = "+str(K-1)+" hops",output)
printer("PACKET TYPE 2 --> Length = "+str(GROUP1_PACKET_TYPE2_SIZE)+"B | TTL = "+str(K)+" hops",output)
printer("PACKET TYPE 3 --> Length = "+str(PACKET_TYPE3_SIZE)+"B | TTL = "+str(K)+" hops\n",output)
RTT1 = LatencyTools().latency_tester(DESTINATION_NAME, PACKET_TYPE1_SIZE, K-1, GROUP1_PACKET_TYPE2_SIZE, K, PACKET_TYPE3_SIZE, K, NUMBER_OF_PACKET_TRAINS, NUMBER_OF_PACKETS_PER_TRAIN, output)

printer("\n==================== Group #2 ====================",output)
printer("\nPACKET TYPE 1 --> Length = "+str(PACKET_TYPE1_SIZE)+"B | TTL = "+str(K-1)+" hops",output)
printer("PACKET TYPE 2 --> Length = "+str(GROUP2_PACKET_TYPE2_SIZE)+"B | TTL = "+str(K)+" hops",output)
printer("PACKET TYPE 3 --> Length = "+str(PACKET_TYPE3_SIZE)+"B | TTL = "+str(K)+" hops\n",output)
RTT2 = LatencyTools().latency_tester(DESTINATION_NAME, PACKET_TYPE1_SIZE, K-1, GROUP2_PACKET_TYPE2_SIZE, K, PACKET_TYPE3_SIZE, K, NUMBER_OF_PACKET_TRAINS, NUMBER_OF_PACKETS_PER_TRAIN, output)

# Calculates end-link capacity
printer("\nIII) Calculating end-link capacity...",output)
if RTT1 > RTT2:
	CAPACITY = (NUMBER_OF_PACKETS_PER_TRAIN-2)*(GROUP1_PACKET_TYPE2_SIZE-GROUP2_PACKET_TYPE2_SIZE)*8/(RTT1-RTT2)
	printer("\nEnd-link capacity = "+str(CAPACITY)+" bps",output)
else:
	printer("\n**Unable to calculate end-link capacity as unexpected values for RTT were obtained. Please try running again.",output)

printer("\nDone!",output)
output.close()
