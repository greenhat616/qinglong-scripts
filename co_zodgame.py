# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "10 1 * * *" co_zodgame.py, tag: Gtloli 社区签到
import os
import requests
from notify import send

cookie = os.getenv('ZODGAME_COOKIES')
if cookie is None:
    print('请设置环境变量 ZODGAME_COOKIES')
    send('ZODGAME 签到执行失败！', '请设置环境变量 ZODGAME_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value

notify_message = '[ZODGAME 签到结果]\n'
print('执行社区签到任务...')
r = requests.post('https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1', headers={
    # 'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Referer': 'https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
},
    cookies=cookies,
    data={
    'formhash':	'59f2dc3e',
    'qdxq':	'kx'
})
# print(r.request.headers)
print(r.status_code)
# print(r.headers)
print(r.text)
notify_message += '社区签到: ' + str(r.status_code) + ' ' + r.text + '\n'
send('[ZODGAME] 签到完成', notify_message)