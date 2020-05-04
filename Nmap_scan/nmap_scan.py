#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import nmap
import json
from time import ctime

port = '1-65535'
arg = '-Pn -sV -sS --open'    # nmap的参数
print('\n' + 'Scanning time: ' + ctime() + '\n')

with open('nmap1.txt', 'r') as lines:
    for line in lines.readlines():
        nm = nmap.PortScanner()
        nm.scan(hosts=line, ports=port, arguments=arg)
        for host in nm.all_hosts():
            hostname = 'Host: %s hostname: (%s)\n' % (host, nm[host].hostname())    # 返回已IP地址和主机名
            tcp_open = json.dumps(nm[host]['tcp'], indent=2)     # 返回已开启的TCP端口
            udp_open = json.dumps(nm[host].all_udp(), indent=2)    # 返回已开启的UDP端口
            show = hostname + '\nTCP: \n' + tcp_open + '\n\nUDP: \n' + udp_open
            print(show + '\n\n\n----------------------------------------\n\n\n')
            with open('host1.txt', 'a+') as files:
                files.write(show + '\n\n\n----------------------------------------\n\n\n')
                print('\n' + 'End of scan time: ' + ctime() + '\n')
                print('\nfinished!\n\n')
