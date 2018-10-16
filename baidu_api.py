import pytesseract
import string
import json

from aip import AipOcr
from PIL import Image

account_info = json.load(open('kol_account.json'))

config = {
    'appId': account_info['appId'],
    'apiKey': account_info['apiKey'],
    'secretKey': account_info['secretKey']
}
client = AipOcr(**config)


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    image = get_file_content(image_path)
    result = client.basicAccurate(image)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])


def extract_image(image_file):
    img = Image.open(image_file)
    gray = img.convert('L')
    gray.save('captcha_greyscale.png')


# def ocr(img):
#     # threshold the image to ignore background and keep text
#     # img.save('capcha_originl.png')
#     gray = img.convert('L')
#     # gray.save('captcha_greyscale.png')
#     # bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
#     # bw.save('captcha_threshold.png')
#     # print bw
#     word = pytesseract.image_to_string(gray)
#     ascii_word = ''.join(c for c in word if c in string.letters).lower()
#     print(ascii_word)
#     return ascii_word


if __name__ == '__main__':
    image = 'default.png'
    image_data = extract_image(image)
    print(img_to_str('captcha_greyscale.png'))
