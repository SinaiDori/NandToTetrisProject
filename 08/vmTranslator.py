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
            elif commandType == "C_LABEL":
                self.codeWriter.writeLabel(self.parser.arg1())
            elif commandType == "C_GOTO":
                self.codeWriter.writeGoto(self.parser.arg1())
            elif commandType == "C_IF-GOTO":
                self.codeWriter.writeIf(self.parser.arg1())
            elif commandType == "C_FUNCTION":
                self.codeWriter.writeFunction(
                    self.parser.arg1(), self.parser.arg2())
            elif commandType == "C_CALL":
                self.codeWriter.writeCall(
                    self.parser.arg1(), self.parser.arg2())
            elif commandType == "C_RETURN":
                self.codeWriter.writeReturn()

            self.parser.advance()
