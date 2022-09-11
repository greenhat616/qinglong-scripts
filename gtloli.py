# -*- coding: utf-8 -*-
# python版本 >=3.8

from distutils import errors
import os
import requests

cookie = os.getenv('GTLOLI_COOKIES')
if cookie is None:
    print('请设置环境变量 GTLOLI_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value
# 签到
print('执行签到任务...')
r = requests.get('https://www.gtloli.gay/plugin.php?id=k_misign:sign&operation=qiandao&format=button&formhash=5909e57e&inajax=1&ajaxtarget=midaben_sign', headers={
    #'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Referer': 'https://www.gtloli.gay/forum.php',
    'Accept': 'application/xml; charset=gbk',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
}, cookies=cookies)
#print(r.request.headers)
print(r.status_code)
#print(r.headers)
print(r.text)


# 胖次任务
print('领取胖次任务...')
r = requests.get('https://www.gtloli.gay/home.php?mod=task&do=apply&id=32', headers={
    #'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Referer': 'https://www.gtloli.gay/home.php?mod=task',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
}, cookies=cookies)
#print(r.request.headers)
print(r.status_code)
#print(r.headers)
#print(r.text)
print('完成胖次任务...')
r = requests.get('https://www.gtloli.gay/home.php?mod=task&do=draw&id=32', headers={
    #'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Referer': 'https://www.gtloli.gay/home.php?mod=task&item=doing',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
}, cookies=cookies)
#print(r.request.headers)
print(r.status_code)
#print(r.headers)
#print(r.text)

# GT 币任务
print('领取 GT 币任务...')
r = requests.get('https://www.gtloli.gay/home.php?mod=task&do=apply&id=33', headers={
    #'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Referer': 'https://www.gtloli.gay/home.php?mod=task',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
}, cookies=cookies)
#print(r.request.headers)
print(r.status_code)
#print(r.headers)
#print(r.text)
print('完成 GT 币任务...')
r = requests.get('https://www.gtloli.gay/home.php?mod=task&do=draw&id=33', headers={
    #'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Referer': 'https://www.gtloli.gay/home.php?mod=task&item=doing',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
}, cookies=cookies)
#print(r.request.headers)
print(r.status_code)
#print(r.headers)
#print(r.text)

