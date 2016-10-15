from fruits_and_vegetables_notifier.diff import Diff


class NextFruitsWithoutCurrentTest:
    def setup_method(self):
        self.diff = Diff()

    def test_should_return_fruits_which_are_in_next_dict_but_not_in_current_dict(self):
        # given
        current_fruits_and_vegetables = {
            'fruits': {'Banane'}
        }

        next_fruits_and_vegetables = {
            'fruits': {'Banane', 'Kiwi', 'Tomate'}
        }

        # when
        next_fruits = self.diff.next_fruits_without_current(current_fruits_and_vegetables, next_fruits_and_vegetables)

        # then
        assert len(next_fruits) is 2
        assert 'Kiwi' and 'Tomate' in next_fruits
