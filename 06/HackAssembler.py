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