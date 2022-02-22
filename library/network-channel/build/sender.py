import sys
import argparse
import socket
import struct
import array

def sender_main(receiverHost, receiverPort, TCPPacket):
    ###########################################################
    # The following 2 lines of code are from a Medium article.
    # It works(?).
    ##########################################################

    # Change to destination port
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.sendto(TCPPacket.build(), (receiverHost, receiverPort))
