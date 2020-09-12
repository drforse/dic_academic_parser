import typing

import requests
from urlpath import URL
from bs4 import BeautifulSoup, Tag

from .types import Dic, Word, SearchResult
from .exceptions import *


class Parser:
    def __init__(self, dic: Dic):
        self.dic: Dic = dic
        if dic.dic_type == 'nsf':
            self.base_uri = f'https://dic.academic.ru/dic.nsf/{self.dic.id}'
        elif dic.dic_type == 'subdomain':
            self.base_uri = f'https://{self.dic.id}.academic.ru'
        else:
            raise DicTypeNotSupported(dic.dic_type)

    def get_word(self, id: int) -> Word:
        """get Word object by word's id

        Attributes:
            id (int): word's id, you can get in in Parser.search_all method
        """
        url = f'{self.base_uri}/{id}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        _, title = self._get_title(soup)
        description_html, description = self._get_description(soup)
        images = self._get_description_images_uris(soup)
        plain_html = description_html
        self.dic.title = self._get_dic_title_by_word_soup(soup)
        return Word(title, description, images, plain_html, url, self.dic)

    @classmethod
    def search_all(cls, query: str) -> typing.List[SearchResult]:
        """search for all results by a query

        Attributes:
            query (str): query for search (for ex.: "Слово")
        """
        results = []
        uri = f'https://academic.ru/searchall.php?SWord={query}'
        r = requests.get(uri)
        soup = BeautifulSoup(r.content, 'lxml')
        found_articles = soup.find('ul', {'class': 'terms-list', 'id': 'found_articles'})
        for art_tag in found_articles.find_all('li'):
            uri = URL(art_tag.a.attrs['href'])
            if not uri.parts[-1].isdigit():
                uri = uri.parent
            id = int(uri.parts[-1])
            dic = cls._get_dic_from_uri(uri)
            dic.title = art_tag.find('p', {'class': 'src'}).get_text()
            word = art_tag.a.get_text()
            short_description = art_tag.get_text()
            results.append(SearchResult(id, word, short_description, dic))
        return results

    @staticmethod
    def get_dic_title(dic: Dic) -> str:
        """get dic title on page of the dic

        Attributes:
            dic (Dic): Dic object
        """
        if dic.title:
            return dic.title
        if dic.dic_type == 'nsf':
            url = f'https://dic.academic.ru/contents.nsf/{dic.id}'
        elif dic.dic_type == 'subdomain':
            url = f'https://{dic.id}.academic.ru'
        else:
            raise DicTypeNotSupported(dic.dic_type)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        title = soup.find('title')
        return title.get_text()

    @staticmethod
    def _get_title(soup: BeautifulSoup) -> tuple:
        tag = soup.find('dt', {'class': 'term', 'itemprop': 'title'})
        title = tag.get_text()
        plain_html = str(tag)
        return plain_html, title

    @classmethod
    def _get_description(cls, soup: BeautifulSoup) -> tuple:
        tag = cls._get_description_tag(soup)
        text = ''

        last_img_num = 0
        divs = tag.find_all('div')
        if not divs:
            return str(tag), tag.get_text()
        plain_html = str(tag)
        for div in divs:
            if 'itemtype' in div.attrs:
                continue
            img = div.find('img')
            if img:
                last_img_num += 1
                text += f'\n\n       Картинка №{last_img_num}'
                plain_html = plain_html.replace(str(img.attrs['src']),
                                                f'https://literary_terms.academic.ru/{img.attrs["src"]}')

            text += f'\n{div.get_text()}'
        return plain_html, text

    def _get_description_images_uris(self, soup: BeautifulSoup) -> list:
        descript_tag = self._get_description_tag(soup)
        images_tags = descript_tag.find_all('img')
        return [f'{self.base_uri}{tag.attrs["src"]}' for tag in images_tags]

    @staticmethod
    def _get_description_tag(soup: BeautifulSoup) -> Tag:
        tag = soup.find('dd', {'class': 'descript', 'itemprop': 'content'})
        if tag is None:
            tag = soup.find('dd', {'class': 'descript', 'itemprop': 'definition'})
        return tag

    @staticmethod
    def _get_dic_from_uri(uri: URL) -> Dic:
        subdomain = uri.hostname.split('.')[0]
        if 'nsf' in uri.as_uri():
            dic_type = 'nsf'
        elif subdomain != 'dic':
            dic_type = 'subdomain'
        else:
            raise DicTypeNotFound(f'Dic type not found in url: {uri}')
        if dic_type == 'nsf':
            dic_name = uri.parts[-2]
        else:
            dic_name = subdomain
        return Dic(dic_name, dic_type)

    @staticmethod
    def _get_dic_title_by_word_soup(soup: BeautifulSoup) -> str:
        tag = soup.find('span', {'itemprop': 'title'})
        return tag.get_text()
