import socket
import os
import ntplib
from time import ctime

def getNTP(server):
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(server, version=3)
    print(server, ': \n', ctime(response.tx_time))
    print('stratum: ', response.stratum)
    print('version: ', response.version)
    print('mode: ', response.mode)
    print('poll: ', response.poll)
    print('precision: ', response.precision)
    print('delay: ', response.delay)
    print('dispersion: ', response.root_dispersion, '\n')

getNTP('time.apple.com')
getNTP('time.windows.com')
getNTP('time.nist.gov')
getNTP('time.google.com')
getNTP('time.cloudflare.com')

#List of Daytime Servers
#https://gist.github.com/mutin-sa/eea1c396b1e610a2da1e5550d94b0453