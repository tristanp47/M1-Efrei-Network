I. Setup
🌞 Le routeur doit pouvoir joindre internet
R1#conf t
R1#conf terminal
R1(config)#interface fastEthernet 1/0
R1(config-if)#ip address dhcp
R1(config-if)#no shutdown
R1(config-if)#exit
R1#show ip interface brief
Interface                  IP-Address      OK? Method Status                                                                                Protocol
FastEthernet0/0            10.2.1.254      YES manual up                                                                                    up
FastEthernet1/0            192.168.122.213 YES DHCP   up                                                                                    up

R1#ping 8.8.8.8

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 60/86/120 ms

🌞 Configuration d'un NAT simpliste
Interfaces "externes" :
(config)# interface fastEthernet 1/0
(config-if)# ip nat outside
(config-if)# exit

Interfaces "internes" :
(config)# interface fastEthernet 0/0
(config-if)# ip nat inside
(config-if)# exit

(config)# access-list 1 permit any
(config)# ip nat inside source list 1 interface fastEthernet 1/0 overload

PC1> ping 8.8.8.8

84 bytes from 8.8.8.8 icmp_seq=1 ttl=114 time=39.101 ms
84 bytes from 8.8.8.8 icmp_seq=2 ttl=114 time=41.978 ms
84 bytes from 8.8.8.8 icmp_seq=3 ttl=114 time=37.773 ms
84 bytes from 8.8.8.8 icmp_seq=4 ttl=114 time=35.953 ms

🌞 Configuration DHCP

PC4> ip dhcp
DORA IP 10.2.1.102/24 GW 10.2.1.254

PC4> ping 10.2.1.51

84 bytes from 10.2.1.51 icmp_seq=1 ttl=64 time=1.812 ms
84 bytes from 10.2.1.51 icmp_seq=2 ttl=64 time=1.146 ms
84 bytes from 10.2.1.51 icmp_seq=3 ttl=64 time=1.228 ms
84 bytes from 10.2.1.51 icmp_seq=4 ttl=64 time=1.215 ms

PC4> ping 8.8.8.8

84 bytes from 8.8.8.8 icmp_seq=1 ttl=114 time=39.831 ms
84 bytes from 8.8.8.8 icmp_seq=2 ttl=114 time=37.853 ms
84 bytes from 8.8.8.8 icmp_seq=3 ttl=114 time=38.441 ms
84 bytes from 8.8.8.8 icmp_seq=4 ttl=114 time=37.227 ms

II. Scapy

4 Scripts sur GitHub :
- dns_cap.py
- dns_lookup.py
- ping.py
- tcp_cap.py

III. Attaques DHCP

🌞 Mettre en place un serveur DHCP sur la machine attaquante

A. DHCP spoofing

DHCP légitime éteint:

PC4> ip dhcp
DORA IP 10.2.1.228/24 GW 10.2.1.254

DHCP légitime allumé :

PC4> ip dhcp
DDORA IP 10.2.1.228/24 GW 10.2.1.254

Capture qui montre que vous avez répondu un DHCP Offer avant le serveur DHCP légitime:
🦈 dhcp_spoof.pcapng

B. DHCP starvation

PC4> ip dhcp
DDD
Can't find dhcp server

Script qui met en place l'attaque:
📜 dhcp_starvation.py

Capture qui montre les trames que votre machine attaquante envoie pendant l'attaque:
🦈 dhcp_starvation_1.pcapng

VPCS qui n'arrive pas à obtenir une adresse IP:
🦈 dhcp_starvation_2.pcapng

IV. Attaques ARP

A. Poisoning

🌞 Injectez de fausses données dans la table ARP de PC1
Fausse mac pour la passerelle.

PC2> arp

ff:ff:ff:ff:ff:ff  10.2.1.254 expires in 114 seconds

Script qui met en place l'attaque:
📜 arp_poisoning.py

B. Spoofing

🌞 Mettez en place un ARP spoofing

PC2> arp

08:00:27:f5:2c:64  10.2.1.51 expires in 118 seconds

Script qui met en place l'attaque:
📜 arp_spoof.py

Machine attaquante reçoit les pings a destinations de PC1 depuis PC2:
🦈 arp_spoof.pcapng

C. MITM

🌞 Mettez en place un Man-in-the-middle ARP

Se faire passer pour la passerelle auprès de PC1:
PC1> arp

08:00:27:f5:2c:64  10.2.1.254 expires in 119 seconds

Se faire passer pour PC1 auprès de la passerelle:
R1#show arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.2.1.52               0   0800.27f5.2c64  ARPA   FastEthernet0/0

PC1> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=56 time=39.932 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=56 time=41.603 ms
84 bytes from 1.1.1.1 icmp_seq=3 ttl=56 time=40.220 ms
84 bytes from 1.1.1.1 icmp_seq=4 ttl=56 time=40.776 ms

MITM effectif les trames entre PC1 et la passerelle transitent par le PC attaquant.

Script qui met en place l'attaque:
📜 arp_mitm.py

Capture qui montre le man-in-the-middle en cours:
🦈 arp_mitm.pcapng

V. DNS spoofing

🌞 Ecrire un script Scapy qui répond à certaines requêtes DNS

Script qui met en place l'attaque:
📜 dns_spoof.py

🌞 Tester depuis un VPCS

Ping fonctionne depuis le VPCS mais retourne l'ip choisie 17.37.17.37 dans wireshark.

PC1> ping efrei.fr
efrei.fr resolved to 51.255.68.208

84 bytes from 51.255.68.208 icmp_seq=1 ttl=52 time=40.136 ms
84 bytes from 51.255.68.208 icmp_seq=2 ttl=52 time=34.801 ms

Capture qui montre les requètes DNS avec réponses légitimes et maalveillante:
🦈 dns_spoof.pcapng

VI. Remediation

A. Attaques DHCP

Le DHCP snooping est d'une fonctionnalité de sécurité intégrée dans les commutateurs réseau qui surveille les communications DHCP et bloque les messages malveillants.

Identifie les ports de confiance et les ports non fiables.
Filtre les messages DHCP provenant de sources non autorisées.
Empêche les attaques comme le DHCP Starvation et le DHCP spoofing.

B. Attaques ARP

Port Security:
Limite le nombre d'adresses MAC autorisées sur un port.
Bloque les périphériques non autorisés.
Idéal pour empêcher les attaques où l'attaquant utilise des équipements inconnus.

Dynamic ARP Inspection (DAI) :
Fonctionnalité de sécurité réseau qui intercepte les requêtes et réponses ARP.
Vérifie l'authenticité des messages ARP en les comparant à une base de données fiable.
Bloque les messages ARP malveillants ou non conformes.

C. DNS spoofing

Chiffrement des requêtes DNS :

DNS-over-HTTPS ou DNS-over-TLS pour protéger la confidentialité des requêtes DNS.
Cela empêche un attaquant d’intercepter ou d’altérer les requêtes DNS en transit.

