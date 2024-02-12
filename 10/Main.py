import sys
import os
from JackAnalyzer import JackAnalyzer

# def removeLastLine(filePath):
#     content = ""
#     with open(filePath, 'r') as file:
#         content = file.read()

#     # Remove the last newline character
#     content = content[:-1]

#     with open(filePath, 'w') as file:
#         file.write(content)


def main():
    read_files_paths_list = []
    if os.path.isdir(sys.argv[1]):
        if not sys.argv[1].endswith("/"):
            sys.argv[1] += "/"
        fileName = sys.argv[1].split("/")[-4]
        for filePath in os.listdir(sys.argv[1]):
            if filePath.endswith(".jack"):
                read_files_paths_list.append(sys.argv[1] + filePath)
        ja = JackAnalyzer(read_files_paths_list)
        ja.analyze()
        # removeLastLine(sys.argv[1] + fileName + ".asm")
    else:
        if not sys.argv[1].endswith(".jack"):
            print("File is not an .asm file")
            return
        read_files_paths_list.append(sys.argv[1])
        ja = JackAnalyzer(read_files_paths_list)
        ja.analyze()
        # removeLastLine(sys.argv[1][:-3] + ".asm")


if __name__ == '__main__':
    main()