from scapy.all import *

def process_packet(packet):
          if packet.haslayer(DNSRR):
              for i in packet[DNS].an:
                  if i.type == 1:  # Type A (adresse IPv4)
                      print(f"- Adresse IP de la réponse DNS : {i.rdata}")

# Lancer la capture des paquets DNS
print("Démarrage de la capture...")
packets = sniff(filter="udp port 53", prn=process_packet, count=10)

