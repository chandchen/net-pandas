# -*- coding: utf-8 -*-
import csv
import time


csv_headers = ['标题', '作者', '简介', '评分', '评分人数', '字数', '分类', '封面']
# file_path = 'douban/results/1-100(2000)/books_[{}-{}].csv'
file_paths = [
    'douban/results/701-1000/books_[801-900].csv',
    'douban/results/701-1000/books_[901-1000].csv',
]

if __name__ == '__main__':
    c_file = open(
        "douban/results/books_[801-1000].csv".format(
            time.strftime("%Y%m%d%H%M")), "w")
    search_file = csv.writer(c_file)
    search_file.writerow(csv_headers)

    # start = 1
    # end = 10
    # for i in range(start, end + 1):
    for file_path in file_paths:
        print(file_path)

        with open(file_path) as csvfile:
            csv_readers = csv.reader(csvfile)
            next(csv_readers)
            count = 1
            for row in csv_readers:
                rating = row[3]
                if rating == '暂无评分':
                    row[3] = 0
                rating_amount = row[4]
                if rating_amount == 'N/A':
                    row[4] = 0
                word_count = str(row[5]).strip()
                if '万' in word_count:
                    string = word_count.replace('万', '')
                    row[5] = float(string) * 10000
                elif '页' in word_count:
                    string = word_count.replace(
                        '共', '').replace('页', '').strip()
                    row[5] = -int(string)
                else:
                    pass

                search_file.writerow(row)

                title = row[0].replace('/', '')
                count += 1

        # start += 10
        # end += 10
