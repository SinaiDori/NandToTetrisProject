class JackTokenizer:
    # CONSTANTS!

    # Token types
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"
    # Keywords
    CLASS = "CLASS"
    METHOD = "METHOD"
    FUNCTION = "FUNCTION"
    CONSTRUCTOR = "CONSTRUCTOR"
    INT = "INT"
    BOOLEAN = "BOOLEAN"
    CHAR = "CHAR"
    VOID = "VOID"
    VAR = "VAR"
    STATIC = "STATIC"
    FIELD = "FIELD"
    LET = "LET"
    DO = "DO"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    THIS = "THIS"

    # Symbols
    SYMBOLS = "{}()[].,;+-*/&|<>=~"


# Remove empty lines, comments, and in-line comments


    def lineValidation(self):
        # create a list to hold the valid lines
        lines = ""
        # loop through each line in the file
        for line in self.read_file.readlines():
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
                        lines += (line.split("//")[0].strip())
                else:
                    # if we make it here, the line does not have an obvious comment or an in-line comment
                    lines += (line.strip())
        self.read_file.close()
        return lines

    def __init__(self, read_file_path: str):
        self.read_file = open(read_file_path, "r")
        self.lines = self.lineValidation()
        self.current_index = 0
        self.current_token = None
        self.current_token_type = None
    
    def close(self):
        self.read_file.close()

    def hasMoreTokens(self):
        return self.current_index < len(self.lines)

    def advance(self):
        while self.lines[self.current_index] == " " or self.lines[self.current_index] == "\t":
            self.current_index += 1
        # symbol
        if self.lines[self.current_index] in JackTokenizer.SYMBOLS:
            self.current_token = self.lines[self.current_index]
            self.current_token_type = JackTokenizer.SYMBOL
            self.current_index += 1
        # integerConstant
        elif self.lines[self.current_index].isnumeric():
            temp_token = ""
            while self.lines[self.current_index].isnumeric():
                temp_token += self.lines[self.current_index]
                self.current_index += 1
            self.current_token = temp_token
            self.current_token_type = JackTokenizer.INT_CONST
        # stringConstant
        elif self.lines[self.current_index] == "\"":
            temp_token = ""
            self.current_index += 1
            while self.lines[self.current_index] != "\"":
                temp_token += self.lines[self.current_index]
                self.current_index += 1
            self.current_token = temp_token
            self.current_token_type = JackTokenizer.STRING_CONST
            self.current_index += 1
        # keyword or identifier
        else:
            temp_token = ""
            while self.lines[self.current_index] != " " and (self.lines[self.current_index].isalpha() or self.lines[self.current_index].isnumeric() or self.lines[self.current_index] == "_"):
                temp_token += self.lines[self.current_index]
                self.current_index += 1
            self.current_token = temp_token
            if temp_token.upper() in [JackTokenizer.CLASS, JackTokenizer.METHOD, JackTokenizer.FUNCTION, JackTokenizer.CONSTRUCTOR, JackTokenizer.INT, JackTokenizer.BOOLEAN, JackTokenizer.CHAR, JackTokenizer.VOID, JackTokenizer.VAR, JackTokenizer.STATIC, JackTokenizer.FIELD, JackTokenizer.LET, JackTokenizer.DO, JackTokenizer.IF, JackTokenizer.ELSE, JackTokenizer.WHILE, JackTokenizer.RETURN, JackTokenizer.TRUE, JackTokenizer.FALSE, JackTokenizer.NULL, JackTokenizer.THIS]:
                self.current_token_type = JackTokenizer.KEYWORD
            else:
                self.current_token_type = JackTokenizer.IDENTIFIER

    def tokenType(self):
        return self.current_token_type

    def keyWord(self):
        return self.current_token.upper()

    def symbol(self):
        return self.current_token

    def identifier(self):
        return self.current_token

    def intVal(self):
        return int(self.current_token)

    def stringVal(self):
        return self.current_token
