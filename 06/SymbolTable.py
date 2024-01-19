class SymbolTable:
    def __init__(self):
        self.table = {}

    def addEntry(self, symbol, address):
        self.table[symbol] = address
    
    def contains(self, symbol):
        return symbol in self.table
    
    def getAddress(self, symbol):
        return self.table[symbol]