# PmonCap

This project aims to estimate the bandwidth of a remote host by measuring
the capacity of the link connected to it.

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
USAGE: sudo python main.py -d DESTINATION -f INPUT_FILE -t NUMBER_OF_TRAINS -c NUMBER_OF_CARS
```

Either *destination* or *file* is to be provided.

The parameters *number of trains* and *cars per train* are required in either case.

**Notice you must provide root credentials as we are dealing with ICMP packets.**
