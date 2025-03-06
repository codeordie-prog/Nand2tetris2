"""
* Python VMEmulator for parsing VMCode to Hack Assembly
* Classes - 3 classes as defined by the API ParserClass, CodeWriter, VMTranslatorClass
* ParserClass - parses each VMCommand to its lexical element

"""
from pathlib import Path

class Parser:

    def __init__(self, file:Path):

        #opens input file and gets it ready to parse
        #returns _
        self.index = 0
        self.vmcode = []
        self.ARITHMETIC_COMMANDS = ["add", "sub", "neg", "eq", "lt", "gt", "and", "or", "not"]
        self.MEMORY_SEGMENT_COMMANDS = ["C_PUSH","C_POP","C_FUNCTION","C_CALL","C_IF_GOTO","C_GOTO","C_LABEL","C_RETURN"]
       


        with open(file, "r") as input_file:

            # emit empty lines and comments
            self.vmcode = [line.strip() for line in input_file.readlines() if not line.startswith("//") and line.strip()]
            self.current_command = self.vmcode[self.index]
            print(self.vmcode)


    def get_current_index(self)->int:
        return int(self.index)           
    
    def hasMoreCommands(self)->bool:
        #are there more commands to process?
        print(f"Currently at index : {self.index}")
        return self.index<len(self.vmcode)


    def advance(self):
        print(f"Advancing the index : from {self.index} to next..")
        self.index += 1
        if self.index < len(self.vmcode):
            self.current_command = self.vmcode[self.index]

    def commandtype(self):
        """
        Returns const representing the type of the current command
        """

        # get current command

        cmd = self.current_command.split()[0]
        print(f"Current command is : {self.current_command}")

        if cmd == "push":
            return "C_PUSH"
        
        elif cmd == "pop":
            return "C_POP"
        
        elif cmd =="call":
            return "C_CALL"
        
        elif cmd == "if-goto":
            return "C_IF_GOTO"
        
        elif cmd == "goto":
            return "C_GOTO"
        
        elif cmd == "function":
            return "C_FUNCTION"
        
        elif cmd == "return":
            return "C_RETURN"
        
        elif cmd == "label":
            return "C_LABEL"
        
        elif cmd in self.ARITHMETIC_COMMANDS:
            return "C_ARITHMETIC"
        

        
        else:
            return



    def args_1(self)->str:
        """
        Returns first argument of the current command e.g in the case of C_ARITHMETIC, the command itself [add,sub, etc]
        Should not be called if the current command is C_RETURN
        """

        cmd_type = self.commandtype()

        #if cmd_type != "C_RETURN":

        if cmd_type == "C_ARITHMETIC":
            return self.current_command.split()[0] # return add, sub or any arithmetic command
        
        elif cmd_type == "C_FUNCTION":
            function = self.current_command.split()[1]
            vars = self.current_command.split()[2]
            return [function,vars]
        
        elif cmd_type == "C_CALL":
            function = self.current_command.split()[1]
            vars = self.current_command.split()[2]

            return [function,vars]
        
        else:

            return self.current_command.split()[1] # return the memory segment part 'local', 'argument' etc



    def args_2(self)->int:
        """
        Returns the second argument of the current command, 
        should only be called if the command is C_PUSH, C_POP, C_FUNCTION, C_CASE
        """

        
        current_command = self.current_command

        cmd_type = self.commandtype()

        #if cmd_type not in self.MEMORY_SEGMENT_COMMANDS:
            #return
        
        if cmd_type == "C_IF_GOTO":
            return current_command.split()[1]
        
        elif cmd_type == "C_GOTO":
            return current_command.split()[1]
        
        elif cmd_type == "C_FUNCTION":
            return current_command.split()[2]
        
        elif cmd_type == "C_LABEL":
            return current_command.split()[1]
        
        elif cmd_type == "C_RETURN":
            return
        
        else:
      
            RAM_TARGET = current_command.split()[2]
            return RAM_TARGET  #e.g push local 2 we return 2






#file = Path(r"C:\Users\LENOVO\Documents\nand_2_tetris_2\nand2tetris\projects\7\MemoryAccess\BasicTest\BasicTest.vm")

#parser = Parser(file=file)

#print(parser.args_1())