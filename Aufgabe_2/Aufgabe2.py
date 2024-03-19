import socket

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
        print(f"IP-Adresse: {address}, Domain-Name: {resolve_ip_to_hostname(address)}", "\n")
    else:
        print(f"Domain-Name: {address}, IP-Adresse: {resolve_hostname_to_ip(address)}", "\n")
    
if __name__ == "__main__":
    address = [
        'localhost',
        '127.0.0.1',
        'google.com',
        'fc.de',
        'facebook.com',
        'eclipse.org',
        'sam.hwr-berlin.de',
        'hwr-berlin.de',
        'github.com',
        'agilemanifesto.org',
        'tagesschau.de',
        'schalke04.de',
        '142.251.37.14',
        '18.245.31.63',
        '185.60.217.35',
        '198.41.30.198',
        '194.94.23.253',
        '194.94.22.19',
        '140.82.121.3',
        '185.199.108.153',
        '34.110.152.241',
        '104.22.25.183'
    ]

    for x in address:
        checkAddress(x)