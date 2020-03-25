# -*- coding: utf-8 -*-
import requests
import csv


file_path = 'douban/results/books_[71-80]_202003251735.csv'


def download_image(image_url, count, title):
    r = requests.get(image_url)
    with open('douban/results/cover_[71-80]/{}-{}.jpg'.format(
            count, title), 'wb') as f:
        f.write(r.content)


if __name__ == '__main__':
    with open(file_path) as csvfile:
        csv_readers = csv.reader(csvfile)
        next(csv_readers)
        count = 1
        for row in csv_readers:
            title = row[0]
            image_url = row[7]
            print(image_url)

            download_image(image_url, count, title)
            count += 1
