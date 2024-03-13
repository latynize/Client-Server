import socket
import os

# Set the path for the Unix socket
server_address = 'time.windows.com'
port=123

# Create the Unix socket client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect to the server
client.connect((server_address, port))

# Receive a response from the server
data = client.recv(1024)
print(f'Received response: {data.decode()}')

# Close the connection
client.close()
