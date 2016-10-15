from unittest.mock import patch, Mock
from urllib.error import HTTPError

from fruits_and_vegetables_notifier.crawler import Crawler


@patch('urllib.request.urlopen')
class GetPageTest:
    def setup_method(self):
        self.url = 'https://www.fruits-legumes.org/'
        self.crawler = Crawler()

    def test_should_return_response_body(self, urlopen):
        # given
        response = Mock()
        response_body = '<a href="http://first_link"></a>'
        response.read.return_value = response_body
        urlopen.return_value = response

        # when
        body = self.crawler._get_page(self.url)

        # then
        assert body == response_body

    def test_should_return_none_if_not_found(self, urlopen):
        # given
        urlopen.side_effect = HTTPError(self.url, 404, '', None, None)

        # when
        body = self.crawler._get_page(self.url)

        # then
        assert body is None

    def test_should_return_none_if_any_error_happened(self, urlopen):
        # given
        urlopen.side_effect = Exception()

        # when
        body = self.crawler._get_page(self.url)

        # then
        assert body is None

    def test_should_return_none_if_internal_server_error(self, urlopen):
        # given
        urlopen.side_effect = HTTPError(self.url, 500, '', None, None)

        # when
        body = self.crawler._get_page(self.url)

        # then
        assert body is None
