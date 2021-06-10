from typing import Counter
from Translate import Translate
from Errors import Error, IllegalCharacterError, ExpectedCharError
from Lexer.position import Position
from Lexer.token import Token
from Constants import *


# -----------LEXER---------------


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        self.translate = Translate()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def peak(self, idx=1):
        if self.pos.idx + idx < len(self.text):
            return self.text[self.pos.idx + idx]
        return None

    def primitive_token(self):
        if self.current_char == "+":
            return TT_PLUS, None

        if self.current_char == "-":
            return self.make_minus_or_arrow()

        if self.current_char == "*":
            return self.make_mul_or_power()

        if self.current_char == "/":
            return TT_DIV, None

        if self.current_char == ",":
            return TT_COMMA, None

        if self.current_char == "(":
            return TT_LPAREN, None

        if self.current_char == ")":
            return TT_RPAREN, None

        if self.current_char == "[":
            return TT_LSQUARE, None

        if self.current_char == "]":
            return TT_RSQUARE , None

        if self.current_char == "=":
            return self.make_equals()
        if self.current_char == "<":
            return self.make_less_than()

        if self.current_char == ">":
            return self.make_greater_than()

        if self.current_char == "!":
            token, error = self.make_not_equals()
            if error:
                return None, error
            return token, None

        if self.current_char in ";\n":
            return TT_NEWLINE,None
        
        
            

        return None, None

    def get_token(self):
        token, error = self.primitive_token()

        if error:
            return error
        if token:
            self.advance()
            return Token(token, pos_start=self.pos)

        if self.current_char == '"':
            return self.make_string()

        if self.current_char in DIGITS:
            return self.make_number()

        if self.current_char in LETTERS:
            return self.make_identifier()

        
            

        position_start = self.pos.copy()

        return IllegalCharacterError(
            position_start, self.pos, "'" + self.current_char + "'"
        )

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
                continue
            if self.current_char == "#":
                self.skip_comment()
            current_token = self.get_token()
            if isinstance(current_token, Error):
                return [], current_token
            tokens.append(current_token)

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ""
        dot = False
        pos_start = self.pos

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot == True:
                    break
                dot = True
                num_str += "."
            else:
                num_str += self.translate.digit_to_eng(self.current_char)
            self.advance()

        if dot:
            return Token(
                TT_FLOAT, float(num_str), pos_start=pos_start, pos_end=self.pos
            )
        else:
            return Token(TT_INT, int(num_str), pos_start=pos_start, pos_end=self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
            escape_character = False
        
        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)


    def make_identifier(self):
        id_str = ""
        pos_start = self.pos

        while self.current_char != None and self.current_char in LETTERS_DIGITS + "_":
            id_str += self.translate.digit_to_eng(self.current_char)
            self.advance()

        token_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(token_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            return TT_NE, None

        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self):
        tok_type = TT_EQ
        nxt = self.peak()
        if nxt == "=":
            self.advance()
            tok_type = TT_EE
        return tok_type, None

    def make_less_than(self):
        tok_type = TT_LT
        nxt = self.peak()

        if nxt == "=":
            self.advance()
            tok_type = TT_LTE

        return tok_type, None

    def make_greater_than(self):
        tok_type = TT_GT
        nxt = self.peak()

        if nxt == "=":
            self.advance()
            tok_type = TT_GTE

        return tok_type, None

    def make_mul_or_power(self):
        tok_type = TT_MUL
        nxt = self.peak()

        if nxt == "*":
            self.advance()
            tok_type = TT_POWER

        return tok_type, None

    def make_minus_or_arrow(self):
        tok_type = TT_MINUS
        nxt = self.peak()

        if nxt == ">":
            self.advance()
            tok_type = TT_ARROW

        return tok_type, None

    def skip_comment(self):
        while self.current_char != '\n':
            self.advance()
        self.advance()
