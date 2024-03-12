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
    checkAddress('kicker.de')
    checkAddress('facebook.com')
    checkAddress('chat.openai.com')
    checkAddress('sam.hwr-berlin.de')
    checkAddress('www.hwr-berlin.de')
    checkAddress('github.com')
    checkAddress('spiegel.de')
    checkAddress('tagesschau.de')
    checkAddress('bvg.de')


  
