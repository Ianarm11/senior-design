import sys
import argparse
import socket
import struct
import array

#TODO:
#host_conver() for destination host

#Server mode values vs Client mode values

#def makeCovertPacket(args):

def sender_main(destinationPort, TCPPacket):
#    args = parser()
#    packet = TCPPacket(
#        0b000101001  # Merry Christmas!
#    )
#    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#    #host = socket.gethostname()
#    #s.connect((args.destination_host, args.destination_port))
#    #s.bind((str(args.destination_host), args.destination_port))
#    s.sendto(packet.build(), (str(args.destination_host), args.destination_port))
#    args = parser()

    host = socket.gethostname()
    port = destinationPort
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(TCPPacket.build())

    #packet = TCPPacket(
    #    0b010101010  # Merry Christmas!
    #)
