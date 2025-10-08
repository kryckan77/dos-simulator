#!/usr/bin/env python3
"""
DoS Simulator - Huvudprogram
Modulär version med 16 olika attack-typer
"""
import sys
import time
import platform

# Importera utility-moduler
from utils.system_check import check_dependencies, require_admin
from utils.ui import print_banner, get_target_ip, get_packet_count, confirm_attack
from utils.network_utils import validate_ip

# Importera ALLA attack-moduler
from attacks import (
    # Grundläggande
    ICMPAttack,
    SSHAttack,
    HTTPAttack,
    HTTPPayloadAttack,
    UDPAttack,
    MultiProtocolAttack,
    # Avancerade
    SlowlorisAttack,
    DNSAmplificationAttack,
    ACKFloodAttack,
    NTPAmplificationAttack,
    FragmentationAttack,
    SSDPAmplificationAttack,
    MemcachedAmplificationAttack,
    LandAttack,
    RUDYAttack,
    SYNACKReflectionAttack
)


def show_attack_menu():
    """Visar UPPDATERAD meny med alla attacker"""
    menu = """
    ╔══════════════════════════════════════════════════════════╗
    ║           ATTACK MODES - 16 OLIKA ATTACKER              ║
    ╚══════════════════════════════════════════════════════════╝
    
    === GRUNDLÄGGANDE ATTACKER ===
    [1]  ICMP Flood
    [2]  SSH Flood (Port 22)
    [3]  HTTP SYN Flood (Port 80)
    [4]  HTTP Flood med Full Payload
    [5]  DNS/UDP Flood (Port 53)
    [6]  Multi-Protocol Attack
    
    === AVANCERADE ATTACKER ===
    [7]  Slowloris (Slow HTTP)          ⭐ Låg bandbredd, hög effekt
    [8]  ACK Flood                      ⭐ Mot stateful firewalls
    [9]  Land Attack                    📚 Klassisk 90-tals attack
    [10] IP Fragmentation               💥 Ping of Death style
    [11] R.U.D.Y (Slow POST)            🐢 Extremt långsam POST
    [12] SYN-ACK Reflection             🔄 Reflection attack
    
    === AMPLIFICATION ATTACKER (KRAFTFULLA!) ===
    [13] DNS Amplification              🔊 28-54x amplification
    [14] SSDP Amplification (UPnP)      🔊 30-35x amplification
    [15] NTP Amplification              🔊🔊 206x amplification
    [16] Memcached Amplification        🔊🔊🔊 51,000x (!!) EXTREM
    
    === INSTÄLLNINGAR ===
    [97] Ändra target IP
    [98] Ändra custom message
    [99] Visa attack-information
    [0]  Avsluta programmet
    
    ══════════════════════════════════════════════════════════
    """
    print(menu)


def show_attack_info():
    """Visar detaljerad information om varje attack"""
    info = """
    ╔══════════════════════════════════════════════════════════╗
    ║              ATTACK-INFORMATION & TIPS                  ║
    ╚══════════════════════════════════════════════════════════╝
    
    📊 EFFEKTIVITETS-RANKING (Mest verkningsfulla):
    
    1. Memcached Amplification    - 51,000x amplification!!
    2. NTP Amplification          - 206x amplification
    3. DNS Amplification          - 28-54x amplification
    4. Slowloris                  - Låg bandbredd, lång varaktighet
    5. R.U.D.Y                    - Svår att detektera
    
    🎓 PEDAGOGISKA FAVORITER (Bäst för lärande):
    
    • Slowloris      - Visar att DoS ≠ hög bandbredd
    • ACK Flood      - Förståelse för TCP-states
    • DNS Amp        - Introducerar amplification
    • Fragmentation  - IP-fragmentering i praktiken
    • Land Attack    - Historisk kontext
    
    ⚠️  SÄKERHETSVARNINGAR:
    
    [13-16] Amplification-attacker kan generera MASSIV trafik!
            Använd ENDAST i isolerade labbmiljöer.
            
    [16] Memcached = Världsrekord DDoS (1.3 Tbps)
         EXTREM FÖRSIKTIGHET krävs!
    
    💡 TIPS FÖR LABORATION:
    
    • Börja med [1-6] för att förstå grunderna
    • Prova [7] Slowloris för att se "low and slow"
    • Testa [8] ACK Flood mot firewall
    • Kör [13] DNS Amp för att förstå amplification
    • [16] Memcached ENDAST om du vet vad du gör!
    
    📝 ÖVERVAKA PÅ TARGET:
    
    tcpdump -i eth0 -A -c 100           # Allmän trafik
    tcpdump -i eth0 'tcp[tcpflags] & tcp-ack != 0'  # ACK flood
    tcpdump -i eth0 'ip[6:2] & 0x1fff != 0'         # Fragments
    
    Tryck Enter för att återgå till menyn...
    """
    print(info)
    input()


