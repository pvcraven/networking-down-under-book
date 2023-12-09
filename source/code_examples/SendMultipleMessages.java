import java.io.PrintWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;

public class SendMultipleMessages {

    private static void sendData(int totalBytes, int messageSizeInBytes)
            throws IOException {

        // Modify this to match to be THIS computer's address
        String ipAddress = "127.0.0.1";
        int serverPort = 10000;

        InetAddress serverAddress = InetAddress.getByName(ipAddress);
        int messagesToSend = totalBytes / messageSizeInBytes;

        String myData = "";
        for(int i = 0; i < messageSizeInBytes; i++) {
            myData += "X";
        }

        Socket socket = new Socket(serverAddress, serverPort);

        // Try changing this to false and see if it changes how packets are sent
        boolean autoFlush = true;
        PrintWriter out = new PrintWriter(socket.getOutputStream(), autoFlush);

        for (int i = 0; i < messagesToSend; i++) {
            out.print(myData);
            // Try enabling this and see if it changes how packets are sent
            // out.flush();
        }
        out.print("\n");

        out.flush();

        socket.close();
    }
    public static void main(String[] args) throws Exception {

        // How many bytes to send
        int totalBytes = 5000;

        // How big each message will be
        int messageSizeInBytes = 10;

        System.out.println("Sending " + totalBytes + "bytes in " + messageSizeInBytes + " byte chunks.");

        // Send the data
        sendData(totalBytes, messageSizeInBytes);

        System.out.println("Done sending message.");
    }
}