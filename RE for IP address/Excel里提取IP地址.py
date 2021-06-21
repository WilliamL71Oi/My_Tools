#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
通过pandas库提取excel内的IP地址
2021-06-19
"""

import pandas as pd
import re

df = pd.read_csv("2021.csv", engine='python', encoding='GB18030')  # 如果csv内容有中文，需要encoding=GB18030
d1 = pd.DataFrame(df)

# 获取某一列
# d1["详细信息"]

# 位置索引：iloc后的方括号中逗号之前的部分表示要获取的行的位置，只输入一个冒号，不输入任何数值表示获取所有的行；逗号之后的方括号表示要获取的列的位置，列的位置同样也是从0开始计数。
# d1.iloc[:,[0,2]]    #获取第1列和第3列的数值

# 切片索引：iloc后的方括号中逗号之前的表示选择的行，当只传入一个冒号是，表示选择所有行；逗号后面表示要选择列的位置区间，0:3表示选择第1列到第4列之间的值(包括第1列但不包含第4列)
# df.iloc[:,0:3] # 获取第1列到第4列的值

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

with open('IP_addr2.txt', 'w+') as ips:
    for pattern1 in new_list2:
        pattern = str(pattern1).replace('[', '').replace(']', '').replace('\'', '')     # 去除 ['] 符号
        ips.write(pattern + '\n')
