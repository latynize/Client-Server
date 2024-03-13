import ntplib
from time import ctime

def getNTP(server):
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(server, version=3)
    print(server, ': \n', ctime(response.tx_time))
    print('stratum: ', response.stratum) #Stratum ist die Schicht des NTP-Servers nach der Atomuhr
    print('version: ', response.version) #Version des NTP-Protokolls
    print('mode: ', response.mode) #Mode des NTP-Servers, in unserem Fall 4 (Broadcast)
    print('poll: ', response.poll) #Polling-Intervall des NTP-Servers
    print('precision: ', response.precision) #Genauigkeit des NTP-Servers
    print('delay: ', response.delay) #Verzögerung des NTP-Servers
    print('dispersion: ', response.root_dispersion*1000, '(ms)\n') #Abweichung des NTP-Servers

getNTP('time.apple.com')
getNTP('time.windows.com')
getNTP('time.nist.gov')
getNTP('time.google.com')
getNTP('time.cloudflare.com')

#List of Daytime Servers
#https://gist.github.com/mutin-sa/eea1c396b1e610a2da1e5550d94b0453