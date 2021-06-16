#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
通过pandas库提取excel内的IP地址
Created by WilliamL71Oi
2021-06-16
"""

import pandas as pd
import re

df = pd.read_csv("2021.csv", engine='python', encoding='GB18030')  # 如果csv内容有中文，需要encoding=GB18030
d1 = pd.DataFrame(df)

new_list1 = []
for index1 in d1.index:
    f2 = d1.loc[index1].values[0:]  # 遍历所有数据，除了索引
    patterns = re.findall(r"[0-9]+(?:\.[0-9]+){3}", str(f2), re.S)  # 正则获取IP地址，当前是list类型
    for i in patterns:
        if i != '':     # 去掉空元素
            new_list1.append(i)     # 把获取到的IP地址写入new_list1列表中

new_list2 = []
for i in new_list1:
    if i not in new_list2:  # 去重复的IP地址
        new_list2.append(i)

with open('IP_addr.txt', 'w+') as ips:
    for pattern1 in new_list2:
        pattern = str(pattern1).replace('[', '').replace(']', '').replace('\'', '')     # 去除 ['] 符号
        ips.write(pattern + '\n')
