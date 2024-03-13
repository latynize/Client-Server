import socket
import os
import ntplib
from time import ctime

server = 'time.windows.com'
ntp_client = ntplib.NTPClient()
response = ntp_client.request(server, version=3)
print(ctime(response.tx_time))

server = 'time.apple.com'
ntp_client = ntplib.NTPClient()
response = ntp_client.request(server, version=3)
print(ctime(response.tx_time))

#List of Daytime Servers
#https://gist.github.com/mutin-sa/eea1c396b1e610a2da1e5550d94b0453