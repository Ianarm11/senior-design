import socket
import struct
import collections


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

def testReceiver(sender_host, receiver_host, receiver_port):
    #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Functions like .listen and .accept will not work with RAW Sockets
    # Should this be IPProto-TCP or UDP?

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    print("Creating socket..")

    # server_socket.bind((socket.gethostname(), 8910))
    server_socket.bind((receiver_host, receiver_port))
    # print("8910: %s" % (8910))
    print("Binding socket..")
    # Port 8910 is any port that is open from 1024 and above
    # .gethostname() is my local machine, like my name on the terminal

    # server_socket.listen(5)
    # print("Listening up to 5 requests on the socket..")

    # print("Waiting for a connection..")
    # (connection, address) = server_socket.accept()

    while True:
        print("Trying to receive the data from socket..")
        data = server_socket.recvfrom(1024)
        print("Data: %s" % (data))
        #print("Data Variable: %s \n" % (str(data))
        if data is True:
            print("Data received: %s \n" % (str(data)))
        else:
            print("No data..")
            break

    print("Closing Receiver.")
#if __name__ == '__main__':
    #receive(666, '127.0.0.2')
