# -*- coding: utf-8 -*-
import time
import csv

from selenium import webdriver


csv_readers = ['标题', '作者', '简介', '评分', '评分人数', '字数', '分类', '封面']


def fetch_data(driver, target_url, start_page=1, end_page=10):
    c_file = open(
        "douban/results/books_[{}-{}]_{}.csv".format(
            start_page, end_page, time.strftime("%Y%m%d%H%M")), "w")
    search_file = csv.writer(c_file)
    search_file.writerow(csv_readers)

    for page in range(start_page, end_page + 1):
        driver.get(target_url.format(page))
        driver.implicitly_wait(10)
        ul = driver.find_element_by_xpath('//div[@class="section-works"]/ul')
        lis = ul.find_elements_by_xpath('li')

        for li in lis:
            counts = lis.index(li)
            print('正在获取第{}页第{}条数据'.format(page, counts + 1))
            title = li.find_element_by_class_name('title').text
            author = li.find_element_by_class_name('author').text
            intro = li.find_element_by_class_name('intro ').text
            extra_info = li.find_element_by_class_name('extra-info')

            try:
                score = extra_info.find_element_by_class_name('score').text
                amount = extra_info.find_element_by_class_name(
                    'amount').text.replace(' 评分', '')
            except:
                score = '暂无评分'
                amount = 'N/A'

            try:
                kind = extra_info.find_element_by_class_name('kind-link').text
            except:
                kind = '暂无分类'

            try:
                extra_info_str = extra_info.text
                start_index = extra_info_str.find('约')
                end_index = extra_info_str.find('字')
                words = extra_info_str[start_index + 2:end_index]
            except:
                words = '未知字数'

            cover = li.find_element_by_class_name(
                'cover').find_element_by_tag_name('img').get_attribute("src")

            search_file.writerow(
                [title, author, intro, score, amount, words, kind, cover])


if __name__ == '__main__':
    target_url = 'https://read.douban.com/category?page={}&kind=1'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) \
        AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 \
        Safari/601.1"')
    driver = webdriver.Chrome(
        executable_path='../chromedriver', chrome_options=options)

    fetch_data(driver, target_url, 71, 80)

    driver.quit()
