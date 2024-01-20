from Parser import Parser

class HackAssembler:
    def __init__(self, file):
        self.parser = Parser(file)
    
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

            #Code(self.parser.dest(), self.parser.comp(), self.parser.jump(), self.parser.advance())
    def firstPass(self):
        while self.parser.hasMoreLines():
            instructionType = self.parser.instructionType()
            if instructionType == self.parser.L_INSTRUCTION:
                symbol = self.parser.symbol()
                self.symbolTable.addEntry(symbol, self.parser.currentLine)
            self.parser.advance()
        self.parser.currentLine = 0

    def secondPass(self, hackFile):
        while self.parser.hasMoreLines():
            instructionType = self.parser.instructionType()
            if instructionType == self.parser.A_INSTRUCTION:
                symbol = self.parser.symbol()
                if not self.symbolTable.contains(symbol):
                    self.symbolTable.addEntry(symbol, self.address)
                    hackFile.write(self.parser.int_to_bin(int(self.symbolTable.getAddress(symbol))) + "\n")
                    address += 1
            elif instructionType == self.parser.C_INSTRUCTION:
                hackFile.write("111" + self.code.comp() + self.code.dest() + self.code.jump() + "\n")
            self.parser.advance()
