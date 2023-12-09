import socket

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

# Create a socket for sending/receiving data
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

while True:

    connection = None
    try:
        # Get a connection, and the address that hooked up to us.
        # The 'client address' is an array that has the IP and the port.
        connection, client_address = my_socket.accept()

        # Read in the data, up to the number of characters in BUFFER_SIZE
        data = connection.recv(BUFFER_SIZE)

        # Print what we read in, and from where
        client_ip = client_address[0]
        client_port = client_address[1]

        # Decode the byte string to a normal string
        data_string = data.decode("UTF-8")

        print(f"Data from {client_ip}:{client_port} --> '{data_string}'")

    except Exception as e:
        # Whoa Nelly! Was there an error?
        print("Unable to receive the message.", e)

    finally:
        # Close the socket. No socket operations can happen after this.
        # If there was more data to send, you would not want to do this.
        # You would want a loop of 'recv' and keep the 'accept' and 'close'
        # out of that loop.
        if connection:
            connection.close()

# Because we have a 'while True' loop we'll never get here. But this
# is the proper code to run when you want to shut down the socket properly.
socket.close()

print("Done")