class DoSSimulatorApp:
    """Huvudapplikation för DoS Simulator med 16 attacker"""

    def __init__(self):
        self.current_target = None
        self.current_message = "LAB_TEST_TRAFFIC"
        self.log_file = "dos_attack.log"

        # Mapping av menyval till attack-klasser (NU 16 ATTACKER!)
        self.attack_map = {
            # Grundläggande (1-6)
            '1': ICMPAttack,
            '2': SSHAttack,
            '3': HTTPAttack,
            '4': HTTPPayloadAttack,
            '5': UDPAttack,
            '6': MultiProtocolAttack,
            # Avancerade (7-12)
            '7': SlowlorisAttack,
            '8': ACKFloodAttack,
            '9': LandAttack,
            '10': FragmentationAttack,
            '11': RUDYAttack,
            '12': SYNACKReflectionAttack,
            # Amplification (13-16)
            '13': DNSAmplificationAttack,
            '14': SSDPAmplificationAttack,
            '15': NTPAmplificationAttack,
            '16': MemcachedAmplificationAttack
        }

        self.attack_names = {
            '1': 'ICMP Flood',
            '2': 'SSH Flood',
            '3': 'HTTP SYN Flood',
            '4': 'HTTP Full Payload',
            '5': 'DNS/UDP Flood',
            '6': 'Multi-Protocol',
            '7': 'Slowloris',
            '8': 'ACK Flood',
            '9': 'Land Attack',
            '10': 'IP Fragmentation',
            '11': 'R.U.D.Y',
            '12': 'SYN-ACK Reflection',
            '13': 'DNS Amplification',
            '14': 'SSDP Amplification',
            '15': 'NTP Amplification',
            '16': 'Memcached Amplification'
        }

    def initialize(self):
        """Initialiserar applikationen"""
        print_banner()

        # Få target IP om inte redan satt
        if not self.current_target:
            print("\n[*] Ingen target IP angiven.")
            self.current_target = get_target_ip()

        print(f"\n[✓] Nuvarande inställningar:")
        print(f"    Target IP: {self.current_target}")
        print(f"    Message: {self.current_message}")
        print(f"    Log file: {self.log_file}")

    def change_target(self):
        """Ändrar target IP"""
        new_target = input(f"\n[?] Ange ny target IP (nuvarande: {self.current_target}): ").strip()
        if new_target and validate_ip(new_target):
            self.current_target = new_target
            print(f"[✓] Target ändrad till: {self.current_target}")
        else:
            print("[!] Ogiltig IP-adress. Behåller nuvarande target.")

    def change_message(self):
        """Ändrar custom message"""
        new_message = input(f"\n[?] Ange nytt meddelande (nuvarande: {self.current_message}): ").strip()
        if new_message:
            self.current_message = new_message
            print(f"[✓] Meddelande ändrat till: {self.current_message}")

    def execute_attack(self, choice):
        """Kör vald attack"""
        # Extra varning för Memcached
        if choice == '16':
            print("\n" + "="*60)
            print("⚠️  KRITISK VARNING - MEMCACHED AMPLIFICATION ⚠️")
            print("="*60)
            print("Denna attack kan generera 51,000x amplification!")
            print("Det betyder att 1 MB du skickar = 51 GB till target!")
            print("ANVÄND ENDAST I HELT ISOLERAT LABB!")
            print("="*60)
            extra_confirm = input("\n[?] Är du ABSOLUT SÄKER? Skriv 'YES' för att fortsätta: ").strip()
            if extra_confirm != 'YES':
                print("[!] Attack avbruten. Bra beslut!")
                return

        # Skapa attack-instans
        attack_class = self.attack_map[choice]
        attack = attack_class(
            target_ip=self.current_target,
            custom_message=self.current_message,
            log_file=self.log_file
        )

        # Få packet count
        count = get_packet_count()

        # Bekräfta attack
        if not confirm_attack(
                self.attack_names[choice],
                self.current_target,
                count,
                self.current_message
        ):
            print("[!] Attack avbruten.")
            return

        # Kör attack
        try:
            if choice == '6':  # Multi-protocol
                attack.execute(icmp=count, http=count, ssh=count, dns=count)
            else:
                attack.execute(count=count)

            print("\n[✓] Attack slutförd! Återgår till menyn...")
            time.sleep(2)

        except KeyboardInterrupt:
            print("\n\n[!] Attack avbruten av användare (Ctrl+C)")
            if hasattr(attack, 'print_summary'):
                attack.print_summary()

    def run(self):
        """Huvudloop för applikationen"""
        while True:
            try:
                show_attack_menu()
                choice = input("[?] Välj alternativ (0-99): ").strip()

                if choice == '0':
                    print("\n[*] Avslutar programmet...")
                    print("[✓] Tack för att du använde DoS Simulator!")
                    break

                elif choice == '97':
                    self.change_target()
                    continue

                elif choice == '98':
                    self.change_message()
                    continue

                elif choice == '99':
                    show_attack_info()
                    continue

                elif choice in self.attack_map:
                    self.execute_attack(choice)

                else:
                    print("[!] Ogiltigt val. Välj 0-16, 97-99.")

            except KeyboardInterrupt:
                print("\n\n[!] Ctrl+C detected")
                exit_confirm = input("[?] Vill du avsluta programmet? (y/N): ").strip().lower()
                if exit_confirm == 'y':
                    print("[*] Avslutar...")
                    break
                else:
                    print("[*] Fortsätter...")
                    continue

            except Exception as e:
                print(f"\n[!] Ett fel uppstod: {e}")
                import traceback
                traceback.print_exc()
                print("[*] Återgår till menyn...")
                time.sleep(2)


def main():
    """Huvudfunktion"""
    # Systemkontroller
    if not check_dependencies():
        sys.exit(1)

    require_admin()

    print(f"\n[✓] Kör som {'Administrator' if platform.system() == 'Windows' else 'root'}")
    print(f"[*] Platform: {platform.system()} {platform.release()}")
    print(f"[*] Python: {sys.version.split()[0]}")
    print(f"[*] Antal tillgängliga attacker: 16")

    # Starta applikationen
    app = DoSSimulatorApp()
    app.initialize()
    app.run()


if __name__ == "__main__":
    main()