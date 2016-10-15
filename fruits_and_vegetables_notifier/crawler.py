import urllib.error
import urllib.parse
import urllib.request
from urllib.error import HTTPError

from bs4 import BeautifulSoup

from fruits_and_vegetables_notifier import logger

ROOT_URL = 'https://www.fruits-legumes.org/mois/'
FRUITS_AND_VEGETABLES_ELEMENT_ID = 'fruit-legume'
VEGETABLES_UL_ID_PREFIX = 'legume'
FRUITS_UL_ID_PREFIX = 'fruit'


class Crawler:
    def get_fruits_and_vegetables_of_month(self, month):
        markup = self._get_page(ROOT_URL)
        fruits = self._parse_fruits_of_month(markup, month)
        vegetables = self._parse_vegetables_of_month(markup, month)
        return {
            'fruits': fruits,
            'vegetables': vegetables
        }

    def _get_page(self, url):
        request = urllib.request.Request(url)
        body = None
        try:
            response = urllib.request.urlopen(request)
            body = response.read()
        except HTTPError as e:
            logger.error('could not fetch page')
        finally:
            return body

    def _parse_fruits_of_month(self, markup, month):
        fruits_and_vegetables_of_current_month = self.__get_fruits_and_vegetables_markup_of_month(markup, month)
        return self.__get_fruits_and_vegetables_from_markup(fruits_and_vegetables_of_current_month, FRUITS_UL_ID_PREFIX)

    def _parse_vegetables_of_month(self, markup, month):
        fruits_and_vegetables_of_current_month = self.__get_fruits_and_vegetables_markup_of_month(markup, month)
        return self.__get_fruits_and_vegetables_from_markup(fruits_and_vegetables_of_current_month,
                                                            VEGETABLES_UL_ID_PREFIX)

    def __get_fruits_and_vegetables_markup_of_month(self, markup, month):
        dom = BeautifulSoup(markup, 'html.parser') if markup else None
        current_month_heading = dom.find('h2', id=month) if dom else None
        return current_month_heading.parent if current_month_heading else None

    def __get_fruits_and_vegetables_from_markup(self, fruits_and_vegetables_of_current_month, ul_id_prefix):
        if fruits_and_vegetables_of_current_month is None:
            return []

        def starts_with_prefix(element_id):
            return element_id.startswith(ul_id_prefix)

        ul_starting_with_given_prefix = fruits_and_vegetables_of_current_month.find_all('ul', id=starts_with_prefix)[0]
        return set([link.get_text() for link in ul_starting_with_given_prefix.select('a')])
