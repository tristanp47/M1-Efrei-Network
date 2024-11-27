from scapy.all import *

def dns_query(domain):
    ip = IP(dst="8.8.8.8")
    udp = UDP(dport=53, sport=RandShort())

    dns = DNS(
        id=RandShort(),
        qr=0,
        opcode=0,
        aa=0,
        tc=0,
        rd=1,
        qdcount=1,
        ancount=0,
        nscount=0,
        arcount=0, 
        qd=DNSQR(qname=domain, qtype="A")
    )

    pkt = ip / udp / dns

    print(pkt.summary())

    response = sr1(pkt, timeout=2, verbose=0)

    if response:
        if response.haslayer(DNS) and response.getlayer(DNS).qr == 1:
            print(f"Réponse DNS: {response.getlayer(DNS).an.rdata}")
        else:
            print("Aucune réponse DNS valide reçue.")
    else:
        print("Aucune réponse reçue.")

dns_query("www.google.com")
