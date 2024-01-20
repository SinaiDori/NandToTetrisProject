import sys
import os
from HackAssembler import HackAssembler

def main():
    try:
        file = open(sys.argv[1], 'r')
    except IsADirectoryError:
        for filePath in os.listdir(sys.argv[1]):
            if filePath.endswith(".asm"):
                file = open(sys.argv[1] + filePath, 'r')
                with open(str(sys.argv[1] + filePath)[:-4] + ".hack", 'w') as hackFile:
                    ha = HackAssembler(file)
                    ha.firstPass()
                    ha.secondPass(hackFile)
                    file.close()
    else:
        if not sys.argv[1].endswith(".asm"):
            print("File is not an .asm file")
            return
        with open(sys.argv[1][:-4] + ".hack", 'w') as hackFile:
                    ha = HackAssembler(file)
                    ha.firstPass()
                    ha.secondPass(hackFile)
                    file.close()
    
if __name__ == '__main__':
    main()