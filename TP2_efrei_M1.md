
# Guide de Configuration et Attaques Réseaux

## I. Setup 

### 🌞 Le routeur doit pouvoir joindre internet

```bash
R1#conf t
R1#conf terminal
R1(config)#interface fastEthernet 1/0
R1(config-if)#ip address dhcp
R1(config-if)#no shutdown
R1(config-if)#exit
R1#show ip interface brief
```
```
Interface                  IP-Address      OK? Method Status    Protocol
FastEthernet0/0            10.2.1.254      YES manual up        up
FastEthernet1/0            192.168.122.213 YES DHCP   up        up
```

```bash
R1#ping 8.8.8.8
```

### 🌞 Configuration d'un NAT simpliste

#### Interfaces "externes" :
```bash
(config)# interface fastEthernet 1/0
(config-if)# ip nat outside
(config-if)# exit
```

#### Interfaces "internes" :
```bash
(config)# interface fastEthernet 0/0
(config-if)# ip nat inside
(config-if)# exit

(config)# access-list 1 permit any
(config)# ip nat inside source list 1 interface fastEthernet 1/0 overload
```

#### Test de ping depuis PC1 :
```bash
PC1> ping 8.8.8.8
```

### 🌞 Configuration DHCP

#### PC4 obtient une adresse IP :
```bash
PC4> ip dhcp
DORA IP 10.2.1.102/24 GW 10.2.1.254
```

#### Tests de connectivité :
```bash
PC4> ping 10.2.1.51
PC4> ping 8.8.8.8
```

## II. Scapy

### 4 Scripts sur GitHub :
- `dns_cap.py`
- `dns_lookup.py`
- `ping.py`
- `tcp_cap.py`

## III. Attaques DHCP

### 🌞 Mettre en place un serveur DHCP sur la machine attaquante

#### A. DHCP spoofing

- **DHCP légitime éteint :**  
  ```bash
  PC4> ip dhcp
  DORA IP 10.2.1.228/24 GW 10.2.1.254
  ```

- **DHCP légitime allumé :**  
  ```bash
  PC4> ip dhcp
  DDORA IP 10.2.1.228/24 GW 10.2.1.254
  ```

#### B. DHCP starvation

- Script utilisé : `📜 dhcp_starvation.py`
- Capture Wireshark : `🦈 dhcp_starvation_1.pcapng`

## IV. Attaques ARP

### A. Poisoning

- Script : `📜 arp_poisoning.py`

### B. Spoofing

- Script : `📜 arp_spoof.py`

### C. MITM

- Script : `📜 arp_mitm.py`
- Capture Wireshark : `🦈 arp_mitm.pcapng`

## V. DNS spoofing

### 🌞 Écrire un script Scapy qui répond à certaines requêtes DNS

- Script : `📜 dns_spoof.py`

### Test depuis un VPCS

- Résultat attendu : `Ping retourne l'IP choisie 17.37.17.37`

## VI. Remediation

### A. Attaques DHCP

- **DHCP snooping :**  
  - Identifie les ports de confiance et non fiables.  
  - Empêche les attaques comme le DHCP Starvation et le DHCP spoofing.

### B. Attaques ARP

- **Port Security :**  
  - Limite les adresses MAC autorisées sur un port.  
  - Bloque les périphériques non autorisés.

- **Dynamic ARP Inspection (DAI) :**  
  - Intercepte les requêtes et réponses ARP.  
  - Bloque les messages ARP malveillants.

### C. DNS spoofing

- **Chiffrement des requêtes DNS :**  
  - DNS-over-HTTPS ou DNS-over-TLS.
