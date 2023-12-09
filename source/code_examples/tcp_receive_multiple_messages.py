import socket
from timeit import default_timer as timer

# Receive info
my_ip_address = '127.0.0.1'
my_ip_port = 10000
BUFFER_SIZE = 65536

# We need to build a "state machine" that keeps
# track of if we are connected or not
NO_CONNECTION = 1
CONNECTED = 2


class MyConnectionHandler:
    """ Handle receiving data """

    def __init__(self):
        """
        Initialize the class
        """
        self.my_socket = None
        self.state = NO_CONNECTION

    def start_listening(self):
        """
        Open the socket for listening
        """
        print("Listening for a connection...")
        # Create a socket for sending/receiving data
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Make the socket non-blocking
        self.my_socket.settimeout(0.0)

        # Tell the socket it will be listening on my_ip_address, and my_port.
        self.my_socket.bind((my_ip_address, my_ip_port))

        # We are going to be listening as a server, not connecting as a client.
        # The "2" specifies the size of the backlog of connections we allow before
        # refusing connections.
        self.my_socket.listen(2)

    def handle_connection(self):
        """ Manage a connected socket """
        # Our full message. Right now it is blank.
        full_message = b""

        done = False
        chunks = 0
        total_time = 0

        while not done:

            # If we have no connection, then see if we can build a connection
            if self.state == NO_CONNECTION:
                try:
                    # Get a connection, and the address that hooked up to us.
                    # The 'client address' is an array that has the IP and the port.
                    connection, client_address = self.my_socket.accept()
                    self.state = CONNECTED

                    print("Connected, receiving data...")

                    # Start timing how long this takes.
                    if len(full_message) == 0:
                        start_time = timer()

                except BlockingIOError:
                    pass

            # If we have a connection, receive data
            if self.state == CONNECTED:
                try:
                    # Read in the data, up to the number of characters in BUFFER_SIZE
                    data = connection.recv(BUFFER_SIZE)
                    chunks += 1

                    # Append this chunk to the full message
                    full_message += data

                    # See if last letter is a \n or 'Y'. If so, close socket.
                    # 'Y' signifies end of this 'chunk', a '\n' signifies end of
                    # the entire message.
                    last_letter = full_message[-1]
                    if last_letter == 10 or last_letter == 89:
                        # Close the socket. No socket operations can happen after this.
                        self.state = NO_CONNECTION
                        connection.close()
                        print(f"Closing connection, total of {len(full_message)} bytes received.")

                        if last_letter == 10:
                            # Stop timing how long this takes.
                            total_time = timer() - start_time
                            done = True
                            print("Done receiving data")

                except BlockingIOError:
                    pass

        # Calculate our results
        total_bytes = len(full_message)
        data_rate = total_bytes / total_time

        # Print our results
        # If you are graphing this, you might want to change the output to be
        # easier to get into Excel.
        print(f"Processed {total_bytes:,} bytes in {chunks:,} chunks.")
        print(f"Total time: {total_time:.3f} seconds.")
        print(f"Data rate: {data_rate:,.0f} bytes/second.")
        print()

    def stop_listening(self):
        # Close the socket. No socket operations can happen after this.
        self.my_socket.close()


def main():
    my_connection_handler = MyConnectionHandler()
    my_connection_handler.start_listening()

    while True:
        my_connection_handler.handle_connection()

    # Ok, we don't actually get here. But if we did, this is how you'd
    # properly shut down.
    my_connection_handler.stop_listening()

main()
