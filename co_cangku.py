# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "22 2 * * *" co_cangku.py, tag: 仓库签到
import os
import requests
import requests.utils
from notify import send
import urllib.parse
import json

cookie = os.getenv('CANGKU_COOKIES')
if cookie is None:
    print('请设置环境变量 CANGKU_COOKIES')
    send('Gtloli 签到执行失败！', '请设置环境变量 CANGKU_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value

notify_message = ''
s = requests.Session()
requests.utils.add_dict_to_cookiejar(s.cookies, cookies)
print('更新仓库 XSRF-TOKEN...')
r = s.request('GET', 'https://cangku.moe/user', headers={
    # 'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Referer': 'https://cangku.icu/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
})
print('页面返回: %d' % r.status_code)
# print(r.request.headers)
# print(r.headers)
# print(r.text)
print('执行仓库签到...')
cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)
r = s.post('https://cangku.icu/api/v1/user/signin', headers={
    # 'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Referer': 'https://cangku.icu/',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'X-XSRF-TOKEN': urllib.parse.unquote(cookies_dict['XSRF-TOKEN']),
})

# print(r.request.headers)
print(r.status_code)
# print(r.headers)
try:
    data = r.json()
    print(data)
    notify_message += '签到: {} \n{}\n'.format(r.status_code, data)
    send('仓库签到完成！', notify_message)
except Exception as e:
    print(e)
    print('签到失败！')
    send('仓库签到失败！', '请登录青龙查看详情!')
