from Translate import Translate
from Errors import Error,IllegalCharacterError,InvalidSyntaxError
from Constants import *



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
            
    def matches(self, type_, value):
        return self.type == type_ and self.value == value
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
    def peak(self,idx=1):
        if self.pos.idx +idx< len(self.text):
            return  self.text[self.pos.idx+idx] 
        return None
        

    def primitive_token(self):
        if self.current_char == '+':
            return TT_PLUS

        if self.current_char == '-':
            return TT_MINUS

        if self.current_char == '*':
            nxt=self.peak()
            if nxt=='*':
                self.advance()
                return TT_POWER
            return TT_MUL

        if self.current_char == '/':
            return TT_DIV

        if self.current_char == '(':
            return TT_LPAREN

        if self.current_char == ')':
            return TT_RPAREN
        
        if self.current_char == '=':
            return TT_EQ

    def get_token(self):
        token = self.primitive_token()

        if token:
            self.advance()
            return Token(token,pos_start=self.pos)

        if self.current_char in DIGITS:
            return self.make_number()
        
        if self.current_char in LATTERS:
            return self.make_identifier()

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

    def make_identifier(self):
        id_str = ''
        pos_start=self.pos

        while self.current_char != None and self.current_char in LATTERS_DIGITS+'_':
            id_str+= self.translate.digit_to_eng(self.current_char)
            self.advance()

        token_type= TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(token_type,id_str,pos_start,self.pos)