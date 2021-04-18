from Errors import InvalidSyntaxError
from Nodes import NumberNode,BinOpNode,UnaryOpNode,VarAssignNode,VarAccessNode
from Constants import *
from results import ParseResult
from Context import Context


# ------------PARSER----------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token
    #-------------------#

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start,self.current_token.pos_end,
                "अपेक्षित(Expected) '+','-', '*' or  '/'"
            ))
        return res

    def atom(self):
        res = ParseResult()
        token = self.current_token
        if self.current_token.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))

        if self.current_token.type in (TT_IDENTIFIER):
            res.register(self.advance())
            return res.success(VarAccessNode(token))


        if token.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if self.current_token.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                self.current_token.pos_start,self.current_token.pos_end,
                "अपेक्षित(Expected) ')' "
            ))
        return res.failure(InvalidSyntaxError(
                self.current_token.pos_start,self.current_token.pos_end,
                "अपेक्षित(Expected) int,float, '+','-' or  '('"
            ))
        


    def factor(self):
        res = ParseResult()
        token = self.current_token
        if token.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.atom, (TT_POWER,),self.factor)


    def term(self):
        return self.bin_op(self.power, (TT_MUL, TT_DIV)) 

    def expr(self):
        res = ParseResult()
        if self.current_token.matches(TT_KEYWORD,'var') or self.current_token.matches(TT_KEYWORD,'चल'):
            res.register(self.advance())
            if self.current_token.type != 'IDENTIFIER':
                return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start,self.current_token.pos_end,
                            "अपेक्षित चल शब्द (Expected Identifier)"
                            ))
            var_name = self.current_token
            res.register(self.advance())

            if self.current_token.type != TT_EQ:
               return  res.failure(InvalidSyntaxError(
                            self.current_token.pos_start,self.current_token.pos_end,
                            "अपेक्षित = (Expected =)"
                            ))
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name,expr))

        node = res.register(self.bin_op(self.term,(TT_PLUS,TT_MINUS)))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected 'VAR', int, float, identifier, '+', '-' or '('"
            ))
        return res.success(node)

    def bin_op(self, func_a, ops,func_b=None):
        if func_b==None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_token.type in ops:
            op_token = self.current_token
            res.register(self.advance())
            right = res.register(func_b())
            if res.error:
                return  res
            left = BinOpNode(left, op_token, right)
        return res.success(left)
