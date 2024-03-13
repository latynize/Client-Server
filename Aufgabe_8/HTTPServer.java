package Aufgabe_8;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;

public class HTTPServer {    
    public static void main(String[] args) throws Exception {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        System.out.println("Server läuft auf http://localhost:" + port);
        server.createContext("/", new RootHandler());
        server.createContext("/post", new PostHandler()); // Neuer Kontext für POST-Methode
        server.setExecutor(null);
        server.start();
    }

    public static class RootHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange he) throws IOException {
            // Behandlung der GET-Methode (Standard)
            File file = new File("Aufgabe_8/index.html");
            if (!file.exists() || file.isDirectory()) {
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
        }
    }

    public static class PostHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange he) throws IOException {
            try {
                // Überprüfen, ob die Anfrage tatsächlich eine POST-Anfrage ist
                if (!"POST".equalsIgnoreCase(he.getRequestMethod())) {
                    // Methode ist nicht POST, daher Fehlermeldung senden
                    String response = "405 - Methode nicht erlaubt";
                    he.sendResponseHeaders(405, response.length());
                    try (OutputStream os = he.getResponseBody()) {
                        os.write(response.getBytes());
                    }
                    return;
                }
    
                // POST-Datenstrom lesen und verarbeiten
                InputStreamReader isr = new InputStreamReader(he.getRequestBody(), "utf-8");
                BufferedReader br = new BufferedReader(isr);
                StringBuilder requestBody = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    requestBody.append(line).append("\n");
                }
                br.close();
                isr.close();
    
                // Beispiel: Ausgabe der empfangenen Daten im Backend
                System.out.println("Empfangene Daten:");
                System.out.println(requestBody.toString());
    
                // Beispiel: Einfache Antwort an den Client
                String responseData = "POST-Anfrage erfolgreich verarbeitet. Daten wurden im Backend ausgegeben.";
                he.sendResponseHeaders(200, responseData.getBytes().length);
                try (OutputStream os = he.getResponseBody()) {
                    os.write(responseData.getBytes());
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
