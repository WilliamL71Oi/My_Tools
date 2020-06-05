#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@author WilliamL71Oi
@date   2020/06/06
"""

import requests
import base64
import re
import time
from lxml import etree
from urllib.parse import quote


# 官网登录fofa vip帐号后，F12-network-cookie-_fofapro_ars_session=-获取cookie的值。
cookie = 'b112838b18495f2e7629f447e49c5929'


def spider():
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/80.0.835.163 "
                      "Safari/535.1",
        "Cookie": "_fofapro_ars_session=" + cookie
    }
    search = input()
    searchbs64 = str(base64.b64encode(search.encode('utf-8')), 'utf-8')
    searchbs64_encode = quote(searchbs64, 'utf-8')  # fofa的url是需要把base64部分进行url编码
    print("\n需要爬行的链接为:\nhttps://fofa.so/result?q=" + search + "&qbase64=" + searchbs64_encode)
    html = requests.get(url="https://fofa.so/result?q=" + search + "&qbase64=" + searchbs64_encode, headers=header).text
    try:
        pagesnums = re.findall('>(\d*)</a> <a class="next_page" rel="next"', html)
        print("发现的总页数: " + pagesnums[0])
        pages1 = input("请输入开始页数： ")
        pages2 = input("请输入结束页数： ")
        with open("result1.txt", "a+") as result:
            for i in range(int(pages1), int(pages2)):
                print("\n现在写入第 " + str(i) + " 页。\n")
                pagesurl = requests.get("https://fofa.so/result?page=" + str(i) + "&q=" + search + "&qbase64=" +
                                        searchbs64_encode, headers=header)
                print("https://fofa.so/result?page=" + str(i) + "&q=" + search + "&qbase64=" + searchbs64_encode + "\n")
                tree = etree.HTML(pagesurl.text)
                urllist = tree.xpath('//div[@class="list_mod_t"]//a[@target="_blank"]/@href')
                for j in urllist:
                    result.write(j + "\n")
                    print(j)
                if i == int(pages2):
                    break
                time.sleep(10)
            print("\n已完成！请查看输出的txt！！")
    except IndexError:
        print('\n您搜索的 {} 获得 0 条匹配结果,可能是语法或关键字问题，或者搜索结果少于一页，请检查语法或者搜索的关键字。'.format(search))


def start():
    print('''
    ***使用说明***
    0.此py为直接爬取fofa搜索结果后的url链接并生成txt.\n
    1.运行此py前，请先在此py里填写自己fofa Pro帐号的cookie.\n
    2.普通帐号只能获取不多于5页的url.\n
    3.如果只能抓取1页，请查看cookie是否有效。\n
    4.如果出现不能获取多页url的情况，请查看cookie是否过期.\n
    5.防止被封IP，所以没做多线程，sleep为12秒.\n
    6.请直接输入fofa的搜索规则,例如输入:title="白帽子".\n
    7.可以进行多语句查询，例如输入：title="白帽子" && country="CN".\n
    8.不支持只有一页搜索结果，都只有一页了，还爬什么虫？\n
    请输入搜索规则：\n 
    ''')


def main():
    start()
    spider()


if __name__ == '__main__':
    main()
