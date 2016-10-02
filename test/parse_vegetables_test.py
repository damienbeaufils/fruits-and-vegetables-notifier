from fruits_and_vegetables_notifier.crawler import Crawler


class ParseVegetablesTest:
    def setup_method(self):
        self.crawler = Crawler()

    def test_should_return_no_vegetables_when_markup_is_none(self):
        # given
        markup = None

        # when
        vegetables = self.crawler.parse_vegetables(markup)

        # then
        assert len(vegetables) is 0

    def test_should_return_no_vegetables_when_markup_contains_no_element_with_id_fruit_legume(self):
        # given
        markup = """<div></div>"""

        # when
        vegetables = self.crawler.parse_vegetables(markup)

        # then
        assert len(vegetables) is 0

    def test_should_return_no_vegetables_when_list_is_empty_in_markup(self):
        # given
        markup = """<div id="fruit-legume">
                      <div class="elements">
                        <ul id="legumes5"></ul>
                      </div>
                      <div class="elements">
                        <ul id="vegetablesRhubarbe"></ul>
                      </div>
                    </div>"""

        # when
        vegetables = self.crawler.parse_vegetables(markup)

        # then
        assert len(vegetables) is 0

    def test_should_return_a_list_containing_vegetables_name_from_markup(self):
        # given
        markup = """<div id="fruit-legume">
                      <div class="elements">
                        <ul id="legumes5">
                          <li><a href="chou-rave/">Chou-rave</a></li>
                          <li><a href="cima-di-rapa/">Cima di Rapa</a></li>
                        </ul>
                      </div>
                      <div class="elements">
                        <ul id="vegetablesRhubarbe"></ul>
                      </div>
                    </div>"""

        # when
        vegetables = self.crawler.parse_vegetables(markup)

        # then
        assert len(vegetables) is 2
        assert 'Chou-rave' and 'Cima di Rapa' in vegetables

    def test_should_not_return_any_vegetables_in_vegetables_list(self):
        # given
        markup = """<div id="fruit-legume">
                      <div class="elements">
                        <ul id="legumes5">
                          <li><a href="chou-rave/">Chou-rave</a></li>
                        </ul>
                      </div>
                      <div class="elements">
                        <ul id="vegetablesRhubarbe">
                            <li><a href="prune/">Prune</a></li>
                            <li><a href="quetsche/">Quetsche</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        vegetables = self.crawler.parse_vegetables(markup)

        # then
        assert len(vegetables) is 1
