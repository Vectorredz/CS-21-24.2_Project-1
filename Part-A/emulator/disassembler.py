from typing import Callable
from pathlib import Path
from sys import argv

type InstEncoder = Callable

instruction_map: dict[str, Callable] = {}

registers = {"000": "RA", 
             "001": "RB", 
             "010": "RC", 
             "O11" : "RD", 
             "100": "RE"}

bin_registers = [0b000, 0b001, 0b010, 0b011, 0b100]

opcodes = ["0001", "0010"]

branches = {
    "bnz-a" : "10100",
    "bnz-b" : "10101",
    "beqz" : "10110",
    "bnez" : "10111",
    "beqz-cf" : "11000",
    "bnez-cf" : "11001",
    "b-timer" : "11010",
    "bnz-d" : "11011"
}
instr_type = {
    "0000": "Type1",
    "0001": "Type2",
    "0011": "Type3",
    "0100": "Type4",
    "0101": "Type5",
    "0110": "type6",
    "0111": "Type7",
    "100X": "Type8",
    "1010": "Type9",
    "1011": "Type10",
    "1100": "Type11",
    "1101": "Type12",
    "1110": "Type13",
    "1111": "Type14"
}

instr_16_bit = ["Type4", "Type8", "Type9", "Type10", "Type11", "Type12", "Type13", "Type14"]

from_operation = {
    "add" : "01000000",
    "sub" : "01000001",
    "and" : "01000010",
    "xor" : "01000011",
    "or"  : "01000100",
    "r4"  : "01000110",
    "timer" : "01000111"
 }

to_operation = {v: k for k, v in from_operation.items()}

immediates_4 = [f"{i:04b}" for i in range(2**4)]
immediates_11 = [f"{i:011b}" for i in range(2**11)]
immediates_12 = [f"{i:012b}" for i in range(2**12)]
immediates_k = [f"{i:02b}" for i in range(2**2)]

def dasm(code: str):
    def _dasm(f: Callable):
        instruction_map[code] = f
        return f
    return _dasm

# ======================================================

# Type 1 (1-16)

@dasm("00000000")
def _(): return "rot-r"

@dasm("00000001")
def _(): return "rot-l"

@dasm("00000010")
def _(): return "rot-rc"

@dasm("00000011")
def _(): return "rot-lc"

@dasm("00000100")
def _(): return "from-mba"

@dasm("00000101")
def _(): return "to-mba"

@dasm("00000110")
def _(): return "from-mdc"

@dasm("00000111")
def _(): return "to-mdc"

@dasm("00001000")
def _(): return "addc-mba"

@dasm("00001001")
def _(): return "add-mba"

@dasm("00001010")
def _(): return "subc-mba"

@dasm("00001011")
def _(): return "sub-mba"

@dasm("00001100")
def _(): return "inc*-mba"

@dasm("00001101")
def _(): return "dec*-mba"

@dasm("00001110")
def _(): return "inc*-mdc"

@dasm("00001111")
def _(): return "dec*-mdc"

# ======================================================

# Type 2 (17-24)

def localizer(binary, opcode, op, reg):
    @dasm(binary)
    def _(): 
        if opcode == "0001":
            return f"inc*-reg {reg}" if op == 0 else f"dec*-reg {reg}"
        elif opcode == "0010":
            return f"to-reg {reg}" if op == 0 else f"from-reg {reg}"

for opcode in opcodes:
    for op in range(2):
        for reg in registers:
            localizer(f"{opcode}{reg}{op}", opcode, op, reg)

@dasm("00011010")
def _(): return "and-ba"

@dasm("00011011")
def _(): return "xor-ba"

@dasm("00011100")
def _(): return "or-ba"

@dasm("00011101")
def _(): return "and*-mba"

@dasm("00011110")
def _(): return "xor*-mba"

@dasm("00011111")
def _(): return "or*-mba"

# ======================================================

# Type 3 (25-48)

@dasm("00101010")
def _(): return "clr-cf"

@dasm("00101011")
def _(): return "set-cf"

@dasm("00101100")
def _(): return "set-ei"

@dasm("00101101")
def _(): return "clr-ei"

@dasm("00101110")
def _(): return "ret"

@dasm("00101111")
def _(): return "retc"

@dasm("00110000")
def _(): return "from-pa"

@dasm("00110001")
def _(): return "inc"

@dasm("00110010")
def _(): return "to-ioa"

@dasm("00110011")
def _(): return "to-iob"

@dasm("00110100")
def _(): return "to-ioc"

@dasm("00110110")
def _(): return "bcd"

@dasm("0011011100111110")
def _(): return "shutdown"

@dasm("00111000")
def _(): return "timer-start"

@dasm("00111001")
def _(): return "timer-end"

@dasm("00111010")
def _(): return "from-timerl"

@dasm("00111011")
def _(): return "from-timerh"

@dasm("00111100")
def _(): return "to-timerl"

@dasm("00111101")
def _(): return "to-timerh"

@dasm("00111110")
def _(): return "nop"

@dasm("00111111")
def _(): return "dec"

# ======================================================

# Type 4 (49-64)

def localizer(binary, ar, imm):
    @dasm(binary)
    def _(): 
        return f"{ar} {imm}"
        
for ar in from_operation.keys():
    for imm in immediates_4:
        binary = f"{from_operation[ar]}0000{imm}"
        localizer(binary, ar, imm)

# ======================================================


# TODO --- nops (nakakatamad)

# type 5 

# TODO --- RARBS

# ======================================================

# type 7 (67)
def localizer(binary,imm):
    @dasm(binary)
    def _(): 
        return f"acc {imm}"
        
for imm in immediates_4:
    binary = f"0111{imm}"
    localizer(binary, imm)

# type 8 (68)

def localizer(binary, k, imm):
    @dasm(binary)
    def _(): 
        return f"b-bit {k}{imm}"
        
for k in immediates_k:
    for imm in immediates_11:
        binary = f"100{k}{imm}"
        localizer(binary, k, imm)

# type 9-14 (69-78)
def localizer(binary, branch, imm):
    @dasm(binary)
    def _(): 
        return f"{branch} {imm}"
        
for branch in branches.keys():
    for imm in immediates_11:
        binary = f"{branches[branch]}{imm}"
        localizer(binary, branch, imm)
