# Arch-242 Instruction Set Architecture 

## Preface

The implementation is developed by a group of (4) CS-21 students, namely, **Glenn Paragas, Louise Gabriel Vilar, Luis Antonio Sarmiento,** and **Ethan Renell Mislang.**

The specifications can be found in this [Mkdocs Page](https://cs21.upd-dcs.work/labs/project/#arch-242-architecture-overview)

## Contributions

### Part A: Arch-242 Assembler + Emulator + Snake Game

#### Part A1
- PARAGAS, Glenn 
- MISLANG, Ethan Renell 
- VILAR, Louise Gabriel

#### Part A2
- PARAGAS, Glenn
- VILAR, Louise Gabriel

#### Part A3
- PARAGAS, Glenn
- VILAR, Louise Gabriel

### Part B: Logisim-based Arch-242 implementation
- SARMIENTO, Luis Antonio
- MISLANG, Ethan Renell 

## Instruction A1

### Arch-242 Assembler Guide

Welcome to the **Arch-242 Instruction Set Architecture**! This guide walks you through how to use the assembler in coding an Arch-242 assembly program.

### Dependencies of the Assembler

The assembler directory contains the following utilities for the assembler:

- `__init__.py` – Initializes the assembler package
- `asm_instructions.py` - Contains the decorators for assembling each arch-242 instructions

### How to Run

```
python assembler.py <my_program.asm> <bin or hex>
```

1. Open the your terminal and type the program into the command line
2. Enter the sample <my_program.asm> as an argument in the command line to select which file assembly program file to let the assembler read.
3. Choose between `bin` or `hex` as the second argument in the command line
4. If `bin` was selected the corresponding assembled program should be presented as lines of binary strings w/out `0b`
5. If `hex` was selected the corresponding assembled program should be presented as lines of hexadecimal strings w/out `0x`
6. Locate the output file dedicated for the assembled program it should be found in the same directory and is named as `Arch242_output.asm`.


## Instruction A2

### Arch-242 Emulator Guide

Welcome to the **Arch-242 Instruction Set Architecture**! This guide walks you through how to use the emulator in coding an Arch-242 assembly program

### Dependencies of the Assembler

The assembler directory contains the following utilities for the assembler:

- `__init__.py`- Initializes the emulator package
- `disassembler.py` - Disassembles the assembled Arch-242 instruction assembly code
- `emu_instructions.py`- Contains the disassmbled instruction from arch242
- `test_emulator.py` - Simple unittesting file using pytest

### How to Run

In order to run the snake game using the emulator we must first run the assembler to get the assembled Arch-242 program.

Run the `snake.asm` first using the assembler to get the assembled code 

```
python assembler.py snake.asm <bin or hex>
```

After running the command with the valid arguments presented, we will now go to the assembled program name `"Arch242_output.asm"` in the same directory.

Now, with the `"Arch242_output.asm"` file at hand, we will now run the emulator with the argument `Arch242_output.asm`

```
python emulator.py Arch242_output.asm
```
### Navigating Through The Arch242 Emulator Pyxel Window

Once the command ran succesfully a `Pyxel` window will abruptly shows up in the screen. The `Pyxel` window represents the Snake Game.

Snake Game is a pyxel-based snake game that is encoded using the custom Arch-242 instruction set. The game screen includes the following:
- **Game HUD:** Displays the instruction on how to play, accumulated score, LED currently on and LED currently off.
- **Benchmark:** Displays the current status of the Arch242 CPU Emulator. It includes: current fetched instruction (in bin and assembly), program counter `(PC)` and register values `(RA, RB, RC, RD, RE, ACC, CF, TEMP)` at the current cycle.  
- **Game Grid:** Displays an LED matrix of 10 rows x 20 columns. This actually displays the `snake` the `player` will play as.
  
### Gameplay

The game starts with the snake of length `3` moving to the right, the player can use the keys `W`, `A`, `S`, `D` to change the direction of the snake. 

The objective of the game is to eat up to `15 food blocks` and by eating each `1 food block` will increase the length of the snake by `1` and score of the player by `1`. The maximum possible score achievable is 15 and by reaching 15 the game will `shutdown` implying the player won the snake game. Note that whenever the snake touches it's own `body` or `game border` the game will halt implying the player died hence needed to restart the game again.







