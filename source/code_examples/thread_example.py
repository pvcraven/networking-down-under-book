import threading
import time


class MyThread(threading.Thread):
    """
    This class will manage a thread.
    """
    def __init__(self, thread_no):
        """
        Constructor. Get stuff set up, set variables.
        """
        super().__init__()
        # thread_no is a label so we can track which thread is printing.
        self.thread_no = thread_no

    def run(self):
        """
        This method will be run concurrently as a separate thread.
        """

        # Loop and pause a bit between each loop
        for count in range(10):
            print(f"Thread {self.thread_no} count {count}")
            time.sleep(0.25)


if __name__ == '__main__':
    """
    Make four threads, and have them run concurrently.
    """
    for x in range(4):

        # Create a new thread
        my_thread = MyThread(x)

        # Notice below we call "start" not "run". The "start" will call the "run"
        # method for you, but as a separate thread.

        # If you change "start" to "run" it will NOT be threaded, and you can
        # see the difference.
        my_thread.start()
