package Aufgabe_5;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;

public class SimpleHTTPClient {
    public static void main(String[] args) {
        String host = "www.google.de";
        int port = 80;
        String path = "/index.html";

        try {
            sendHTTPRequest(host, port, path);
        } catch (UnknownHostException e) {
            System.err.println("Unbekannter Host: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Fehler beim Kommunizieren mit dem Server: " + e.getMessage());
        }
    }

    private static void sendHTTPRequest(String host, int port, String path) throws IOException {
        Socket socket = null;
        OutputStream outputStream = null;
        BufferedReader reader = null;

        try {
            socket = new Socket(host, port);
            outputStream = socket.getOutputStream();

            String httpRequest = "GET " + path + " HTTP/1.1\r\n" +
                    "Host: " + host + "\r\n" +
                    "Connection: close\r\n\r\n";
            outputStream.write(httpRequest.getBytes());
            outputStream.flush();

            reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String line;
            StringBuilder response = new StringBuilder();

            while ((line = reader.readLine()) != null) {
                response.append(line).append("\n");
            }

            System.out.println("Serverantwort:\n" + response.toString());
        } finally {
            if (outputStream != null) {
                outputStream.close();
            }
            if (reader != null) {
                reader.close();
            }
            if (socket != null) {
                socket.close();
            }
        }
    }
}
