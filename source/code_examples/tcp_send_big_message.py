import socket

# IP address and port of where we'll send the message.
server_ip_address = '127.0.0.1'
server_ip_port = 10000

# Size of our message.
# Must be at least 1
message_size_in_bytes = 600000

# Create a message as a byte array.
# Use multiplication to quickly create an array of n-1 bytes.
# Add a \n at the end which we will use to detect end-of-message.
my_message = b"X" * (message_size_in_bytes - 1) + b"\n"

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

print("Done")