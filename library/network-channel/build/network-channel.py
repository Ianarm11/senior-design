import sys
import argparse
import reciever
import sender
import struct
import socket
import array
import binascii

# TODO:
# Tweak print statements so it is clear what data is what
# Develop the encoding function for covert trasmission
    # Have a .txt file in the 'data' directory
    # Get the contents of that file in a byte array?
    # In a loop, insert the specifc amount of bytes into a value of the TCP Header. Send a the packet.
# Develop the decoding function for covert transmission
# Smile and think about Saturday
# On Saturday, get drunk and talk shit about Noah and Chase

def main(argv):
    args = parser()

    # Dependent on the --sender or --receiver arguements
    if args.action == True:
        sender.sender_main(createTCPPacket(args))
    else:
        reciever.testReceiver()

def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    #Taking in all arguments from command line to be able to properly create the TCP packets for sending.
    #Alternatively this is information needed to be able to recieve packets from another user.
    #parser.add_argument('sender_host', type=str, help='Sender Host')
    #parser.add_argument('receiver_host', type=str, help='Reciveing Host')
    #parser.add_argument('sender_port', type=int, help='Sender Port')
    #parser.add_argument('receiver_port', type=int, help='Receiver Port')
    #parser.add_argument('--method', choices=['PID', 'SEQ', 'ACK'], default='PID', help='Choose between PID, Sequence, ACK')
    parser.add_argument('--sender', dest='action', action='store_true')
    parser.add_argument('--receiver', dest='action', action='store_false')
    parser.set_defaults(action=True)
    #parser.add_argument('file_name', type=str, help='File Name')
    #parser.add_argument('file', type=int, help='File')
    #parser.add_argument('destination_host_string', type=string, help='Destination Host')
    #parser.add_argument('source_host_string', type=string, help='Source Host')

    args = parser.parse_args()

    return args

def getCovertMessage():
    messageFile = open(__file__ + "/../../data/covertMessage.txt")
    plainCovertMessage = messageFile.read()
    messageFile.close()

    return plainCovertMessage

def getBinaryMessage():

    plainCovertMessage = getCovertMessage()
    binaryCovertMessage = ' '.join(format(ord(x), 'b') for x in plainCovertMessage)
    return binaryCovertMessage

#############################################################
# Function to create a custom TCP packet based on user input.
#############################################################
def createTCPPacket(args):
    #packet = TCPPacket(args, 0b010101010)
    ip_header  = b'\x45\x00\x00\x28'  # Version, IHL, Type of Service | Total Length
    ip_header += b'\xab\xcd\x00\x00'  # Identification | Flags, Fragment Offset
    ip_header += b'\x40\x06\xa6\xec'  # TTL, Protocol | Header Checksum
    ip_header += b'\x7f\x00\x00\x01'  # Source Address
    ip_header += b'\x7f\x00\x00\x01'  # Destination Address, currently 127.0.0.1

    tcp_header  = b'\x30\x39\x00\x50' # Source Port | Destination Port
    tcp_header += b'\x00\x00\x00\x00' # Sequence Number
    tcp_header += b'\x00\x00\x00\x00' # Acknowledgement Number

    #tcp_header = covertThings(tcp_header)
    #########################################################################################################
    #A good option for doing bit by bit encoding would be suing the PSH flag and turning that on or off
    #the part were messing with is x02 = 0010. That third bit will be the one were changing (possibly)
    #########################################################################################################
    tcp_header += b'\x50\x02\x71\x10' # Data Offset, Reserved, Flags | Window Size

    tcp_header += b'\xe6\x32\x00\x00' # Checksum | Urgent Pointer

    data = b'Hello World'

    #packet = ip_header + tcp_header
    packet = tcp_header + data

    return packet

#######################################################
# Class to encapsulate our user input in a TCP Packet.
# We pass in the arguements as an array and intialize
# the packet.
#######################################################
class TCPPacket:
    def __init__(self, args, flags=0):
        # Hardcoding for now.
        self.sender_host = '127.0.0.1'
        self.sender_port = 1234
        self.receiver_host = '127.0.0.1'
        self.receiver_port = 1234
        self.flags = flags

    def build(self):
        packet = struct.pack(
            '!sssssssss',               # Format for 9 values in bytes
            bytes(1234),                # Source Port
            bytes(1234),                # Destination Port
            bytes(0),                   # Sequence Number
            bytes(0),                   # Acknoledgement Number
            bytes(5 << 4),              # Data Offset
            bytes(self.flags),          # Flags
            bytes(8192),                # Window
            bytes(0),                   # Checksum (initial value)
            bytes(0)                    # Urgent pointer
        )

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton('127.0.0.1'),           # Source Address
            socket.inet_aton('127.0.0.1'),           # Destination Address
            socket.IPPROTO_TCP,                      # Protocol ID
            len(packet)                              # TCP Length
        )
        checksum = chksum(pseudo_hdr + packet)

        # This packet is definetly not built correctly.
        packet = packet[:16] + struct.pack('s', bytes(checksum)) + packet[18:]

        return packet

###############################################
# Checksum function that calculates the sum of
# 16 bit words and returns it.
###############################################
def chksum(packet):
    if len(packet) % 2 != 0:
        packet += b'\0'
    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff

main(sys.argv)
