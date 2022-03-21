import sys
import argparse
import receiver
import sender
import struct
import socket
import array
import binascii

# References
# Inc 0x0, Manually create and send raw TCP/IP packets.

def main(argv):
    args = parser()
    fudgedLineArray = createFudgedLineArray()
    # Dependent on the --sender or --receiver arguements
    if args.action == True:

        for i in range(len(fudgedLineArray)):
            sender.Sender(createTCPPacket(args, fudgedLineArray[i]))
    else:
        receiver.Receiver()

##################
# Paser arguments.
##################
def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    # Arguments for whether the user wants to send or receive
    # Defaults as sender
    parser.add_argument('--sender', dest='action', action='store_true')
    parser.add_argument('--receiver', dest='action', action='store_false')
    parser.set_defaults(action=True)

    args = parser.parse_args()

    return args

####################################
# Extracting message from text file.
####################################
def getCovertMessage():
    messageFile = open(__file__ + "/../../data/covertMessage.txt")
    plainCovertMessage = messageFile.read()
    messageFile.close()

    return plainCovertMessage

##########################################
# Converts the covert message into Binary.
##########################################
def getBinaryMessage():
    plainCovertMessage = getCovertMessage()
    binaryCovertMessage = "{0:08b}".format(int(plainCovertMessage, 16))
    return binaryCovertMessage

##########################################################################
# Takes in the covert message in Binary.
# For each character in the Binary representation, we will convert it the
# Hex equilvalent. It will return this Hex array for the TCP Packet.
##########################################################################
def createFudgedLineArray():
    binaryString = getBinaryMessage()
    fudgedLineArray = []
    for i in range(len(binaryString)):
        if binaryString[i] == '0':
            fudgedLineArray.append(b'\x50\x00\x71\x10')
        else:
            fudgedLineArray.append(b'\x50\x02\x71\x10')

    return fudgedLineArray

#############################################################
# Function to create a custom TCP packet based on user input.
#############################################################
def createTCPPacket(args, fudgedLine):
    ip_header  = b'\x45\x00\x00\x28'  # Version, IHL, Type of Service | Total Length
    ip_header += b'\xab\xcd\x00\x00'  # Identification | Flags, Fragment Offset
    ip_header += b'\x40\x06\xa6\xec'  # TTL, Protocol | Header Checksum
    ip_header += b'\x7f\x00\x00\x01'  # Source Address
    ip_header += b'\x7f\x00\x00\x01'  # Destination Address

    tcp_header  = b'\x30\x39\x00\x50' # Source Port | Destination Port
    tcp_header += b'\x00\x00\x00\x00' # Sequence Number
    tcp_header += b'\x00\x00\x00\x00' # Acknowledgement Number

    # A good option for doing bit by bit encoding would be suing the PSH flag and turning that on or off
    # the part were messing with is x02 = 0010. That third bit will be the one were changing (possibly)
    # We are changing the PSH Flag, to either a 1 or a 0. Our covert message is in this line.
    tcp_header += fudgedLine          # Data Offset, Reserved, Flags | Window Size
    tcp_header += b'\xe6\x32\x00\x00' # Checksum | Urgent Pointer
    data = b'Hello'

    packet = tcp_header + data

    return packet

main(sys.argv)
