from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
from Context import Context
from SymbolTable import SymbolTable, global_symbol_table


# ------------RUN-----------------
# global_symbol_table = SymbolTable()


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
