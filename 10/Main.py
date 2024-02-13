import sys
import os
from JackAnalyzer import JackAnalyzer


def main():
    read_files_paths_list = []
    if os.path.isdir(sys.argv[1]):
        if not sys.argv[1].endswith("/"):
            sys.argv[1] += "/"
        fileName = sys.argv[1].split("/")[:-1][:-4]
        for filePath in os.listdir(sys.argv[1]):
            if filePath.endswith(".jack"):
                read_files_paths_list.append(sys.argv[1] + filePath)
        ja = JackAnalyzer(read_files_paths_list)
        ja.analyze()
    else:
        if not sys.argv[1].endswith(".jack"):
            print("File is not an .asm file")
            return
        read_files_paths_list.append(sys.argv[1])
        ja = JackAnalyzer(read_files_paths_list)
        ja.analyze()


if __name__ == '__main__':
    main()