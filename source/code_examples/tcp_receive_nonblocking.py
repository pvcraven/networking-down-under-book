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

current_state = NO_CONNECTION

# Create a socket for sending/receiving data
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Make the socket non-blocking
my_socket.settimeout(0.0)

# Tell the socket it will be listening on my_ip_address, and my_port.
# Note that Python expects ip and port as a list
listen_to = (my_ip_address, my_ip_port)
my_socket.bind(listen_to)

# We are going to be listening as a server, not connecting as a client.
# So we call the 'listen' method of our socket.
# The "1" specifies the size of the backlog of connections we allow before
# refusing connections. If we specify 1, then once we pick up a connection
# we won't accept any others until we close the current connection.
my_socket.listen(1)

connection = None
client_ip = None
client_port = None

while True:

    # If we have no connection, then see if we can build a connection
    if current_state == NO_CONNECTION:
        try:
            # Get a connection, and the address that hooked up to us.
            # The 'client address' is an array that has the IP and the port.
            connection, client_address = my_socket.accept()
            client_ip = client_address[0]
            client_port = client_address[1]
            current_state = CONNECTED
        except BlockingIOError:
            # There was no connection. Wait before checking again.
            time.sleep(DELAY)

    # If we have a connection, receive data
    if current_state == CONNECTED:
        try:
            # Read in the data, up to the number of characters in BUFFER_SIZE
            data = connection.recv(BUFFER_SIZE)

            # See if we have data
            if len(data) > 0:

                # Decode the byte string to a normal string
                data_string = data.decode("UTF-8")

                # Print what we read in, and from where
                print(f"Data from {client_ip}:{client_port} --> '{data_string}'")

            # Close the socket. No socket operations can happen after this.
            # If there was more data to send, you would not want to do this.
            # You would want a loop of 'recv' and keep the 'accept' and 'close'
            # out of that loop.
            # Normally you'd send some kind of 'special' data that would indicate
            # you are done.
            current_state = NO_CONNECTION
            connection.close()

        except BlockingIOError:
            # There was no data. Wait before checking again.
            time.sleep(DELAY)

# Because we have a 'while True' loop we'll never get here. But this
# is the proper code to run when you want to shut down the socket properly.
my_socket.close()

print("Done")
