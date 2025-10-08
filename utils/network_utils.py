"""
Nätverksrelaterade utility-funktioner
"""
import random


def generate_random_ip():
    """Genererar en slumpmässig IPv4-adress"""
    while True:
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        if not ip.startswith(("127.", "0.", "255.")):
            return ip


def generate_random_port():
    """Genererar en slumpmässig källport (1024-65535)"""
    return random.randint(1024, 65535)


def validate_ip(ip):
    """Validerar IP-adress format"""
    try:
        parts = ip.split('.')
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            return True
        return False
    except:
        return False
