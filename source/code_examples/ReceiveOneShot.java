import java.util.Iterator;
import java.util.Set;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;

public class ReceiveOneShot {

    private Selector channelSelector;
    private ServerSocketChannel myServerSocketChannel;

    public void setupSocket() throws Exception {

        // Selector: multiplexor of SelectableChannel objects
        channelSelector = Selector.open(); // selector is open here

        // ServerSocketChannel: selectable channel for stream-oriented listening sockets
        myServerSocketChannel = ServerSocketChannel.open();
        InetSocketAddress myAddress = new InetSocketAddress("127.0.0.1", 10000);

        // Binds the channel's socket to a local address and configures the socket to listen for connections
        myServerSocketChannel.bind(myAddress);

        // Adjusts this channel's blocking mode.
        myServerSocketChannel.configureBlocking(false);

        // Used as a 'state machine' for figuring if socket is waiting for a connection,
        // or if we have a connection and instead should be receiving data
        int ops = myServerSocketChannel.validOps();
        SelectionKey selectKy = myServerSocketChannel.register(channelSelector, ops, null);

        System.out.println("\nStarting...");

    }
    public boolean checkConnection() throws Exception {
        // Set to true when we have our whole message
        boolean done = false;

        // Selects a set of keys whose corresponding channels are ready for I/O operations
        // For blocking I/O use a select with no data:
        // channelSelector.select(10);
        // For non-blocking, use a select with a number in ms to wait. (Using zero will chew a lot
        // of CPU unless something else in the loop waits.)
        // channelSelector.select(0);
        channelSelector.select(0);

        // Token representing the registration of a SelectableChannel with a Selector
        Set<SelectionKey> myKeys = channelSelector.selectedKeys();
        Iterator<SelectionKey> keyIterator = myKeys.iterator();

        while (keyIterator.hasNext()) {
            SelectionKey myKey = keyIterator.next();

            // Tests whether this key's channel is ready to accept a new socket connection
            if (myKey.isAcceptable()) {
                SocketChannel myClient = myServerSocketChannel.accept();

                // Adjusts this channel's blocking mode to false
                myClient.configureBlocking(false);

                // Operation-set bit for read operations
                myClient.register(channelSelector, SelectionKey.OP_READ);
                System.out.println("Connection Accepted: " + myClient.getLocalAddress());

                // Tests whether this key's channel is ready for reading
            } else if (myKey.isReadable()) {

                    SocketChannel myClient = (SocketChannel) myKey.channel();
                    ByteBuffer myBuffer = ByteBuffer.allocate(65536);
                    int bytesRead = myClient.read(myBuffer);
                    String result = new String(myBuffer.array());
                    result = result.substring(0, bytesRead);
                    if (result.length() > 0) {
                        System.out.println("Message received " + result.length() + " bytes: \"" + result + "\"");
                    }

                if (result.endsWith("\n")) {
                    myClient.close();
                    done = true;
                    System.out.println("It's time to close connection as we got a Z");
                }
            }
            keyIterator.remove();
        }
        return done;
    }

    public static void main(String[] args) throws Exception {
        ReceiveOneShot receiveOneShot = new ReceiveOneShot();

        receiveOneShot.setupSocket();

        boolean done = false;
        while(!done)
            done = receiveOneShot.checkConnection();
    }
}