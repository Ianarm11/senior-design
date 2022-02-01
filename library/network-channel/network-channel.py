import sys
import argparse

#TODO:
#host_conver() for destination host

#Server mode values vs Client mode values

def main(argv):
    arguments = parser()
    makeFakePacket(arguments)

def makeCovertPacket(args):
    print("We got here!")

def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    parser.add_argument('source_host', type=string, help='Source Host')
    parser.add_argument('desination_host', type=string, help='Destination Host')
    parser.add_argument('source_port', type=int, help='Source Port')
    parser.add_argument('destination_port', type=int, help='Destination Port')
    parser.add_argument('--method', choices=['PID', 'SEQ', 'ACK'], default='PID', help='Choose between PID, Sequence, ACK')
    parser.add_argument('-s', '--server', type=bool, help='Server')
    parser.add_argument('file_name', type=string, help='File Name')

    #parser.add_argument('file', type=int, help='File')
    #parser.add_argument('destination_host_string', type=string, help='Destination Host')
    #parser.add_argument('source_host_string', type=string, help='Source Host')

    args = parser.parse_args()

    return args
