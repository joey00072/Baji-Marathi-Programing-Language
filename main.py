from translate import Translate
from errors import Error, IllegalCharacterError,InvalidSyntaxError

# -----------CONSTANTS-----------
DIGITS = '0123456789०१२३४५६७८९'


# ----------Position--------------

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


# -----------TOKEN---------------
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF ="EOF"


class Token(object):
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value else f"{self.type}"


# -----------LEXER---------------

class Lexer(object):
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        self.translate = Translate()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def primitive_token(self):
        if self.current_char == '+':
            return TT_PLUS

        if self.current_char == '-':
            return TT_MINUS

        if self.current_char == '*':
            return TT_MUL

        if self.current_char == '/':
            return TT_DIV

        if self.current_char == '(':
            return TT_LPAREN

        if self.current_char == ')':
            return TT_RPAREN

    def get_token(self):
        token = self.primitive_token()

        if token:
            self.advance()
            return Token(token,pos_start=self.pos)

        if self.current_char in DIGITS:
            return self.make_number()

        position_start = self.pos.copy()

        return IllegalCharacterError(position_start, self.pos, "'"+self.current_char+"'")

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
                continue

            current_token = self.get_token()
            if isinstance(current_token, Error):
                return [], current_token
            tokens.append(current_token)

        tokens.append(Token(TT_EOF,pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot = False
        pos_start=self.pos

        while self.current_char != None and self.current_char in DIGITS+'.':
            if self.current_char == '.':
                if dot == True:
                    break
                dot = True
                num_str += '.'
            else:
                num_str += self.translate.digit_to_eng(self.current_char)
            self.advance()

        if dot:
            return Token(TT_FLOAT, float(num_str),pos_start=pos_start,pos_end=self.pos)
        else:
            return Token(TT_INT, int(num_str),pos_start=pos_start,pos_end=self.pos)


# ------------NODES----------------
class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token}"


class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f'( {self.left_node} {self.op_token} {self.right_node} )'


# ---------PARSE_RESULT------------
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error= res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


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
        if self.current_token.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))
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


# ------------RUN-----------------

def run(fn, text):
    lexer = Lexer(fn, text)
    # Genarate Tokens
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error