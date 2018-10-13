# -*- coding: utf-8 -*-
import urllib
import urllib.request
import random
import time
import csv
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from parsel import Selector


# file = open("kol_data.csv", "w")

# csv_file = csv.writer(file)
# csv_file.writerow([
#     '昵称', '主页', '头像', '平台', '联系方式', '粉丝数', '线上报价', '线下报价', '所在地',
#     '标签', '直播间', '简介'])

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
    total_count = 0
    success_count = 0
    failed_count = 0

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

        for content in contents:
            counts = contents.index(content)
            try:
                profile_url = content.findAll('td')[2].find('a')['href']
            except:
                profile_url = ''

            if profile_url is not None:
                profile_url = "https://kolranking.com" + profile_url

                ss = "正在爬取第%d页的第%d条信息，网址为%s" % (i, counts + 1, profile_url)
                print(ss)
                total_count += 1

                detail_html = sessions.get(
                    profile_url, headers=headers).text
                detail = Selector(text=detail_html)

                try:
                    avatar = detail.xpath(
                        "//img[@class='avatar']/@src").extract_first()
                except:
                    avatar = ''

                try:
                    # username.find('div', class_="align-center")
                    username = detail.xpath(
                        "//div[@class='align-center']").extract_first()
                    print('2231243', username)
                    # username = username.findAll("p")[0].text
                except:
                    username = ''
                print('>>>>', username)


if __name__ == '__main__':
    # email = input('请输入邮箱：')
    # password = input('请输入密码：')
    # cs = Authentication(email, password)
    # cs.login()

    start_url = "https://kolranking.com/"
    index_url = "https://kolranking.com/?s=&category=&ot=DESC&order=follower_count&page="
    fetch_info(start_url, index_url)

# file.close()
