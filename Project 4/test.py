#!/usr/bin/env python

import SocketServer
import dpkt, pcap, socket
from sys import argv
from ipaddr import IPv4Address, IPv6Address
import syslog
import time
import os

def read_pcap(pcap_file):
    f = open(str(pcap_file), "rb")
    pcap = dpkt.pcap.Reader(f)

    for ts, pkt in pcap:
        try:
            eth=dpkt.ethernet.Ethernet(pkt)
            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
                continue

            #Parsing IP data
            ip=eth.data
            if type(ip) == dpkt.ip.IP:
                ipaddr = IPv4Address(socket.inet_ntop(socket.AF_INET, ip.dst))
            else:
                IPv6Address(socket.inet_ntop(socket.AF_INET6, ip.dst))

            #Parsing TCP data
            if ip.p==dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data

                src = socket.inet_ntoa(ip.src)
                dst = socket.inet_ntoa(ip.dst)
                tcp_sport = tcp.sport
                tcp_dport = tcp.dport

                # if "192.168" in str(src):
                #     total_ips[str(src)] = 1
                #     con = "|" + str(src) + "|" + str(tcp_sport) + "|" + str(dst) + "|" + str(tcp_dport) + "|other|"
                #     total_connections[con] = 1
                #
                # if "192.168" in str(dst):
                #     total_ips[str(dst)] = 1
                #     # con = "|" + str(src) + "|" + str(tcp_sport) + "|" + str(dst) + "|" + str(tcp_dport) + "|" + "|"
                #     # total_connections[con] = 1
                #     con = "|" + str(dst) + "|" + str(tcp_dport) + "|" + str(src) + "|" + str(tcp_sport) + "|other|"
                #     total_connections[con] = 0

                con = "|" + str(src) + "|" + str(tcp_sport) + "|" + str(dst) + "|" + str(tcp_dport) + "|other|"
                reversecon = "|" + str(dst) + "|" + str(tcp_dport) + "|" + str(src) + "|" + str(tcp_sport) + "|other|"

                if con not in total_connections:
                    total_connections[con]=1
                if reversecon not in total_connections:
                    total_connections[con]=0

                #Parsing HTTP data Responses:
                if (tcp.sport == 80) and len(tcp.data) > 0:

                    http = dpkt.http.Response(tcp.data)

                #Parsing HTTP data Requests:
                elif tcp.dport == 80 and len(tcp.data) > 0:

                    http = dpkt.http.Request(tcp.data)

            if ip.p==dpkt.ip.IP_PROTO_UDP:

                udp = ip.data

                src = socket.inet_ntoa(ip.src)
                dst = socket.inet_ntoa(ip.dst)
                udp_sport = udp.sport
                udp_dport = udp.dport

                if "192.168" in str(src):
                    total_ips[str(src)] = 1
                    con = "|" + str(src) + "|" + str(udp_sport) + "|" + str(dst) + "|" + str(udp_dport) + "|" + "|"
                    total_connections[con] = 1

                if "192.168" in str(dst):
                    total_ips[str(dst)] = 1
                    con = "|" + str(dst) + "|" + str(udp_dport) + "|" + str(src) + "|" + str(udp_sport) + "|" + "|"
                    total_connections[con] = 1

        except dpkt.UnpackError as e:
            pass

        except Exception as e:
            pass

    f.close()


if __name__ == "__main__":

    total_ips = {}
    total_connections = {}

    read_pcap(str("new.pcap"))
    #read_pcap(str("new_SAMPLE_bad_ddos.pcap"))
    
    for con in total_connections:
        if total_connections[con]:
            print con
