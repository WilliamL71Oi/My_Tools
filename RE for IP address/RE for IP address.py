#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

with open('result1.txt','r') as f:
    f2 = str(f.readlines())
    patterns = re.findall(r"http[s]?://(?:[0-9]{1,3}.){3}[0-9]{1,3}:[0-9]{1,5}",f2,re.S)
    #如果txt只有IP地址，直接输入r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"即可。
    if patterns:
        print("RE can find the IP Address! Pls check the ip_addr.txt")
        with open('ip_addr.txt', 'w+') as ips:
            for pattern in patterns:
                print(pattern)
                ips.write(pattern + '\n')
    else:
        print("RE cannot find the IP Address!")
