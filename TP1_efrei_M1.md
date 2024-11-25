
# Topologie Réseaux

## 3. Setup topologie 1

```plaintext
PC1> ip 10.3.1.1 255.255.255.0
PC2> ip 10.3.1.2 255.255.255.0

PC1> ping 10.3.1.2
84 bytes from 10.3.1.2 icmp_seq=1 ttl=64 time=0.498 ms
84 bytes from 10.3.1.2 icmp_seq=2 ttl=64 time=0.647 ms
84 bytes from 10.3.1.2 icmp_seq=3 ttl=64 time=0.601 ms
84 bytes from 10.3.1.2 icmp_seq=4 ttl=64 time=0.629 ms

PC2> ping 10.3.1.1
84 bytes from 10.3.1.1 icmp_seq=1 ttl=64 time=0.466 ms
84 bytes from 10.3.1.1 icmp_seq=2 ttl=64 time=0.716 ms
84 bytes from 10.3.1.1 icmp_seq=3 ttl=64 time=0.705 ms
84 bytes from 10.3.1.1 icmp_seq=4 ttl=64 time=0.633 ms

IOU1#show mac address-table

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    0050.7966.6800    DYNAMIC     Et0/1
   1    0050.7966.6801    DYNAMIC     Et0/0
```

## 3. Setup topologie 2

```plaintext
PC1> ip 10.3.1.1 255.255.255.0
PC2> ip 10.3.1.2 255.255.255.0
PC3> ip 10.3.1.2 255.255.255.0

ping : ok

IOU1#conf t
IOU1(config)#vlan 10
IOU1(config-vlan)#exit
IOU1(config)#vlan 20
IOU1(config-vlan)#exit

IOU1#conf t
IOU1(config)#interface ethernet 0/0
IOU1(config-if)#switchport mode access
IOU1(config-if)#switchport access vlan 10
IOU1(config-if)#exit
IOU1(config)#interface ethernet 0/1
IOU1(config-if)#switchport mode access
IOU1(config-if)#switchport access vlan 10
IOU1(config-if)#exit
IOU1(config)#interface ethernet 0/2

PC1> ping 10.3.1.2

84 bytes from 10.3.1.2 icmp_seq=1 ttl=64 time=0.454 ms
84 bytes from 10.3.1.2 icmp_seq=2 ttl=64 time=0.666 ms
84 bytes from 10.3.1.2 icmp_seq=3 ttl=64 time=0.720 ms
84 bytes from 10.3.1.2 icmp_seq=4 ttl=64 time=0.663 ms
84 bytes from 10.3.1.2 icmp_seq=5 ttl=64 time=0.730 ms

PC1> ping 10.3.1.3

host (10.3.1.3) not reachable

PC3> ping 10.3.1.1

host (10.3.1.1) not reachable

PC3> ping 10.3.1.2

host (10.3.1.2) not reachable
```

## III. Ptite VM DHCP

```plaintext
port server DHCP sur switch
IOU1#conf t
IOU1(config)#interface ethernet 0/3
IOU1(config-if)#switchport mode access
IOU1(config-if)#switchport access vlan 20
IOU1(config-if)#exit

port PC4 sur switch
IOU1#conf t
IOU1(config)#interface ethernet 1/0
IOU1(config-if)#switchport mode access
IOU1(config-if)#switchport access vlan 20
IOU1(config-if)#exit

port PC5 sur switch
IOU1#conf t
IOU1(config)#interface ethernet 1/1
IOU1(config-if)#switchport mode access
IOU1(config-if)#switchport access vlan 10
IOU1(config-if)#exit

PC4> ip dhcp
DORA IP 10.3.1.100/24 GW 10.3.1.1

PC5> ip dhcp
DDD
Can't find dhcp server
```
