package Aufgabe_8;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;

import com.sun.net.httpserver.*;

public class HTTPServer {    
    public static void main(String[] args) throws Exception {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        System.out.println("Server läuft auf http://localhost:" + port);
        server.createContext("/", new RootHandler());
        server.setExecutor(null);
        server.start();
    }

    public static class RootHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange he) throws IOException {
            try {
                File file = new File("Aufgabe_8/index.html");
                if (!file.exists() || file.isDirectory()) {
                    // Wenn die Datei nicht gefunden wurde, eine Fehlermeldung senden
                    String response = "404 - Datei nicht gefunden";
                    he.sendResponseHeaders(404, response.length());
                    try (OutputStream os = he.getResponseBody()) {
                        os.write(response.getBytes());
                    }
                    return;
                }

                he.sendResponseHeaders(200, file.length());
                try (OutputStream os = he.getResponseBody()) {
                    Files.copy(file.toPath(), os);
                }
            } catch (IOException e) {
                e.printStackTrace();
                String response = "500 - Interner Serverfehler";
                he.sendResponseHeaders(500, response.length());
                try (OutputStream os = he.getResponseBody()) {
                    os.write(response.getBytes());
                }
            }
        }
    }
}
