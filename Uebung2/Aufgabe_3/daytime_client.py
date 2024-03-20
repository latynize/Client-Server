import socket

def query_daytime_service(server):
    try:
        # Erstelle Socket für Verbindung
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Verbindung zum Server auf Port 13
            s.connect((server, 13))
            
            # Antwort vom Server
            data = s.recv(1024)
            
            # DayTime-Service-Antwort
            print(f"Received: {data.decode().strip()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Funktion zur DayTime-Service Abfrage
query_daytime_service('time.nist.gov')
query_daytime_service('time.windows.com')
