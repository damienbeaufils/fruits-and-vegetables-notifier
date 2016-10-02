import logging
import urllib.error
import urllib.parse
import urllib.request
from urllib.error import HTTPError

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

ROOT_URL = 'https://www.fruits-legumes.org/mois/'
FRUITS_AND_VEGETABLES_ELEMENT_ID = 'fruit-legume'
VEGETABLES_UL_ID_PREFIX = 'legume'
FRUITS_UL_ID_PREFIX = 'fruit'


class Crawler:
    def get_fruits_and_vegetables_of_month(self, month):
        markup = self.get_page(ROOT_URL)
        fruits = self.parse_fruits_of_month(markup, month)
        vegetables = self.parse_vegetables_of_month(markup, month)
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

    def parse_fruits_of_month(self, markup, month):
        fruits_and_vegetables_of_current_month = self.parse_fruits_and_vegetables_of_current_month(markup, month)
        return self.parse_links_from_specific_ul(fruits_and_vegetables_of_current_month, FRUITS_UL_ID_PREFIX)

    def parse_vegetables_of_month(self, markup, month):
        fruits_and_vegetables_of_current_month = self.parse_fruits_and_vegetables_of_current_month(markup, month)
        return self.parse_links_from_specific_ul(fruits_and_vegetables_of_current_month, VEGETABLES_UL_ID_PREFIX)

    @staticmethod
    def parse_fruits_and_vegetables_of_current_month(markup, month):
        dom = BeautifulSoup(markup, 'html.parser') if markup else None
        current_month_heading = dom.find('h2', id=month) if dom else None
        return current_month_heading.parent if current_month_heading else None

    @staticmethod
    def parse_links_from_specific_ul(fruits_and_vegetables_of_current_month, ul_id_prefix):
        if fruits_and_vegetables_of_current_month is None:
            return []

        def starts_with_prefix(id):
            return id.startswith(ul_id_prefix)

        ul_starting_with_given_prefix = fruits_and_vegetables_of_current_month.find_all('ul', id=starts_with_prefix)[0]
        return [link.get_text() for link in ul_starting_with_given_prefix.select('a')]
