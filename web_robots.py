# -*- coding: utf-8 -*-
import urllib
import urllib.request
import random
import time
import csv
import requests

from bs4 import BeautifulSoup
from selenium import webdriver


file = open("robots_data.csv", "w")

csv_file = csv.writer(file)
csv_file.writerow([
    '昵称', '主页', '头像', '平台', '联系方式', '粉丝数', '线上报价', '线下报价', '所在地',
    '标签', '直播间', '简介'])

sessions = requests.Session()


class Authentication:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = 'http://www.zhaihehe.com/?/n_login/0'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                          AppleWebKit/537.36 (KHTML, like Gecko) \
                          Chrome/59.0.3071.115 Safari/537.36",
            'Referer': 'http://www.zhaihehe.com/?/member_n/4228'
        }

    def login(self):
        data = {
            'loginname': self.username,
            'password': self.password,
            'submit': '登 录'
        }
        r = sessions.post(self.login_url, data=data)
        if r.status_code == 200:
            print('登陆成功！')
        else:
            print('登陆失败！')
        # self.headers['Referer'] = 'http://www.zhaihehe.com/?/n_login/0'
        # resp = sessions.get(
        #     'http://www.zhaihehe.com/?/authentication_anchor_detail/2273394',
        #     headers=self.headers)

        # soup0 = BeautifulSoup(resp.text, features="html.parser")
        # print(soup0)


def fetch_info(start_url, index_url):

    total_count = 0
    success_count = 0
    failed_count = 0

    # req0 = urllib.request.Request(start_url)
    # req0.add_header(
    #     "User-Agent",
    #     "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    #     (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                      AppleWebKit/537.36 (KHTML, like Gecko) \
                      Chrome/59.0.3071.115 Safari/537.36",
        'Referer': 'http://www.zhaihehe.com/?/n_login/0'
    }

    # html0 = urllib.request.urlopen(req0).read()
    html0 = sessions.get(start_url, headers=headers).text
    soup0 = BeautifulSoup(html0, features="html.parser")

    total_page = int(soup0.find('li', id='Page_End').find(
        "a")['href'].split('=')[-1])
    # total_page = 1

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

        contents = soup.find('div', class_="index_anchor").findAll(
            'div', class_="index_anchor-25")

        for content in contents:
            counts = contents.index(content)
            try:
                top_section = content.find('div', class_="index_anchor-25-top")
                try:
                    nickname = top_section.find("p").get_text().strip().replace(
                        "\n", "").replace("\t", "").replace("\r", "")
                except:
                    nickname = ""

                try:
                    profile_url = top_section.find("a")['href']
                except:
                    profile_url = ""

                ss = "正在爬取第%d页的第%d条信息，网址为%s" % (i, counts + 1, profile_url)
                print(ss)
                total_count += 1

                # Get Profile Detail Informations
                if profile_url is not None:
                    # profile_req = urllib.request.Request(profile_url)
                    # profile_req.add_header(
                    #     "User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
                    #     (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
                    # detail_html = urllib.request.urlopen(profile_req).read()
                    detail_html = sessions.get(
                        profile_url, headers=headers).text
                    detail_soup = BeautifulSoup(
                        detail_html, features="html.parser")
                    detail = detail_soup.find('div', class_="user-content")

                    basic_section = detail.find('div', class_="user-basic")
                    info_section = detail.find('div', class_="user-info")
                    contact_section = detail.find(
                        'div', class_="clickin-wrapper")

                    intro_section = detail_soup.find(
                        'div', class_="container").find(
                        'div', class_="content").find(
                        'div', class_="live-col").find(
                        'div', class_="col-list")

                    try:
                        avatar_url = basic_section.find(
                            'div', class_="avatar").find("img")['src']
                    except:
                        avatar_url = ""

                    try:
                        platname = basic_section.find(
                            'div', class_="motto").get_text().strip().replace(
                            "\n", "").replace("\t", "").replace("\r", "")
                    except:
                        platname = ""

                    # need login to fetch contacts
                    try:
                        contacts = contact_section.find('a').find(
                            "span").get_text().strip().replace(
                            "\n", "").replace("\t", "").replace("\r", "")
                    except:
                        contacts = ""

                    # fetch ajax follower data
                    # NOTE: change executable_path to your local path
                    driver = webdriver.PhantomJS(
                        executable_path='../phantomjs/bin/phantomjs')
                    driver.get(profile_url)
                    time.sleep(1)

                    try:
                        follower_count = driver.find_element_by_class_name(
                            'user-info').find_element_by_xpath(
                            "//span[@id='v_follower']").text
                    except:
                        follower_count = ''

                    infos = info_section.findAll('li')
                    try:
                        prize_on = infos[4].find(
                            'span').get_text().strip().replace(
                            "\n", "").replace("\t", "").replace("\r", "")
                    except:
                        prize_on = ''

                    try:
                        prize_off = infos[5].find(
                            'span').get_text().strip().replace(
                            "\n", "").replace("\t", "").replace("\r", "")
                    except:
                        prize_off = ''

                    try:
                        location = infos[3].find(
                            'span').get_text().strip().replace(
                            "\n", "").replace("\t", "").replace("\r", "")
                    except:
                        location = ''

                    tags = []
                    tags_section = infos[6].findAll('a')
                    for ts in tags_section:
                        try:
                            tag = ts.get_text().strip().replace(
                                "\n", "").replace("\t", "").replace("\r", "")
                        except:
                            tag = ''
                        if tag:
                            tags.append(tag)

                    try:
                        platform_url = infos[7].find(
                            'span').get_text().strip().replace(
                            "\n", "").replace("\t", "").replace("\r", "")
                    except:
                        platform_url = ''

                    intro = ''
                    intro_lines = intro_section.findAll('p')
                    for intro_line in intro_lines:
                        try:
                            context = intro_line.find(
                                'span').get_text().strip().replace(
                                "\n", "").replace("\t", "").replace("\r", "")
                        except:
                            context = ''
                        if context:
                            intro += context

                    csv_file.writerow([
                        nickname, profile_url, avatar_url, platname, contacts,
                        follower_count, prize_on, prize_off, location, tags,
                        platform_url, intro])
                    success_count += 1

                time.sleep(stop)

            except:
                error = "爬取第%d页的第%d条信息失败，网址为%s" % (i, counts + 1, url)
                print(error)
                failed_count += 1
                pass
    print('总共爬取{}条数据({}成功/{}失败)'.format(
        total_count, success_count, failed_count))


if __name__ == '__main__':
    username = input('请输入账号：')
    password = input('请输入密码：')
    cs = Authentication(username, password)
    cs.login()

    start_url = "http://www.zhaihehe.com/?/authentication_anchor/0/&p=1"
    index_url = "http://www.zhaihehe.com/?/authentication_anchor/0/&p="
    fetch_info(start_url, index_url)


file.close()
