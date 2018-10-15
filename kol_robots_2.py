# -*- coding: utf-8 -*-
import urllib
import urllib.request
import random
import time
import csv
import requests
import json
import xlrd

from bs4 import BeautifulSoup
from selenium import webdriver
from parsel import Selector


file = open("kol_data.csv", "w")

csv_file = csv.writer(file)
csv_file.writerow([
    'UID', '昵称', '性别', '个人签名', '城市', '生日', '星座', '粉丝数', '获赞数',
    '视频数', '采集时间'])

sessions = requests.Session()


class Authentication:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.login_url = 'https://kolranking.com/login'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                          AppleWebKit/537.36 (KHTML, like Gecko) \
                          Chrome/59.0.3071.115 Safari/537.36",
            'Referer': 'https://kolranking.com/settings/account'
        }

    def login(self):
        html = sessions.get(self.login_url, headers=self.headers).text
        soup = BeautifulSoup(html, features="html.parser")
        token = soup.select('input[name="_token"]')[0].get('value')
        data = {
            'email': self.email,
            'password': self.password,
            '_token': token
        }
        r = sessions.post(self.login_url, data=data)
        if r.status_code == 200:
            print('登陆成功！')
        else:
            print('登陆失败！')


def fetch_info(start_url, index_url):

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                      AppleWebKit/537.36 (KHTML, like Gecko) \
                      Chrome/59.0.3071.115 Safari/537.36",
        'Referer': 'https://kolranking.com/settings/account'
    }

    # html0 = sessions.get(start_url, headers=headers).text
    # soup0 = BeautifulSoup(html0, features="html.parser")

    # total_page = int(soup0.find('li', id='Page_End').find(
    #     "a")['href'].split('=')[-1])
    total_page = 1

    for i in list(range(1, total_page + 1)):
        stop = random.uniform(1, 3)
        url = index_url + str(i)
        # req = urllib.request.Request(url)
        # req.add_header(
        #     "User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
        #     (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        # html = urllib.request.urlopen(req).read()
        html = sessions.get(url, headers=headers).text
        soup = BeautifulSoup(html, features="html.parser")

        contents = soup.find('tbody').findAll('tr')

        time.sleep(stop)


def download_info():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                      AppleWebKit/537.36 (KHTML, like Gecko) \
                      Chrome/59.0.3071.115 Safari/537.36",
        'Referer': 'https://kolranking.com/settings/account'
    }
    # download_url = "https://kolranking.com/home?order=follower_count&ot=\
    #                 DESC&page=1&type=download"
    for i in list(range(1, 6)):
        url = "https://kolranking.com/home?order=follower_count&ot=\
               DESC&page={}&type=download".format(i)
        target = sessions.get(url, headers=headers)
        file_name = "kol_demo/demo_page_{}.xlsx".format(i)
        with open(file_name, "wb") as code:
            code.write(target.content)

        data = xlrd.open_workbook(file_name).sheets()[0]
        for c in list(range(1, 11)):
            print('正在获取第{}页的第{}条数据'.format(i, c))
            csv_file.writerow(data.row_values(c))


if __name__ == '__main__':
    try:
        account_info = json.load(open('kol_account.json'))
        email = account_info['email']
        password = account_info['password']
    except:
        email = input('请输入邮箱：')
        password = input('请输入密码：')
    cs = Authentication(email, password)
    cs.login()

    # start_url = "https://kolranking.com/"
    # index_url = "https://kolranking.com/?s=&category=&ot=DESC&order=follower_count&page="
    # fetch_info(start_url, index_url)
    download_info()

file.close()
