#! /usr/bin/env python

import socket
import sys
import dpkt
import argparse

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
        open_pcap(results.filename)
