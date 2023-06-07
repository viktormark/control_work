from main import LinkParser, Save
import pytest


#
class TestParsePdf:

    def setup(self):
        self.parser = LinkParser()

    def test_parse_valid_links_in_list(self):
        url = "../1.pdf"

        self.parser.find_links_in_pdf(url)

        assert len(self.parser.valid_links) > 0

    def test_parse_invalid_links_in_list(self):
        url = "../1.pdf"

        self.parser.find_links_in_pdf(url)

        assert len(self.parser.broken_links) > 0

    def test_save_valid_links_in_file(self):
        url = "../1.pdf"

        expected_valid_links = [
            "https://lms.ithillel.ua/",
            "https://pypi.org/project/lorem/",
            "https://gorest.co.in/",
            "https://medium.com/",
            "https://metanit.com/python/tutorial/6.5.php",
        ]
        self.parser.find_links_in_pdf(url)

        link_saver = Save(self.parser.valid_links, [])
        link_saver.save_links()

        with open('valid_links.txt', 'r') as file:
            file_contents = file.read().splitlines()

        assert file_contents == expected_valid_links

    def test_save_invalid_links_in_file(self):
        url = "../1.pdf"

        expected_invalid_links = [
            "https://translater",
            "https://uk.lipsum.cor/",
            "https://www",
            "https://www",
            "https://docs.pytest.org/en/7.3.x/).",
            "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D",
            "https://www",
            "https://www",
            "https://githurbar",
            "https://www",
        ]
        self.parser.find_links_in_pdf(url)

        link_saver = Save([], self.parser.broken_links)
        link_saver.save_links()

        with open('broken_links.txt', 'r') as file:
            file_contents = file.read().splitlines()

        assert file_contents == expected_invalid_links

    def test_parse_pdf_with_invalid_link(self):
        pdf_file = url = "../8.pdf"

        with pytest.raises(FileNotFoundError):
            self.parser.find_links_in_pdf(pdf_file)

        assert len(self.parser.valid_links) == 0
        assert len(self.parser.broken_links) == 0


class TestParseUrl:
    def setup(self):
        self.parser = LinkParser()

    def test_parse_valid_links_in_list_url(self):
        url = "https://www.google.com.ua/"

        self.parser.pars_link(url)

        assert len(self.parser.valid_links) > 0

    def test_parse_invalid_links_in_list_url(self):
        url = "https://www.google.com.ua/"

        self.parser.pars_link(url)

        assert len(self.parser.broken_links) > 0

    def test_save_valid_links_in_file_url(self):
        url = "https://www.google.com.ua/"

        expected_valid_links = [
            "https://www.google.com.ua/imghp?hl=uk&tab=wi",
            "https://maps.google.com.ua/maps?hl=uk&tab=wl",
            "https://play.google.com/?hl=uk&tab=w8",
            "https://www.youtube.com/?tab=w1",
            "https://news.google.com/?tab=wn",
            "https://mail.google.com/mail/?tab=wm",
            "https://drive.google.com/?tab=wo",
            "https://www.google.com.ua/intl/uk/about/products?tab=wh",
            "https://www.google.com.ua//preferences?hl=uk",
            "https://accounts.google.com/ServiceLogin?hl=uk&passive=true&continue=https://www.google.com.ua/&ec=GAZAAQ",
            "https://www.google.com.ua//advanced_search?hl=uk&amp;authuser=0",
            "https://www.google.com.ua//intl/uk/ads/",
            "https://www.google.com.ua//intl/uk/about.html",
            "https://www.google.com.ua/setprefdomain?prefdom=US&amp;sig=K_hsAe-RCWR6yN2-TwUhFxuuNls7c%3D",
        ]

        self.parser.pars_link(url)

        link_saver = Save(self.parser.valid_links, [])
        link_saver.save_links()

        with open("valid_links.txt", "r") as file:
            file_contents = file.read().splitlines()

        assert file_contents == expected_valid_links

    def test_save_invalid_links_in_file(self):
        url = "https://www.google.com.ua/"

        expected_invalid_links = [
            "https://www.google.com.ua/http://www.google.com.ua/history/optout?hl=uk",
            "https://www.google.com.ua/http://www.google.com.ua/intl/uk/services/",
        ]

        self.parser.pars_link(url)

        link_saver = Save([], self.parser.broken_links)
        link_saver.save_links()

        with open("broken_links.txt", "r") as file:
            file_contents = file.read().splitlines()

        assert file_contents == expected_invalid_links
