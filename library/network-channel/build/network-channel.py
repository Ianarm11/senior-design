import sys
import argparse
import reciever
import sender

#TODO:
#Server mode values vs Client mode values

def main(argv):
    args = parser()
    #Reciever Main Function
    reciever.receive_main(args.reciever_port, args.sender_host, args.reciever_host)
    #Sender Main Function
    sender.sender_main(args.reciever_port, createTCPPacket(args))

def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    #Taking in all arguments from command line to be able to properly create the TCP packets for sending.
    #Alternatively this is information needed to be able to recieve packets from another user.
    parser.add_argument('sender_host', type=str, help='Sender Host')
    parser.add_argument('reciever_host', type=str, help='Reciveing Host')
    parser.add_argument('sender_port', type=int, help='Sender Port')
    parser.add_argument('reciever_port', type=int, help='Reciever Port')\
    #parser.add_argument('--method', choices=['PID', 'SEQ', 'ACK'], default='PID', help='Choose between PID, Sequence, ACK')
    #parser.add_argument('-s', '--sender', type=bool, help='Sender')
    #parser.add_argument('file_name', type=str, help='File Name')

    #parser.add_argument('file', type=int, help='File')
    #parser.add_argument('destination_host_string', type=string, help='Destination Host')
    #parser.add_argument('source_host_string', type=string, help='Source Host')

    args = parser.parse_args()

    return args

def createTCPPacket(args):
    packet = TCPPacket(
        args,
        0b010101010  # Merry Christmas!
    )
    print(packet.flags)
    print(packet.src_port)
    return packet

class TCPPacket:
    def __init__(self, args, flags=0):
        self.src_host = args.sender_host
        self.src_port = args.sender_port
        self.dst_host = args.reciever_host
        self.dst_port = args.reciever_port
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

main(sys.argv)
