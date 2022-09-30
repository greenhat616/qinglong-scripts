# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "20 2 * * *" co_sstm.py, tag: 绯月签到
import os
import httpx
import asyncio
from notify import send
from bs4 import BeautifulSoup

cookie = os.getenv('KFMAX_COOKIES')
if cookie is None:
    print('请设置环境变量 KFMAX_COOKIES')
    send('绯月签到执行失败！', '请设置环境变量 KFMAX_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value
async def task():
    notify_message = '[绯月签到结果]\n'
    async with httpx.AsyncClient(cookies=httpx.Cookies(cookies), http2=True) as client:

        # 获取签到页信息
        r = await client.get('https://bbs.kfmax.com/kf_growup.php', headers={
            # 'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Referer': 'https://bbs.kfmax.com/index.php',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cache-control': 'max-age=0'
        })

        print('页面返回状态码：', r.status_code)
        # print(r.headers)
        # print(r.request.headers)
        # print(r.text)
        print('尝试解析页面...')
        dom = BeautifulSoup(r.text, 'lxml')
        a = dom.find('table').findChild('a')
        if a is None or a.text == '今天的每日奖励已经领过了，请明天继续。':
            print('已签到')
            print(r.text)
            notify_message += '已签到'
            send('绯月签到执行成功！', notify_message)
            return
        print('签到链接：', a['href'])
        print('签到奖励：', a.text)
        print('尝试签到...')
        r = await client.get('https://bbs.kfmax.com/{}'.format(a['href']), headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Referer': 'https://bbs.kfmax.com/kf_growup.php',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cache-control': 'max-age=0'
        })
        print(r.status_code)
        print(r.text)
        notify_message += '签到成功！\n 签到奖励：{}'.format(r.text)
        send('绯月签到执行成功！', notify_message)
try: 
    asyncio.run(task())
except Exception as e:
    print(e)
    print('签到失败！')
    send('绯月签到执行失败！', '请到青龙面板查看日记！')
