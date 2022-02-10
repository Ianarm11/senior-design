import sys
import argparse

#TODO:
#host_conver() for destination host

#Server mode values vs Client mode values

def main(argv):
    arguments = parser()
    print(getKey())
    #makeCovertPacket(arguments)

#def makeCovertPacket(args):
    

def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    #Taking in all arguments from command line to be able to properly create the TCP packets for sending.
    #Alternatively this is information needed to be able to recieve packets from another user. 
    parser.add_argument('source_host', type=str, help='Source Host')
    parser.add_argument('desination_host', type=str, help='Destination Host')
    parser.add_argument('source_port', type=int, help='Source Port')
    parser.add_argument('destination_port', type=int, help='Destination Port')\
    parser.add_argument('--method', choices=['PID', 'SEQ', 'ACK'], default='PID', help='Choose between PID, Sequence, ACK')
    parser.add_argument('-s', '--sender', type=bool, help='Sender')
    parser.add_argument('file_name', type=str, help='File Name')

    #parser.add_argument('file', type=int, help='File')
    #parser.add_argument('destination_host_string', type=string, help='Destination Host')
    #parser.add_argument('source_host_string', type=string, help='Source Host')

    args = parser.parse_args()

    return args


main(sys.argv)