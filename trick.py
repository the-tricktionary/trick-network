class Trick:

    def __init__(self, id, level, name, type, prereqs=[]):
        self.id = id
        self.level = level
        self.name = name
        self.type = type
        self.prereqs = prereqs