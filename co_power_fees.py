# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "22 2 * * *" co_cylink.py, tag: 次元链接流量签到
import os
import requests
import requests.utils
import json
from notify import send

cookie = os.getenv('POWER_FEES_COOKIES')
if cookie is None:
    print('请设置环境变量 POWER_FEES_COOKIES')
    send('获取电费信息失败', '请设置环境变量 POWER_FEES_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value
s = requests.Session()
requests.utils.cookiejar_from_dict(cookies, s.cookies)
'''
r = s.get('https://wsjgg02.gxust.edu.cn/Home/GetYzm', headers={
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c24) NetType/WIFI Language/zh_CN',
    'Referer': 'https://zywxhd02.gxust.edu.cn/Home',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Content-Type': 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'Jgg-User=Jgg-User-orOX3v29KmlY8R7R8urMTLbkOq-A; ASP.NET_SessionId=o1jrm2fsdip3v12od3ix3x1j'
})
print(r.status_code)
yzm = r.text
print(r.text)

r = s.get('https://wsjgg02.gxust.edu.cn/?Yzm={}'.format(yzm) , headers={
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c24) NetType/WIFI Language/zh_CN',
    'Referer': 'https://wsjgg02.gxust.edu.cn/',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
}, cookies=cookies)
print(r.status_code)
print(r.text)
'''
# exit(0)
print('获取电费信息...')
try:
    r = s.post('https://zywxhd02.gxust.edu.cn/Home/GetRoomInfo', data={
    'Yzm': '123',
    'RoomID': '2545'
}, headers={
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c24) NetType/WIFI Language/zh_CN',
    'Referer': 'https://wsjgg02.gxust.edu.cn/',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    # 'Content-Type': 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'
})
except Exception as e:
    print(e)
    send('获取电费信息失败', '请登录青龙面板查看详细信息！')

print('返回状态: {}'.format(r.status_code))
# print(r.request.headers)
data = json.loads(json.loads(r.text))
print('接口返回：{}'.format(data))
if r.status_code != 200 or data['Msg'] != '成功':
    print('接口请求失败，请更新 Cookie！')
    send('获取电费信息失败', '请更新 Cookie！')
    exit(1)

need_send = False
for key in data['component']:
    if key['Name'] == '剩余':
        if float(key['Value']) < 100:
            need_send = True

if need_send:
    send('电费缴费提醒', '电费不足，请准备充值！\n[电费信息]\n宿舍状态: {}\n剩余电量: {}度'.format(data['component'][0]['Value'], data['component'][1]['Value']))
    
