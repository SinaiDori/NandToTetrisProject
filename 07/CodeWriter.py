import os


class CodeWriter:
    segmentsWithPointersDict = {'local': 'LCL', 'argument': 'ARG',
                                'this': 'THIS', 'that': 'THAT', 'pointer 0': 'THIS', 'pointer 1': 'THAT'}

    def __init__(self, file):
        self.file = file
        self.counter = 0

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------

    def writeArithmetic(self, command: str):
        self.file.write(f'// {command}\n')
        self.file.write('@SP\n')
        self.file.write('M=M-1\n')
        self.file.write('A=M\n')
        self.file.write('D=M\n')
        self.file.write('@R13\n')
        self.file.write('M=D\n')
        self.file.write('@SP\n')
        self.file.write('M=M-1\n')
        self.file.write('A=M\n')
        self.file.write('D=M\n')
        self.file.write('@R14\n')
        self.file.write('M=D\n')
        # at this point we have stack[SP-1] in R13 and stack[SP-2] in R14
        # let's do the arithmetic:
        if command == 'add' or command == 'sub' or command == 'and' or command == 'or':
            action = '+' if command == 'add' else (
                '-' if command == 'sub' else ('&' if command == 'and' else '|'))
            self.file.write('@R13\n')
            self.file.write('D=M\n')
            self.file.write('@R14\n')
            self.file.write(f'D=D{action}M\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')
        elif command == 'neg' or command == 'not':
            action = '-' if command == 'neg' else '!'
            self.file.write('@R13\n')
            self.file.write(f'D={action}M\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')
        elif command == 'eq' or command == 'gt' or command == 'lt':
            self.file.write('@R13\n')
            self.file.write('D=M\n')
            self.file.write('@R14\n')
            self.file.write('D=D-M\n')
            self.file.write(f'@TRUE{self.counter}\n')
            self.file.write(f'D;J{command.upper()}\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=0\n')
            self.file.write(f'@END{self.counter}\n')
            self.file.write('0;JMP\n')
            self.file.write(f'(TRUE{self.counter})\n')
            self.file.write('@SP\n')
            self.file.write('A=M\n')
            self.file.write('M=-1\n')
            self.file.write(f'(END{self.counter})\n')
            self.file.write('@SP\n')
            self.file.write('M=M+1\n')
            self.counter += 1


# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------


    def writePushPop(self, command: str, segment: str, index: int):
        if command == 'C_PUSH':
            self.file.write(f'// push {segment} {index}\n')
            if segment == 'constant':
                self.file.write(f'@{index}\n')
                self.file.write('D=A\n')
                self.file.write('@SP\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M+1\n')
            elif segment in self.segmentsWithPointersDict.keys():
                self.file.write(f'@{self.segmentsWithPointersDict[segment]}\n')
                self.file.write('D=M\n')
                self.file.write(f'D=D+{index}\n')
                self.file.write('A=D\n')
                self.file.write('D=M\n')
                self.file.write('@SP\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M+1\n')
            elif segment == 'static':
                self.file.write(
                    f'@{os.path.basename(self.file.name)}.{index}\n')
                self.file.write('D=M\n')
                self.file.write('@SP\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M+1\n')
            elif segment == 'temp':
                self.file.write(f'@{5+index}\n')
                self.file.write('D=M\n')
                self.file.write('@SP\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M+1\n')
            elif segment == 'pointer':
                self.file.write(
                    f'@{self.segmentsWithPointersDict[str(segment) + str(index)]}\n')
                self.file.write('A=M\n')
                self.file.write('D=M\n')
                self.file.write('@SP\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M+1\n')

        elif command == 'C_POP':
            self.file.write(f'// pop {segment} {index}\n')
            if segment in self.segmentsWithPointersDict.keys():
                self.file.write(f'@{self.segmentsWithPointersDict[segment]}\n')
                self.file.write('D=M\n')
                self.file.write(f'D=D+{index}\n')
                self.file.write('@R13\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M-1\n')
                self.file.write('A=M\n')
                self.file.write('D=M\n')
                self.file.write('@R13\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
            elif segment == 'static':
                self.file.write(
                    f'@{os.path.basename(self.file.name)}.{index}\n')
                self.file.write('D=A\n')
                self.file.write('@R13\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M-1\n')
                self.file.write('A=M\n')
                self.file.write('D=M\n')
                self.file.write('@R13\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
            elif segment == 'temp':
                self.file.write('@SP\n')
                self.file.write('M=M-1\n')
                self.file.write('A=M\n')
                self.file.write('D=M\n')
                self.file.write(f'@{5+index}\n')
                self.file.write('M=D\n')
            elif segment == 'pointer':
                self.file.write(
                    f'@{self.segmentsWithPointersDict[str(segment) + str(index)]}\n')
                self.file.write('D=M\n')
                self.file.write('@R13\n')
                self.file.write('M=D\n')
                self.file.write('@SP\n')
                self.file.write('M=M-1\n')
                self.file.write('A=M\n')
                self.file.write('D=M\n')
                self.file.write('@R13\n')
                self.file.write('A=M\n')
                self.file.write('M=D\n')
