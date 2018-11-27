# -*- coding: utf-8 -*-
import requests
import json
import csv
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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


def update_forge_data(driver):
    url = 'https://forge.channelfix.com/channelfix/channelfix/issues/1118'
    # html = sessions.get(url, headers=headers).text
    # soup = BeautifulSoup(html, features="html.parser")
    # contents = soup.find(
    #     'ul', class_="main-notes-list")

    # driver = webdriver.PhantomJS(
    #     executable_path='../phantomjs/bin/phantomjs')
    driver.get(url)
    time.sleep(5)

    try:
        contents = driver.find_element_by_xpath('//*[@id="content-body"]/div[2]/div[1]/div[1]/div/div[1]/h2')
    except:
        contents = ''

    print('>>', contents)

    # for content in contents:
    #     print(">>?????")
    # contents = soup.find(
    #     'ul', class_="main-notes-list").findAll(
    #     'li', class_="timeline-entry")
    # for content in contents:
    #     try:
    #         name = content.find(
    #             'span', class_="note-header-author-name").get_text().replace(
    #             '\n', '').replace('/', '')
    #     except Exception as e:
    #         name = ''
    #     print('>>>', name)


def webdriver_login(driver, account, passwd):
    driver.find_element_by_id('user_login').send_keys(account)
    driver.find_element_by_id('user_password').send_keys(passwd)
    driver.find_element_by_class_name('btn-save').click()
    # time.sleep(2)
    # title = driver.find_element_by_class_name('shortcuts-activity').text
    # try:
    #     assert title == 'Your projects'
    #     print('>>>>>yead!!!!')
    #     return 'Success'
    # except AssertionError as e:
    #     return 'Failed!'

    url = 'https://forge.channelfix.com/channelfix/channelfix/issues/1118'
    driver.get(url)
    # time.sleep(20)
    driver.implicitly_wait(10)

    # try:
    #     WebDriverWait(driver, 20, 0.5)
    #     driver.save_screenshot('3.png')
    # finally:
    #     driver.close()

    # try:
    #     contents = driver.find_element_by_xpath(
    #         '//*[@id="note_68102"]/div').text
    # except:
    #     contents = ''

    # print('>>', contents)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="notes-list"]')))

    ul = driver.find_element_by_id('notes-list')
    contents = ul.find_elements_by_xpath('li')
    for content in contents:
        try:
            username = content.find_element_by_class_name(
                'note-headline-light').text
            print(username)
        except:
            pass

        try:
            action = content.find_element_by_class_name(
                'system-note-message').find_element_by_xpath('span').text
            print(action)
        except:
            pass

        try:
            time = content.find_element_by_tag_name(
                'time').get_attribute('data-original-title')
            print(time)
        except:
            pass


if __name__ == '__main__':
    try:
        email = account_info['email']
        password = account_info['password']
    except Exception as e:
        email = input('请输入邮箱：')
        password = input('请输入密码：')
    # cs = Authentication(email, password)
    # cs.login()

    # keywords = {}

    # state = input('状态(opened/closed/all): ')
    # if state:
    #     keywords['state'] = state
    # else:
    #     print('状态不能为空！')
    # assignee = input('被指派人(username): ')
    # if assignee:
    #     keywords['assignee'] = assignee
    # else:
    #     print('指派人不能为空！')
    # author = input('创建人(username): ')
    # if author:
    #     keywords['author'] = author
    # milestone = input('里程碑(空格用%20)： ')
    # if milestone:
    #     keywords['milestone'] = milestone
    # label = input('标签(Bug/空格用%20)： ')
    # if label:
    #     keywords['label'] = label

    # fetch_user_issue_list(**keywords)
    login_url = 'https://forge.channelfix.com/users/sign_in'
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap['phantomjs.page.settings.userAgent'] = (
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) \
    #     Gecko/20100101 Firefox/25.0 ')
    # driver = webdriver.PhantomJS(
    #     executable_path='../phantomjs/bin/phantomjs',
    #     desired_capabilities=dcap)

    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument(
    #     'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) \
    #     AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 \
    #     Safari/601.1"')
    # driver = webdriver.Chrome(
    #     executable_path='/usr/bin/chromedriver', chrome_options=options)

    driver = webdriver.Chrome()
    driver.get(login_url)
    driver.maximize_window()
    webdriver_login(driver, email, password)
    # update_forge_data(driver)
    driver.quit()
