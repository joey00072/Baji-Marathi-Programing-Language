from Errors import InvalidSyntaxError
from Constants import *
from Results import ParseResult
from Nodes import *


# ------------PARSER----------------


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        self.update_current_token()
        return self.current_token

    def reverse(self, amount=1):
        self.token_idx -= amount
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        if self.token_idx >= 0 and self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]

    def peak(self):
        idx = self.token_idx + 1
        if idx < len(self.tokens):
            return self.tokens[idx]

    # -------------------#

    def parse(self):
        res = self.statements()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "अपेक्षित(Expected) '+','-', '*' or  '/'",
                )
            )
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = -1
            while self.current_token.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == -1:
                more_statements = False

            if not more_statements:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(
            ListNode(statements, pos_start, self.current_token.pos_end.copy())
        )

    def statement(self):
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.matches(TT_KEYWORD, ("RETURN", "परत")):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(
                ReturnNode(expr, pos_start, self.current_token.pos_start.copy())
            )

        if self.current_token.matches(TT_KEYWORD, ("CONTINUE", "सुरू")):
            res.register_advancement()
            self.advance()
            return res.success(
                ContinueNode(pos_start, self.current_token.pos_start.copy())
            )

        if self.current_token.matches(TT_KEYWORD, ("BREAK", "थांबवा")):
            res.register_advancement()
            self.advance()
            return res.success(
                BreakNode(pos_start, self.current_token.pos_start.copy())
            )

        expr = res.register(self.expr())
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'",
                )
            )
        return res.success(expr)

    def expr(self):
        res = ParseResult()
        if self.current_token.matches(TT_KEYWORD, ("VAR", "चल")):
            res.register_advancement()
            self.advance()
            if self.current_token.type != "IDENTIFIER":
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "अपेक्षित चल शब्द (Expected Identifier)",
                    )
                )
            var_name = self.current_token
            res.register_advancement()
            self.advance()

            if self.current_token.type != TT_EQ:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "अपेक्षित = (Expected =)",
                    )
                )
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr, True))

        if self.current_token.type == "IDENTIFIER":
            var_name = self.current_token
            next_token = self.peak()
            if next_token != None and next_token.type == TT_EQ:
                res.register_advancement()
                self.advance()
                res.register_advancement()
                self.advance()
                expr = res.register(self.expr())
                if res.error:
                    return res
                return res.success(VarAssignNode(var_name, expr, False))

        pass_keywords = (
            (TT_KEYWORD, "AND"),
            (TT_KEYWORD, "आणि"),
            (TT_KEYWORD, "OR"),
            (TT_KEYWORD, "किंवा"),
        )
        node = res.register(self.bin_op(self.comp_expr, pass_keywords))

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected 'VAR', int, float, identifier,'IF', 'FOR', 'WHILE', 'FUN', '+', '-','(' or '[' ",
                )
            )
        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_token.matches(TT_KEYWORD, ("NOT", "नाही")):
            op_token = self.current_token
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_token, node))

        node = res.register(
            self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE))
        )

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected int, float, identifier, '+', '-', '(','[' or 'NOT'",
                )
            )

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.power, (TT_MUL, TT_DIV))

    def factor(self):
        res = ParseResult()
        token = self.current_token
        if token.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (TT_POWER,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.current_token.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_token.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(','[' or 'NOT'",
                        )
                    )

                while self.current_token.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_token.type != TT_RPAREN:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            f"Expected ',' or ')'",
                        )
                    )

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        token = self.current_token
        if self.current_token.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        if self.current_token.type in (TT_STRING):
            res.register_advancement()
            self.advance()
            return res.success(StringNode(token))

        if self.current_token.type in (TT_IDENTIFIER):
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))

        if token.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)

        if token.type == TT_LSQUARE:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if self.current_token.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "अपेक्षित(Expected) ')' ",
                    )
                )

        if token.matches(TT_KEYWORD, ("IF", "जर")):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)
        if token.matches(TT_KEYWORD, ("FOR", "वारंवार")):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        if token.matches(TT_KEYWORD, ("WHILE", "जोपर्यंत")):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        if token.matches(TT_KEYWORD, ("FUN", "कार्य")):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        return res.failure(
            InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                "अपेक्षित(Expected) int,float, identifier,'IF', 'FOR', 'WHILE', 'FUN', '+','-','[' or  '('",
            )
        )

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != TT_LSQUARE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '['",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'",
                    )
                )

            while self.current_token.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

            if self.current_token.type != TT_RSQUARE:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected ',' or ']'",
                    )
                )

            res.register_advancement()
            self.advance()

        return res.success(
            ListNode(element_nodes, pos_start, self.current_token.pos_end.copy())
        )

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases(("IF", "जर")))
        if res.error:
            return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases(("ELIF", "किंवाजर"))

    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_token.matches(TT_KEYWORD, ("ELSE", "नाहीतर")):
            res.register_advancement()
            self.advance()

            if self.current_token.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.current_token.matches(TT_KEYWORD, ("END", "शेवट")):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected 'END'",
                        )
                    )
            else:
                expr = res.register(self.statement())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_token.matches(TT_KEYWORD, ("ELIF", "किंवाजर")):
            all_cases = res.register(self.if_expr_b())
            if res.error:
                return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(TT_KEYWORD, case_keyword):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '{case_keyword}'",
                )
            )

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, ("THEN", "तर")):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'THEN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.current_token.matches(TT_KEYWORD, ("END", "शेवट")):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error:
                    return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error:
                return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, ("FOR", "वारंवार")):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'FOR'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected identifier",
                )
            )

        var_name = self.current_token
        res.register_advancement()
        self.advance()

        if self.current_token.type != TT_EQ:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '='",
                )
            )

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, ("TO", "ते")):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'TO'",
                )
            )

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_token.matches(TT_KEYWORD, ("STEP", "पाऊल")):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_token.matches(TT_KEYWORD, ("THEN", "तर")):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'THEN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_token.matches(TT_KEYWORD, ("END", "शेवट")):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected 'END'",
                    )
                )

            res.register_advancement()
            self.advance()

            return res.success(
                ForNode(var_name, start_value, end_value, step_value, body, True)
            )

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(
            ForNode(var_name, start_value, end_value, step_value, body, False)
        )

    def while_expr(self):
        res = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, ("WHILE", "जोपर्यंत")):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'WHILE'",
                )
            )

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, ("THEN", "तर")):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'THEN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_token.matches(TT_KEYWORD, ("END", "शेवट")):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected 'END'",
                    )
                )

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(WhileNode(condition, body, False))

    def func_def(self):
        res = ParseResult()
    
        if not self.current_token.matches(TT_KEYWORD, ("FUN", "कार्य")):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'FUN'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TT_IDENTIFIER:
            var_name_tok = self.current_token
            res.register_advancement()
            self.advance()
            if self.current_token.type != TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected '('",
                    )
                )
        else:
            var_name_tok = None
            if self.current_token.type != TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected identifier or '('",
                    )
                )

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_token.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_token)
            res.register_advancement()
            self.advance()

            while self.current_token.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_token.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            f"Expected identifier",
                        )
                    )

                arg_name_toks.append(self.current_token)
                res.register_advancement()
                self.advance()

            if self.current_token.type != TT_RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected ',' or ')'",
                    )
                )
        else:
            if self.current_token.type != TT_RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected identifier or ')'",
                    )
                )

        res.register_advancement()
        self.advance()

        if self.current_token.type == TT_ARROW:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error:
                return res

            return res.success(FuncDefNode(var_name_tok, arg_name_toks, body, True))

        if self.current_token.type != TT_NEWLINE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '->' or NEWLINE",
                )
            )

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, "END"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'END'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(var_name_tok, arg_name_toks, body, False))

    ################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while (
            self.current_token.type in ops
            or (self.current_token.type, self.current_token.value) in ops
        ):
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_token, right)
        return res.success(left)
