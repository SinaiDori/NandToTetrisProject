from Parser import Parser

class HackAssembler:
    def __init__(self, file):
        self.parser = Parser(file)
    
    def assemble(self):
        while self.parser.hasMoreLines():
            if self.parser.instructionType() is not None:
                print('instruction type: ' + self.parser.instructionType())
            if self.parser.symbol() is not None:
                print('symbol: ' + self.parser.symbol())
            if self.parser.dest() is not None:
                print('dest: ' + self.parser.dest())
            if self.parser.comp() is not None:
                print('comp: ' + self.parser.comp())
            if self.parser.jump() is not None:
                print('jump: ' + self.parser.jump())
            print('line: ' + self.parser.advance())

            #Code(self.parser.dest(), self.parser.comp(), self.parser.jump(), self.parser.advance())