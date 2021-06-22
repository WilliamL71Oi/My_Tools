#!/usr/bin/env python
# -*- coding=utf-8 -*-

import multiprocessing
from scapy.all import *
from random import randint
import time


def Scan(ip):
    ip_id = randint(1, 65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)
    packet1 = IP(dst=ip, ttl=64, id=ip_id) / ICMP(id=icmp_id, seq=icmp_seq) / b'rootkit'
    # sr1()函数和sr()函数作用基本一样，但是值返回一个应答包。只需要使用一个列表就可以保存这个函数的返回值.
    result = sr1(packet1, timeout=1, verbose=False)
    if result:
        for rcv in result:
            scan_ip = rcv[IP].src
            print(scan_ip + '--->' 'Host is up')
    else:
        print(ip + '--->' 'host is down')


if __name__ == "__main__":
    print("开始时间：" + time.strftime("%Y-%m-%d, %H:%M:%S"))
    with open("ip_addr.txt", 'r') as f:
        for i in f.readlines():
            i = i.strip()
            multiPing = multiprocessing.Process(target=Scan(i))
            multiPing.start()
    print("结束时间： " + time.strftime("%Y-%m-%d, %H:%M:%S"))

