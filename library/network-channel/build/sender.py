import sys
import argparse
import socket
import struct
import array

############################
# Main sender functionality.
############################
def Sender(TCPPacket):
    host = '127.0.0.1'
    port = 1234

    # Create a raw socekt..
    # Parameter 1: AF_INET indicates this is for IPv4
    # Parameter 2: SOCK_RAW just indicates we are using a raw socket
    # Parameter 3: IPPROTO_RAW indicates that we supply the IP Header
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    print("Created raw socket..")

    # We bind the socket with the receiver host and port.
        # bind() is for defining the communication end point, usually a server-side operation.
    s.bind((host, port))
    print("Successfully binded the socket at " + str(host) + " on port " + str(port))

    # Lets send data to the socket. Per documentation, this socket should not be connected to a remote socket.
    # snedto() takes in bytes and an address (a tuple).
    #s.sendto(TCPPacket.build(), (host, port)) # port used to be 0
    s.sendto(TCPPacket, (host, port))
    print("Sent packet to " + host + " at port " + str(port))
