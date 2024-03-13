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
            // Socket-Verbindung zum angegebenen Host und Port aufbauen
            Socket socket = new Socket(host, port);

            // OutputStream für das Senden von Daten an den Server erhalten
            OutputStream outputStream = socket.getOutputStream();

            // Senden des GET-Anforderungsbefehls an den Server
            String httpRequest = "GET " + path + " HTTP/1.1\r\n" +
                                  "Host: " + host + "\r\n" +
                                  "Connection: close\r\n\r\n";
            outputStream.write(httpRequest.getBytes());
            outputStream.flush();

            // InputStream für das Lesen der Serverantwort erhalten
            BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String line;
            StringBuilder response = new StringBuilder();

            // Serverantwort lesen
            while ((line = reader.readLine()) != null) {
                response.append(line).append("\n");
            }

            // Serverantwort ausgeben
            System.out.println("Serverantwort:\n" + response.toString());

            // Ressourcen freigeben
            outputStream.close();
            reader.close();
            socket.close();
        } catch (UnknownHostException e) {
            System.err.println("Unbekannter Host: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Fehler beim Kommunizieren mit dem Server: " + e.getMessage());
        }
    }
}

    

