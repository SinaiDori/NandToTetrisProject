import JackTokenizer


class CompileEngine:
    op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    def __init__(self, input_file_path, output_file_path):
        self.output_file = open(output_file_path, 'w')
        self.jack_tokenizer = JackTokenizer(input_file_path)
        self.indentation = 0
        self.class_name = ""
        self.compileClass()

    def process(self, str_list):
        if self.jack_tokenizer.current_token in str_list:
            self.printXMLToken(self.jack_tokenizer.current_token)
        else:
            print("syntax error")
        self.jack_tokenizer.advance()

    def processIdentifier(self):
        if self.jack_tokenizer.current_token_type == "IDENTIFIER":
            self.printXMLToken(self.jack_tokenizer.current_token)
        else:
            print("syntax error")
        self.jack_tokenizer.advance()

    def printXMLToken(self, token: str):
        self.output_file.write("  " * self.indentation + "<" +
                               self.jack_tokenizer.current_token_type.lower() + "> " + token + " </" + self.jack_tokenizer.current_token_type.lower() + ">\n")

    def compileClass(self):
        # TODO: implement
        pass

    def compileClassVarDec(self):
        self.output_file.write("  " * self.indentation + "<classVarDec>\n")
        self.indentation += 1
        self.process(["static", "field"])
        self.process(["int", "char", "boolean", self.class_name])
        self.processIdentifier()
        # Optional list of variables
        while self.jack_tokenizer.current_token == ",":
            self.process([","])
            self.processIdentifier()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</classVarDec>\n")

    def compileSubroutine(self):
        # TODO: implement
        pass

    def compileParameterList(self):
        if self.jack_tokenizer.current_token == "(":
            self.output_file.write(
                "  " * self.indentation + "<parameterList>\n")
            self.indentation += 1
            self.process(["("])
            self.process(["int", "char", "boolean", self.class_name])
            self.processIdentifier()
            # Optional list of variables
            while self.jack_tokenizer.current_token == ",":
                self.process([","])
                self.process(["int", "char", "boolean", self.class_name])
                self.processIdentifier()
            self.process([")"])
            self.indentation -= 1
            self.output_file.write(
                "  " * self.indentation + "</parameterList>\n")

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

    def compileVarDec(self):
        self.output_file.write("  " * self.indentation + "<varDec>\n")
        self.indentation += 1
        self.process(["var"])
        self.process(["int", "char", "boolean", self.class_name])
        self.processIdentifier()
        # Optional list of variables
        while self.jack_tokenizer.current_token == ",":
            self.process([","])
            self.processIdentifier()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</varDec>\n")

    def compileStatements(self):
        self.output_file.write("  " * self.indentation + "<statements>\n")
        self.indentation += 1
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

    def compileLet(self):
        # TODO: implement
        pass

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

    def compileDo(self):
        self.output_file.write("  " * self.indentation + "<doStatement>\n")
        self.indentation += 1
        self.process(["do"])
        self.compileSubroutineCall()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write("  " * self.indentation + "</doStatement>\n")

    def compileReturn(self):
        self.output_file.write("  " * self.indentation + "<returnStatement>\n")
        while self.jack_tokenizer.current_token in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.process(["return"])
        # Optional expression
        if self.jack_tokenizer.current_token != ";":
            self.compileExpression()
        self.process([";"])
        self.indentation -= 1
        self.output_file.write(
            "  " * self.indentation + "</returnStatement>\n")

    def compileExpression(self):
        self.output_file.write("  " * self.indentation + "<expression>\n")
        self.indentation += 1
        self.compileTerm()
        while self.jack_tokenizer.current_token in CompileEngine.op:
            self.process(CompileEngine.op)
            self.compileTerm()

    def compileTerm(self):
        # TODO: implement
        pass

    def compileExpressionList(self):
        # TODO: implement
        pass
