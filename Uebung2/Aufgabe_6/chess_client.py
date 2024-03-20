import socket

# Definieren der Serverdetails
host = 'freechess.org'
port = 5000

try:
    # Erstellen eines Socket-Objekts
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Verbindung zum Server herstellen
        s.connect((host, port))
        
        # Eine Willkommensnachricht vom Server empfangen und ausgeben
        welcome_message = s.recv(1024).decode('utf-8')
        print("Verbindung erfolgreich. Willkommensnachricht vom Server:\n")
        print(welcome_message)
        
        # Wenn Sie weiter interagieren möchten, können Sie hier Befehle senden und Antworten empfangen
        # Beispiel: s.sendall(b'ihre_nachricht\n')
        # Antwort = s.recv(1024)
        # print(Antwort.decode('utf-8'))
        
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {str(e)}")
