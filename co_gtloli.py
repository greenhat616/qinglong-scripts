# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "20 2 * * *" co_sstm.py, tag: Gtloli 社区签到
import os
import requests
from notify import send
import httpx
import asyncio
from bs4 import BeautifulSoup

cookie = os.getenv('GTLOLI_COOKIES')
if cookie is None:
    print('请设置环境变量 GTLOLI_COOKIES')
    send('Gtloli 签到执行失败！', '请设置环境变量 GTLOLI_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value
    
async def task():
    notify_message = '[Gtloli 签到结果]\n'
    async with httpx.AsyncClient(cookies=httpx.Cookies(cookies), http2=True) as client:
        try:
            print('获取 formhash...')
            r = await client.get('https://www.gtloli.gay/forum.php', headers= {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Referer': 'https://www.gtloli.gay/forum.php',
                'Accept': 'application/xml; charset=gbk',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            })
            print(r.status_code)
            if r.status_code != 200:
                raise Exception('获取 Formhash 失败！')
            # print(r.text)
            dom = BeautifulSoup(r.text, 'lxml')
            input = dom.find('input', {
                'name': 'formhash'
            })
            # print(input)
            formhash = input.attrs['value']
            print('formhash: {}'.format(formhash))
            print('执行社区签到任务...')
            r = await client.get('https://www.gtloli.gay/plugin.php?id=k_misign:sign&operation=qiandao&format=button&formhash={}&inajax=1&ajaxtarget=midaben_sign'.format(formhash), headers={
                # 'Cookie': cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Referer': 'https://www.gtloli.gay/forum.php',
                'Accept': 'application/xml; charset=gbk',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            })
            print(r.request.headers)
            print(r.status_code)
            print(r.headers)
            print(r.text)
            notify_message += '社区签到: ' + str(r.status_code) + ' ' + r.text + '\n'
            
            # 胖次任务
            print('领取胖次任务...')
            r = await client.get('https://www.gtloli.gay/home.php?mod=task&do=apply&id=32', headers={
                # 'Cookie': cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Referer': 'https://www.gtloli.gay/home.php?mod=task',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            })
            # print(r.request.headers)
            print(r.status_code)
            # print(r.headers)
            # print(r.text)
            notify_message += '领取胖次任务: ' + str(r.status_code) + '\n'

            print('完成胖次任务...')
            r = await client.get('https://www.gtloli.gay/home.php?mod=task&do=draw&id=32', headers={
                # 'Cookie': cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Referer': 'https://www.gtloli.gay/home.php?mod=task&item=doing',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            })
            # print(r.request.headers)
            print(r.status_code)
            # print(r.headers)
            # print(r.text)
            notify_message += '完成胖次任务: ' + str(r.status_code) + '\n'

            # GT 币任务
            print('领取 GT 币任务...')
            r = await client.get('https://www.gtloli.gay/home.php?mod=task&do=apply&id=33', headers={
                # 'Cookie': cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Referer': 'https://www.gtloli.gay/home.php?mod=task',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            })
            # print(r.request.headers)
            print(r.status_code)
            # print(r.headers)
            # print(r.text)
            notify_message += '领取 GT 币任务: ' + str(r.status_code) + '\n'
            print('完成 GT 币任务...')
            r = await client.get('https://www.gtloli.gay/home.php?mod=task&do=draw&id=33', headers={
                # 'Cookie': cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Referer': 'https://www.gtloli.gay/home.php?mod=task&item=doing',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            })
            # print(r.request.headers)
            print(r.status_code)
            # print(r.headers)
            # print(r.text)
            notify_message += '完成 GT 币任务: ' + str(r.status_code) + '\n'
            send('Gtloli 签到完成！', notify_message)
        except Exception as e:
            print(e)
            send('Gtloli 签到失败！', str(e))
        
    

try: 
    asyncio.run(task())
except Exception as e:
    print(e)
    print('签到失败！')
    send('GTloli 签到执行失败！', '请到青龙面板查看日记！')