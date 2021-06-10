class ForNode:
    def __init__(
        self,
        var_name_token,
        start_value_node,
        end_value_node,
        step_value_node,
        body_node,
        should_return_null,
    ):
        self.var_name_token = var_name_token
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.body_node.pos_end
        self.should_return_null = should_return_null

    def __repr__(self):
        return f"For Loop[{self.start_value_node},{self.end_value_node},{self.step_value_node}] :{self.body_node}"


class WhileNode:
    def __init__(self, condition_node, body_node, should_return_null):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end
        self.should_return_null = should_return_null

    def __repr__(self):
        return f"WHILE {self.body_node}"


class ContinueNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end


class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
