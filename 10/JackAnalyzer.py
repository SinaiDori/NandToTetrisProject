from CompilationEngine import CompilationEngine


class JackAnalyzer:
    def __init__(self, read_files_paths_list):
        self.read_files_paths_list = read_files_paths_list
    
    def analyze(self):
        for read_file_path in self.read_files_paths_list:
            write_file_path = read_file_path[:-5] + ".xml"
            ce = CompilationEngine(read_file_path, write_file_path)