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
                ha = HackAssembler(file)
                ha.assemble()
                file.close()
    else:
        if not sys.argv[1].endswith(".asm"):
            print("File is not an .asm file")
            return
        ha = HackAssembler(file)
        ha.assemble()
        file.close()
    
if __name__ == '__main__':
    main()