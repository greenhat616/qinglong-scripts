# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "12 1 * * *" co_poi.py, tag: Poi 签到
import os
import requests
import requests.utils
from notify import send
import json

cookie = os.getenv('POI_COOKIES')
if cookie is None:
    print('请设置环境变量 POI_COOKIES')
    send('Poi 签到执行失败！', '请设置环境变量 GTLOLI_COOKIES')
    exit(1)
try:
    cookies = {}
    for line in cookie.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    print(cookies)

    notify_message = '[Poi 签到结果]\n'
    s = requests.Session()
    requests.utils.add_dict_to_cookiejar(
        s.cookies, cookies)  # 加入本地存储的 Cookies 到 CookieJar

    # 刷新 Cookies
    print('刷新 Cookies...')
    r = s.get('https://poi6.com/', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://poi6.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
    })

    print('接口返回: {}'.format(r.status_code))
    if r.status_code != 200:
        print('刷新 Cookies 失败！')
        print(r.text)
        send('Poi 签到失败！', '请登录青龙查看详情!')
        exit(1)
    # print(r.text)
    # print(r.headers)

    # 获取心跳包
    cookie_dict = requests.utils.dict_from_cookiejar(s.cookies)
    r = s.get('https://poi6.com/heartbeat', headers={
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://poi6.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Bearer {}'.format(cookie_dict['auth_token'])
    })
    print('页面状态：{}'.format(r.status_code))
    print('页面返回：{}'.format(r.text))
    data = r.json()
    if data['signed'] == True:
        print('今日已签到')
        send('Poi 签到失败！', '今日已签到，请明天再来哦！')
        exit(0)
    cookie_dict = requests.utils.dict_from_cookiejar(s.cookies)
    r = s.get('https://poi6.com/heartbeat', headers={
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://poi6.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Bearer {}'.format(cookie_dict['auth_token'])
    })
    print('页面状态：{}'.fomat(r.status_code))
    print('页面返回：{}'.format(r.text))
    notify_message += '页面状态：{}\n页面返回：{}\n'.format(r.status_code, r.text)
    send('Poi 签到成功！', notify_message)
except Exception as e:
    print(e)
    send('Poi 签到执行失败！', '{}'.format(e))
    exit(1)