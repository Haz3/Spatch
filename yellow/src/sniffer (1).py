#! /usr/bin/env python

import json
import socket
import sys
import argparse
from struct import *


def eth_addr (a) :
      b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
      return b


#define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */

def openSocket():
      try:
            s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
      except (socket.error , msg):
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
      return s

def getPacket(s):
      listPackets = []
      currentPacket = {}
      # receive a packet
      while True:
            currentPacket = {}
            packet = s.recvfrom(65565)

            #packet string from tuple
            packet = packet[0]

            #parse ethernet header
            eth_length = 14

            eth_header = packet[:eth_length]
            eth = unpack('!6s6sH' , eth_header)
            eth_protocol = socket.ntohs(eth[2])
            print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)

            currentPacket['MAC_DEST'] =  eth_addr(packet[0:6])
            currentPacket['MAC_SOURCE'] = eth_addr(packet[6:12])
            currentPacket['PROT'] =  str(eth_protocol)

            #Parse IP packets, IP Protocol number = 8
            if eth_protocol == 8 :
                  #Parse IP header
                  #take first 20 characters for the ip header
                  ip_header = packet[eth_length:20+eth_length]

                  #now unpack them :)
                  iph = unpack('!BBHHHBBH4s4s' , ip_header)

                  version_ihl = iph[0]
                  version = version_ihl >> 4
                  ihl = version_ihl & 0xF

                  iph_length = ihl * 4

                  ttl = iph[5]
                  protocol = iph[6]
                  s_addr = socket.inet_ntoa(iph[8]);
                  d_addr = socket.inet_ntoa(iph[9]);

                  if results.filter == "src":
                        src_ip_addr_str = s_addr
                        if results.ip_addr == src_ip_addr_str:
                            print 'Source Adress ' + str(s_addr)
                            print 'Destination Adress' + str(d_addr)
                            print 'Version ' + str(version)
                            print 'IP Header Length ' + str(ihl)
                            print 'TTL ' + str(ttl)
                            print 'Protocol ' + str(protocol)
                  elif results.filter == "dst":
                        dst_ip_addr_str = d_addr
                        if results.ip_addr == dst_ip_addr_str:
                            print 'Destination Adress' + str(d_addr)
                            print 'Source Adress ' + str(s_addr)
                            print 'Version ' + str(version)
                            print 'IP Header Length ' + str(ihl)
                            print 'TTL ' + str(ttl)
                            print 'Protocol ' + str(protocol)
                  else:
                      print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + 'Destination Address : ' + str(d_addr)


                  currentPacket['VERSION'] = str(version)
                  currentPacket['IHL'] = str(ihl)
                  currentPacket['TTL'] = str(ttl)
                  currentPacket['PROTOCOL'] = str(protocol)
                  currentPacket['ADDRESS_SOURCE'] = str(s_addr)
                  currentPacket['DESTINATION_SOURCE'] = str(d_addr)

                  #TCP protocol
                  if protocol == 6 :
                        t = iph_length + eth_length
                        tcp_header = packet[t:t+20]

                        #now unpack them :)
                        tcph = unpack('!HHLLBBHHH' , tcp_header)

                        source_port = tcph[0]
                        dest_port = tcph[1]
                        sequence = tcph[2]
                        acknowledgement = tcph[3]
                        doff_reserved = tcph[4]
                        tcph_length = doff_reserved >> 4

                        print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)

                        currentPacket['SOURCE_PORT'] = str(source_port)
                        currentPacket['DEST_PORT'] = str(dest_port)
                        currentPacket['SEQUENCE_NUM'] = str(sequence)
                        currentPacket['ACKNOWLEDGEMENT'] = str(acknowledgement)
                        currentPacket['TCP_HEADER_LENGTH'] = str(tcph_length)

                        h_size = eth_length + iph_length + tcph_length * 4
                        data_size = len(packet) - h_size

                        #get data from the packet
                        data = packet[h_size:]
                        currentPacket['DATA_SIZE'] = data_size
                        currentPacket['DATA'] = data

                        #print 'Data : ' + data

                        #ICMP Packets
                  elif protocol == 1 :

                        u = iph_length + eth_length
                        icmph_length = 4
                        icmp_header = packet[u:u+4]

                        #now unpack them :)
                        icmph = unpack('!BBH' , icmp_header)

                        icmp_type = icmph[0]

                        checksum = icmph[2]

                        print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)

                        currentPacket['TYPE'] = str(icmp_type)
                        currentPacket['CODE'] = str(code)
                        currentPacket['CHECKSUM'] = str(checksum)

                        h_size = eth_length + iph_length + icmph_length
                        data_size = len(packet) - h_size

                        #get data from the packet
                        data = packet[h_size:]

                        currentPacket['DATA_SIZE'] = data_size
                        currentPacket['DATA'] = data

                        #print 'Data : ' + data

                        #UDP packets
                  elif protocol == 17 :
                        print "UDP\n"
                        u = iph_length + eth_length
                        udph_length = 8
                        udp_header = packet[u:u+8]

                        #now unpack them :)
                        udph = unpack('!HHHH' , udp_header)

                        source_port = udph[0]
                        dest_port = udph[1]
                        length = udph[2]
                        checksum = udph[3]

                        print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)

                        currentPacket['SOURCE_PORT'] = str(source_port)
                        currentPacket['DEST_PORT'] = str(dest_port)
                        currentPacket['LENGTH'] = str(length)
                        currentPacket['CHECKSUM'] = str(checksum)
                        h_size = eth_length + iph_length + udph_length
                        data_size = len(packet) - h_size

                        #get data from the packet
                        data = packet[h_size:]

                        currentPacket['DATA_SIZE'] = data_size
                        currentPacket['DATA'] = data

                        #print 'Data : ' + data

                        #some other IP packet like IGMP
                  else :
                        print 'Protocol other than TCP/UDP/ICMP'

                  listPackets.append(currentPacket)

def open_pcap(filename):

    counter = 0
    tcp_counter = 0

    for ts, pkt in dpkt.pcap.Reader(open(filename,'r')):

        counter += 1
        eth = dpkt.ethernet.Ethernet(pkt)
        if eth.type != dpkt.ethernet.ETH_TYPE_IP:
           continue

        ip = eth.data

        if results.filter == "src":
            src_ip_addr_str = socket.inet_ntoa(ip.src)
            if results.ip_addr == src_ip_addr_str:
                print "src: " + src_ip_addr_str

        elif results.filter == "dst":
            dst_ip_addr_str = socket.inet_ntoa(ip.dst)
            if results.ip_addr == dst_ip_addr_str:
                print "dst: " + dst_ip_addr_str

        else:
            print "Unknow command"
            break

        if ip.p == dpkt.ip.IP_PROTO_TCP:
           tcp_counter += 1

    print "Total number of packets in the pcap file: ", counter
    print "Total number of tcp packets: ", tcp_counter



if __name__ == '__main__':

      if len(sys.argv) > 1:
            parser = argparse.ArgumentParser()
            parser.add_argument('-filename', action='store', dest='filename',
                help='pcap file')
            parser.add_argument('-filter', action='store', dest='filter',
                default=10, help='filter [src] or [dst]')
            parser.add_argument('-addr', action='store', dest='ip_addr',
                default=10, help='ip adress')
            parser.add_argument('--version', action='version',
                version="%(prog)s 0.1")
            results = parser.parse_args()
            getPacket(openSocket())
