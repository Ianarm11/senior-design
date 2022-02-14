import socket
import struct
import collections


def receive(port, source):
    HOST = '127.0.0.1'
    PORT = port
    IP_header = collections.namedtuple("IP_header", "ers_n_ihl srv_type total_len ip_id flags_n_frag_offset lifetime protocol header_chksum \
                     src_addr dest_addr opt_n_padding")
    TCP_header = collections.namedtuple("TCP_header", "src_port dst_port seq ack offset flags window checksum urgent")
    data_array = []
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        if addr == source:
            with conn:
                while True:
                    data = s.recv(65536)
                    if not data:
                        break
                    start_index = 14  # I'm not sure this is correct, but it's something I found online; needs testing
                    IP_header._make(struct.unpack("!BBHHHBBHIII", data[start_index:start_index+24]))
                    # (src_port, dst_port, seq, ack, offset, flags, window, checksum, urgent) \
                    TCP_header._make(struct.unpack("!HHIIBBHHHI", data[start_index+24:start_index+48]))

                    data_array.append((IP_header, TCP_header, data[48:]))

    return data_array


if __name__ == '__main__':
    receive(666, '127.0.0.2')

