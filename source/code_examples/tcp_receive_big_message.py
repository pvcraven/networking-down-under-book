import socket
import time

# This is your buffer size.
# You can't receive anything more than the buffer size at one time.
BUFFER_SIZE = 65535

# This should be the IP address of the computer you run this
# code on (the server). It should be the SAME IP address that
# the client hooks up to.
# Note: If you use '127.0.0.1' you can only receive connections
# from the same computer. Outside computers cannot connect to a
# computer listening to 127.0.0.1.
my_ip_address = '127.0.0.1'
my_ip_port = 10000

# We will loop until we get a connection or we get data. We don't want
# to check thousands of times per second for these because that would
# max our CPU. If we have nothing to do, how long we wait before we
# check again.
DELAY = 0.1

# We need to build a "state machine" that keeps
# track of if we are connected or not
NO_CONNECTION = 1
CONNECTED = 2

state = NO_CONNECTION

# Our full message. Starts empty.
full_message = b""

# We will keep receiving data until we get a \n. Once we see that, we'll set
# done to true.
done = False

# Keep track of how many chunks of data we receive.
chunks = 0

connection = None
client_ip = None
client_port = None


# Create a socket for sending/receiving data
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Make the socket non-blocking
my_socket.settimeout(0.0)

# Tell the socket it will be listening on my_ip_address, and my_port.
# Note that Python expects ip and port as a list
listen_to = (my_ip_address, my_ip_port)
my_socket.bind(listen_to)

# We are going to be listening as a server, not connecting as a client.
# The "1" specifies the size of the backlog of connections we allow before
# refusing connections.
my_socket.listen(1)

while not done:

    # If we have no connection, then see if we can build a connection
    if state == NO_CONNECTION:
        try:
            # Get a connection, and the address that hooked up to us.
            # The 'client address' is an array that has the IP and the port.
            connection, client_address = my_socket.accept()
            client_ip = client_address[0]
            client_port = client_address[1]
            state = CONNECTED
        except BlockingIOError:
            pass

    # If we have a connection, receive data
    if state == CONNECTED:
        try:
            # Read in the data, up to the number of characters in BUFFER_SIZE
            data = connection.recv(BUFFER_SIZE)
            chunks += 1

            if len(data) > 0:
                print(f"Data from {client_ip}:{client_port} '{data}'")

            # Append this chunk to the full message
            full_message += data

            # If we get a \n, then assume we have received all the data.
            if full_message[-1] == 10:
                # Close the socket. No socket operations can happen after this.
                state = NO_CONNECTION
                connection.close()
                done = True

        except BlockingIOError:
            pass

# Close the socket. No socket operations can happen after this.
my_socket.close()

print(f"Done receiving message.")
print(f"Processed {len(full_message)} bytes in {chunks} chunks.")