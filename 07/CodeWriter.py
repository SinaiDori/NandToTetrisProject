import os


class CodeWriter:
    segmentsWithPointersDict = {'local': 'LCL', 'argument': 'ARG',
                                'this': 'THIS', 'that': 'THAT', 'pointer 0': 'THIS', 'pointer 1': 'THAT'}

    def __init__(self, file):
        self.file = file

    def writeArithmetic(self, command: str):
        # use R13 and R14 as temp registers to store stack[SP-1] and stack[SP-2]
        pass

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
