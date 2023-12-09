import socket

# IP address and port of where we'll send the message.
server_ip_address = '127.0.0.1'
server_ip_port = 10000


def send_data(total_bytes, message_size_in_bytes):
    """
    Send a bunch of messages that sum "total_bytes" of data. Break each
    message into chunks of "message_size_in_bytes". (Try to anyway.)
    """
    # Total number of messages to send.
    messages_to_send = total_bytes // message_size_in_bytes

    # Message as a byte array. (Hence the b at the front.)
    # Send byte array with an X:   b"X"
    # Repeat this (message_size_in_bytes - 1) times.
    my_message = b"X" * (message_size_in_bytes - 1)

    # Open a socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Connect to this server, and this port.
    my_socket.connect((server_ip_address, server_ip_port))

    # Repeat, and send our message over and over.
    for i in range(messages_to_send):
        my_socket.sendall(my_message)

    # Send a message signaling we are done sending packets.
    my_socket.sendall(b"\n")

    # Close the socket
    my_socket.close()

    print("Done")


def main():
    """ Main program. """

    # How many bytes to send
    total_bytes = 5000

    # How big each message will be
    message_size_in_bytes = 10
    print(f"Sending {total_bytes:,} bytes in {message_size_in_bytes} byte chunks.")
    send_data(total_bytes, message_size_in_bytes)


main()
