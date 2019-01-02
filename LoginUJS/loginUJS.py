#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
from PIL import Image
import numpy as np

def kill_captcha(data):
    with open('captcha.png', 'wb') as fp:
        fp.write(data)
    image = Image.open('captcha.png')
    image.show()
    return input('请输入验证码: ')


def get_balance(handled_json):
    balance = handled_json[0]['description']
    soup = BeautifulSoup(balance, "html5lib")
    balance = soup.find('span').text
    print("校园卡余额：", balance, "元")


def log_in(user_name, password, oncaptcha):
    with open('cookie.txt', 'r') as file:
        cookie = file.readline()
        headers = {'Cookie': cookie}
        url = 'http://my.ujs.edu.cn/pnull.portal?.f=f1346&.pmn=view&action=informationCenterAjax&.ia=false&.pen=pe570'
        captcha_url = 'http://my.ujs.edu.cn/captchaGenerate.portal?s=0.19485349472026403'
        login_url = 'http://my.ujs.edu.cn/userPasswordValidate.portal'
    try:
        requests.post(url, headers=headers)
        response_json = requests.post(url, headers=headers).content
        handled_json = json.loads(response_json)[]

    except json.decoder.JSONDecodeError as json_error:
        print("读取缓存失败，开始登陆")
        session = requests.session()
        session.get('http://my.ujs.edu.cn/index.portal')
        captcha_content = session.get(captcha_url).content
        data = {
            'Login.Token1': user_name,
            'Login.Token2': password,
            'captchaField': oncaptcha(captcha_content)
        }
        resp = session.post(login_url, data).text
        assert 'LoginSuccessed' in resp

        cookie = {}
        for item in session.cookies.items():
            cookie[item[0]] = item[1]
        str_cookie = 'JSESSIONID=' + cookie['JSESSIONID'] + ';' + 'iPlanetDirectoryPro=' + cookie['iPlanetDirectoryPro'] + ';'
        with open('cookie.txt', 'w') as file:
            file.write(str_cookie)
        headers = {'Cookie': str_cookie}
        requests.post(url, headers=headers)
        response_json = requests.post(url, headers=headers).content
        handled_json = json.loads(response_json)
        get_balance(handled_json)

    else:
        get_balance(handled_json)


if __name__ == '__main__':
    log_in('id','password',kill_captcha)
