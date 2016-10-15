class Diff:
    def next_fruits_without_current(self, current, next):
        return self.__search_next(current, next, 'fruits')

    def next_vegetables_without_current(self, current, next):
        return self.__search_next(current, next, 'vegetables')

    def __search_next(self, current, next, key):
        return next[key].difference(current[key])
