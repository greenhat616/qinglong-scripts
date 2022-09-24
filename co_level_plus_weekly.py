# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "5 4 * * 0" co_sstm.py, tag: 南加每周签到
import os
import httpx
import asyncio
from notify import send
from bs4 import BeautifulSoup

cookie = os.getenv('LEVEL_PLUS_COOKIES')
if cookie is None:
    print('请设置环境变量 LEVEL_PLUS_COOKIES')
    send('南加签到执行失败！', '请设置环境变量 LEVEL_PLUS_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value
async def task():
    notify_message = '[南加周常签到结果]\n'
    async with httpx.AsyncClient(cookies=httpx.Cookies(cookies), http2=True) as client:

        # 获取周常签到任务
        print('获取周常签到任务...')
        r = await client.get('https://www.level-plus.net/plugin.php?H_name=tasks&action=ajax&actions=job&cid=14', headers={
            # 'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Referer': 'https://www.level-plus.net/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            'cache-control': 'max-age=0'
        })

        print('页面返回状态码：', r.status_code)
        # print(r.headers)
        # print(r.request.headers)
        print(r.text)
        notify_message += '获取周常签到任务: {} \n{}\n'.format(r.status_code, r.text)
        
        print('完成签到任务...')
        r = await client.get('https://www.level-plus.net/plugin.php?H_name=tasks&action=ajax&actions=job2&cid=14', headers={
            # 'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Referer': 'https://www.level-plus.net/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            'cache-control': 'max-age=0'
        })
        print('页面返回状态码：', r.status_code)
        # print(r.headers)
        # print(r.request.headers)
        print(r.text)
        notify_message += '获取周常签到任务: {} \n{}\n'.format(r.status_code, r.text)
        send('南加周常签到执行成功！', notify_message)
try: 
    asyncio.run(task())
except Exception as e:
    print(e)
    print('签到失败！')
    send('南加周常签到执行失败！', '请到青龙面板查看日记！')
