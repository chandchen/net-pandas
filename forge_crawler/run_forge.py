# -*- coding: utf-8 -*-
import requests
import json
import csv

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


def fetch_user_issue_list(state, assignee, author='', milestone='', label=''):
    if author:
        filter_url = "https://forge.channelfix.com/channelfix/channelfix/issues?\
            cope=all&utf8=%E2%9C%93&state={}&author_username={}&\
            assignee_username={}&milestone_title={}&label_name[]={}".format(
            state, author, assignee, milestone, label)
    else:
        filter_url = 'https://forge.channelfix.com/channelfix/channelfix/issues?\
            scope=all&utf8=%E2%9C%93&state={}&assignee_username={}'.format(
            state, assignee)

    html = sessions.get(filter_url, headers=headers).text
    soup = BeautifulSoup(html, features="html.parser")

    contents = soup.find(
        'ul', class_="issues-list").findAll('li', class_="issue")

    c_file = open(
        "forge_crawler/search_results/search_results_[{}].csv".format(
            assignee), "w")
    search_file = csv.writer(c_file)
    search_file.writerow(csv_readers)

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

        if link:
            detail_url = 'https://forge.channelfix.com' + link
            html0 = sessions.get(detail_url, headers=headers).text
            soup0 = BeautifulSoup(html0, features="html.parser")
            contents0 = soup0.find(
                'ul', class_="main-notes-list").findAll(
                'li', class_="timeline-entry")
            for content0 in contents0:
                try:
                    owner = content0.find(
                        'span', class_="note-header-author-name").get_text()
                    action = content0.find(
                        'span', class_="system-note-message").find(
                        'span').get_text()
                    action_info = {
                        'owner': owner,
                        'action': action
                    }
                except Exception as e:
                    action_info = {}

        search_file.writerow(
            [number, title, author, link, labels, action_info])


if __name__ == '__main__':
    try:
        email = account_info['email']
        password = account_info['password']
    except Exception as e:
        email = input('请输入邮箱：')
        password = input('请输入密码：')
    cs = Authentication(email, password)
    cs.login()

    keywords = {}

    state = input('状态(opened/closed/all): ')
    if state:
        keywords['state'] = state
    else:
        print('状态不能为空！')
    assignee = input('被指派人(username): ')
    if assignee:
        keywords['assignee'] = assignee
    else:
        print('指派人不能为空！')
    author = input('创建人(username): ')
    if author:
        keywords['author'] = author
    milestone = input('里程碑(空格用%20)： ')
    if milestone:
        keywords['milestone'] = milestone
    label = input('标签(Bug/空格用%20)： ')
    if label:
        keywords['label'] = label

    fetch_user_issue_list(**keywords)
