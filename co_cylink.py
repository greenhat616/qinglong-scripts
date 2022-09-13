# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "22 2 * * *" co_cylink.py, tag: 次元链接流量签到
import os
import requests
from notify import send

cookie = os.getenv('CYLINK_COOKIES')
if cookie is None:
    print('请设置环境变量 CYLINK_COOKIES')
    send('Gtloli 签到执行失败！', '请设置环境变量 CYLINK_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value

notify_message = ''
print('执行次元链接流量签到...')
r = requests.post('https://cylink.moe/user/checkin', headers={
    # 'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Referer': 'https://cylink.moe/user',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
}, cookies=cookies)
# print(r.request.headers)
print(r.status_code)
# print(r.headers)
try:
    data = r.json()
    print(data)
    notify_message += '签到: {} \n{}\n'.format(r.status_code, data)
    send('Cylink 签到完成！', notify_message)
except Exception as e:
    print(e)
    print('签到失败！')
    print(r.text)
    send('Cylink 签到失败！', '请登录青龙查看详情!')
