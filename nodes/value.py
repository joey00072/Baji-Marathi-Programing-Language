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


class IndexNode:
    def __init__(self, index_node, expr):
        self.index_node = index_node
        self.expr = expr

        self.pos_start = self.index_node.pos_start

        self.pos_end = self.index_node.pos_end

    def __repr__(self):
        return f"( Index {self.index_node}->expr({self.expr}) ) "


class IndexAssignNode:
    def __init__(self, index_node, expr,assgin_expr):
        self.index_node = index_node
        self.expr = expr

        self.pos_start = self.index_node.pos_start

        self.pos_end = self.index_node.pos_end
        self.assgin_expr = assgin_expr

    def __repr__(self):
        return f"( Index  assign {self.index_node}->expr({self.expr}) := expr({self.assgin_expr}) ) "