# Створити програму яка парсить HTML сторінку або pdf  залежно від параметрів виклику, виклик формату:
# python main.py -url https://www.google.com.ua/
# Якщо не вказано шлях зробити запит у користувача
# Знайти всі лінки на сторінці(Перевірити що лінка валідна requests.get (status code == 200))
# Посилання у яких статус код 200 зберегти в окремий файл , всі інші у файл з назвою broken_links.txt

import argparse
import re
import requests
import PyPDF2
import logging


class LinkParser:
    def __init__(self):
        self.valid_links = []
        self.broken_links = []

    logging.basicConfig(level=logging.INFO, filename='my_log.log', filemode='w',
                        format="%(asctime)s %(levelname)s %(message)s")

    def pars_link(self, param):
        logging.info(f"Parsing links from {param}")

        response = requests.get(param)
        pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
        links = re.findall(pattern, response.text)

        for link in links:
            if not link.startswith('https://'):
                link_url = param + link
            else:
                link_url = link

            link_response = requests.get(link_url)
            if link_response.status_code == 200:
                self.valid_links.append(link_url)
                logging.info(f"Valid link: {link_url}")
            else:
                self.broken_links.append(link_url)
                logging.error(f"Broken link: {link_url}")

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
        parser.add_argument('-pdf', type=str, help='Please set pdf')
        args = parser.parse_args()

        if args.url:
            self.pars_link(args.url)
        elif args.pdf:
            self.find_links_in_pdf(args.pdf)
        else:
            pars = input('Please set URL/pdf for parsing: ')
            if pars.endswith('.pdf'):
                self.find_links_in_pdf(pars)
            else:
                self.pars_link(pars)

        self.save_links()

    def find_links_in_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            num_pages = len(pdf.pages)

            links = []

            for page_number in range(num_pages):
                page = pdf.pages[page_number]
                page_text = page.extract_text()
                pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                matches = re.findall(pattern, page_text)

                links.extend(matches)

            for link in links:
                try:
                    link_response = requests.get(link)
                    if link_response.status_code == 200:
                        self.valid_links.append(link)
                    else:
                        self.broken_links.append(link)
                except requests.exceptions.RequestException as e:
                    print(f"Error occurred while accessing {link}: {e}")


link_parser = LinkParser()
link_parser.user_input()
