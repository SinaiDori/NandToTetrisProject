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


def main():
    filesList = []
    if os.path.isdir(sys.argv[1]):
        if not sys.argv[1].endswith("/"):
            sys.argv[1] += "/"
        fileName = sys.argv[1].split("/")[-2]
        writeFile = sys.argv[1] + fileName + ".asm"
        for filePath in os.listdir(sys.argv[1]):
            if filePath.endswith(".vm"):
                filesList.append(sys.argv[1] + filePath)
        vm = vmTranslator(filesList, writeFile)
        vm.translate()
        removeLastLine(sys.argv[1] + fileName + ".asm")
    else:
        if not sys.argv[1].endswith(".vm"):
            print("File is not an .asm file")
            return
        writeFile = sys.argv[1][:-3] + ".asm"
        filesList.append(sys.argv[1])
        vm = vmTranslator(filesList, writeFile)
        vm.translate()
        removeLastLine(sys.argv[1][:-3] + ".asm")


if __name__ == '__main__':
    main()
