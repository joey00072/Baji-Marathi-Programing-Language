from Errors import InvalidSyntaxError
from Nodes import NumberNode,BinOpNode,UnaryOpNode,VarAssignNode,VarAccessNode,IfNode
from Constants import *
from Results import ParseResult


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

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(TT_KEYWORD, ('IF','जर')):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'IF'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_token.matches(TT_KEYWORD, ('THEN','तर')):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'तर' ('THEN')"
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_token.matches(TT_KEYWORD, ('ELIF','किंवाजर')):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_token.matches(TT_KEYWORD, ('THEN','तर')):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected 'तर' ('THEN') "
                ))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr))

        if self.current_token.matches(TT_KEYWORD, ('ELSE',"नाहीतर")):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error: return res

        return res.success(IfNode(cases, else_case))

    def atom(self):
        res = ParseResult()
        token = self.current_token
        if self.current_token.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        if self.current_token.type in (TT_IDENTIFIER):
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))


        if token.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if self.current_token.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                self.current_token.pos_start,self.current_token.pos_end,
                "अपेक्षित(Expected) ')' "
            ))

        if token.matches(TT_KEYWORD, ('IF',"जर")):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        return res.failure(InvalidSyntaxError(
                self.current_token.pos_start,self.current_token.pos_end,
                "अपेक्षित(Expected) int,float, identifier '+','-' or  '('"
            ))
        


    def factor(self):
        res = ParseResult()
        token = self.current_token
        if token.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.atom, (TT_POWER,),self.factor)


    def term(self):
        return self.bin_op(self.power, (TT_MUL, TT_DIV)) 

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def comp_expr(self):
        res = ParseResult()

        if self.current_token.matches(TT_KEYWORD, ("NOT","नाही")):
            op_token = self.current_token
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_token, node))
        
        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected int, float, identifier, '+', '-', '(' or 'NOT'"
            ))

        return res.success(node)

    def expr(self):
        res = ParseResult()
        if self.current_token.matches(TT_KEYWORD,('var','चल')):
            res.register_advancement()
            self.advance()
            if self.current_token.type != 'IDENTIFIER':
                return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start,self.current_token.pos_end,
                            "अपेक्षित चल शब्द (Expected Identifier)"
                            ))
            var_name = self.current_token
            res.register_advancement()
            self.advance()

            if self.current_token.type != TT_EQ:
               return  res.failure(InvalidSyntaxError(
                            self.current_token.pos_start,self.current_token.pos_end,
                            "अपेक्षित = (Expected =)"
                            ))
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name,expr))

        pass_keywords = ((TT_KEYWORD, 'AND'),(TT_KEYWORD, 'आणि'), (TT_KEYWORD, 'OR'),(TT_KEYWORD, 'किंवा'))
        node = res.register(self.bin_op(self.comp_expr,pass_keywords))
        
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

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return  res
            left = BinOpNode(left, op_token, right)
        return res.success(left)
