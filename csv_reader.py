# -*- coding: utf-8 -*-
import csv


def csv_reader(reader_path, writer_path):

    file = open(writer_path, "w")
    csv_file = csv.writer(file)
    csv_file.writerow([
        'UID', '昵称', '性别', '个人签名', '城市', '生日', '星座', '粉丝数', '获赞数',
        '视频数', '采集时间'])

    filters = ["微信", "微", "商务", "合作", "微博", "联系", "邮箱",
               "搜", "VX", "vx", "Vx", "v", "W", "WB", "We ibo",
               "wb", "vb", "QQ", "Q", "qq", "q", "tb", "V博", "❤"]

    with open(reader_path) as csvfile:
        csv_readers = csv.reader(csvfile)
        next(csv_readers)
        count = 0
        for row in csv_readers:
            for word in filters:
                if word in row[3]:
                    count += 1
                    print("Find No.", count)
                    csv_file.writerow(row)
                    break
    file.close()


if __name__ == '__main__':
    category_ids = [1, 6, 7, 10, 13, 14, 17, 22, 56, 63]
    for i in category_ids:
        reader_file_path = "kol_data/kol_data_category_{}.csv".format(i)
        writer_file_path = "kol_data/kol_data_category_{}_filter.csv".format(i)
        csv_reader(reader_file_path, writer_file_path)
    print('Done!')
