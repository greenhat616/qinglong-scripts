# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "12 2 * * *" cp_sstm.py, tag: SSTM 签到
import os
import requests
import datetime
import re
from notify import send
from bs4 import BeautifulSoup

# 一些配置
use_hitokoto = True


# 工具函数
def get_hitokoto():
    r = requests.get('https://v1.hitokoto.cn/?c=a&c=b&c=c')
    return r.json()


# cookie 处理逻辑
cookie = os.getenv('SSTM_COOKIES')
if cookie is None:
    print('请设置环境变量 SSTM_COOKIES')
    exit(1)
cookies = {}
for line in cookie.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value


# 获取签到页信息
print('获取签到页信息...')
r = requests.get(url='https://sstm.moe/forum/72-%E5%90%8C%E7%9B%9F%E7%AD%BE%E5%88%B0%E5%8C%BA/', headers={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}, cookies=cookies)

print('签到页面返回：{}'.format(r.status_code))
sign_page_str = r.text
print('尝试解析签到页面...')

dom = BeautifulSoup(sign_page_str, 'lxml')
top_sign_page = dom.find('ol', {
    'class': ['ipsClear', 'ipsDataList', 'cForumTopicTable', 'cTopicList'],
    'data-role': 'tableRows'
}).findChildren('li')[0]
top_sign_page_element = top_sign_page.find(
    'span', {'class': ['ipsType_break', 'ipsContained']}).find('a')
top_sign_page_title = top_sign_page_element.attrs['title']
top_sign_page_href = top_sign_page_element.attrs['href']
print('当前最新的签到页：{}'.format(top_sign_page_title))
now = datetime.datetime.now()
current_date = '{}/{}/{}'.format(now.year, now.month, now.day)
print('当前日期： {}'.format(current_date))
top_sign_page_date = re.search(r'【(.*)】', top_sign_page_title).group(1).strip()
print('签到页日期：{}'.format(top_sign_page_date))
if current_date != top_sign_page_date:
    print('签到页日期与当前日期不符，跳过签到流程！')
    exit()
is_signed = top_sign_page.find(
    'i', {'class': ['fa', 'fa-star']}) is not None
print('是否已签到: {}'.format(is_signed))
if is_signed == True:
    print('今日已签到，跳过签到流程！')
    exit()


# 签到参数准备流程
topic_id = re.search(r'https://sstm.moe/topic/(\d+)-*',
                     top_sign_page_href).group(1)  # topic_id
print('签到贴 ID: {}'.format(topic_id))
print('获取必要参数, Part 1. 访问: {} ...'.format(top_sign_page_href))
r = requests.get(url=top_sign_page_href, headers={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'referer': 'https://sstm.moe/forum/72-%E5%90%8C%E7%9B%9F%E7%AD%BE%E5%88%B0%E5%8C%BA/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}, cookies=cookies)
print('页面返回: {}'.format(r.status_code))
# print(r.text)
print('尝试解析页面...')
dom = BeautifulSoup(r.text, 'lxml')
post_params = {}
inputs = dom.find('form', {
    'class': ['ipsForm', 'ipsForm_vertical']
}).findChildren('input')
print('解析成功！')
for input in inputs:
    post_params[input.attrs['name']] = input.attrs['value']
del post_params['topic_auto_follow_checkbox']
for param in post_params:
    print('参数 {}: {}'.format(param, post_params[param]))

editor_url = '{}?{}={}&{}={}'.format(top_sign_page_href,
                                     'csrfKey', post_params['csrfKey'], 'getUploader', 'topic_comment_{}'.format(topic_id))
print('获取必要参数, Part 2. 访问: {} ...'.format(editor_url))
r = requests.get(url=editor_url, headers={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'referer': top_sign_page_href,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}, cookies=cookies)
print('页面返回: {}'.format(r.status_code))
# print(r.text)
print('尝试解析页面...')
dom = BeautifulSoup(r.text, 'lxml')
topic_comment_upload_element = dom.find('input', {
    # name: 'topic_comment_{}_upload'.format(topic_id)
})
print('解析成功！')
print('参数 {}: {}'.format(
    topic_comment_upload_element.attrs['name'], topic_comment_upload_element.attrs['value']))
post_params[topic_comment_upload_element.attrs['name']
            ] = topic_comment_upload_element.attrs['value']

print('添加一些不知道作用（如何解析）的参数')
post_params['currentPage'] = '1'
post_params['_lastSeenID'] = '16110378'
print('参数 {}: {}'.format('currentPage', 1))
print('参数 {}: {}'.format('_lastSeenID', 16110378))

comment = '<p>{}年{}月{}日签到。<p>'.format(now.year, now.month, now.day)
if use_hitokoto is True:
    sentence = get_hitokoto()
    comment += '<p>{} —— {}</p>'.format(sentence['hitokoto'], sentence['from'])
print('拟发送签到内容：{}'.format(comment))
post_params['topic_comment_{}'.format(topic_id)] = comment
print('回复签到贴...')
r = requests.post(url=top_sign_page_href, headers={
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'referer': top_sign_page_href,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with': 'XMLHttpRequest'
}, cookies=cookies, data=post_params)
print('接口返回: {}'.format(r.status_code))
try:
    data = r.json()
    if data['type'] == 'add' or data['type'] == 'redirect':
        print('签到成功！')
    else:
        print('签到失败！')
        raise Exception('签到失败！')
except Exception:
    print('签到内容解析失败或程序无法辨别是否成功！')
    print(r.text)
