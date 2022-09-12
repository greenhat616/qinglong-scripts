# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "22 2 * * *" co_cangku.py, tag: 仓库签到
import os
import requests
from notify import send

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
print('执行仓库签到...')
r = requests.post('https://cangku.icu/api/v1/user/signin', headers={
    # 'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Referer': 'https://cangku.icu/',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
}, cookies=cookies)
# print(r.request.headers)
print(r.status_code)
# print(r.headers)
print(r.text)
notify_message += '仓库签到: ' + str(r.status_code) + ' ' + r.text + '\n'
send('仓库签到完成！', notify_message)
