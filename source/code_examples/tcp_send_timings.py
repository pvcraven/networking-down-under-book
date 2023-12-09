import socket
from timeit import default_timer as timer

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
    start = timer()
    my_socket.connect(destination)
    elapsed_time = timer() - start
    print(f"Setting up the connection took {elapsed_time:.6f} seconds")

    # Send the message
    start = timer()
    my_socket.sendall(my_message)
    elapsed_time = timer() - start
    print(f"Data sent in {elapsed_time:.6f} seconds")

    # Close the socket
    start = timer()
    my_socket.close()
    elapsed_time = timer() - start
    print(f"Closed connection in {elapsed_time:.6f} seconds")

except ConnectionRefusedError:
    print("Client refused to accept the connection.")

except Exception as e:
    print("Error: ", e)

print("Done sending message.")
