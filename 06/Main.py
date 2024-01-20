import sys
import os
from HackAssembler import HackAssembler

def main():
    try:
        file = open(sys.argv[1], 'r')
    except IsADirectoryError:
        for strPath in os.listdir(sys.argv[1]):
            if strPath.endswith(".asm"):
                file = open(sys.argv[1] + "/" + strPath, 'r')
                with open(file.name[:-4] + ".hack", 'w') as hackFile:
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