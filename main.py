# Створити програму яка парсить HTML сторінку залежно від параметрів виклику, виклик формату:
# python main.py -url www.google.com
# Якщо не вказано шлях зробити запит у користувача
# Перевірка чи валідна лінка
# Знайти всі лінки на сторінці(Перевірити що лінка валідна requests.get (status code == 200))
# Посилання у яких статус код 200 зберегти в окремий файл , всі інші у файл з назвою broken_links.txt

import argparse
import re
from pprint import pprint

import requests

#
# class UrlAnalyzer:
#
#     def __new__(cls, *args, **kwargs):
#         analyzer = super().__new__(cls)
#         if not args and not kwargs:
#             analyzer.url = cls.user_input
#         return analyzer
#
#     def __init__(self, url=None):
#         if url:
#             self.url = url
#         self.link_analyzer = LinkAnalyzer(self.url)
#
#     @staticmethod
#     def user_input():
#         parse = argparse.ArgumentParser()
#         parse.add_argument('-url', type=str, help='Please se url for parsing')
#         args = parse.parse_args()
#         if args.url:
#             return args.url
#         else:
#             url = input('Please set url for parsing')
#             return url
#
#     def info_from_link(self, url):
#         self.link_analyzer.check_link(url)
#
#     def get_links_from_url(self, url) -> list:
#         return re.findall('', url)
#
#
# class LinkAnalyzer:
#
#     def __init__(self, url):
#         self.url = url
#
#     def check_link(self, link):
#         pass
#
#     def check_links(self, links):
#         for link in links:
#             self.check_link(link)
#
#
# if __name__ == "__main__":
#     url = UrlAnalyzer('www.google.com')
#     url_1 = UrlAnalyzer()
#     print(url_1)


# parse = argparse.ArgumentParser()
# parse.add_argument('-url', type=str, help='Please se url for parsing')
# args = parse.parse_args()
# /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/

url = "https://www.google.com.ua/"
response = requests.get(url)

pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
links = re.findall(pattern, response.text)

valid_links = []
broken_links = []

#------------- html
for link in links:
    '''якщо  посилання link не починається з 'https://' тоді до базової url
        додається відносний шлях link для створення повної URL-адреси.
        Результат зберігається в змінну link_url.'''
    if not link.startswith('https://'):
        link_url = url + link
    else:
        link_url = link

    link_response = requests.get(link_url)
    if link_response.status_code == 200:
        valid_links.append(link_url)
    else:
        broken_links.append(link_url)

with open("valid_links.txt", "w") as file:
    for link in valid_links:
        file.write(link + "\n")


with open("broken_links.txt", "w") as file:
    for link in broken_links:
        file.write(link + "\n")

#----------------- pdf
