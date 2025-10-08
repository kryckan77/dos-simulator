"""
Basklass för alla attack-typer
"""
from abc import ABC, abstractmethod
import time
from datetime import datetime
from scapy.all import send


class BaseAttack(ABC):
    """Abstrakt basklass för alla attacker"""

    def __init__(self, target_ip, custom_message="LAB_TEST_TRAFFIC", log_file="dos_attack.log"):
        self.target_ip = target_ip
        self.custom_message = custom_message
        self.log_file = log_file
        self.packets_sent = 0
        self.start_time = None

    @abstractmethod
    def execute(self, **kwargs):
        """Måste implementeras av varje attack-klass"""
        pass

    @abstractmethod
    def get_attack_name(self):
        """Returnerar attack-namnet"""
        pass

    def send_packet(self, packet):
        """Skickar ett paket och räknar upp"""
        send(packet, verbose=0)
        self.packets_sent += 1

    def log_attack(self, attack_type, details=""):
        """Loggar attack-aktivitet"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {attack_type} - {details}\n"

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[!] Kunde inte skriva till logg: {e}")

        print(f"[+] {log_entry.strip()}")

    def print_summary(self):
        """Skriver ut sammanfattning"""
        if self.start_time is None:
            print("[!] Ingen attack kördes")
            return

        elapsed = time.time() - self.start_time
        pps = self.packets_sent / elapsed if elapsed > 0 else 0

        print(f"\n{'='*60}")
        print(f"[✓] Attack Completed")
        print(f"[*] Total packets sent: {self.packets_sent}")
        print(f"[*] Duration: {elapsed:.2f} seconds")
        print(f"[*] Average rate: {pps:.1f} packets/second")
        print(f"[*] Custom message: {self.custom_message}")
        print(f"[*] Log saved to: {self.log_file}")
        print(f"{'='*60}\n")

    def print_header(self, attack_type, port=None, count=100):
        """Skriver ut attack header"""
        print(f"\n{'='*60}")
        print(f"[!] Startar {attack_type}")
        print(f"[!] Target: {self.target_ip}" + (f":{port}" if port else ""))
        print(f"[!] Packets: {count}")
        print(f"[!] Message: {self.custom_message}")
        print(f"{'='*60}\n")
