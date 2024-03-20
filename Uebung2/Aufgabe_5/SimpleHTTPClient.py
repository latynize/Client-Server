import socket
import chardet

host = 'www.google.de'
port = 80
path = '/index.html'

try:
    # Socket-Verbindung zum angegebenen Host und Port aufbauen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        # Senden des GET-Anforderungsbefehls an den Server
        httpRequest = f"GET {path} HTTP/1.1\r\n" \
                      f"Host: {host}\r\n" \
                      "Connection: close\r\n\r\n"
        client_socket.sendall(httpRequest.encode())

        # Serverantwort empfangen
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        # Zeichenkodierung der Antwort automatisch erkennen und dekodieren
        detected_encoding = chardet.detect(response)['encoding']
        decoded_response = response.decode(detected_encoding)
        print("Serverantwort:\n")
        print(decoded_response)

except socket.error as e:
    print("Fehler beim Kommunizieren mit dem Server:", e)
