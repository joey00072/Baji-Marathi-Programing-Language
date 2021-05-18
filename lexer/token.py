class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        if isinstance(value,tuple):
            match=False
            for val in value:
                match = match or (self.type == type_ and self.value == val)
            return match
        return self.type == type_ and self.value == value

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value else f"{self.type}"
