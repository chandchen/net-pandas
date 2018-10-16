# -*- coding: utf-8 -*-
import csv
import requests
import json
import xlrd
import os

from bs4 import BeautifulSoup


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36",
    'Referer': 'https://kolranking.com/settings/account'
}

csv_readers = ['UID', '昵称', '性别', '个人签名', '城市', '生日', '星座',
               '粉丝数', '获赞数', '视频数', '采集时间']

account_info = json.load(open('kol_account.json'))

dirlis_new = "data_collection"
if not os.path.exists(dirlis_new):
    os.mkdir(dirlis_new)

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


def download_user_info(top, bottom):
    file = open("data_collection/kol_ranking_data.csv", "w")

    csv_file = csv.writer(file)
    csv_file.writerow(csv_readers)

    for i in list(range(top, bottom)):
        url = "https://kolranking.com/home?order=follower_count&ot=\
               DESC&page={}&type=download".format(i)
        dirlis_new = "kol_demo/kol_ranking_{}_{}".format(top, bottom - 1)
        if not os.path.exists(dirlis_new):
            os.makedirs(dirlis_new)

        file_name = dirlis_new + "/kol_demo_page_{}.xlsx".format(i)
        try:
            target = sessions.get(url, headers=headers)
            with open(file_name, "wb") as code:
                code.write(target.content)
            data = xlrd.open_workbook(file_name).sheets()[0]
            for c in list(range(1, 11)):
                print('正在获取第{}页的第{}条数据'.format(i, c))
                csv_file.writerow(data.row_values(c))
        except:
            sign = input('请打开网页进行验证(Y/N):')

            if sign == 'y':
                target = sessions.get(url, headers=headers)
                with open(file_name, "wb") as code:
                    code.write(target.content)
                data = xlrd.open_workbook(file_name).sheets()[0]
                for c in list(range(1, 11)):
                    try:
                        print('正在获取第{}页的第{}条数据'.format(i, c))
                        csv_file.writerow(data.row_values(c))
                    except:
                        print('获取第{}页的第{}条数据失败！'.format(i, c))
                        break
            else:
                break
    file.close()


if __name__ == '__main__':
    try:
        email = account_info['email']
        password = account_info['password']
    except:
        email = input('请输入邮箱：')
        password = input('请输入密码：')
    cs = Authentication(email, password)
    cs.login()

    top = int(input('请输入起始页码：'))
    bottom = int(input('请输入结束页码：'))
    # top = 1
    # bottom = 10

    download_user_info(top, bottom)
