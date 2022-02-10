import sys
import argparse
import socket
import struct
import array

#TODO:
#host_conver() for destination host

#Server mode values vs Client mode values

#def makeCovertPacket(args):

def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    #Taking in all arguments from command line to be able to properly create the TCP packets for sending.
    #Alternatively this is information needed to be able to recieve packets from another user. 
    parser.add_argument('source_host', type=str, help='Source Host')
    parser.add_argument('destination_host', type=str, help='Destination Host')
    parser.add_argument('source_port', type=int, help='Source Port')
    parser.add_argument('destination_port', type=int, help='Destination Port')\
    #parser.add_argument('--method', choices=['PID', 'SEQ', 'ACK'], default='PID', help='Choose between PID, Sequence, ACK')
    #parser.add_argument('-s', '--sender', type=bool, help='Sender')
    #parser.add_argument('file_name', type=str, help='File Name')

    args = parser.parse_args()

    return args

class TCPPacket:
    def __init__(self,flags=0):
        args = parser()
        self.src_host = args.source_host
        self.src_port = args.source_port
        self.dst_host = args.destination_host
        self.dst_port = args.destination_port
        self.flags = flags

    def build(self):

        packet = struct.pack(
            '!HHIIBBHHH',
            self.src_port,  # Source Port
            self.dst_port,  # Destination Port
            0,              # Sequence Number
            0,              # Acknoledgement Number
            5 << 4,         # Data Offset
            self.flags,     # Flags
            8192,           # Window
            0,              # Checksum (initial value)
            0               # Urgent pointer
        )

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),    # Source Address
            socket.inet_aton(self.dst_host),    # Destination Address
            socket.IPPROTO_TCP,                 # Protocol ID
            len(packet)                         # TCP Length
        )

        checksum = chksum(pseudo_hdr + packet)
        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]

        return packet


def chksum(packet):
    if len(packet) % 2 != 0:
        packet += b'\0'
    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff

def main(argv):
#    args = parser()
#    packet = TCPPacket(
#        0b000101001  # Merry Christmas!
#    )
#    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#    #host = socket.gethostname()
#    #s.connect((args.destination_host, args.destination_port))
#    #s.bind((str(args.destination_host), args.destination_port))
#    s.sendto(packet.build(), (str(args.destination_host), args.destination_port))
    args = parser()
    host = socket.gethostname()
    port = args.destination_port
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
    s.connect((host,port))

    packet = TCPPacket(
        0b010101010  # Merry Christmas!
    )


    s.sendall(packet.build())



main(sys.argv)