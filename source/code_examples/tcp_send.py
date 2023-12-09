import socket

# IP address and port of where we'll send the message.
server_ip_address = '127.0.0.1'
server_ip_port = 10000

# Message to be sent. Stored as a byte array.
# (Hence the b at the front.)
my_message = b"Hello, World!"

try:
    # Create a socket for IPv4 (AF_INET), TCP stream (SOCK_STREAM)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to this specified server and port
    # Note that Python expects ip and port as a list
    destination = (server_ip_address, server_ip_port)
    my_socket.connect(destination)

    # Send the message
    my_socket.sendall(my_message)

    # Close the socket
    my_socket.close()

except ConnectionRefusedError:
    print("Client refused to accept the connection.")

except Exception as e:
    print("Error: ", e)

print("Done sending message.")
