from fruits_and_vegetables_notifier.crawler import Crawler


class ParseFruitsTest:
    def setup_method(self):
        self.crawler = Crawler()

    def test_should_return_no_fruits_when_markup_is_none(self):
        # given
        markup = None

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 1)

        # then
        assert len(fruits) is 0

    def test_should_return_no_fruits_when_markup_contains_no_element_with_id_fruit_legume(self):
        # given
        markup = """<div></div>"""

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 1)

        # then
        assert len(fruits) is 0

    def test_should_return_no_fruits_when_list_is_empty_in_markup(self):
        # given
        markup = """<div id="fruit-legume">
                      <h2 id="1">Janvier</h2>
                      <div class="elements">
                        <ul id="legumesde-XXX"></ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsde-XXX"></ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 1)

        # then
        assert len(fruits) is 0

    def test_should_return_a_list_containing_fruits_name_from_markup(self):
        # given
        markup = """<div id="fruit-legume">
                      <h2 id="1">Janvier</h2>
                      <div class="elements">
                        <ul id="legumesde-XXX"></ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsde-XXX">
                          <li><a href="prune/">Prune</a></li>
                          <li><a href="quetsche/">Quetsche</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 1)

        # then
        assert len(fruits) is 2
        assert 'Prune' and 'Quetsche' in fruits

    def test_should_return_a_list_containing_unique_fruits_name_when_there_are_duplicates_in_markup(self):
        # given
        markup = """<div id="fruit-legume">
                      <h2 id="1">Janvier</h2>
                      <div class="elements">
                        <ul id="legumesde-XXX"></ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsde-XXX">
                          <li><a href="prune/">Prune</a></li>
                          <li><a href="quetsche/">Quetsche</a></li>
                          <li><a href="prune/">Prune</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 1)

        # then
        assert len(fruits) is 2
        assert 'Prune' and 'Quetsche' in fruits

    def test_should_not_return_any_vegetables_in_fruits_list(self):
        # given
        markup = """<div id="fruit-legume">
                      <h2 id="1">Janvier</h2>
                      <div class="elements">
                        <ul id="legumesde-XXX">
                          <li><a href="chou-rave/">Chou-rave</a></li>
                          <li><a href="cima-di-rapa/">Cima di Rapa</a></li>
                        </ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsde-XXX">
                          <li><a href="prune/">Prune</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 1)

        # then
        assert len(fruits) is 1

    def test_should_return_only_fruits_of_given_month(self):
        # given
        markup = """<div id="fruit-legume">
                      <h2 id="11">Novembre</h2>
                      <div class="elements">
                        <ul id="legumesde-XXX"></ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsde-XXX">
                          <li><a href="prune/">Prune</a></li>
                        </ul>
                      </div>
                    </div>
                    <div id="fruit-legume">
                      <h2 id="12">Décembre</h2>
                      <div class="elements">
                        <ul id="legumesde-XXX"></ul>
                      </div>
                      <div class="elements">
                        <ul id="fruitsde-XXX">
                          <li><a href="citron/">Citron</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 12)

        # then
        assert len(fruits) is 1
        assert 'Citron' in fruits

    def test_should_return_only_fruits_even_if_lists_are_inverted(self):
        # given
        markup = """<div id="fruit-legume">
                      <h2 id="1">Janvier</h2>
                      <div class="elements">
                        <ul id="fruitsde-XXX">
                          <li><a href="prune/">Prune</a></li>
                        </ul>
                      </div>
                      <div class="elements">
                        <ul id="legumesde-XXX">
                          <li><a href="chou-rave/">Chou-rave</a></li>
                        </ul>
                      </div>
                    </div>"""

        # when
        fruits = self.crawler._parse_fruits_of_month(markup, 1)

        # then
        assert 'Prune' in fruits
