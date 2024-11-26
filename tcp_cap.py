from scapy.all import sniff, TCP, IP

def print_it_please(packet):
    packet_source_ip = packet['IP'].src
    pong = packet['TCP']
    print(f"Un petit pong qui revient de {packet_source_ip} : {pong}")

output = sniff(filter="tcp", prn=print_it_please, count=1)
print("TCP SYN ACK reçu !")
print(f"- Adresse IP src : {output[0][IP].src}")
print(f"- Adresse IP dst : {output[0][IP].dst}")
print(f"- Port TCP src : {output[0][TCP].sport}")
print(f"- Port TCP dst : {output[0][TCP].dport}")
