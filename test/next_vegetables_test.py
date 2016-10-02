from fruits_and_vegetables_notifier.diff import Diff


class NextVegetablesTest:
    def setup_method(self):
        self.diff = Diff()

    def test_should_return_vegetables_which_are_in_next_dict_but_not_in_current_dict(self):
        # given
        current_vegetables_and_vegetables = {
            'vegetables': ['Asperge', 'Radis']
        }

        next_vegetables_and_vegetables = {
            'vegetables': ['Asperge', 'Carotte', 'Epinard', 'Radis']
        }

        # when
        next_vegetables = self.diff.next_vegetables(current_vegetables_and_vegetables, next_vegetables_and_vegetables)

        # then
        assert len(next_vegetables) is 2
        assert 'Carotte' and 'Epinard' in next_vegetables
