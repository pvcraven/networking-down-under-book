import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

public class SendData {

    public static void main(String[] args) throws Exception {

        InetAddress serverAddress = InetAddress.getByName("127.0.0.1");
        int serverPort =  10000;
        String myData = "Hello world!";

        Socket socket = new Socket(serverAddress, serverPort);

        boolean autoFlush = true;
        PrintWriter out = new PrintWriter(socket.getOutputStream(), autoFlush);
        out.print(myData);
        out.flush();

        socket.close();

        System.out.println("Done sending message.");
    }
}