class Diff:
    def next_fruits(self, current, next):
        return self.search_next(current, next, 'fruits')

    def next_vegetables(self, current, next):
        return self.search_next(current, next, 'vegetables')

    def search_next(self, current, next, key):
        return [fruit for fruit in next[key] if fruit not in current[key]]
