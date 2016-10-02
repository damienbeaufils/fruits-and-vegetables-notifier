from fruits_and_vegetables_notifier.crawler import Crawler


class ParseFruitsTest:
    def setup_method(self):
        self.crawler = Crawler()

    def test_should_return_no_fruits_when_markup_is_none(self):
        # given
        markup = None

        # when
        fruits = self.crawler.parse_fruits(markup)

        # then
        assert len(fruits) is 0

    def test_should_return_no_fruits_when_markup_contains_no_element_with_id_fruit_legume(self):
        # given
        markup = """<div></div>"""

        # when
        fruits = self.crawler.parse_fruits(markup)

        # then
        assert len(fruits) is 0

    def test_should_return_no_fruits_when_list_is_empty_in_markup(self):
        # given
        markup = """<div id="fruit-legume">
                      <div class="elements">
                        <ul id="legumes5"></ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsRhubarbe"></ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler.parse_fruits(markup)

        # then
        assert len(fruits) is 0

    def test_should_return_a_list_containing_fruits_name_from_markup(self):
        # given
        markup = """<div id="fruit-legume">
                      <div class="elements">
                        <ul id="legumes5"></ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsRhubarbe">
                          <li><a href="prune/">Prune</a></li>
                          <li><a href="quetsche/">Quetsche</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler.parse_fruits(markup)

        # then
        assert len(fruits) is 2
        assert 'Prune' and 'Quetsche' in fruits

    def test_should_not_return_any_vegetables_in_fruits_list(self):
        # given
        markup = """<div id="fruit-legume">
                      <div class="elements">
                        <ul id="legumes5">
                          <li><a href="chou-rave/">Chou-rave</a></li>
                          <li><a href="cima-di-rapa/">Cima di Rapa</a></li>
                        </ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsRhubarbe">
                          <li><a href="prune/">Prune</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler.parse_fruits(markup)

        # then
        assert len(fruits) is 1
