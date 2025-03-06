from codewriter import CodeWriter
from pathlib import Path
import os
import sys

class VMTranslator:
    def __init__(self, filename:str):
        
        self.base_dir = os.path.dirname(filename)

        print(self.base_dir)

        # check if its a directory
        if os.path.isdir(filename):
            self.files = [os.path.join(filename, f) for f in os.listdir(filename) if f.endswith('.vm')]

            self.inputfile = self.files[0] if self.files else None
            self.file_index = 0

        else:
            self.files =[filename]
            self.file_index = 0
            self.inputfile=filename

          


    # checks whether there is a next file
    def hasMoreFiles(self):
        return self.file_index<len(self.files)
    

    # advances to next file
    def advance(self):
        
        self.file_index+=1

        if self.hasMoreFiles():
            # set input file to the next file
            self.inputfile = self.files[self.file_index]


    def main(self):

         #initialize code writer
        codewriter = CodeWriter(input_file=self.inputfile, dir=self.base_dir)

        while self.hasMoreFiles():
            
            codewriter.processfiles(self.inputfile)
            self.advance()
      


if __name__ == "__main__":
    filename = sys.argv[1]
    translator = VMTranslator(filename)
    translator.main()
