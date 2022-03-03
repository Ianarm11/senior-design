import sys
import argparse
import socket
import struct
import array

# Used to take in 2 args variables
def sender_main(TCPPacket):
    # host = '192.168.200.205'
    host = '127.0.0.1'
    port = 1234

    # Create a raw socekt..
    # Parameter 1: AF_INET indicates this is for IPv4
    # Parameter 2: SOCK_RAW just indicates we are using a raw socket
    # Parameter 3: IPPROTO_RAW indicates that we supply the IP Header
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    print("Created raw socket..")

    # Function to set the socket options, not sure if we should be using it
    # s.setsockopt()

    # We bind the socket with the receiver host and port.
        # bind() is for defining the communication end point, usually a server-side operation.
    s.bind((host, port))
    print("Successfully binded the socket at " + str(host) + " on port " + str(port))

    # Lets send data to the socket. Per documentation, this socket should not be connected to a remote socket.
    # snedto() takes in bytes and an address (a tuple).
    s.sendto(TCPPacket.build(), (host, port)) # port used to be 0
    print("Sent packet to " + host + " at port " + str(port))
