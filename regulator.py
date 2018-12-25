#regulator.py 
#team 

# This file utilizes capy and nfqueue to sniff and modify dns packets

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from netfilterqueue import NetfilterQueue
from scapy.all import *
import os

def process(packet):
   payload =  packet.get_payload()
   pkt = IP(payload)
   if not pkt.haslayer(DNSRR):
       packet.accept()
   else:
    print("")
    print("Original Packet Info: ")
    print("SRC IP = %s" % str(pkt[IP].src))
    print("DST IP = %s" % str(pkt[IP].dst))

    oldTTL = pkt[DNS].an.ttl
    print("oldTTL = %s" % str(oldTTL))
    mins = oldTTL / 60
    rounded = round(mins,  0)
    newTTL = rounded * 60
    print ("")

    newPkt = IP(dst=pkt[IP].dst,  src=pkt[IP].src)/\
                    UDP(dport=pkt[UDP].dport,  sport=pkt[UDP].sport)/\
                    DNS(id = pkt[DNS].id,  qr = 1,  aa =1, qd=pkt[DNS].qd, \
                    an=DNSRR(rrname=pkt[DNS].qd.qname, ttl = newTTL, rdata = pkt[DNS].an.rdata))
    print("Regulated Info: ")
    print("SRC IP = %s" % str(newPkt[IP].src))
    print("DST IP = %s" % str(newPkt[IP].dst))
    print("NEW TTL = %s" % str(newTTL))    
    packet.set_payload(str(newPkt))
    packet.accept()
    
def main():  
   os.system('iptables -t nat -A PREROUTING -p udp --dport 53 -j NFQUEUE --queue-num 2')
   q = NetfilterQueue()  
   q.bind(2, process)
   try:
        q.run()
        print("Running")
   except KeyboardInterrupt:
        print("exiting....")
        q.unbind()
        os.system('iptables -t nat -F')
        exit(0)

if __name__ == '__main__':
	main()


    
