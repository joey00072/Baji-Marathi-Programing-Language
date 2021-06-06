class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end
        

    def __repr__(self):
        return f"{self.var_name_token}"

class VarAssignNode:
    def __init__(self, var_name_token,value_node,declare=True):
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.declare = declare

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

    def __repr__(self):
        return f"{self.var_name_token}"