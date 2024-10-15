import socket


def get_system_info():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.error:
        ip_address = None
    return hostname, ip_address
