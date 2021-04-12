from translate import Translate

#-----------CONSTANTS-----------
DIGITS = '0123456789०१२३४५६७८९'

#-----------ERROR--------------
class Error(object):
    def __init__(self,error_name,pos_start,pos_end,details):
        self.pos_start  = pos_start
        self.pos_end    = pos_end
        self.error_name = error_name
        self.details    = details
        
    def as_string(self):
        result= f'{self.error_name} : {self.details} \n' 
        result +=f'File {self.pos_start.fn}, line {self.pos_start.ln+1}'
        return result

class IllegalCharacterError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__("Illegal Character",pos_start,pos_end,details)


#----------Position--------------

class Position:
    def __init__(self,idx,ln,col,fn,ftxt):
        self.idx  = idx
        self.ln   = ln
        self.col  = col
        self.fn   = fn
        self.ftxt = ftxt

    def advance(self,current_char=None):
        self.idx+=1
        self.col+=1

        if current_char=='\n':
            self.ln+=1
            self.col=0
        return self
    def copy(self):
        return Position(self.idx,self.ln,self.col,self.fn,self.ftxt)



#-----------TOKEN---------------

TT_INT    = 'INT'
TT_FLOAT  = 'FLOAT'
TT_PLUS   = 'PLUS'
TT_MINUS  = 'MINUS'
TT_MUL    = 'MUL'
TT_DIV    = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


TT_INT      = 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'


class Token(object):
    def __init__(self,type_,value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value if self.value is not None else 'नल' }"



#-----------LEXER---------------

class Lexer(object):
    def __init__(self,fn,text):
        self.fn = fn
        self.text = text 
        self.pos = Position(-1,0,-1,fn,text)
        self.current_char = None
        self.advance()
        self.translate = Translate()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx <len(self.text) else None

    def primitive_tocken(self):
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
        token = self.primitive_tocken()

        if token:
            self.advance()
            return token

        if self.current_char in DIGITS:
            return self.make_number()


        position_start = self.pos.copy()

        return IllegalCharacterError(position_start,self.pos,"'"+self.current_char+"'")

        

    def make_tokens(self):
        tokens = []
        while self.current_char!=None:
            if self.current_char in ' \t':
                self.advance()
                continue

            current_token = self.get_token()
            if isinstance(current_token,Error):
                return [],current_token
            tokens.append(current_token)

        return tokens,None

    def make_number(self):
        num_str = ''
        dot     = False

        while self.current_char!=None and self.current_char in DIGITS+'.':
            if self.current_char=='.':
                if dot==True:break
                dot = True
                num_str+='.'
            else:
                num_str += self.translate.digit_to_eng(self.current_char)
            self.advance()

        if dot:
            return Token(TT_FLOAT,float(num_str)) 
        else:
            return Token(TT_INT,int(num_str))








#------------RUN-----------------

def run(fn,text):
    lexer = Lexer(fn,text)
    token,error = lexer.make_tokens()
    return token,error
