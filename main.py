# Створити програму яка парсить HTML сторінку залежно від параметрів виклику, виклик формату:
# python main.py -url https://www.google.com.ua/
# Якщо не вказано шлях зробити запит у користувача
# Перевірка чи валідна лінка
# Знайти всі лінки на сторінці(Перевірити що лінка валідна requests.get (status code == 200))
# Посилання у яких статус код 200 зберегти в окремий файл , всі інші у файл з назвою broken_links.txt

import argparse
import re
import requests


class LinkParser:
    def __init__(self):
        self.valid_links = []
        self.broken_links = []

    def pars_link(self, param):
        # url = "https://www.google.com.ua/"
        response = requests.get(param)
        pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
        links = re.findall(pattern, response.text)

        for link in links:
            '''якщо  посилання link не починається з 'https://' тоді до базової url
                додається відносний шлях link для створення повної URL-адреси.
                Результат зберігається в змінну link_url.'''
            if not link.startswith('https://'):
                link_url = param + link
            else:
                link_url = link

            link_response = requests.get(link_url)
            if link_response.status_code == 200:
                self.valid_links.append(link_url)
            else:
                self.broken_links.append(link_url)

    def save_links(self):
        with open("valid_links.txt", "w") as file:
            for link in self.valid_links:
                file.write(link + "\n")

        with open("broken_links.txt", "w") as file:
            for link in self.broken_links:
                file.write(link + "\n")

    def user_input(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-url', type=str, help='Please set URL')
        args = parser.parse_args()

        if args.url:
            self.pars_link(args.url)
        else:
            url = input('Please set URL for parsing: ')
            self.pars_link(url)

        self.save_links()


link_parser = LinkParser()
link_parser.user_input()
