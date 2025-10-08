"""
System- och säkerhetskontroller
"""
import os
import sys
import platform


def is_admin():
    """Kontrollerar om scriptet körs med admin/root-rättigheter"""
    try:
        if platform.system() == "Windows":
            if 'MSYSTEM' in os.environ or 'SHELL' in os.environ:
                print("[*] Git Bash detekterat - tillåter körning")
                return True

            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False


def check_dependencies():
    """Kontrollerar att alla dependencies finns"""
    issues = []

    try:
        from scapy.all import IP, TCP, ICMP
    except ImportError:
        issues.append("Scapy är inte installerat. Kör: pip install scapy")

    if platform.system() == "Windows":
        try:
            from scapy.all import get_if_list
            interfaces = get_if_list()
            if not interfaces:
                issues.append("Inga nätverksgränssnitt hittades. Installera Npcap från https://npcap.com/")
        except:
            issues.append("Npcap verkar inte vara korrekt installerat. Ladda ner från https://npcap.com/")

    if issues:
        print("\n[!] Följande problem måste åtgärdas:\n")
        for issue in issues:
            print(f"  ✘ {issue}")
        print()
        return False

    return True


def require_admin():
    """Kräver admin-rättigheter, avslutar annars"""
    if not is_admin():
        if platform.system() == "Windows":
            print("\n[!] ERROR: Detta skript kräver administratörsrättigheter")
            print("[*] Högerklicka på PowerShell/CMD och välj 'Run as Administrator'")
        else:
            print("\n[!] ERROR: Detta skript kräver root-rättigheter (sudo)")
            print("[*] Kör: sudo python3", " ".join(sys.argv))
        sys.exit(1)
