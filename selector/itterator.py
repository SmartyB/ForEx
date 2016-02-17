class Itterator:
    def __init__(self, itList):
        self.list = itList
    def length(self):
        return len(self.list)
    def hasNext(self):
        return self.length() > 0
    def next(self):
        if self.hasNext():
            return self.list.pop(0)
        return None
    def last(self):
        if self.hasNext():
            return self.list.pop()
        return None
    def reverse(self):
        self.list = list(reversed(self.list))
        return self

    def closeAll(self):
        '''only for trade and order itterators'''
        while self.hasNext():
            self.next().close()

    def __add__(self, other):
        assert self.__class__.__name__ == other.__class__.__name__
        itt = Itterator(self.list + other.list)
        return itt
