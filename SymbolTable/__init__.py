from Values import Number
from SymbolTable.symbol_table import SymbolTable


#Global Symbols
global_symbol_table = SymbolTable()

global_symbol_table.set('null',Number(0))
global_symbol_table.set('true',Number(1))
global_symbol_table.set('false',Number(0))