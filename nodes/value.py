class NumberNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"

class StringNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"


class ListNode:
    def __init__(self, element_nodes,pos_start,pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end  

    def __repr__(self):
        return f"{self.element_nodes}"