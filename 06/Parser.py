class Parser:
    A_INSTRUCTION = 'A_INSTRUCTION'
    C_INSTRUCTION = 'C_INSTRUCTION'
    L_INSTRUCTION = 'L_INSTRUCTION'

    # Remove empty lines, comments, and in-line comments
    def lineValidation(self):
        # create a list to hold the valid lines
        lines = []
        # loop through each line in the file
        for line in self.file.readlines():
            # check for obvious comment (starts with...)
            if line.strip() and not line.startswith("//") and not line.startswith("/*") and not line.startswith("*") and not line.startswith("*/"):
                # if we make it here, the line is not an obvious comment
                # the line does not start with a comment, check for in-line comment
                if "//" in line:
                    # if we make it here, the line has an in-line comment
                    # the line has an in-line comment, check if the part before the comment is not empty
                    if line.split("//")[0].strip() != "":
                        # if we make it here, the line has an in-line comment, and the part before the comment is not empty                        
                        # add the non-empty part before the comment to the list
                        lines.append(line.split("//")[0].strip())
                else:
                    # if we make it here, the line does not have an obvious comment or an in-line comment
                    lines.append(line.strip())
        return lines

    def __init__(self, file):
        self.file = file
        self.lines = self.lineValidation()
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
        else:
            return "null"
    
    def jump(self):
        if self.instructionType() == self.C_INSTRUCTION:
            if ";" in self.lines[self.currentLine]:
                return self.lines[self.currentLine].split(";")[1]
            else:
                return "null"
        else:
            return "null"
        
    def int_to_bin(self, i):
        return str(bin(i))[2:].zfill(16)