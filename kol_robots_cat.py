# -*- coding: utf-8 -*-
import csv
import requests
import json
import xlrd
import pytesseract
import string
import os

from bs4 import BeautifulSoup
from parsel import Selector
from PIL import Image
from io import BytesIO


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


def fetch_category():

    c_file = open("category.csv", "w")
    category_file = csv.writer(c_file)
    category_file.writerow(['ID', 'Category Name'])

    total_page = 71

    for i in list(range(1, total_page + 1)):
        category_url = "https://kolranking.com/douyin/users/category/{}".format(i)
        print('Loading: ', category_url)
        html = sessions.get(category_url, headers=headers).text
        soup = BeautifulSoup(html, features="html.parser")

        category_name = soup.find('head').find(
            'title').get_text().strip().replace('KOL排行榜', '')
        if category_name == 'TooBigData':
            sign = input('请打开网页进行验证(Y/N):')
            if sign.lower() == 'y':
                html = sessions.get(category_url, headers=headers).text
                soup = BeautifulSoup(html, features="html.parser")
                category_name = soup.find('head').find(
                    'title').get_text().strip().replace('KOL排行榜', '')
            else:
                return
        category_file.writerow([i, category_name])

    c_file.close()


def download_category_specified(category_id, top, bottom):
    """ Download category specified data for kol ranking """

    category_url = "https://kolranking.com/douyin/users/category/{}".format(
        category_id)

    dirlis_new = "kol_demo/kol_category_{}".format(category_id)
    if not os.path.exists(dirlis_new):
        os.makedirs(dirlis_new)

    file = open("data_collection/kol_category_{}.csv".format(category_id), "w")

    csv_file = csv.writer(file)
    csv_file.writerow(csv_readers)

    for i in list(range(top, bottom)):
        suffix = "?order=follower_count&ot=DESC&page={}&type=download".format(
            i)
        url = category_url + suffix
        file_name = "kol_demo/kol_category_{}/category_{}_page_{}.xlsx".format(
            category_id, category_id, i)

        try:
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


# def extract_image(image_file):
#     # tree = lxml.html.fromstring(html)
#     # img_data = tree.cssselect('div#recaptcha img')[0].get('src')
#     # img_data = img_data.partition(',')[-1]
#     # #open('test_.png', 'wb').write(data.decode('base64'))
#     # ##进行base64解码，回到最初的二进制
#     # binary_img_data = img_data.decode('base64')
#     # ##要想加载该图片，PIL需要对一个类似文件的接口，在传给Image类，我们又使用ByteIO对这个二进制进行封装
#     # file_like = BytesIO(binary_img_data)
#     img0 = Image.open(image_file)
#     return img0


# def ocr(img):
#     # threshold the image to ignore background and keep text
#     # img.save('capcha_originl.png')
#     gray = img.convert('L')
#     # gray.save('captcha_greyscale.png')
#     bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
#     # bw.save('captcha_threshold.png')
#     # print bw
#     word = pytesseract.image_to_string(bw)
#     ascii_word = ''.join(c for c in word if c in string.letters).lower()
#     print(ascii_word)
#     return ascii_word


if __name__ == '__main__':
    try:
        email = account_info['email']
        password = account_info['password']
    except:
        email = input('请输入邮箱：')
        password = input('请输入密码：')
    cs = Authentication(email, password)
    cs.login()

    category_id = int(input('请输入需要获取的分类ID:'))
    top = int(input('请输入起始页码：'))
    bottom = int(input('请输入结束页码：'))
    # top = 1
    # bottom = 10

    # fetch_category()

    download_category_specified(category_id, top, bottom)

    # image = "./default.png"
    # img_data = extract_image(image)
    # captcha = ocr(img_data)
