"""
User Interface funktioner
"""
import platform
from .network_utils import validate_ip


def print_banner():
    """Skriver ut banner med varning"""
    os_name = platform.system()
    banner = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║      DoS Simulator med Custom Payloads                   ║
    ║                  Platform: {os_name:<15}                 ║
    ║                                                          ║
    ║   VARNING: ENDAST FÖR UTBILDNINGSSYFTE!                  ║
    ║                                                          ║
    ║  Detta skript simulerar DoS-attacker och är OLAGLIGT     ║
    ║  att använda mot system du inte äger!                    ║
    ║                                                          ║
    ║  Använd ENDAST i:                                        ║
    ║  • Isolerade VM-miljöer utan internet                    ║
    ║  • Egna test-nätverk                                     ║
    ║  • Med explicit skriftligt tillstånd                     ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def show_attack_menu():
    """Visar menyn för att välja attack-typ"""
    menu = """
    ╔══════════════════════════════════════════════════════════╗
    ║              ATTACK MODES - VÄL ETT ALTERNATIV           ║
    ╚══════════════════════════════════════════════════════════╝

    [1] ICMP Flood
    [2] SSH Flood (Port 22)
    [3] HTTP SYN Flood (Port 80)
    [4] HTTP Flood med Full Payload
    [5] DNS/UDP Flood (Port 53)
    [6] Multi-Protocol Attack
    [7] Ändra target IP
    [8] Ändra custom message
    [0] Avsluta programmet

    ══════════════════════════════════════════════════════════
    """
    print(menu)


def get_target_ip():
    """Frågar användaren efter target IP"""
    while True:
        target = input("[?] Ange target IP-adress (t.ex. 192.168.1.50): ").strip()
        if target and validate_ip(target):
            return target
        else:
            print("[!] Ogiltig IP-adress format. Försök igen.")


def get_packet_count(default=100):
    """Frågar användaren efter antal paket"""
    count_input = input(f"\n[?] Antal paket att skicka (default: {default}): ").strip()
    return int(count_input) if count_input.isdigit() else default


def confirm_attack(attack_name, target, count, message):
    """Bekräftar attack innan den körs"""
    print(f"\n[!] Kommer att köra: {attack_name}")
    print(f"[!] Target: {target}")
    print(f"[!] Packets: {count}")
    print(f"[!] Message: {message}")

    confirm = input("\n[?] Fortsätt? (y/N): ").strip().lower()
    return confirm == 'y'
