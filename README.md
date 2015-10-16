# pmonCap

This project aims to estimate the bandwidth of a remote host by measuring
the capacity of the link immediately connected to it (i.e. the link in the very last hop to the remote host).

### 1. How we do it

```
-----------------------------------------------------------------------------------------------------------------
ALGORITHM: END-LINK CAPACITY CALCULATOR
-----------------------------------------------------------------------------------------------------------------
1. Runs traceroute to calculate the number of hops (K) till destination;
2. Sends 2 groups of packet trains to destination:
    2.1 GROUP_1:
        2.1.1 For each packet train of GROUP_1:
            2.1.1.1 ONE packet (LOCOMOTIVE)* is sent: SIZE = 1500 bytes (MTU) & TTL = K - 1;
            2.1.1.2 ONE or MORE packets (CARS)* is/are sent: SIZE = 500 bytes & TTL = K;
            2.1.1.3 ONE packet (CABOOSE) is sent: SIZE = 44 bytes & TTL = K;
            2.1.1.4 Returns RTT = time between the sending of the locomotive and the response to the caboose;
        2.1.2 Returns the smallest RTT (RTT1).
    2.2 GROUP_2:
        2.2.1 For each packet train of GROUP_2:
            2.2.1.1 ONE packet (LOCOMOTIVE)* is sent: SIZE = 1500 bytes (MTU) & TTL = K - 1;
            2.2.1.2 ONE or MORE packets (CARS)* is/are sent: SIZE = 50 bytes & TTL = K;
            2.2.1.3 ONE packet (CABOOSE) is sent: SIZE = 44 bytes & TTL = K;
            2.2.1.4 Returns RTT = time between the sending of the locomotive and the response to the caboose;
        2.2.2 Returns the smallest RTT (RTT2).
3. Calculates end-link capacity: C = N*(SIZE1-SIZE2)*8/(RTT1-RTT2),
				where N = NUMBER_OF_CARS,
					SIZE1 = GROUP1_CAR_SIZE,
					SIZE2 = GROUP2_CAR_SIZE,
					RTT1 > RTT2.
* Locomotive and car packets do not cause response as they are ICMP ECHO REPLY MESSAGES.
-----------------------------------------------------------------------------------------------------------------
```

### 2. How to install it

```
Requirements: Python 2.7+
OS: Unix systems
```
Uncompress the GitHub project folder and it's ready for use.

### 3. How to use it

```
USAGE: sudo python pmonCap.py -d DESTINATION -f INPUT_FILE -t NUMBER_OF_TRAINS -c NUMBER_OF_CARS
```

Either *destination* or *file* is to be provided.

The parameters *number of trains* and *cars per train* are required when *file* is given, for their *default value* (100) may not match your *file*.

**Notice you must provide root credentials as we are dealing with ICMP packets.**

### 4. Local file specification

This file contains RTT values for each packet train group. Hence, it replaces the sending of packet trains to destination.

You must create your file as follows:

```
group 1 - packet train #1 RTT
group 1 - packet train #2 RTT
group 1 - packet train #3 RTT
group 2 - packet train #1 RTT
group 2 - packet train #2 RTT
group 2 - packet train #3 RTT
```

For each line, one RTT value (in seconds).

Now, let's see a real example.

Imagine you have 5 RTT values for each group.

These are the RTT values for group 1:

```
0.0480751991272
0.0439519882202
0.0450620651245
0.0477740764618
0.0406899452209
```

These are the RTT values for group 2:

```
0.0292770862579
0.0310640335083
0.0362038612366
0.033399105072
0.0450990200043
```

Your file must contain all those values. Nothing more, nothing less.

Here is what your file should look like:

```
0.0480751991272
0.0439519882202
0.0450620651245
0.0477740764618
0.0406899452209
0.0292770862579
0.0310640335083
0.0362038612366
0.033399105072
0.0450990200043
```

First group first. Second group second.

So if you have 5 values for each group, your file will have 10 values (10 lines). 

The command you should run in this case follows (assuming rtt values were obtained by sending 100 car packets per train):

```
sudo python pmonCap.py -f file -t 5 -c 100
```

The expected end-link capacity for this example is 31 mbps. 

**Notice you must provide equal number of RTT values for each group. The reason for that is both groups are supposed to have same number of packet trains.**
