import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class ReceiveDataBlocking {
    public static void main(String[] args) throws Exception {
        // Set up the socket
        int port = 10000;
        int backlog = 1;
        InetAddress address = InetAddress.getByName("127.0.0.1");
        ServerSocket server = new ServerSocket(port, backlog, address);

        // Accept a connection
        System.out.println("Accepting connections...");
        Socket client = server.accept();
        String clientAddress = client.getInetAddress().getHostAddress();
        System.out.println("\r\nNew connection from " + clientAddress);

        // Read in the message
        BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        String data = null;
        data = in.readLine();

        // Print the message
        System.out.println("\r\nMessage from " + clientAddress + ": " + data);

        // Close the connection
        server.close();
        System.out.println("Done");
    }
}