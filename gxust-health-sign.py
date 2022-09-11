# -*- coding: utf8 -*-
# python版本 >=3.8

from audioop import reverse
import os
import requests
import json
import time
import hashlib

raw_tokens = os.getenv('GXUST_HEALTH_AUTH_TOKENS')
if raw_tokens is None:
    print('请设置环境变量 GXUST_HEALTH_AUTH_TOKENS')
    exit(1)
tokens = raw_tokens.split('&')  # 切分多个账号
'''
units = []
for info in infos:
    info = info.split(',')
    units.append({
        'sno': info[0],
        'passwd': info[1],
        'code': info[2]
    })
'''

for token in tokens:
    '''
    print('测试账户： ' + unit['sno'] + '...')

    def sign(table, ts, salt):
        i = ''
        keys = [*table.keys()]
        keys.sort()
        for key in keys:
            i = i + key + '=' + table[key] + '&'
        o = len(i)
        md5 = hashlib.md5()
        md5.update((i[0:o-1] + ts + salt).encode('utf-8'))
        return md5.hexdigest()
    data = {
        'username': unit['sno'],
        'password': unit['passwd'],
        'code': unit['code']
    }
    now = str(int(round(time.time() * 1000)))
    r = requests.post(url='https://fuxuewuyou.gxust.edu.cn:9045/auth/loginByUserOrCode',
                      headers={
                          'Accept': 'application/json, text/plain, */*',
                          'content-type': 'application/json;charset=UTF-8',
                          'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b35) NetType/WIFI Language/zh_CN',
                          'Referer': 'https://servicewechat.com/wxe9c88300c9903b6d/84/page-frame.html',
                          's': sign(data, now, '75t4yqlyx3in0aqird5ih4l0o6mn1shi88ad0ufqx1swukznd16hfd2jymhtey9f'),
                          't': now,
                          'XZT-APP-VERSION': 'win10',
                          'XZT-APP-VERSION-CODE': 'v1.0',
                          'XZT-Authorization': 'Basic dGVzdDoxMjM0NTY=',
                          'XZT-CLIENTID': 'PC-001',
                          'XZT-CLIENT-TYPE': 'PC',
                          'XZT-DEVICE-INFO': 'windows',
                          'XZT-LOGIN-IP': '1.1.1.1'
                      },
                      data=json.dumps(data)
                      )
    print(r)
    print(r.text)
    '''

    print('获取签到列表...')
    headers = {
        'XZT-CLIENTID': 'PC-001',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b35) NetType/WIFI Language/zh_CN',
        'Accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + token
    }
    data = {'schoolId':790}
    r = requests.post(url='https://fuxuewuyou.gxust.edu.cn:9045/api/reportNode/getListAndSystemTime', headers=headers, data=json.dumps(data))
    print(r)
    print(r.text)