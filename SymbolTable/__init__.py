from Values import *
from SymbolTable.symbol_table import SymbolTable




#Global Symbols
global_symbol_table = SymbolTable()

# global_symbol_table.set('null',Number(0))
# global_symbol_table.set('true',Number(1))
# global_symbol_table.set('false',Number(0))
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number(3.141592653589793))
