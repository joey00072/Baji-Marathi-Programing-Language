class SymbolTable:
    def __init__(self):
        self.symbols={}
        self.parent=None
    def get(self,var_name):
        value = self.symbols.get(var_name,None)
        if value==None and self.parent:
            return self.parent.get()
        return value
    def set(self,name,value):
        self.symbols[name]=value
    def remove(self,name):
        del self.symbols[name]

global_symbol_table = SymbolTable()

global_symbol_table.set('null',0)