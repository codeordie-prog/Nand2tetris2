from parser import Parser
import os
from pathlib import Path

class CodeWriter:
    def __init__(self, input_file: str, dir:any):
        self.inputfile = input_file
        self.dir = dir
        self.newFileHasStarted = False
        self.hasMoreFiles = False
        self.fileName = None
        self.return_counter = 0
        #self.output_file = os.path.splitext(input_file)[0] + ".asm"
        self.output_file = os.path.join(self.dir, "output.asm")
        self.parser = None
        self.CMD_ABBR = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": "temp",
            "constant": "CST",
            "pointer":"POINTER"
        }



        with open(self.output_file, "w") as f:

            print(f"Opened an output file at {self.dir}")

            hack_asm = self.writeInit()
            f.write(hack_asm)

    # process file
    def processfiles(self, filename:str):
        
        # set filename
        self.setFileName(fileName=filename)
        # handle the bootstrapping here

        with open(self.output_file, "a") as self.file:

            while self.parser.hasMoreCommands():
                # Get current command
                current_command = self.parser.current_command
                print(f"Current command is: {current_command}")

                # Process command
                cmd_type = self.parser.commandtype()
                print(f"And the command type is: {cmd_type}")

                if cmd_type == "C_PUSH":
                    print("Writing push...")
                    hack_asm = self.writePush()
                    self.file.write(hack_asm)
                    self.parser.advance()

                elif cmd_type == "C_POP":
                    hack_asm = self.writePop()
                    self.file.write(hack_asm)
                    self.parser.advance()

                elif cmd_type == "C_ARITHMETIC":
                    hack_asm = self.writeArithmetic()
                    self.file.write(hack_asm)
                    self.parser.advance()

                elif cmd_type == "C_IF_GOTO":
                    label = self.parser.args_2()
                    hack_asm = self.writeIf(label=label)
                    self.file.write(hack_asm)
                    self.parser.advance()


                elif cmd_type == "C_FUNCTION":
                    params_list = self.parser.args_1()
                    function =params_list[0]
                    vars = params_list[1]
                    hack_asm = self.writeFunction(functionName=function, numVars=vars)
                    self.file.write(hack_asm)
                    self.parser.advance()

                elif cmd_type == "C_GOTO":
                    label = self.parser.args_2()
                    hack_asm = self.writeGoto(label=label)
                    self.file.write(hack_asm)
                    self.parser.advance()


                elif cmd_type == "C_LABEL":
                    label = self.parser.args_2()
                    hack_asm = self.writeLabel(label=label)
                    self.file.write(hack_asm)
                    self.parser.advance()

                elif cmd_type == "C_CALL":
                    params_list = self.parser.args_1()
                    function = params_list[0]
                    numAgs = params_list[1]

                    hack_asm = self.writeCall(functionName=function, numArgs=numAgs)
                    self.file.write(hack_asm)
                    self.parser.advance()

                elif cmd_type == "C_RETURN":
                    hack_asm = self.writeReturn()
                    self.file.write(hack_asm)
                    self.parser.advance()

                else:
                    self.parser.advance()

            
            # set has started to false
            self.newFileHasStarted=False
            self.fileName = None

            if not self.hasMoreFiles:

                with open(self.output_file, "a") as file:

                    hack_asm_end_loop = """
                    (END_OF_THE_PROGRAM)
                    @END_OF_THE_PROGRAM
                    0;JMP
                    """
                    file.write(hack_asm_end_loop)

                

    def writeArithmetic(self):
        command = self.parser.args_1()

        if command == "add":
            hack_asm = """
            @SP
            AM=M-1
            D=M
            A=A-1
            M=D+M
            """
            return hack_asm

        elif command == "sub":
            hack_asm = """
            @SP
            AM=M-1
            D=M
            A=A-1
            M=M-D
            """
            return hack_asm

        elif command == "lt":
            
            hack_asm = f"""
            @SP
            AM=M-1
            D=M
            A=A-1
            D=M-D
            @TRUE_LT
            D;JLT
            @SP
            A=M-1
            M=0
            @END_LT
            0;JMP
            (TRUE_LT)
            @SP
            A=M-1
            M=-1
            (END_LT)
            """
            return hack_asm

        elif command == "gt":
           
            hack_asm = f"""
            @SP
            AM=M-1
            D=M
            A=A-1
            D=M-D
            @TRUE_GT
            D;JGT
            @SP
            A=M-1
            M=0
            @END_GT
            0;JMP
            (TRUE_GT)
            @SP
            A=M-1
            M=-1
            (END_GT)
            """
            return hack_asm

        elif command == "eq":
    
            hack_asm = f"""
            @SP
            AM=M-1
            D=M
            A=A-1
            D=M-D
            @TRUE_EQ
            D;JEQ
            @SP
            A=M-1
            M=0
            @END_EQ
            0;JMP
            (TRUE_EQ)
            @SP
            A=M-1
            M=-1
            (END_EQ)
            """
            return hack_asm

        elif command == "and":
            hack_asm = """
            @SP
            AM=M-1
            D=M
            A=A-1
            M=D&M
            """
            return hack_asm

        elif command == "or":
            hack_asm = """
            @SP
            AM=M-1
            D=M
            A=A-1
            M=D|M
            """
            return hack_asm
        
        elif command == "neg":
            hack_asm = """
            @SP
            A=M-1
            M=-M
            """
            return hack_asm

        elif command == "not":
            hack_asm = """
            @SP
            A=M-1
            M=!M
            """
            return hack_asm

        else:
            return ""

    def writePush(self):
        memory_address = self.parser.args_1()

        if memory_address == "constant":
            i = self.parser.args_2()
            hack_asm = f"""
            @{i}
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
            return hack_asm

        elif memory_address == "static":
            i = self.parser.args_2()
            #base_name = os.path.splitext(os.path.basename(self.fileName))[0]
            base_name = Path(self.fileName)# gets 'Class1' from Class1.vm
            hack_asm = f"""
            @{base_name}.{i}
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
            return hack_asm

        elif memory_address == "temp":
            i = self.parser.args_2()
            temp_address = 5 + int(i)
            hack_asm = f"""
            @{temp_address}
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
            return hack_asm
        
        elif memory_address == "pointer":
            index = int(self.parser.args_2())
            if index == 0:
                hack_asm = """
                @THIS
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """
            elif index == 1:
                hack_asm = """
                @THAT
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """
            return hack_asm

        else:
            cmd_abbr = self.CMD_ABBR.get(memory_address, "")
            i = self.parser.args_2()
            hack_asm = f"""
            @{i}
            D=A
            @{cmd_abbr}
            A=M+D
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
            return hack_asm

    def writePop(self):
        memory_address = self.parser.args_1()

        if memory_address == "static":
            i = self.parser.args_2()
            #base_name = os.path.splitext(os.path.basename(self.fileName))[0]
            base_name = Path(self.fileName)
            hack_asm = f"""
            @SP
            AM=M-1
            D=M
            @{base_name}.{i}
            M=D
            """
            return hack_asm

        elif memory_address == "temp":
            i = self.parser.args_2()
            temp_address = 5 + int(i)
            hack_asm = f"""
            @SP
            AM=M-1
            D=M
            @{temp_address}
            M=D
            """
            return hack_asm
        
        elif memory_address == "pointer":
            index = int(self.parser.args_2())
            if index == 0:
                hack_asm = """
                @SP
                AM=M-1
                D=M
                @THIS
                M=D
                """
            elif index == 1:
                hack_asm = """
                @SP
                AM=M-1
                D=M
                @THAT
                M=D
                """
            return hack_asm

        else:
            cmd_abbr = self.CMD_ABBR.get(memory_address, "")
            i = self.parser.args_2()
            hack_asm = f"""
            @{i}
            D=A
            @{cmd_abbr}
            D=M+D
            @R13
            M=D
            @SP
            AM=M-1
            D=M
            @R13
            A=M
            M=D
            """
            return hack_asm
        

    def writeInit(self):
        hack_asm = """
        @256  // Initialize stack pointer
        D=A
        @SP
        M=D

        // Call Sys.init
        @Sys.init$ret.0  // Push return address
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @LCL  // Push LCL
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @ARG  // Push ARG
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @THIS  // Push THIS
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @THAT  // Push THAT
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        @SP  // ARG = SP - 5 - 0
        D=M
        @5
        D=D-A
        @0
        D=D-A
        @ARG
        M=D

        @SP  // LCL = SP
        D=M
        @LCL
        M=D

        @Sys.init  // Jump to Sys.init
        0;JMP

        (Sys.init$ret.0)  // Return address label
        """
        return hack_asm

    def setFileName(self, fileName:str):
        #informs code writer that a new vm file has started(called by the main program)
        self.newFileHasStarted=True
        self.hasMoreFiles = True
        self.fileName=Path(fileName).stem
        self.newFileHasStarted = True

        #self.file = open(self.output_file, "a")
        # open parser
        self.parser = Parser(file=fileName)
        print(f"Successfully opened output file for {fileName}")
        return

    def writeLabel(self,label:str):
        #writes assemble code that effects the label command
        function_name = self.fileName if self.fileName else ""
        full_label = f"{function_name}${label}"
        return f"""
                ({full_label})
                """


    def writeGoto(self,label:str):
        #writes assemble code that effects goto commands
        function_name = self.fileName if self.fileName else ""
        full_label = f"{function_name}${label}"
        return f"""
                @{full_label}
                0;JMP 
                """


    def writeIf(self,label:str):
        #writes assembly code that effectc if goto commands
        function_name = self.fileName if self.fileName else ""
        full_label = f"{function_name}${label}"
        return f"""
            @SP
            AM=M-1

            D=M

            @{full_label}  //Jump if True else dont jump
            D;JNE

            """

    def writeFunction(self, functionName: str, numVars: int):
        # Function label
        label = f"({functionName})\n"

        # Initialize local variables to 0
        push_cmd = ""
        for _ in range(int(numVars)):
            push_cmd += """
                @0    // Load 0
                D=A   // Store 0 in D
                @SP   // Push D onto the stack
                A=M
                M=D
                @SP   // Increment SP
                M=M+1
            """

    

        return label + push_cmd



    def writeCall(self, functionName:str, numArgs:int):
        # Writes assembly code that effects call command
        self.return_counter += 1
        
        return_label = f"{functionName}$ret.{self.return_counter}"
        
        ARG_displ = int(numArgs) + 5
        push_cmd = f"""
            @{return_label} //push return address
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1

            @LCL //push local segment of caller
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            
            @ARG //push ARG of caller
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1

            @THIS //push this of caller
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1

            @THAT // push that of caller
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1

            @SP // set ARG = SP-n-5
            D=M
            @{ARG_displ} //SP-n-5
            D=D-A
            @ARG
            M=D

            @SP
            D=M
            @LCL // set LCL=SP
            M=D

            @{functionName} //goto
            0;JMP

            ({return_label}) //insert the return label
        """
        
        return push_cmd

    def writeReturn(self):
        # Writes assembly code for return command
        return_cmd = f"""
            // endFrame = LCL
            @LCL
            D=M
            @R13    // R13 is endFrame
            M=D
            
            // retAddr = *(endFrame-5)
            @5
            A=D-A   // A = LCL-5
            D=M     // D = *(LCL-5)
            @R14    // R14 is retAddr
            M=D
            
            // *ARG = pop()
            @SP
            AM=M-1
            D=M
            @ARG
            A=M
            M=D
            
            // SP = ARG+1
            @ARG
            D=M+1
            @SP
            M=D
            
            // THAT = *(endFrame-1)
            @R13
            D=M
            @1
            A=D-A
            D=M
            @THAT
            M=D
            
            // THIS = *(endFrame-2)
            @R13
            D=M
            @2
            A=D-A
            D=M
            @THIS
            M=D
            
            // ARG = *(endFrame-3)
            @R13
            D=M
            @3
            A=D-A
            D=M
            @ARG
            M=D
            
            // LCL = *(endFrame-4)
            @R13
            D=M
            @4
            A=D-A
            D=M
            @LCL
            M=D
            
            // goto retAddr
            @R14
            A=M
            0;JMP
        """
        return return_cmd


    def close(self):
        # Add the infinite loop at the end
        with open(self.output_file, "a") as file:
            hack_asm_end_loop = """
            (END_OF_THE_PROGRAM)
            @END_OF_THE_PROGRAM
            0;JMP
            """
            file.write(hack_asm_end_loop)


#CodeWriter(input_file=r"C:\Users\LENOVO\Documents\nand_2_tetris_2\nand2tetris\projects\7\MemoryAccess\BasicTest\BasicTest.vm")