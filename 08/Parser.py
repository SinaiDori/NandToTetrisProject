class Parser:
    C_ARITHMETIC = 'C_ARITHMETIC'
    C_PUSH = 'C_PUSH'
    C_POP = 'C_POP'
    C_LABEL = 'C_LABEL'
    C_GOTO = 'C_GOTO'
    C_IF-GOTO = 'C_IF-GOTO'
    C_FUNCTION = 'C_FUNCTION'
    C_RETURN = 'C_RETURN'
    C_CALL = 'C_CALL'

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

    def commandType(self):
        if self.lines[self.currentLine].startswith("push"):
            return self.C_PUSH
        elif self.lines[self.currentLine].startswith("pop"):
            return self.C_POP
        elif self.lines[self.currentLine].startswith("label"):
            return self.C_LABEL
        elif self.lines[self.currentLine].startswith("goto"):
            return self.C_GOTO
        elif self.lines[self.currentLine].startswith("if-goto"):
            return self.C_IF-GOTO
        elif self.lines[self.currentLine].startswith("function"):
            return self.C_FUNCTION
        elif self.lines[self.currentLine].startswith("return"):
            return self.C_RETURN
        elif self.lines[self.currentLine].startswith("call"):
            return self.C_CALL
        else:
            return self.C_ARITHMETIC

    def arg1(self):
        if self.commandType() == self.C_ARITHMETIC:
            return self.lines[self.currentLine]
        else:
            return self.lines[self.currentLine].split(" ")[1]

    def arg2(self):
        if self.commandType() in [self.C_PUSH, self.C_POP, self.C_FUNCTION, self.C_CALL]:
            return self.lines[self.currentLine].split(" ")[2]
