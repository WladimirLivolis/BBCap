import sys, time
from hop_count import HopCount
from latency import LatencyTools

# Author: Wladimir Cabral
# 	      wladimircabral@gmail.com

#Generate messages on --> http -->//www.lipsum.com/
#Check message size on --> http -->//bytesizematters.com/

# Message 1 (1.44KB)
MESSAGE1 = "MESSAGE1Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin rhoncus faucibus tincidunt. Fusce eleifend neque a varius vulputate. Morbi fermentum, enim sit amet fermentum tempor, nulla elit blandit metus, sed tempus est mi at nunc. Duis aliquam rhoncus felis. Curabitur porttitor et tortor sit amet ultricies. Curabitur feugiat, enim non rhoncus dapibus, risus tellus congue augue, sed maximus magna sem et sapien. Curabitur malesuada tempus nulla et elementum. Sed sagittis nibh eu enim viverra suscipit. Quisque fringilla ultricies risus eu elementum. Pellentesque ac hendrerit nibh. Vestibulum id condimentum dui. Vivamus eget dignissim felis. Donec aliquet elit pellentesque, varius ex ut, ultrices enim. Nulla convallis congue massa, non tincidunt mi cursus eu. In quis mi sit amet mauris ornare facilisis. Aenean et mi efficitur, molestie lacus eu, placerat nulla. Nullam eu nibh vel mi facilisis pulvinar a a elit. Mauris blandit hendrerit molestie. Fusce pharetra magna sapien, quis placerat massa tincidunt ut. Fusce quis nibh non libero fermentum consectetur a eu nulla. In sit amet nibh velit. Vivamus nec metus mattis, dictum felis in, sagittis arcu. Nulla facilisi. Nullam quis rhoncus est. Nam non maximus augue. Aenean quis elementum quam. Phasellus sit amet erat ac magna auctor mollis in nec mi. Donec suscipit, leo eget bibendum consequat, ante turpis auctor lectus, et ultrices nibh justo ac dolor. Etiam ultrices lacus ut ipsum turpis duis."

# Message 2 (500B)
MESSAGE2 = "MESSAGE2Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel leo sit amet risus mattis rutrum nec non eros. In vitae lacinia sem. Aenean auctor sem et volutpat suscipit. Nulla vitae orci quis purus efficitur bibendum non vitae tellus. Mauris venenatis mi vitae felis interdum ultrices ut id augue. Nullam vitae purus quam. Suspendisse non odio hendrerit, mattis nisl nec, facilisis enim. Nunc tincidunt neque dui, et lobortis purus fermentum sed. Sed dictum fringilla aliquam cras amet."

# Message 3 (50B)
MESSAGE3 = "MESSAGE3Lorem ipsum dolor sit amet nullam sodales."

def printer(status, outputFile):
	print status
	outputFile.write(status+"\n")

localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d%H%M%S", localtime)

output = open(timeString+".out","w")

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

printer("\nII) Sending groups of packet pairs...",output)

printer("\n==================== Group #1 ====================",output)
printer("\nPacket 1 --> data size = 1.44KB | TTL = "+str(k-1)+" hops",output)
printer("Packet 2 --> data size = 500B   | TTL = "+str(k)+" hops\n",output)
group_1.latency_tester(dest_name, MESSAGE1, k-1, MESSAGE2, k, output)

printer("\n==================== Group #2 ====================",output)
printer("\nPacket 1 --> data size = 1.44KB | TTL = "+str(k-1)+" hops",output)
printer("Packet 2 --> data size = 50B    | TTL = "+str(k)+" hops\n",output)
group_2.latency_tester(dest_name, MESSAGE1, k-1, MESSAGE3, k, output)

printer("\nDone!",output)
output.close()
