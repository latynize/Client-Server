import socket

def query_daytime_service(server='time.nist.gov'):
    try:
        # Erstelle einen Socket für die Verbindung
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Baue die Verbindung zum Server auf Port 13 auf
            s.connect((server, 13))
            
            # Lese die Antwort vom Server
            data = s.recv(1024)
            
            # Gib die empfangenen Daten aus (DayTime-Service-Antwort)
            print(f"Received: {data.decode().strip()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Verwende die Funktion, um den DayTime-Service abzufragen
query_daytime_service()
