import logging
import urllib.error
import urllib.parse
import urllib.request
from urllib.error import HTTPError

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

ROOT_URL = 'https://www.fruits-legumes.org/'
ROOT_ELEMENT_ID = 'fruit-legume'
VEGETABLES_UL_INDEX = 0
FRUITS_UL_INDEX = 1


class Crawler:
    def get_current_fruits_and_vetegables(self):
        markup = self.get_page(ROOT_URL)
        fruits = self.parse_fruits(markup)
        vegetables = self.parse_vegetables(markup)
        return {
            'fruits': fruits,
            'vegetables': vegetables
        }

    @staticmethod
    def get_page(url):
        request = urllib.request.Request(url)
        body = None
        try:
            response = urllib.request.urlopen(request)
            body = response.read()
        except HTTPError as e:
            logger.error('could not fetch page')
        finally:
            return body

    def parse_fruits(self, markup):
        return self.parse_links_from_specific_ul(markup, FRUITS_UL_INDEX)

    def parse_vegetables(self, markup):
        return self.parse_links_from_specific_ul(markup, VEGETABLES_UL_INDEX)

    @staticmethod
    def parse_links_from_specific_ul(markup, ul_index):
        fruits_and_vegetables = BeautifulSoup(markup, 'html.parser').find(id=ROOT_ELEMENT_ID) if markup else None
        if fruits_and_vegetables is None:
            return []
        return [link.get_text() for link in fruits_and_vegetables.find_all('ul')[ul_index].select('a')]
