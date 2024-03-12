import subprocess
import socket
import platform

def resolve_hostname_to_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error as err:
        return f"Fehler beim Auflösen des Hostnamens: {err}"

def resolve_ip_to_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.error as err:
        return f"Fehler bei der Auflösung der IP-Adresse: {err}"
    
def checkAddress (address):
    if address.replace('.', '').isdigit():  # Prüfung, ob IP
        print(f"IP-Adresse: {address}, Domain-Name: {resolve_ip_to_hostname(address)}")
    else:
        print(f"Domain-Name: {address}, IP-Adresse: {resolve_hostname_to_ip(address)}")
    
if __name__ == "__main__":
    
    checkAddress('localhost')
    
    checkAddress('google.com')
    checkAddress('fc.de')
    checkAddress('facebook.com')
    checkAddress('eclipse.org')
    checkAddress('sam.hwr-berlin.de')
    checkAddress('hwr-berlin.de')
    checkAddress('github.com')
    checkAddress('agilemanifesto.org')
    checkAddress('tagesschau.de')
    checkAddress('schalke04.de')

    checkAddress('127.0.0.1')
    checkAddress('142.251.37.14')
    checkAddress('18.245.31.63')
    checkAddress('185.60.217.35')
    checkAddress('198.41.30.198')
    checkAddress('194.94.23.253')
    checkAddress('194.94.22.19')
    checkAddress('140.82.121.3')
    checkAddress('185.199.108.153')
    checkAddress('34.110.152.241')
    checkAddress('104.22.25.183')
  
