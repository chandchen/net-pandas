# -*- coding: utf-8 -*-
import re
import requests
import w3lib
import csv

from parsel import Selector
from pprint import pprint

try:
    from urllib.parse import urljoin
except ImportError:
    from six.moves.urllib.parse import urljoin


file = open("douyin_data.csv", "w")

csv_file = csv.writer(file)
csv_file.writerow([
    'Nickname', 'Douyin_id', 'Avatar', 'Verify_info', 'Intro',
    'Location', 'Constellation', 'Following', 'Follower',
    'Like_count', 'Entry_count', 'Entry_likes'])


def fetch_data(url, proxy=None, rain_num=2):
    print("Loading:", url)
    heads = {
        'Accept': 'text/*, application/xml',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
                       AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.62 Mobile Safari/537.36',
        "X-Requested-With": "XMLHttpRequest",
        "Host": "www.douyin.com",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        html = requests.get(url, headers=heads).text
    except Exception as e:
        print("Loading Faild:", e.reason)
        html = None
        if rain_num > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return fetch_data(url, rain_num - 1)
    return html


def fetch_info(uid):
    url = "https://www.douyin.com/share/user/%s" % uid
    body = fetch_data(url)
    xbody = Selector(text=body)
    # item = dict()

    try:
        error_msg = xbody.xpath(
            "//div[@class='error-text']/p/text()").extract_first()
    except Exception as e:
        error_msg = ''
    if error_msg == '页面不见啦~':
        print('----------用户不存在！----------')
        return

    try:
        nickname = xbody.xpath(
            "//p[@class='nickname']/text()").extract_first()
    except:
        nickname = ''

    try:
        entry_count = xbody.xpath(
            "//div[@class='user-tab active tab get-list']/span").extract_first()
        entry_count = re.findall(r'>([\s\S]+?)<', entry_count)
        entry_count = jiexi(entry_count).strip()
    except:
        entry_count = ''

    try:
        entry_likes = xbody.xpath(
            "//div[@class='like-tab tab get-list']/span").extract_first()
        entry_likes = re.findall(r'>([\s\S]+?)<', entry_likes)
        entry_likes = jiexi(entry_likes).strip()
    except:
        entry_likes = ''

    try:
        douyin_id = xbody.xpath("//p[@class='shortid']").extract_first()
        douyin_id = re.findall(r'>([\s\S]+?)<', douyin_id)
        douyin_id = jiexi(douyin_id).replace(u"抖音ID：", '').strip()
    except:
        douyin_id = ''

    try:
        verify_info = xbody.xpath(
            "//span[@class='info']/text()").extract_first().strip()
    except Exception as e:
        verify_info = ''

    try:
        following = xbody.xpath(
            "//span[contains(@class,'focus block')]/span[@class='num']")\
            .extract_first()
        following = re.findall(r'>([\s\S]+?)<', following)
        following = jiexi(following)
    except:
        following = ''

    try:
        follower = xbody.xpath(
            "//span[contains(@class,'follower block')]/span[@class='num']")\
            .extract_first()
        follower = re.findall(r'>([\s\S]+?)<', follower)
        follower = jiexi(follower)
    except:
        follower = ''

    try:
        like_count = xbody.xpath(
            "//span[contains(@class,'liked-num block')]/span[@class='num']")\
            .extract_first()
        like_count = re.findall(r'>([\s\S]+?)<', like_count)
        like_count = jiexi(like_count)
    except:
        like_count = ''

    try:
        intro = xbody.xpath("//p[@class='signature']/text()").extract_first()
    except:
        intro = ''

    try:
        avatar = xbody.xpath("//img[@class='avatar']/@src").extract_first()
    except:
        avatar = ''

    try:
        location = xbody.xpath(
            "//span[@class='location']/text()").extract_first()
    except Exception as e:
        location = ''

    try:
        constellation = xbody.xpath(
            "//span[@class='constellation']/text()").extract_first()
    except Exception as e:
        constellation = ''

    # item['douyin_id'] = douyin_id
    # item['nickname'] = nickname
    # item["follower"] = follower
    # item["like_count"] = like_count
    # item["following"] = following
    # item['entry_count'] = entry_count
    # item['entry_likes'] = entry_likes
    # item['verify_info'] = verify_info
    # item['intro'] = intro
    # item['avatar'] = avatar
    # item['location'] = location
    # item['constellation'] = constellation
    # pprint(item)

    if douyin_id:
        csv_file.writerow([
            nickname, douyin_id, avatar, verify_info, intro, location,
            constellation, following, follower, like_count, entry_count,
            entry_likes])


def jiexi(lists):
    pat = {
        u"\ue60d": 0,
        u"\ue603": 0,
        u"\ue616": 0,
        u"\ue60e": 1,
        u"\ue618": 1,
        u"\ue602": 1,
        u"\ue605": 2,
        u"\ue610": 2,
        u"\ue617": 2,
        u"\ue611": 3,
        u"\ue604": 3,
        u"\ue61a": 3,
        u"\ue606": 4,
        u"\ue619": 4,
        u"\ue60c": 4,
        u"\ue60f": 5,
        u"\ue607": 5,
        u"\ue61b": 5,
        u"\ue61f": 6,
        u"\ue612": 6,
        u"\ue608": 6,
        u"\ue61c": 7,
        u"\ue60a": 7,
        u"\ue613": 7,
        u"\ue60b": 8,
        u"\ue61d": 8,
        u"\ue614": 8,
        u"\ue615": 9,
        u"\ue61e": 9,
        u"\ue609": 9,
        "w": "w",
        ".": "."
    }
    _li = list()
    for i in lists:
        if str(i).strip():
            i = i.replace(u'<i class="icon iconfont follow-num">', "").strip()
            i = i.replace(u'<i class="icon iconfont ">', "").strip()
            i = i.replace(u'<i class="icon iconfont tab-num">', "").strip()
            i = pat.get(i, i)
            _li.append(str(i))
    return "".join(_li)


if __name__ == '__main__':
    uids = [
        "57720812347", "93046013277", "72096309936", "60637177764",
        "69914084602", "72722865756", "58486060366", "95433824498",
        "77267568314", "52616983119", "61141281259", "58900737309"
    ]
    # uids = ["84990209480"]
    # for uid in uids:
    #     fetch_info(uid)

    for i in list(range(1, 100)):
        fetch_info(i)
    # fetch_info(50)

file.close()
