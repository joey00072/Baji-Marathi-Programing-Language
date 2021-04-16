from lexer import Lexer
from Parser import Parser 
from Interpreter import Interpreter
from Context import Context



# ------------RUN-----------------

def run(fn, text):
    lexer = Lexer(fn, text)
    # Genarate Tokens
    tokens, error = lexer.make_tokens()
    print(tokens)
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast.node)
    if ast.error: 
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)
    
    return  result.value, result.error
