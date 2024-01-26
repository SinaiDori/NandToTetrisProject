from Parser import Parser
from CodeWriter import CodeWriter
import os


class vmTranslator:
    def __init__(self, readfile, writefile):
        self.parser = Parser(readfile)
        self.codeWriter = CodeWriter(writefile)

    def translate(self):
        while self.parser.hasMoreLines():
            commandType = self.parser.commandType()

            if commandType == "C_ARITHMETIC":
                self.codeWriter.writeArithmetic(self.parser.arg1())
            elif commandType == "C_PUSH" or commandType == "C_POP":
                self.codeWriter.writePushPop(
                    commandType, self.parser.arg1(), self.parser.arg2())

            # elif
            # elif
            # elif
            # elif
            # elif
            # elif

            self.parser.advance()
