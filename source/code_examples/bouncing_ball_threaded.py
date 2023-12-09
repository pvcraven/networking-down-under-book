"""
Networked bouncing ball program.
Can bounce a ball from one computer to another, or between two programs on the
same computer.

Currently, this is set up for two programs on the same computer.
If you want to bounce between different computers, see the main() method and
modify the addresses/ports accordingly.

Requires "Arcade" library (which doesn't run on Raspberry Pi.)

Run with:
python bouncing_ball_threaded.py left

"""
import arcade
import random
import socket
import sys
import threading
import time

INITIAL_SCREEN_WIDTH = 800
INITIAL_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Networked Bouncing Balls"

BUFFER_SIZE = 65536


class Ball:
    """ This class holds the info about our bouncing ball. """
    def __init__(self):
        self.center_x = 0
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0
        self.radius = 0
        self.color = None

        # Set to 'True' if we are trying to send this ball out
        self.sending = False

    def move(self):
        # Only move the ball if it isn't in the middle of being sent
        if not self.sending:
            self.center_x += self.change_x
            self.center_y += self.change_y

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y,
                                  self.radius, self.color)


class MyGame(arcade.Window):
    """ Main application class. """
    def __init__(self,
                 width,
                 height,
                 title,
                 send_left,
                 send_right,
                 listen_left,
                 listen_right):
        super().__init__(width, height, title, resizable=True)

        # Set out background color
        arcade.set_background_color(arcade.color.EERIE_BLACK)

        # List of balls
        self.ball_list = []

        # Info on what network connections we send balls out to if they
        # hit the edge of the screen. Stored as an (address, port) tuple.
        self.send_left = send_left
        self.send_right = send_right

        # Info on what network connections listen for incoming balls.
        self.listen_left = listen_left
        self.listen_right = listen_right

        # Socket info, as we need to keep the incoming connections open.
        self.left_socket = None
        self.right_socket = None
        self.thread_left = None
        self.thread_right = None

        # Set up the sockets for receiving data
        if listen_left:
            print("Opening socked to listen for incoming balls from the LEFT.")
            self.left_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.left_socket.settimeout(0.0)
            self.left_socket.bind(listen_left)
            self.left_socket.listen(1)
            self.thread_left = ReceiveThread(self, self.left_socket, "left")
            self.thread_left.start()

        if listen_right:
            print("Opening socked to listen for incoming balls from the RIGHT.")
            self.right_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.right_socket.settimeout(0.0)
            self.right_socket.bind(listen_right)
            self.right_socket.listen(1)
            self.thread_right = ReceiveThread(self, self.right_socket, "right")
            self.thread_right.start()

    def create_ball(self):
        """ Create a random ball on the screen. """
        ball = Ball()

        # Create a random color, radius, and position
        ball.color = (random.randrange(256), random.randrange(256), random.randrange(256))
        # ball.color = (0, 0, 0)
        ball.radius = random.randrange(20, 41)
        ball.center_x = random.randrange(self.width)
        ball.center_y = random.randrange(self.height)

        # Loop until the ball isn't stationary
        while ball.change_x == 0 and ball.change_y == 0:
            ball.change_x = random.randrange(-5, 6)
            ball.change_y = random.randrange(-5, 6)

        return ball

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        # Draw each ball
        for ball in self.ball_list:
            ball.draw()

    def send_ball(self,
                  ball: Ball,
                  connection_info: (int, int)):
        """ Make a network call to send the ball out over the network."""

        # Create the message
        my_message = f"{ball.center_x},{ball.center_y}," \
            f"{ball.change_x},{ball.change_y}," \
            f"{ball.radius}," \
            f"{ball.color[0]},{ball.color[1]},{ball.color[2]}"

        # Convert the message to a byte array that our socket expects.
        my_message_bytes = my_message.encode()

        # Send the data
        print(f"Send {my_message}")

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect(connection_info)
        send_socket.sendall(my_message_bytes)
        send_socket.close()
        print("Sent")

        # Remove the ball from the list
        self.ball_list.remove(ball)

    def receive_ball(self, my_socket):
        """
        Receive a ball from an incoming network socket.
        Returns immediately if no incoming ball.
        """
        # Our return ball value, if we get one.
        ball = None
        try:
            # Accept a connection on the socket
            connection, client_address = my_socket.accept()

            # Retrieve the data
            data = connection.recv(BUFFER_SIZE)

            # Close the connection
            connection.close()

            # Decode the byte array into a regular UTF-8 string
            my_string = data.decode("UTF-8")
            print("Got data:", my_string)

            # Split the data into a list based on a comma
            my_data = my_string.split(",")

            # Create the ball, and set the fields. Convert the items into
            # an integer before setting the fields.
            ball = Ball()
            ball.color = (int(my_data[5]), int(my_data[6]), int(my_data[7]))
            ball.radius = int(my_data[4])
            ball.center_x = int(my_data[0])
            ball.center_y = int(my_data[1])
            ball.change_x = int(my_data[2])
            ball.change_y = int(my_data[3])

        except BlockingIOError:
            # No balls on this check.
            pass

        # Return the ball variable
        return ball

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        for ball in self.ball_list:
            ball.move()

            # Ball hits left side of the screen
            if ball.change_x < 0 \
                    and ball.center_x - ball.radius < 0 \
                    and not ball.sending:

                # Do we have a computer  to send the ball to?
                if self.send_left is None:
                    # No, bounce it.
                    ball.change_x *= -1
                else:
                    # Yes, try to send it
                    print("Send left")
                    ball.sending = True
                    thread = SendThread(self, ball, self.send_left)
                    thread.start()

            # Ball hits right side of the screen
            if ball.change_x > 0 \
                    and ball.center_x + ball.radius > self.width\
                    and not ball.sending:

                # Do we have a computer  to send the ball to?
                if self.send_right is None:
                    # No, bounce it.
                    ball.change_x *= -1
                else:
                    # Yes, try to send it
                    print("Send right")
                    ball.sending = True
                    thread = SendThread(self, ball, self.send_right)
                    thread.start()


            # Ball hits bottom of screen, bounce
            if ball.change_y < 0 and ball.center_y - ball.radius < 0:
                ball.change_y *= -1

            # Ball hits top of screen, bounce
            if ball.change_y > 0 and ball.center_y + ball.radius > self.height:
                ball.change_y *= -1

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """

        # Spawn a new ball with a space
        if key == arcade.key.SPACE:
            ball = self.create_ball()
            self.ball_list.append(ball)

        # Quit with a Q
        if key == arcade.key.Q:
            exit()

        # Flip between full/windowed with F
        if key == arcade.key.F:
            # User hits s. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, self.screen.width, 0, self.screen.height)


class ReceiveThread(threading.Thread):
    """
    This class will manage a thread.
    """

    def __init__(self,
                 game: MyGame,
                 socket,
                 side: str):
        """
        Constructor. Get stuff set up, set variables.
        """
        super().__init__()
        # thread_no is a label so we can track which thread is printing.
        self.game = game
        self.socket = socket
        self.keep_running = True
        self.side = side

    def run(self):
        """
        This method will be run concurrently as a separate thread.
        """

        # Loop and pause a bit between each loop
        while self.keep_running:
            ball = self.game.receive_ball(self.socket)

            if ball:
                print(f"Receive {self.side}.")
                if self.side == "right":
                    ball.center_x = self.game.width
                    print(f"Ball's x: {ball.center_x}")
                if self.side == "left":
                    ball.center_x = 0
                self.game.ball_list.append(ball)

            time.sleep(0.1)

        print("Shutting down receiving thread.")

class SendThread(threading.Thread):
    """
    This class will manage a thread.
    """

    def __init__(self, game: MyGame, ball, info):
        """
        Constructor. Get stuff set up, set variables.
        """
        super().__init__()

        self.game = game
        self.info = info
        self.ball = ball

    def run(self):
        """
        This method will be run concurrently as a separate thread.
        """
        try:
            print("Send")
            self.game.send_ball(self.ball, self.info)
        except:
            self.ball.change_x *= -1
            self.ball.sending = False
            print("Failed to send")


def main():
    """ Main method """

    # Startup.
    print("Welcome to the networked bouncing ball program!")

    # Read in the command-line parameter, and error our if we don't specify
    # what position this computer is in.
    if len(sys.argv) != 2 or (sys.argv[1] != "right" and sys.argv[1] != "left"):
        print("Run this program with the command line argument of either 'left' or 'right'.")
        print("Such as: python bouncing_ball.py left")
        return

    # Left or right computer? Grab from command-line parameter.
    computer_location = sys.argv[1]

    if computer_location == "right":
        # Ok, this is the right-side computer.
        # Listen to the listed address and port for incoming
        # balls from the left side.
        my_address = '127.0.0.1'
        port_i_listen_to = 10001
        listen_left = (my_address, port_i_listen_to)

        # We won't listed for incoming balls from the right.
        listen_right = None

        # If the ball hits the left edge, try to send the ball to the address
        # and port.
        left_computer_address = '127.0.0.1'
        left_computer_port = 10002
        send_left = (left_computer_address, left_computer_port)

        # Don't send any balls that hit the right edge
        send_right = None
    else:
        # Ok, this is the left-side computer.
        my_address = '127.0.0.1'
        port_i_listen_to = 10002
        listen_right = (my_address, port_i_listen_to)

        listen_left = None

        right_computer_address = '127.0.0.1'
        right_computer_port = 10001
        send_right = (right_computer_address, right_computer_port)

        send_left = None

    # Create the game object
    game_object = MyGame(INITIAL_SCREEN_WIDTH,
                  INITIAL_SCREEN_HEIGHT,
                  SCREEN_TITLE,
                  send_left,
                  send_right,
                  listen_left,
                  listen_right)

    # Run the game
    arcade.run()

    # Shut down any listening threads
    if game_object.thread_left:
        game_object.thread_left.keep_running = False

    if game_object.thread_right:
        game_object.thread_right.keep_running = False


if __name__ == "__main__":
    main()
