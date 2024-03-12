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

def ping(address):
    command = ['ping', '-c', '4', address] if platform.system() != "Windows" else ['ping', '-n', '4', address]
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ping: {e}")

def trace_route(address):
    command = ['traceroute', address] if platform.system() != "Windows" else ['tracert', address]
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Routenverfolgung: {e}")

if __name__ == "__main__":
    address = input("Gebe IP-Adresse oder Domain ein: ")

    if address.replace('.', '').isdigit():  # Prüfung, ob IP
        print(f"Domain-Name: {resolve_ip_to_hostname(address)}")
    else:
        print(f"IP-Adresse: {resolve_hostname_to_ip(address)}")
    
    ping(address)
    print("\nRoute:")
    trace_route(address)
