import socket
import struct
import collections
import os


def receive_main(destinationPort, sourceHost, destinationHost):
    HOST = destinationHost
    PORT = destinationPort

    IP_header = collections.namedtuple("IP_header", "ers_n_ihl srv_type total_len ip_id flags_n_frag_offset lifetime protocol header_chksum \
                     src_addr dest_addr opt_n_padding")
    TCP_header = collections.namedtuple("TCP_header", "src_port dst_port seq ack offset flags window checksum urgent")
    data_array = []
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as s:
        print("Binding to the socket with Host: %s and Port: %s .." % (str(HOST), str(PORT)))
        s.bind((HOST, PORT))

        print("Begining to listen..")
        s.listen(5)

        #if addr == sourceHost:
        #with conn:
        while True:
            print("Waiting for a connection..")
            conn, addr = s.accept()

            # This will wait until there is data to return
            data = s.recvfrom(1024)
            if not data:
                break
            # data[0].decode() ?
            start_index = 14  # I'm not sure this is correct, but it's something I found online; needs testing
            IP_header._make(struct.unpack("!BBHHHBBHIII", data[start_index:start_index+24]))


            # (src_port, dst_port, seq, ack, offset, flags, window, checksum, urgent) \
            TCP_header._make(struct.unpack("!HHIIBBHHHI", data[start_index+24:start_index+48]))
            data_array.append((IP_header, TCP_header, data[48:]))

    return data_array

def testReceiver():
    # Full message
    aes_key = []

    # Hardcode the destination address and the destination port, for now
    host = '127.0.0.1'
    port = 1234

    # Create a raw socekt..
    # Parameter 1: AF_INET indicates this is for IPv4
    # Parameter 2: SOCK_RAW just indicates we are using a raw socket
    # Parameter 3: IPPROTO_RAW indicates that we supply the IP Header
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    print("Created raw socket..")

    # connect() associates the socket with its local address, a client side operation.
    s.connect((host, port))
    print("Successfully connected to " + str(host) + " on port " + str(port))

    # ******* OLD CODE FOR REFERENCE ******* #
    # server_socket.bind((socket.gethostname(), 8910))
        # Port 8910 is any port that is open from 1024 and above
        # .gethostname() is my local machine, like my name on the terminal

    # Now, lets see if we are receiving any packets..
    while True:

        for packet_count in range(0, 129):
            # recvfrom() receives data from the socket. Return value is a pair (bytes, address)
                # bytes: bytes object representing the data recieved.
                # address: address of the socket that sent the data.
                # Takes in a buffer size. For now, just try to get it all using 1024 (large size)
            print("Trying to receive the data from socket..")
            data = s.recvfrom(1024)

            # Let's print out our data..
            print("Length of bytes object from our received data: " + str(len(data[0])))
            print("Printing out the data, bit by bit..")
            count = 0
            for element in data[0]:
                if count == 20:
                    print("TCP Header: ")
                if count == 0:
                    print("IP Header supplied by the kernel: ")
                if count == 40:
                    print("Data: ")
                print((element))
                count += 1

            print("Covert byte: " + str(data[0][33]))
            # Once we get covert byte, what do we do with it?
                # Create a decoding fundtion
                # Append to aes_key array
            aes_key += str(data[0][33])

            print("Length of our address from our recieved data: " + str(len(data[1])))
            print("Address of sending socket: " + data[1][0])

        # ****** OLD CODE, NOT SURE WHAT TO DO WITH IT ***** #
        #unpacked_data = struct.unpack('!sssssssss', bytes(data[1][0][0], encoding="utf-8"))
        #for x in unpacked_data:
            #try:
                #print("Decoded Byte: %s" % (str(x.decode("utf-8"))))
            #except:
                #print("Error decoding the byte: " + str(x))

        #if data is True:
            #print("Data received: %s \n" % (str(data)))
        #else:
            #print("No data..")
            #break
        break
    # Create a function to print key
    print("AES KEY: " + str(aes_key))
    print("Closing Receiver.")
