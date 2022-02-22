import sys
import argparse
import reciever
import sender
import struct
import socket
import array

def main(argv):
    args = parser()
    # Create Socket here?
    # Dependent on the --sender or --receiver arguements
    if args.action == True:
        sender.sender_main(args.receiver_host, args.receiver_port, createTCPPacket(args))
    else:
        reciever.testReceiver(args.sender_host, args.receiver_host, args.receiver_port)

def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    #Taking in all arguments from command line to be able to properly create the TCP packets for sending.
    #Alternatively this is information needed to be able to recieve packets from another user.
    parser.add_argument('sender_host', type=str, help='Sender Host')
    parser.add_argument('receiver_host', type=str, help='Reciveing Host')
    parser.add_argument('sender_port', type=int, help='Sender Port')
    parser.add_argument('receiver_port', type=int, help='Receiver Port')
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

#############################################################
# Function to create a custom TCP packet based on user input.
#############################################################
def createTCPPacket(args):
    packet = TCPPacket(args, 0b010101010)
    #print("Packet Variable: %s Packet Sender Host: %s /n" % (packet, packet.sender_host))
    return packet

#######################################################
# Class to encapsulate our user input in a TCP Packet.
# We pass in the arguements as an array and intialize
# the packet.
#######################################################
class TCPPacket:
    def __init__(self, args, flags=0):
        self.sender_host = args.sender_host
        self.sender_port = args.sender_port
        self.receiver_host = args.receiver_host
        self.receiver_port = args.receiver_port
        self.flags = flags

    def build(self):

        packet = struct.pack(
            '!HHIIBBHHH',
            self.sender_port,    # Source Port
            self.receiver_port,  # Destination Port
            0,                   # Sequence Number
            0,                   # Acknoledgement Number
            5 << 4,              # Data Offset
            self.flags,          # Flags
            8192,                # Window
            0,                   # Checksum (initial value)
            0                    # Urgent pointer
        )

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.sender_host),      # Source Address
            socket.inet_aton(self.receiver_host),    # Destination Address
            socket.IPPROTO_TCP,                      # Protocol ID
            len(packet)                              # TCP Length
        )

        checksum = chksum(pseudo_hdr + packet)
        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]

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
