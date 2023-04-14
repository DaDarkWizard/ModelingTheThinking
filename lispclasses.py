

class Cons:
    def __init__(self):
        self.first = None
        self.second = None


class Macro:
    def __init__(self, name):
        self.name = name
        self.args = []
        self.code = []
