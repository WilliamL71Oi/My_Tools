#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from multiprocessing import Process
import pandas as pd
import requests
import json
import time
import re


def dataPd():
    with open(r"IP_addr1.txt", "r", encoding='UTF-8') as ipAddrs:
        aa = []
        bb = []
        cc = []
        dd = []
        ee = []
        ff = []
        gg = []
        for ipAddr in ipAddrs.readlines():
            # 微步企业版v3
            url = "http://your-ip/api/v3/intelligence_search?apiKey=your-key&data={}".format(
                ipAddr).strip()
            response = requests.get(url)
            content = response.text
            json_dict = json.loads(content)['content']
            # 微步的api结果为json多层结构，所以需要用到多层次获取结果，例如json_dict[0]['location']['country']来获取城市名称
            # IP地址
            try:
                aa.append(json_dict[0]['data'])
            except IndexError:
                pass
            # 地理位置
            try:
                bb.append([json_dict[0]['location']['country'] + "-" + json_dict[0]['location']['province'] + "-" +
                           json_dict[0]['location']['city']])
            except IndexError:
                pass
            # IP注册机构
            try:
                for i in [json_dict[0]['asn']]:    # 如果用for循环，导出excel后每行会多出"[]"字符。还有其他方法，例如下面代码的replace
                    cc.append(i)
            except (IndexError, ValueError):
                cc.append(['null'])
            # 情报来源
            try:
                dd.append([json_dict[0]['now'][0]['source_name']])
            except IndexError:
                dd.append(['null'])
            # 微步标签
            try:
                threadType0 = json_dict[0]['now'][0]['type']
                threadType1 = json_dict[0]['now'][1]['type']
                threadType2 = json_dict[0]['now'][2]['type']
                ee.append([threadType0 + '/' + threadType1 + '/' + threadType2])
            except IndexError:
                ee.append([threadType0 + '/' + threadType1])
            # 威胁级别
            try:
                ff.append([json_dict[0]['now'][0]['severity']])
            except IndexError:
                ff.append(['null'])
            # 置信度
            try:
                confidence = str(json_dict[0]['now'][0]['confidence'])
                gg.append([confidence])
            except IndexError:
                gg.append(['null'])
        # 去除字符"g[]'"，去除后悔变成str，用split转换回list，在代入到pd.DataFrame中
        # bb为地理位置，元素中有多个空格，暂时不知道怎么去除"[]'"
        bb = str(bb).replace('[', '').replace(']', '').replace('\'', '').replace(',', '').split(' ')
        dd = str(dd).replace('[', '').replace(']', '').replace('\'', '').replace(',', '').split(' ')
        ee = str(ee).replace('[', '').replace(']', '').replace('\'', '')
        # 去除逗号后的空格并把str转成list：去除前“, Residence/Dynamic IP”，去除后“, 'Residence/Dynamic IP'”
        ee = [x for x in re.split(', ', ee) if x != ' ']
        ff = str(ff).replace('[', '').replace(']', '').replace('\'', '').replace(',', '').split(' ')
        gg = str(gg).replace('[', '').replace(']', '').replace('\'', '').replace(',', '').split(' ')
        # 把index和数据内容添加到pandas中的DataFrame中
        df = pd.DataFrame({"IP": aa, "地理位置": bb, "IP注册机构": cc, "情报来源": dd, "微步标签": ee, "威胁级别": ff, "置信度": gg})
        # 添加序号索引，默认值为1
        df.index.names = ['序号']
        df.index = df.index + 1
        # 通过pandas导出csv
        df.to_csv("test1.csv", mode='w+', sep=',', encoding="utf_8_sig")


if __name__ == '__main__':
    print("开始时间：" + time.strftime("%Y-%m-%d, %H:%M:%S"))
    # 多进程
    p = Process(target=dataPd(), args=('python',))
    p.start()
    print("结束时间： " + time.strftime("%Y-%m-%d, %H:%M:%S"))
