from JackTokenizer import JackTokenizer


class CompilationEngine:
    OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    STATEMENTS_OPENERS = ["let", "if", "while", "do", "return"]

    def __init__(self, input_file_path, output_file_path):
        self.output_file = open(output_file_path, 'w')
        self.jack_tokenizer = JackTokenizer(input_file_path)
        self.indentation = 0
        self.jack_tokenizer.advance()
        self.compileClass()
        self.output_file.close()
        self.jack_tokenizer.close()

    def process(self, str_list):
        if self.jack_tokenizer.current_token in str_list:
            if self.jack_tokenizer.current_token in ["<", ">", "&", "\""]:
                self.printXMLToken({"<": "&lt;", ">": "&gt;", "&": "&amp;", "\n": "&quot;"}[self.jack_tokenizer.current_token])
            else:
                self.printXMLToken(self.jack_tokenizer.current_token)
        else:
            print("(process) syntax error: \"" + str(self.jack_tokenizer.current_token) + "\"")
        # moved the advance to the printXMLToken method
        # self.jack_tokenizer.advance()

    def processIdentifier(self):
        if self.jack_tokenizer.current_token_type == "identifier":
            self.printXMLToken(self.jack_tokenizer.current_token)
        else:
            print("(processIdentifier) syntax error: \"" + str(self.jack_tokenizer.current_token) + "\" is not an identifier")
        # moved the advance to the printXMLToken method
        # self.jack_tokenizer.advance()

    def printXMLToken(self, token: str):
        self.output_file.write("  " * self.indentation + "<" +
                               self.jack_tokenizer.current_token_type + "> " + token + " </" + self.jack_tokenizer.current_token_type + ">\n")
        #ADDED!!!!!!!!!!!!!!!
        if (self.jack_tokenizer.hasMoreTokens()):
            self.jack_tokenizer.advance()

    def compileClass(self):
        self.output_file.write("  " * self.indentation + "<class>\n")
        self.indentation += 1
        self.process(["class"])
        self.processIdentifier()
        self.process(["{"])
        while self.jack_tokenizer.current_token in ["static", "field"]:
            self.compileClassVarDec()
        while self.jack_tokenizer.current_token in ["constructor", "function", "method"]:
            self.compileSubroutine()
        self.process(["}"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</class>\n")
    
    def compileType(self, extraList: list = []):
        if self.jack_tokenizer.current_token in ["int", "char", "boolean"] + extraList:
            self.process(["int", "char", "boolean"] + extraList)
        else:
            self.processIdentifier()

    # 'static'|'field' type varName(','varName)*';'
    def compileClassVarDec(self):
        self.output_file.write("  " * self.indentation + "<classVarDec>\n")
        self.indentation += 1
        self.process(["static", "field"])
        self.compileType()
        self.processIdentifier()
        # Optional list of variables
        while self.jack_tokenizer.current_token == ",":
            self.process([","])
            self.processIdentifier()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</classVarDec>\n")

    # ('constructor'|'function'|'method') ('void'|type) subroutineName '('parameterList')' subroutineBody
    def compileSubroutine(self):
        self.output_file.write("  " * self.indentation + "<subroutineDec>\n")
        self.indentation += 1
        self.process(["constructor", "function", "method"])
        self.compileType(["void"])
        self.processIdentifier()
        self.process(["("])
        self.compileParameterList()
        self.process([")"])
        self.compileSubroutineBody()
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</subroutineDec>\n")

    # ((type varName)(','type varName)*)?
    def compileParameterList(self):
        self.output_file.write(
                "  " * self.indentation + "<parameterList>\n")
        if self.jack_tokenizer.current_token != ")":
            self.indentation += 1
            self.compileType()
            self.processIdentifier()
            # Optional list of variables
            while self.jack_tokenizer.current_token == ",":
                self.process([","])
                self.compileType()
                self.processIdentifier()
            self.indentation -= 1
        self.output_file.write(
                "  " * self.indentation + "</parameterList>\n")

    # '{'varDec* statements'}'
    def compileSubroutineBody(self):
        self.output_file.write("  " * self.indentation + "<subroutineBody>\n")
        self.indentation += 1
        self.process(["{"])
        # Optional list of variables
        while self.jack_tokenizer.current_token == "var":
            self.compileVarDec()
        self.compileStatements()
        self.process(["}"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</subroutineBody>\n")

    # 'var' type varName(','varName)*';'
    def compileVarDec(self):
        self.output_file.write("  " * self.indentation + "<varDec>\n")
        self.indentation += 1
        self.process(["var"])
        self.compileType()
        self.processIdentifier()
        # Optional list of variables
        while self.jack_tokenizer.current_token == ",":
            self.process([","])
            self.processIdentifier()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</varDec>\n")

    # statement*
    def compileStatements(self):
        self.output_file.write("  " * self.indentation + "<statements>\n")
        self.indentation += 1
        if self.jack_tokenizer.current_token in CompilationEngine.STATEMENTS_OPENERS:
            while self.jack_tokenizer.current_token in ["let", "if", "while", "do", "return"]:
                if self.jack_tokenizer.current_token == "let":
                    self.compileLet()
                elif self.jack_tokenizer.current_token == "if":
                    self.compileIf()
                elif self.jack_tokenizer.current_token == "while":
                    self.compileWhile()
                elif self.jack_tokenizer.current_token == "do":
                    self.compileDo()
                elif self.jack_tokenizer.current_token == "return":
                    self.compileReturn()
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</statements>\n")

    # 'let' varName('['expression']')?'='expression';'
    def compileLet(self):
        self.output_file.write("  " * self.indentation + "<letStatement>\n")
        self.indentation += 1
        self.process(["let"])
        self.processIdentifier()
        if self.jack_tokenizer.current_token == "[":
            self.process(["["])
            self.compileExpression()
            self.process(["]"])
        self.process(["="])
        self.compileExpression()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</letStatement>\n")

    # 'if' '('expression')''{'statements'}' ('else''{'statements'}')?
    def compileIf(self):
        self.output_file.write("  " * self.indentation + "<ifStatement>\n")
        self.indentation += 1
        self.process(["if"])
        self.process(["("])
        self.compileExpression()
        self.process([")"])
        self.process(["{"])
        self.compileStatements()
        self.process(["}"])
        # else
        if self.jack_tokenizer.current_token == "else":
            self.process(["else"])
            self.process(["{"])
            self.compileStatements()
            self.process(["}"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</ifStatement>\n")

    # 'while''('expression')''{'statements'}'
    def compileWhile(self):
        self.output_file.write("  " * self.indentation + "<whileStatement>\n")
        self.indentation += 1
        self.process(["while"])
        self.process(["("])
        self.compileExpression()
        self.process([")"])
        self.process(["{"])
        self.compileStatements()
        self.process(["}"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</whileStatement>\n")
    
    # subroutineName'('expressionList')'|(className|varName)'.'subroutineName'('expressionList')'
    # def compileSubroutineCall(self):
    #     self.processIdentifier()
    #     if self.jack_tokenizer.current_token == "(":
    #         self.process(["("])
    #         self.compileExpressionList()
    #         self.process([")"])
    #     else:
    #         self.processIdentifier()
    #         self.process(["."])
    #         self.processIdentifier()
    #         self.process(["("])
    #         self.compileExpressionList()
    #         self.process([")"])

    # 'do' subroutineCall';'
    def compileDo(self):
        self.output_file.write("  " * self.indentation + "<doStatement>\n")
        self.indentation += 1
        self.process(["do"])
        self.processIdentifier()
        if self.jack_tokenizer.current_token == "(":
            self.process(["("])
            self.compileExpressionList()
            self.process([")"])
        else:
            self.process(["."])
            self.processIdentifier()
            self.process(["("])
            self.compileExpressionList()
            self.process([")"])
        self.process([";"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</doStatement>\n")

    # 'return' expression?';'
    def compileReturn(self):
        self.output_file.write("  " * self.indentation + "<returnStatement>\n")
        self.indentation += 1
        self.process(["return"])
        # Optional expression
        if self.jack_tokenizer.current_token != ";":
            self.compileExpression()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write(
            "  " * self.indentation + "</returnStatement>\n")

    # term (op term)*
    def compileExpression(self):
        self.output_file.write("  " * self.indentation + "<expression>\n")
        self.indentation += 1
        self.compileTerm()
        while self.jack_tokenizer.current_token in CompilationEngine.OP:
            self.process(CompilationEngine.OP)
            self.compileTerm()
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</expression>\n")

    # subroutineName integerConstant|stringConstant|keywordConstant|varName|varName'['expression']'|'('expression')'|unaryOp term
    def compileTerm(self):
        self.output_file.write("  " * self.indentation + "<term>\n")
        self.indentation += 1
        if self.jack_tokenizer.current_token_type in ["integerConstant", "stringConstant", "keyword"]:
            self.printXMLToken(self.jack_tokenizer.current_token)
        elif self.jack_tokenizer.current_token == "(":
            self.process(["("])
            self.compileExpression()
            self.process([")"])
        elif self.jack_tokenizer.current_token in ["-", "~"]:
            self.process(["-", "~"])
            self.compileTerm()
        else:
            self.processIdentifier()
            if self.jack_tokenizer.current_token == "[":
                self.process(["["])
                self.compileExpression()
                self.process(["]"])
            elif self.jack_tokenizer.current_token == "(":
                self.process(["("])
                self.compileExpressionList()
                self.process([")"])
            elif self.jack_tokenizer.current_token == ".":
                self.process(["."])
                self.processIdentifier()
                self.process(["("])
                self.compileExpressionList()
                self.process([")"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</term>\n")

    # (expression(','expression)*)?
    def compileExpressionList(self):
        # check if there is at least one expression
        self.output_file.write("  " * self.indentation + "<expressionList>\n")
        if self.jack_tokenizer.current_token != ")":
            self.indentation += 1
            self.compileExpression()
            # Optional list of expressions
            while self.jack_tokenizer.current_token == ",":
                self.process([","])
                self.compileExpression()
            self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</expressionList>\n")
