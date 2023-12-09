import arcade
import random
import socket

INITIAL_SCREEN_WIDTH = 800
INITIAL_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Networked Bouncing Balls"

BUFFER_SIZE = 65536

# Listen to the listed listed address and port for incoming
# balls. Set to None if we aren't listening.
listen_right = ('127.0.0.1', 10001)
listen_left = ('127.0.0.1', 10002)

# Try to send the ball to the address and port if it
# hits the edge. Set to None if it doesn't go anywhere.
send_left = ('127.0.0.1', 10003)
send_right = None

# Set up the sockets for receiving data
# Todo: Create the socket, set the timeout, bind, and listen
# left_socket = ?
# right_socket = ?


class Ball:
    """ This class holds the info about our bouncing ball. """
    def __init__(self):
        self.center_x = 0
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0
        self.radius = 0
        self.color = None

    def move(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y,
                                  self.radius, self.color)


class MyGame(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        arcade.set_background_color(arcade.color.AMAZON)
        self.ball_list = []

    def create_ball(self):
        """ Create a random ball on the screen. """
        ball = Ball()

        # Create a random color, radius, and position
        ball.color = (random.randrange(256), random.randrange(256), random.randrange(256))
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

    def send_ball(self, ball, connection_info):
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

        # Todo: Create a send_socket. Connect. Send the message. Close.
        # send_socket = ?

        print("Sent")

        # Remove the ball from the list
        self.ball_list.remove(ball)

    def receive_ball(self, my_socket):
        ball = None
        try:
            # Todo:
            # Accept a connection on the socket
            # Retrieve the data
            # Close the connection

            # Decode the byte array into a regular UTF-8 string
            # my_string = data.decode("UTF-8")
            # print("Got data:", my_string)

            # Split the data into a list based on a comma
            # my_data = my_string.split(",")

            # Create the ball, and set the fields. Convert the items into
            # an integer before setting the fields.


        except BlockingIOError:
            pass

        # Return the ball variable
        return ball

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        for ball in self.ball_list:
            ball.move()

            if ball.change_x < 0 and ball.center_x - ball.radius < 0:
                if send_left is None:
                    ball.change_x *= -1
                else:
                    try:
                        self.send_ball(ball, send_left)
                    except:
                        ball.change_x *= -1
                        print("Failed to send")

            if ball.change_x > 0 and ball.center_x + ball.radius > self.width:
                if send_right is None:
                    ball.change_x *= -1
                else:
                    try:
                        self.send_ball(ball, send_right)
                    except:
                        ball.change_x *= -1
                        print("Failed to send")

            if ball.change_y < 0 and ball.center_y - ball.radius < 0:
                ball.change_y *= -1
            if ball.change_y > 0 and ball.center_y + ball.radius > self.height:
                ball.change_y *= -1

        # Todo: See if we have any incoming balls from the left
        # Use receive_ball method and left_socket to see if there's a ball
        # If we do, add them to the ball list
        # Set the center to 0
        # Check for a y that is out of bounds and if it is, reverse course
        # Note that you can check self.height to get height of window

        # Todo: Same thing from the right

    def on_key_press(self, key, key_modifiers):
        """ Called whenever a key on the keyboard is pressed. """
        if key == arcade.key.SPACE:
            ball = self.create_ball()
            self.ball_list.append(ball)


def main():
    """ Main method """
    MyGame(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
