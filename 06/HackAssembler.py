from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable

class HackAssembler:
    def __init__(self, file):
        self.parser = Parser(file)
        self.symbolTable = SymbolTable()
        self.code = Code()
        self.address = 16
    
    def assemble(self):
        while self.parser.hasMoreLines():
            instructionType = self.parser.instructionType()
            symbol = self.parser.symbol()
            dest = self.parser.dest()
            comp = self.parser.comp()
            jump = self.parser.jump()
            print('line: ' + self.parser.advance())
            print('\tinstruction type: ' + instructionType)
            if symbol != "null":
                print('\tsymbol: ' + symbol)
            if dest != "null":
                print('\tdest: ' + dest)
            if comp != "null":
                print('\tcomp: ' + comp)
            if jump != "null":
                print('\tjump: ' + jump)
            print()

    def firstPass(self):
        self.parser.currentLine = 0
        while self.parser.hasMoreLines():
            instructionType = self.parser.instructionType()
            if instructionType == self.parser.L_INSTRUCTION:
                symbol = self.parser.symbol()
                self.symbolTable.addEntry(symbol, self.parser.currentLineWithOutLabels)
            self.parser.advance()

    def secondPass(self, hackFile):
        self.parser.currentLine = 0
        while self.parser.hasMoreLines():
            instructionType = self.parser.instructionType()
            isLastLine = self.parser.currentLine == len(self.parser.lines) - 1

            if instructionType == self.parser.A_INSTRUCTION:
                symbol = self.parser.symbol()
                if symbol.isdigit():
                    hackFile.write(self.parser.int_to_bin(int(symbol)))
                elif not self.symbolTable.contains(symbol):
                    self.symbolTable.addEntry(symbol, self.address)
                    self.address += 1
                    hackFile.write(self.parser.int_to_bin(int(self.symbolTable.getAddress(symbol))))
                else:
                    hackFile.write(self.parser.int_to_bin(int(self.symbolTable.getAddress(symbol))))
            elif instructionType == self.parser.C_INSTRUCTION:
                hackFile.write("111" + self.code.comp(self.parser.comp()) + self.code.dest(self.parser.dest()) + self.code.jump(self.parser.jump()))
            
            if instructionType != self.parser.L_INSTRUCTION and not isLastLine:
                hackFile.write("\n")

            self.parser.advance()