# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "20 2 * * *" co_gmgard.py, tag: Gtloli 社区签到
import os
import requests
import json
from notify import send

cookie = os.getenv('GMGARD_COOKIES')
if cookie is None:
    print('请设置环境变量 GMGARD_COOKIES')
    send('GMGARD 签到执行失败！', '请设置环境变量 GMGARD_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value

try:
    
    notify_message = '[Gmgard 签到结果]\n'
    # 签到
    print('执行签到任务...')
    r = requests.post('https://gmgard.com/api/PunchIn/Do', headers={
        # 'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Referer': 'https://www.gtloli.gay/forum.php',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest'
    }, cookies=cookies, data=json.dumps({}))
    # print(r.request.headers)
    print(r.status_code)
    # print(r.headers)
    try:
        data = r.json()
        print(data)
        notify_message += '签到: {} \n{}\n'.format(r.status_code, data)
        send('Gmgard 签到完成！', notify_message)
    except Exception as e:
        print(e)
        print('签到失败！')
        print(r.text)
        send('Gmgard 签到失败！', '请登录青龙查看详情!')

except Exception as e:
    print(e)
    send('Gmgard 签到失败！', '请登录青龙查看详情!')