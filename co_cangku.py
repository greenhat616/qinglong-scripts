# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "22 2 * * *" co_cangku.py, tag: 仓库签到
import os
import requests
import requests.utils
from notify import send
import urllib.parse
import json
import qinglong
import asyncio
import httpx


cookie = os.getenv('CANGKU_COOKIES')
if cookie is None:
    print('请设置环境变量 CANGKU_COOKIES')
    send('CANGKU 签到执行失败！', '请设置环境变量 CANGKU_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value


async def task():
    cookie_jar = httpx.Cookies()
    for key, value in cookies.items():
        cookie_jar.set(key, value, domain='cangku.moe', path='/')
    notify_message = '[CANGKU] 仓库签到\n'
    async with httpx.AsyncClient(cookies=cookie_jar, http2=True) as client:
        print('更新仓库 XSRF-TOKEN...')
        r = await client.get('https://cangku.moe/user', headers={
            # 'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Referer': 'https://cangku.moe/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        })
        print('页面返回: %d' % r.status_code)
        # print(r.request.headers)
        # print(r.headers)
        # print(r.text)
        print('执行仓库签到...')
        # print(client.cookies)
        # print(client.cookies.get('XSRF-TOKEN'))
        r = await client.post('https://cangku.moe/api/v1/user/signin', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Referer': 'https://cangku.moe/',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            'X-XSRF-TOKEN': urllib.parse.unquote(client.cookies.get('XSRF-TOKEN')),
        })
        # print(r.request.headers)
        print(r.status_code)
        # print(r.headers)
        data = r.json()
        print(data)
        notify_message += '签到: {} \n{}\n'.format(r.status_code, data)
        send('仓库签到完成！', notify_message)

        # 更新仓库 Cookie
        cookie_str = ''
        cookies_list = []
        for key in client.cookies.keys():
            cookies_list.append(('{}={}'.format(key, client.cookies.get(key))))
        cookie_str = "; ".join(cookies_list)
        # print(cookie_str)
        await qinglong.update_env('CANGKU_COOKIES', cookie_str)
        print('更新仓库环境 Cookie 成功！')
    

if __name__ == '__main__':
    try:
        asyncio.run(task())
    except Exception as e:
        print(e)
        print('签到失败！')
        send('仓库签到失败！', '请登录青龙查看详情!')