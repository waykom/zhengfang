#!/usr/bin/python
# -*- coding:utf-8 -*-

import getpass
import requests
import time
from lxml import html
import execjs
import urllib.parse
from texttable import Texttable

def getCsrfToken(loginurl):
    # csrftoken
    bodyByGet = client.get(loginurl)
    tree = html.fromstring(bodyByGet.text)
    csrftoken = tree.xpath('//*[@id="csrftoken"]/@value')[0]
    return csrftoken
def getModExp(key):
    # exponent,modulus
    ntime = round(time.time()*1000)
    modExpurl = f'http://jwxt.gxust.edu.cn:9600/xtgl/login_getPublicKey.html?time={ntime}&_={ntime-50}'
    modExp = client.get(modExpurl).json()
    # mm
    JS = open('D:\AppData\PycharmProjects\EduCrawler\crypto_rsa.js').read()
    mm = execjs.compile(JS).call('start', modExp['exponent'], modExp['modulus'], key)
    return mm
def login(user, mm):
    # login
    mm = getModExp(mm)
    csrftoken = getCsrfToken('http://jwxt.gxust.edu.cn:9600/xtgl/login_slogin.html')
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jwxt.gxust.edu.cn:9600',
        'Origin': 'http://jwxt.gxust.edu.cn:9600',
        'Referer': 'http://jwxt.gxust.edu.cn:9600/xtgl/login_slogin.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    data = f'csrftoken={urllib.parse.quote(csrftoken)}&language=zh_CN&yhm={user}&mm={urllib.parse.quote(mm)}&mm={urllib.parse.quote(mm)}'
    status = client.post(loginurl, headers=headers, data=data)
# print(status.text)
    if '用户名或密码不正确，请重新输入！' in status.text:
        print("用户名或密码不正确，请重新输入！")
# 查询课表
    else:
        print('登录成功!欢迎您!')
        getInfo(user)
        print("当前为第1周")
        showText(1)
        while True:
            week = input('请输入第 周(0退出):')
            if week == "0":
                break
            print(f"当前为第{week}周")
            showText(int(week))

def getInfo(user):
    infourl = f'http://jwxt.gxust.edu.cn:9600/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su={user}'
    response = client.get(infourl).text
    tree = html.fromstring(response)
    name = tree.xpath('//*[@id="col_xm"]/p/text()')[0]
    cla = tree.xpath('//*[@id="col_bh_id"]/p/text()')[0]
    department = tree.xpath('//*[@id="col_zyh_id"]/p/text()')[0]
    print(name.strip(), cla.strip(), department.strip())
def getKb(user):
    scheduleurl = f'http://jwxt.gxust.edu.cn:9600/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151&su={user}'
    data = {
        'xnm': '2021',
        'xqm': '12',
        'kzlx': 'ck'
    }
    response = client.post(scheduleurl, data=data).json()
    return response
def showText(week):
    kblist = getKb(user)
    t11 = t12 = t13 = t14 = t15 = t21 = t22 = t23 = t24 = t25 = t31 = t32 = t33 = t34 = t35 = t41 = t42 = t43 = t44 = t45 = t51 = t52 = t53 = t54 = t55 = t61 = t62 = t63 = t64 = t65 = t71 = t72 = t73 = t74 = t75 = t81 = t82 = t83 = t84 = t85 = t91 = t92 = t93 = t94 = t95 = t101 = t102 = t103 = t104 = t105 = ''

    for item in kblist['kbList']:
        if len(item['zcd'].split('周')[0]) > 2:
            if int(item['zcd'].split('周')[0].split('-')[0]) <= week and int(
                    item['zcd'].split('周')[0].split('-')[1]) >= week:
                # print(item['kcmc'], item['jc'], item['zcd'], item['cdmc'])
                if item['xqjmc'] == '星期一':
                    if item['jc'] == '1-2节':
                        t11 = t21 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-4节':
                        t31 = t41 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-5节':
                        t31 = t41 = t51 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-7节':
                        t61 = t71 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-8节':
                        t61 = t71 = t81 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-9节':
                        t81 = t91 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-10节':
                        t81 = t91 = t101 = item['kcmc'] + item['cdmc']
                if item['xqjmc'] == '星期二':
                    if item['jc'] == '1-2节':
                        t12 = t22 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-4节':
                        t32 = t42 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-5节':
                        t32 = t42 = t52 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-7节':
                        t62 = t72 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-8节':
                        t62 = t72 = t82 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-9节':
                        t82 = t92 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-10节':
                        t82 = t92 = t102 = item['kcmc'] + item['cdmc']
                if item['xqjmc'] == '星期三':
                    if item['jc'] == '1-2节':
                        t13 = t23 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-4节':
                        t33 = t43 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-5节':
                        t33 = t43 = t53 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-7节':
                        t63 = t73 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-8节':
                        t63 = t73 = t83 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-9节':
                        t83 = t93 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-10节':
                        t83 = t93 = t103 = item['kcmc'] + item['cdmc']
                if item['xqjmc'] == '星期四':
                    if item['jc'] == '1-2节':
                        t14 = t24 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-4节':
                        t34 = t44 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-5节':
                        t34 = t44 = t54 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-7节':
                        t64 = t74 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-8节':
                        t64 = t74 = t84 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-9节':
                        t84 = t94 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-10节':
                        t84 = t94 = t104 = item['kcmc'] + item['cdmc']
                if item['xqjmc'] == '星期五':
                    if item['jc'] == '1-2节':
                        t15 = t25 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-4节':
                        t35 = t45 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '3-5节':
                        t35 = t45 = t55 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-7节':
                        t65 = t75 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '6-8节':
                        t65 = t75 = t85 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-9节':
                        t85 = t95 = item['kcmc'] + item['cdmc']
                    if item['jc'] == '8-10节':
                        t85 = t95 = t105 = item['kcmc'] + item['cdmc']
            continue
        if int(item['zcd'].split('周')[0]) == week:
            print(item['kcmc'], item['jc'], item['zcd'], item['cdmc'])
    table = Texttable(max_width=160)
    table.set_cols_align(["c", "c", "c", "c", "c", "c"])
    table.set_cols_valign(["t", "t", "t", "t", "t", "t"])
    table.add_rows([
        ["***", "星期一", "星期二", "星期三", "星期四", "星期五"],
        [1, t11, t12, t13, t14, t15],
        [2, t21, t22, t23, t24, t25],
        [3, t31, t32, t33, t34, t35],
        [4, t41, t42, t43, t44, t45],
        [5, t51, t52, t53, t54, t55],
        [6, t61, t62, t63, t64, t65],
        [7, t71, t72, t73, t74, t75],
        [8, t81, t82, t83, t84, t85],
        [9, t91, t92, t93, t94, t95],
        [10, t101, t102, t103, t104, t105],
    ])

    print(table.draw())


if __name__ == '__main__':
    client = requests.session()
    loginurl = 'http://jwxt.gxust.edu.cn:9600/xtgl/login_slogin.html'
    user = input("账号：")
    password = input("密码：")
    # password = getpass.getpass("密码:")
    # login(input("账号："), input("账号："))
    login(user, password)











