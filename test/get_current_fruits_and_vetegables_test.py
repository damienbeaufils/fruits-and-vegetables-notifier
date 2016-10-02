from unittest.mock import Mock

from fruits_and_vegetables_notifier.crawler import Crawler


class GetCurrentFruitsAndVegetablesTest:
    def setup_method(self):
        self.crawler = Crawler()
        self.crawler.get_page = Mock(return_value='')

    def test_should_get_page_showing_fruits_and_vegetables_for_all_months(self):
        # when
        self.crawler.get_fruits_and_vegetables_of_month(1)

        # then
        self.crawler.get_page.assert_called_once_with('https://www.fruits-legumes.org/mois/')

    def test_should_return_a_dict_of_current_fruits_and_vegetables(self):
        # given
        self.crawler.get_page.return_value = """
                    <div id="fruit-legume">
                      <h2 id="3">Mars</h2>
                      <div class="elements">
                        <ul id="legumes5">
                          <li><a href="chou-rave/">Chou-rave</a></li>
                          <li><a href="cima-di-rapa/">Cima di Rapa</a></li>
                        </ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsRhubarbe">
                          <li><a href="prune/">Prune</a></li>
                          <li><a href="quetsche/">Quetsche</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        current_fruits_and_vegetables = self.crawler.get_fruits_and_vegetables_of_month(3)

        # then
        assert len(current_fruits_and_vegetables) is 2
        assert 'Chou-rave' and 'Cima di Rapa' in current_fruits_and_vegetables['vegetables']
        assert 'Prune' and 'Quetsche' in current_fruits_and_vegetables['fruits']
