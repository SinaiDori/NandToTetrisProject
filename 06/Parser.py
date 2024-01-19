class Parser:
    A_INSTRUCTION = 'A_INSTRUCTION'
    C_INSTRUCTION = 'C_INSTRUCTION'
    L_INSTRUCTION = 'L_INSTRUCTION'

    def __init__(self, file):
        self.file = file
        self.lines = [line.strip() for line in self.file.readlines() \
        # Remove empty lines
        if line.strip() \
        # Remove one-line comments
        and not line.startswith("//") \
        # Remove multi-line comments
        and not line.startswith("/*") \
        and not line.startswith("*") \
        and not line.startswith("*/")]
        self.currentLine = 0
    
    def hasMoreLines(self):
        return self.currentLine < len(self.lines)
    
    def advance(self):
        self.currentLine += 1
        return self.lines[self.currentLine - 1]
    
    def instructionType(self):
        if self.lines[self.currentLine].startswith("@"):
            return self.A_INSTRUCTION
        elif self.lines[self.currentLine].startswith("("):
            return self.L_INSTRUCTION
        else:
            return self.C_INSTRUCTION
    
    def symbol(self):
        if self.instructionType() == self.A_INSTRUCTION:
            return self.lines[self.currentLine][1:]
        elif self.instructionType() == self.L_INSTRUCTION:
            return self.lines[self.currentLine][1:-1]
        else:
            return "null"


    def dest(self):
        if self.instructionType() == self.C_INSTRUCTION:
            if "=" in self.lines[self.currentLine]:
                return self.lines[self.currentLine].split("=")[0]
            else:
                return "null"
    
    def comp(self):
        if self.instructionType() == self.C_INSTRUCTION:
            if "=" in self.lines[self.currentLine]:
                if ";" in self.lines[self.currentLine]:
                    return self.lines[self.currentLine].split("=")[1].split(";")[0]
                else:
                    return self.lines[self.currentLine].split("=")[1]
            else:
                return self.lines[self.currentLine].split(";")[0]
    
    def jump(self):
        if self.instructionType() == self.C_INSTRUCTION:
            if ";" in self.lines[self.currentLine]:
                return self.lines[self.currentLine].split(";")[1]
            else:
                return "null"