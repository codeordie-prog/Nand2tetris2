# VM Translator (Nand2Tetris)

A Python implementation of the VM Translator for the Nand2Tetris course. This translator converts VM code (similar to Java bytecode) to Hack Assembly language.

## Overview

The VM Translator processes `.vm` files and translates them into Hack Assembly (`.asm`) code. It handles:
- Arithmetic/logical commands
- Memory access commands
- Program flow commands
- Function calling commands

## Structure

```

## Usage

Run the translator with:

```bash
python VMTranslator.py path/to/file.vm
```

The translator can handle:
- Single .vm files
- Directories containing multiple .vm files

## Implementation Details

### Parser
- Handles parsing of VM commands
- Removes comments and whitespace
- Breaks commands into their components

### CodeWriter
- Translates VM commands to Hack Assembly
- Handles memory segments (local, argument, this, that, constant, static, temp, pointer)
- Implements arithmetic and logical operations
- Manages function calls and program flow

### VMTranslator
- Main class that coordinates parsing and code generation
- Handles file I/O
- Manages multiple file translation

## Testing

Test files are included to verify:
- Memory access commands
- Arithmetic operations
- Program flow
- Function calls

## Requirements

- Python 3.x
- No additional dependencies required

## Contributing

Feel free to submit issues and enhancement requests.



## Acknowledgments

This project is part of the Nand2Tetris course (The Elements of Computing Systems)
by Noam Nisan and Shimon Schocken.