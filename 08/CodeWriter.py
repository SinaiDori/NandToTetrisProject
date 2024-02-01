import os


class CodeWriter:
    segmentsWithPointersDict = {'local': 'LCL', 'argument': 'ARG',
                                'this': 'THIS', 'that': 'THAT'}

    def __init__(self, filePath):
        self.writeFile = open(filePath, 'w')
        self.counter = 0
        self.return_value_counter = 0
        self.current_read_file_name = ""
        self.current_function_name = ""

    def setFileName(self, file_name):
        self.current_read_file_name = file_name

    def resetReturnValueCounter(self):
        self.return_value_counter = 0

    def setCurrentFunctionName(self, function_name):
        self.current_function_name = function_name

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
    def writeBootstrap(self):
        self.writeFile.write('@256\n')
        self.writeFile.write('D=A\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=D\n')
        self.writeCall('Sys.init', 0)

    def writeArithmetic(self, command: str):
        self.writeFile.write(f'// {command}\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M-1\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@R13\n')
        self.writeFile.write('M=D\n')
        # at this point we have the first value in R13
        # later on - if the command is add, sub, and, or, eq, gt, lt - we will have the second value in R14
        # let's do the arithmetic:
        if command == 'add' or command == 'sub' or command == 'and' or command == 'or':
            action = '+' if command == 'add' else (
                '-' if command == 'sub' else ('&' if command == 'and' else '|'))
            # put the second value in R14
            self.writeFile.write('@SP\n')
            self.writeFile.write('M=M-1\n')
            self.writeFile.write('A=M\n')
            self.writeFile.write('D=M\n')
            self.writeFile.write('@R14\n')
            self.writeFile.write('M=D\n')
            # do the arithmetic
            self.writeFile.write('@R13\n')
            self.writeFile.write('D=M\n')
            self.writeFile.write('@R14\n')
            self.writeFile.write(f'D=M{action}D\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('A=M\n')
            self.writeFile.write('M=D\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('M=M+1\n')
        elif command == 'neg' or command == 'not':
            action = '-' if command == 'neg' else '!'
            self.writeFile.write('@R13\n')
            self.writeFile.write(f'D={action}M\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('A=M\n')
            self.writeFile.write('M=D\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('M=M+1\n')
        elif command == 'eq' or command == 'gt' or command == 'lt':
            # put the second value in R14
            self.writeFile.write('@SP\n')
            self.writeFile.write('M=M-1\n')
            self.writeFile.write('A=M\n')
            self.writeFile.write('D=M\n')
            self.writeFile.write('@R14\n')
            self.writeFile.write('M=D\n')
            # do the arithmetic
            self.writeFile.write('@R13\n')
            self.writeFile.write('D=M\n')
            self.writeFile.write('@R14\n')
            self.writeFile.write('D=M-D\n')
            self.writeFile.write(f'@TRUE{self.counter}\n')
            self.writeFile.write(f'D;J{command.upper()}\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('A=M\n')
            self.writeFile.write('M=0\n')
            self.writeFile.write(f'@END{self.counter}\n')
            self.writeFile.write('0;JMP\n')
            self.writeFile.write(f'(TRUE{self.counter})\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('A=M\n')
            self.writeFile.write('M=-1\n')
            self.writeFile.write(f'(END{self.counter})\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('M=M+1\n')
            self.counter += 1


# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------


    def writePushPop(self, command, segment, index):
        if command == 'C_PUSH':
            self.writeFile.write(f'// push {segment} {index}\n')
            if segment == 'constant':
                self.writeFile.write(f'@{index}\n')
                self.writeFile.write('D=A\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M+1\n')
            elif segment in self.segmentsWithPointersDict.keys():
                self.writeFile.write(
                    f'@{self.segmentsWithPointersDict[segment]}\n')
                self.writeFile.write('D=M\n')
                for i in range(int(index)):
                    self.writeFile.write('D=D+1\n')
                self.writeFile.write('A=D\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M+1\n')
            elif segment == 'pointer':
                thisORthat = 'THIS' if index == '0' else 'THAT'
                self.writeFile.write(f'@{thisORthat}\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M+1\n')
            elif segment == 'static':
                #self.writeFile.write(f'@{os.path.basename(self.writeFile.name)}.{index}\n')
                self.writeFile.write(f'@{self.current_read_file_name}.{index}\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M+1\n')
            elif segment == 'temp':
                self.writeFile.write(f'@{5+int(index)}\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M+1\n')
            elif segment == 'pointer':
                self.writeFile.write(
                    f'@{self.segmentsWithPointersDict[str(segment) + str(index)]}\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M+1\n')

        elif command == 'C_POP':
            self.writeFile.write(f'// pop {segment} {index}\n')
            if segment in self.segmentsWithPointersDict.keys():
                self.writeFile.write(
                    f'@{self.segmentsWithPointersDict[segment]}\n')
                self.writeFile.write('D=M\n')
                for i in range(int(index)):
                    self.writeFile.write('D=D+1\n')
                self.writeFile.write('@R13\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M-1\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write('@R13\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
            elif segment == 'static':
                #self.writeFile.write(f'@{os.path.basename(self.writeFile.name)}.{index}\n')
                self.writeFile.write(f'@{self.current_read_file_name}.{index}\n')
                self.writeFile.write('D=A\n')
                self.writeFile.write('@R13\n')
                self.writeFile.write('M=D\n')
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M-1\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write('@R13\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('M=D\n')
            elif segment == 'temp':
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M-1\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write(f'@{5+int(index)}\n')
                self.writeFile.write('M=D\n')
            elif segment == 'pointer':
                thisORthat = 'THIS' if index == '0' else 'THAT'
                self.writeFile.write('@SP\n')
                self.writeFile.write('M=M-1\n')
                self.writeFile.write('A=M\n')
                self.writeFile.write('D=M\n')
                self.writeFile.write(f'@{thisORthat}\n')
                self.writeFile.write('M=D\n')

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------

    def writeLabel(self, label):
        self.writeFile.write('// label\n')
        self.writeFile.write(
            f'({self.current_function_name}${label})\n')

    def writeGoto(self, label):
        self.writeFile.write('// goto\n')
        self.writeFile.write(
            f'@{self.current_function_name}${label}\n')
        self.writeFile.write('0;JMP\n')

    def writeIf(self, label):
        self.writeFile.write('// if-goto\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M-1\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write(
            f'@{self.current_function_name}${label}\n')
        self.writeFile.write('D;JNE\n')

    def writeFunction(self, functionName, nVars):
        self.writeFile.write(
            f'// function {functionName} {nVars}\n')
        self.writeFile.write(
            f'({functionName})\n')
        self.writeFile.write('@LCL\n')
        self.writeFile.write('A=M\n')
        for _ in range(int(nVars)):
            self.writeFile.write('M=0\n')
            self.writeFile.write('A=A+1\n')
            self.writeFile.write('D=A\n')
            self.writeFile.write('@SP\n')
            self.writeFile.write('M=M+1\n')
            self.writeFile.write('A=D\n')
        

    def writeCall(self, functionName, nArgs):
        self.writeFile.write(
            f'// call {functionName} {nArgs}\n')
        # Saves the return address
        self.writeFile.write(
            f'@{self.current_function_name}$ret.{self.return_value_counter}\n')
        self.writeFile.write('D=A\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('M=D\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M+1\n')
        # Saves the caller's LCL
        self.writeFile.write('@LCL\n')
        #self.writeFile.write('D=A\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('M=D\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M+1\n')
        # Saves the caller's ARG
        self.writeFile.write('@ARG\n')
        #self.writeFile.write('D=A\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('M=D\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M+1\n')
        # Saves the caller's THIS
        self.writeFile.write('@THIS\n')
        #self.writeFile.write('D=A\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('M=D\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M+1\n')
        # Saves the caller's THAT
        self.writeFile.write('@THAT\n')
        #self.writeFile.write('D=A\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('M=D\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M+1\n')
        # Repositions ARG
        self.writeFile.write('@SP\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@5\n')
        self.writeFile.write('D=D-A\n')
        self.writeFile.write(f'@{nArgs}\n')
        self.writeFile.write('D=D-A\n')
        self.writeFile.write('@ARG\n')
        self.writeFile.write('M=D\n')
        # Repositions LCL
        self.writeFile.write('@SP\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@LCL\n')
        self.writeFile.write('M=D\n')
        # Transfer control to the callee
        self.writeFile.write(
            f'@{functionName}\n')
        self.writeFile.write('0;JMP\n')
        # inject the return label
        self.writeFile.write(
            f'({self.current_function_name}$ret.{self.return_value_counter})\n')
        self.return_value_counter += 1

    def writeReturn(self):
        self.writeFile.write('// return\n')
        # gets the address at the frame's end
        self.writeFile.write('@LCL\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@R13\n')  # R13 = endFrame
        self.writeFile.write('M=D\n')
        # gets the return address
        self.writeFile.write('@R13\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@5\n')
        self.writeFile.write('D=D-A\n')
        self.writeFile.write('A=D\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@R14\n')  # R14 = retAddr
        self.writeFile.write('M=D\n')
        # puts the return value for the caller
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=M-1\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@ARG\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('M=D\n')
        # repositions SP
        self.writeFile.write('@ARG\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@SP\n')
        self.writeFile.write('M=D+1\n')
        # restores THAT
        self.writeFile.write('@R13\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@1\n')
        self.writeFile.write('D=D-A\n')
        self.writeFile.write('A=D\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@THAT\n')
        self.writeFile.write('M=D\n')
        # restores THIS
        self.writeFile.write('@R13\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@2\n')
        self.writeFile.write('D=D-A\n')
        self.writeFile.write('A=D\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@THIS\n')
        self.writeFile.write('M=D\n')
        # restores ARG
        self.writeFile.write('@R13\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@3\n')
        self.writeFile.write('D=D-A\n')
        self.writeFile.write('A=D\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@ARG\n')
        self.writeFile.write('M=D\n')
        # restores LCL
        self.writeFile.write('@R13\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@4\n')
        self.writeFile.write('D=D-A\n')
        self.writeFile.write('A=D\n')
        self.writeFile.write('D=M\n')
        self.writeFile.write('@LCL\n')
        self.writeFile.write('M=D\n')
        # jumps to the return address
        self.writeFile.write('@R14\n')
        self.writeFile.write('A=M\n')
        self.writeFile.write('0;JMP\n')

# --------------------------------------------------------------------

    def close(self):
        self.writeFile.close()
