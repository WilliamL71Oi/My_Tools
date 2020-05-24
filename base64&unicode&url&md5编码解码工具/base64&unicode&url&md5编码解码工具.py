#! /usr/bin/python3
# -*- coding: UTF-8 -*-

from itertools import islice
import urllib.parse
import argparse
import hashlib
import base64
import sys


def _argparse():
    parser = argparse.ArgumentParser(description="base64/unicode/url/md5 encode & decode.")
    parser.add_argument('--b64en', dest='b64_en', help='base64_encode')
    parser.add_argument('--b64de', dest='b64_de', help='base64_decode')
    parser.add_argument('--unien', dest='uni_en', help='unicode_encode')
    parser.add_argument('--unide', dest='uni_de', help='unicode_decode')
    parser.add_argument('--urlen', dest='url_en', help='url_encode')
    parser.add_argument('--urlde', dest='url_de', help='url_decode')
    parser.add_argument('--md5en', dest='md5_en', help='md5_encode')
    parser.add_argument('--md5de', dest='md5_de', help='md5_decode')
    return parser.parse_args()


# base64编码
def b64_encode():
    text = sys.argv[2]
    bstring = text.encode(encoding='utf-8')
    encodestr = base64.b64encode(bstring)
    return encodestr.decode()


# base64解码
def b64_decode():
    text = sys.argv[2]
    decodestr = base64.b64decode(text)
    return decodestr.decode()


# unicode编码
def uni_en():
    text = sys.argv[2]
    un_en = text.encode("unicode_escape")
    return un_en


# unicode解码
def uni_de():
    text = sys.argv[2]
    un_de = text.encode('utf-8').decode("unicode_escape")
    return un_de


# url编码
def url_en():
    text = sys.argv[2]
    return urllib.parse.quote(text)


# url解码
def url_de():
    text = sys.argv[2]
    return urllib.parse.unquote(text)


# md5加密
def md5_en():
    text = sys.argv[2]
    a = hashlib.md5()
    a.update(text.encode(encoding='utf-8'))
    return a.hexdigest()


# md5解密
def md5_de():
    text = sys.argv[2].strip()
    with open('60万条MD5密文.txt', 'r') as f:
        for line in f:
            if text == line.strip():
                r = '\n' + text + ' MD5解密为：'
                print(r, end='')
                print(''.join(islice(f, 1)))
                break
        else:
            print('\n您输入的MD5解密无匹配结果。')


def main():
    parser = _argparse()
    sys.argv.append("")
    if sys.argv[1] == '--b64en':
        print(parser.b64_en, " 的base64编码为： ", b64_encode())
    if sys.argv[1] == '--b64de':
        print(parser.b64_de, " 的base64解码为： ", b64_decode())
    if sys.argv[1] == '--unien':
        print(parser.uni_en, " 的unicode编码为： ", uni_en())
    if sys.argv[1] == '--unide':
        print(parser.uni_de, " 的unicode解码为： ", uni_de())
    if sys.argv[1] == '--urlen':
        print(parser.url_en, " url编码为： ", url_en())
    if sys.argv[1] == '--urlde':
        print(parser.url_de, " url解码为： ", url_de())
    if sys.argv[1] == '--md5en':
        print(parser.md5_en, " md5加密为： ", md5_en())
    if sys.argv[1] == '--md5de':
        return md5_de()


if __name__ == '__main__':
    main()
