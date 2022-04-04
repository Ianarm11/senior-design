import socket
import struct
import collections
import os
import binascii

##############################################################################
# Takes in an array of all the received tcp packets.
# Pulls out the specific flag that we are manipulating for each tcp packet
# and puts it into a new array. This is our covert binary string
# convert the binary string into hex representation and print it to terminal.
# Prints our original covert message.
##############################################################################
def getCovertMessage(dataArray):
    temp = []
    binaryCovertMessage = []
    for i in range(len(dataArray)):
        if dataArray[i][33] == 2:
            binaryCovertMessage.append('1')
        else:
            binaryCovertMessage.append('0')

    binaryCovertMessage = ''.join(binaryCovertMessage)
    print("Original covert message (Binary): " + binaryCovertMessage)
    binaryCovertMessage = int(binaryCovertMessage,2)
    print("Original covert message (Hex): " + hex(binaryCovertMessage))

###############################
# Main receiver functionality.
###############################
def Receiver():
    # Hardcode the destination address and the destination port
    host = '127.0.0.1'
    port = 1234

    # Create a raw socket..
    # Parameter 1: AF_INET indicates this is for IPv4
    # Parameter 2: SOCK_RAW just indicates we are using a raw socket
    # Parameter 3: IPPROTO_RAW indicates that we supply the IP Header
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    print("Created raw socket..")

    # connect() associates the socket with its local address, a client side operation.
    s.connect((host, port))
    print("Successfully connected to " + str(host) + " on port " + str(port))

    # Now, lets see if we are receiving any packets..
    dataArray = []

    while True:
        # recvfrom() receives data from the socket. Return value is a pair (bytes, address)
            # bytes: bytes object representing the data recieved.
            # address: address of the socket that sent the data.
            # Takes in a buffer size. For now, just try to get it all using 1024 (large size)
        print("Trying to receive the data from socket..")
        timeout = s.settimeout(5.0)
        try:
            data = s.recvfrom(1024)
        except socket.timeout:
                print("No more incoming data. Pulling out Covert Message...")
                getCovertMessage(dataArray)
                break

        dataArray.append(data[0])

        # Let's print out our data..
        print("Length of bytes object from our received data: " + str(len(data[0])))
        print("Printing out the data, bit by bit..")
        count = 0
        for element in data[0]:
            if count == 20:
                print("TCP Header: ")
            if count == 0:
                print("IP Header supplied by the kernel: ")
            if count == 40:
                print("Data: ")
            print((element))
            count += 1

        print("Length of our address from our recieved data: " + str(len(data[1])))
        print("Address of sending socket: " + data[1][0])

    print("Closing Receiver.")
