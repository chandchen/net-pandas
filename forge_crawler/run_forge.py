# -*- coding: utf-8 -*-
import requests
import json

from bs4 import BeautifulSoup


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36",
    'Referer': 'https://forge.channelfix.com/'
}

csv_readers = ['Issue', 'Title', 'Author', 'Link', 'Labels']

account_info = json.load(open('forge_crawler/accounts.json'))

sessions = requests.Session()


class Authentication:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.login_url = 'https://forge.channelfix.com/users/sign_in'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                          AppleWebKit/537.36 (KHTML, like Gecko) \
                          Chrome/59.0.3071.115 Safari/537.36",
            'Referer': 'https://forge.channelfix.com/'
        }

    def login(self):
        html = sessions.get(self.login_url, headers=self.headers).text
        soup = BeautifulSoup(html, features="html.parser")
        token = soup.select('input[name="authenticity_token"]')[0].get('value')
        data = {
            'user[login]': self.email,
            'user[password]': self.password,
            'authenticity_token': token
        }
        r = sessions.post(self.login_url, data=data)
        if r.status_code == 200:
            print('登陆成功！')
        else:
            print('登陆失败！')


def fetch_user_issue_list(state, username):
    filter_url = 'https://forge.channelfix.com/channelfix/channelfix/issues?\
        scope=all&utf8=%E2%9C%93&state={}&assignee_username={}'.format(
        state, username)

    html = sessions.get(filter_url, headers=headers).text
    soup = BeautifulSoup(html, features="html.parser")

    contents = soup.find(
        'ul', class_="issues-list").findAll('li', class_="issue")
    for content in contents:
        counts = contents.index(content)
        print('正在获取第1页第{}条数据'.format(counts + 1))
        try:
            title = content.find('span', class_="issue-title-text").get_text()
        except Exception as e:
            title = ''
        try:
            link = content.find(
                'span', class_="issue-title-text").find('a')['href']
        except Exception as e:
            link = ''
        try:
            number = content.find(
                'span', class_="issuable-reference").get_text()
        except Exception as e:
            number = ''
        try:
            author = content.find('span', class_="author").get_text()
        except Exception as e:
            author = ''

        labels = []
        try:
            xlabels = content.findAll('a', class_="label-link")
            if xlabels:
                for label in xlabels:
                    labels.append(label.find('span').get_text())
        except Exception as e:
            labels = []

        infos = {
            'title': title,
            'link': link,
            'number': number,
            'author': author,
            'labels': labels
        }

        print('>>>', infos)


if __name__ == '__main__':
    try:
        email = account_info['email']
        password = account_info['password']
    except Exception as e:
        email = input('请输入邮箱：')
        password = input('请输入密码：')
    cs = Authentication(email, password)
    cs.login()

    username = input('请输入要获取的用户名：')
    state = input('请输入要获取的状态：')

    fetch_user_issue_list(state, username)
