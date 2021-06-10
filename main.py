from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
from Context import Context
from SymbolTable import global_symbol_table

import sys


#------------EXECUTE--------------

# ------------RUN-----------------


def run(fn, text, debug=False):

    lexer = Lexer(fn, text)
    # Genarate Tokens
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    if debug:
        print("---symbols--\n")
        print(global_symbol_table.symbols, "\n")
        print("---tokens--\n")
        print(tokens, "\n")
        print("--AST--\n")
        print(ast.node, "\n")
        print("--output--\n")

    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error


def run_from_file(file_name):
    splits  = file_name.strip().split(".")

    if len(splits)<2:
        print("Invalid argument")

    name = "".join(splits[:-1])
    
    extension = splits[-1].lower()

    if extension!='baji':
        print("File extension should .baji")
        print(f"Found -> {extension}")
        exit()
    
    try:
        with open(file_name , 'r') as f:
            script = f.read()
    except BaseException as e:
        print("Failed to load Script")
        print(str(e))
    
    _,error = run(f"<{name}>", script, debug=True)

    if error:
        print(error.as_string())


if __name__=="__main__":
    args = sys.argv

    if len(args)>1:
        run_from_file(args[1])
    else:
        print("Provide file name")
        


