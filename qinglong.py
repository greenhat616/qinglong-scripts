import os
import httpx
import asyncio
import json

qinglong_config = {
    'CLIENT_ID': '',
    'CLIENT_SECRET': '',
    'QINGLONG_URL': 'http://127.0.0.1:1234'
}

for k in qinglong_config:
    qinglong_config[k] = os.getenv(k, qinglong_config[k])


async def get_token():
    async with httpx.AsyncClient() as client:
        response = await client.get('{}/open/auth/token?client_id={}&client_secret={}'.format(
            qinglong_config['QINGLONG_URL'], qinglong_config['CLIENT_ID'], qinglong_config['CLIENT_SECRET']))
        data = response.json()
        if data.get('code') != 200:
            print(data)
            raise Exception('获取 token 失败！')
        return data.get('data').get('token')


async def get_envs():
    token = await get_token()
    async with httpx.AsyncClient(headers={
        'Authorization': 'Bearer {}'.format(token)
    }) as client:
        response = await client.get('{}/open/envs'.format(qinglong_config['QINGLONG_URL']))
        data = response.json()
        if data.get('code') != 200:
            print(data)
            raise Exception('获取 envs 失败！')
        return data.get('data')

# 只支持更新获取到的第一个 env id


async def update_env(name, value, remarks=None):
    envs = await get_envs()
    id = 0
    for env in envs:
        if env['name'] == name:
            id = env['id']
            if remarks is None:
                remarks = env['remarks']
    token = await get_token()
    async with httpx.AsyncClient(headers={
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json'
    }) as client:
        request_data = {
            'value': value,
            'id': id,
            'name': name}
        if remarks is not None:
            request_data['remarks'] = remarks
        response = await client.put('{}/open/envs'.format(qinglong_config['QINGLONG_URL']), data=json.dumps(request_data)
                                    )
        data = response.json()
        
    if data.get('code') != 200:
        print(data)
        raise Exception('更新 env 失败！')
    return data.get('data')
        

if __name__ == '__main__':
    asyncio.run(get_envs())
    asyncio.run(update_env('A', 'CCCC'))
