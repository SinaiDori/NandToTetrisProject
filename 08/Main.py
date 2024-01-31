import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter
from vmTranslator import vmTranslator


def removeLastLine(filePath):
    content = ""
    with open(filePath, 'r') as file:
        content = file.read()

    # Remove the last newline character
    content = content[:-1]

    with open(filePath, 'w') as file:
        file.write(content)
    

    def writeBootstrap(file):
        file.write('@256\n')
        file.write('D=A\n')
        file.write('@SP\n')
        file.write('M=D\n')
        # TODO: call Sys.init - after completing writeCall in CodeWriter.py


def main():
    return_address_counter = 0
    try:
        readFile = open(sys.argv[1], 'r')
    except IsADirectoryError:
        if not sys.argv[1].endswith("/"):
            sys.argv[1] += "/"
        fileName = sys.argv[1].split("/")[-2]
        with open(sys.argv[1] + fileName + ".asm", 'w') as writeFile:
            for filePath in os.listdir(sys.argv[1]):
                if filePath.endswith(".vm"):
                    readFile = open(sys.argv[1] + filePath, 'r')
                    vm = vmTranslator(readFile, writeFile)
                    vm.translate()
                    readFile.close()
        removeLastLine(sys.argv[1] + fileName + ".asm")
    else:
        if not sys.argv[1].endswith(".vm"):
            print("File is not an .asm file")
            return
        with open(sys.argv[1][:-3] + ".asm", 'w') as asmFile:
            vm = vmTranslator(readFile, asmFile)
            vm.translate()
            readFile.close()
        removeLastLine(sys.argv[1][:-3] + ".asm")


if __name__ == '__main__':
    main()
