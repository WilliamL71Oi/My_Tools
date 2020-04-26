#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests,re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#不添加这条的话会报错："InsecureRequestWarning: Unverified HTTPS request is being made."

url = "http://www.89ip.cn/tqdl.html?api=1&num=1000"
#这里的num=1000,指的是从该网站获取1000个代理ip，可以自定义数量,但获取的代理IP地址不一定可用。
#如果以上网址失效，可以用这个网址代替：http://www.66ip.cn/
types = "https"
proxys = {}

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_10) App leWebKit/600.1.25 (KHTML, like Gecko) Version/12.0 Safari/1200.1.25'}
    r = requests.get(url,headers=headers).text
    ips = re.findall(r"((?:[0-9]{1,3}.){3}[0-9]{1,3}:[0-9]{1,5})",r)    #正则匹配IP与端口
    print('获取到的有效代理IP地址： \n' )
    for proxy in ips:
        proxys[types.lower()] = '%s'%proxy
        #proxys["https"] = proxy 无需types，直接这样也行。
        try:
            tar = requests.get("https://ifconfig.me/ip",headers=headers,proxies=proxys,timeout=5,verify=False).text
            # "https://ifconfig.me/ip"为验证代理ip是否有效的网站
            # 如果写入的ip地址比显示的少，请查看ipconfig.me/ip这网站延时是否很大，可以增加timeout的数值。
            if tar in str(proxys):
                print(proxy)
                with open("ip1.txt",'a') as files:
                    files.write(proxy+'\n')
        except:
            pass

if __name__ == '__main__':
    main()
    print("\n已完成IP代理地址的验证。")
