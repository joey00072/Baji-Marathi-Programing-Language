from translate import Translate
from Errors import InvalidSyntaxError
from nodes import NumberNode,BinOpNode,UnaryOpNode
from lexer import Lexer
from lexer.constants import *
from results import ParseResult
from values import Number
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

    def factor(self):
        res = ParseResult()
        token = self.current_token
        if token.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        if self.current_token.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))

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
            token.pos_start,
            token.pos_end,
            "अपेक्षित संख्या किंवा फ्लोट (Expected int or float)"
        ))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_token.type in ops:
            op_token = self.current_token
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return  res
            left = BinOpNode(left, op_token, right)
        return res.success(left)
