import socket
import os
import ntplib
from time import ctime

server = 'time.windows.com'
ntp_client = ntplib.NTPClient()
response = ntp_client.request(server, version=3)
print(ctime(response.tx_time))

