import socket

def handle_client(client_socket):
    welcome_message = 'Willkommen zum Echo-Server. Typ "quit" zum Beenden.\n'
    client_socket.sendall(welcome_message.encode())

    while True:
        data = client_socket.recv(1024).decode().strip()
        if not data or data.lower() == "quit":
            break
        response = f"Echo: {data}\n"
        client_socket.sendall(response.encode())

    client_socket.close()

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server lauscht auf {host}:{port}")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Verbunden mit {addr}")
            handle_client(client_socket)

if __name__ == "__main__":
    HOST = 'localhost'  # Erlaubt Verbindungen von überall
    PORT = 65432      # Nicht-privilegierter Port für den Server
    
    start_server(HOST, PORT)
