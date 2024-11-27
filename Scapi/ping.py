from scapy.all import *

ping = ICMP(type=8)

packet = IP(src="10.2.1.56", dst="10.2.1.254")

frame = Ether(src="08:00:27:f5:2c:64", dst="ca:01:05:19:00:00")

final_frame = frame/packet/ping

answers, unanswered_packet = srp(final_frame, timeout=10)

print(f"Pong reçu : {answers[0]}")

