# -*- coding: utf-8 -*-
from selenium import webdriver


def fetch_data(driver, target_url):
    driver.get(target_url)
    driver.implicitly_wait(3)
    video = driver.find_element_by_id('theVideo').get_attribute("src")
    image_str = driver.find_element_by_id('videoPoster').get_attribute("style")
    user = driver.find_element_by_id('videoUser')
    avatar_str = user.find_element_by_class_name(
        'user-avator').get_attribute("style")
    username = user.find_element_by_class_name('user-name').text

    image = image_str.split('"')[1]
    avatar = avatar_str.split('"')[1]

    return {
        'video': video,
        'image': image,
        'name': username,
        'avatar': avatar,
    }


if __name__ == '__main__':
    target_url = 'https://v.douyin.com/EEx8fs/'

    mobileEmulation = {'deviceName': 'iPhone 6/7/8'}

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) \
        AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 \
        Safari/601.1"')
    options.add_experimental_option('mobileEmulation', mobileEmulation)

    driver = webdriver.Chrome(
        executable_path='../chromedriver', chrome_options=options)

    fetch_data(driver, target_url)

    driver.quit()
