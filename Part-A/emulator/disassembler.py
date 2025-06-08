from typing import Callable
from shared import utils

type InstEncoder = Callable

# -- INITIALIZATIONS

instruction_map: dict[str, Callable] = {}

# - Instructions
instr_type: dict[str, str] = {
    "0000": "Type1",
    "0001": "Type2",
    "0010": "Type3",
    "0011": "Type4",
    "0100": "Type5",
    "0101": "Type6",
    "0110": "Type7",
    "0111": "Type8",
    "100X": "Type9",
    "1010": "Type10",
    "1011": "Type11",
    "1100": "Type12",
    "1101": "Type13",
    "1110": "Type14",
    "1111": "Type15"
}
instr_16_bit_type: list[str] = ["Type5", "Type6", "Type7", "Type9",  "Type10", "Type11", "Type12", "Type13", "Type14", "Type15"]

instr_branch_imm: list[str] = ["bnz-a", "bnz-b", "beqz", "bnez",
    "beqz-cf", "bnez-cf",
    "bnz-d", "b", "call", "b-bit"]
instr_reg_imm: list[str] = ["rarb", "rcrd", "acc", "r4"]

instr_reg_arg: list[str] = [
    "inc*-reg",     # Increment REG[RRR]
    "dec*-reg",     # Decrement REG[RRR]
    "to-reg",       # ACC → REG[RRR]
    "from-reg"      # REG[RRR] → ACC
]

instr_no_arg: list[str] = [
    "rot-r",       # 00000000
    "rot-l",       # 00000001
    "rot-rc",      # 00000010
    "rot-lc",      # 00000011
    "from-mba",    # 00000100
    "to-mba",      # 00000101
    "from-mdc",    # 00000110
    "to-mdc",      # 00000111
    "addc-mba",    # 00001000
    "add-mba",     # 00001001
    "subc-mba",    # 00001010
    "sub-mba",     # 00001011
    "inc*-mba",    # 00001100
    "dec*-mba",    # 00001101
    "inc*-mdc",    # 00001110
    "dec*-mdc",    # 00001111
    "and-ba",      # 00011010
    "xor-ba",      # 00011011
    "or-ba",       # 00011100
    "and*-mba",    # 00011101
    "xor*-mba",    # 00011110
    "or*-mba",     # 00011111
    "clr-cf",      # 00101010
    "set-cf",      # 00101011
    "ret",         # 00101110
    "from-ioa",    # 00110010
    "inc",         # 00110001
    "bcd",         # 00110110
    "shutdown",    # 00110111 
    "nop",         # 00111110
    "dec",         # 00111111
]

# - Registers

registers: dict[str, str] = {"000": "RA", "001": "RB", "010": "RC", "011" : "RD", "100": "RE"}
bin_registers: list[int] = [0b000, 0b001, 0b010, 0b011, 0b100]
concat_reg: dict[str, str] = {"0101" : "rarb", "0110" : "rcrd"}
opcodes: list[str] = ["0001", "0010"]
branches: list[str, str] = {
    "bnz-a" : "10100",
    "bnz-b" : "10101",
    "beqz" : "10110",
    "bnez" : "10111",
    "beqz-cf" : "11000",
    "bnez-cf" : "11001",
    "bnz-d" : "11011"
}
jump_or_branch: list[str] = ["ret", "bnz-a", "bnz-b", "beqz", "b-bit", "bnez", "beqz-cf", "bnez-cf", "bnz-d", "b", "call"]
from_operation: dict[str, str] = {
    "add" : "01000000",
    "sub" : "01000001",
    "and" : "01000010",
    "xor" : "01000011",
    "or"  : "01000100",
    "r4"  : "01000110",
 }
to_operation: dict[str, str] = {v: k for k, v in from_operation.items()}

# - Immediates

immediates_4: list[int] = [f"{i:04b}" for i in range(2**4)]
immediates_8: list[int] = [f"{i:08b}" for i in range (2**8)]
immediates_11: list[int] = [f"{i:011b}" for i in range(2**11)]
immediates_12: list[int] = [f"{i:012b}" for i in range(2**12)]
immediates_k: list[int] = [f"{i:02b}" for i in range(2**2)]

# --- Decorators

def dasm(code: str):
    def _dasm(f: Callable):
        instruction_map[code] = f
        return f
    return _dasm

def localizer(binary, opcode, op, reg):
    @dasm(binary)
    def _(): 
        pass

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
            return f"inc*-reg {int(utils.to_strbin(reg), 2)}" if op == 0 else f"dec*-reg {int(utils.to_strbin(reg), 2)}"
        elif opcode == "0010":
            return f"to-reg {int(utils.to_strbin(reg), 2)}" if op == 0 else f"from-reg {int(utils.to_strbin(reg), 2)}"

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

# Type 3 (25-31)

@dasm("00101010")
def _(): return "clr-cf"

@dasm("00101011")
def _(): return "set-cf"

@dasm("00101110")
def _(): return "ret"

# Type 4 (32-48)

@dasm("00110010")
def _(): return "from-ioa"

@dasm("00110001")
def _(): return "inc"

@dasm("00110110")
def _(): return "bcd"

@dasm("0011011100111110")
def _(): return "shutdown"

@dasm("00111110")
def _(): return "nop"

@dasm("00111111")
def _(): return "dec"

# ======================================================

# Type 5 (49-64)

def localizer(binary, ar, imm):
    @dasm(binary)
    def _(): 
        return f"{ar} {int(utils.to_strbin(imm), 2)}"
        
for ar in from_operation.keys():
    for imm in immediates_4:
        binary = f"{from_operation[ar]}0000{imm}"
        localizer(binary, ar, imm)

# ======================================================

# Type 6 (65-66)

def localizer(binary,imm, ar):
    @dasm(binary)
    def _(): 
        if (ar == "0101"):
            return f"rarb {int(utils.to_strbin(f"{imm}"), 2)}"
        elif (ar == "0110"):
            return f"rcrd {int(utils.to_strbin(f"{imm}"), 2)}"

for ar in concat_reg.keys():
    for imm in immediates_8:
        # binary = f"{ar}{imm[4:8]}0000{imm[8:]}"
        binary = f"{ar}{imm[4:8]}0000{imm[:4]}"
        localizer(binary, imm, ar)

# ======================================================

# Type 7 (67) # acc <imm>

def localizer(binary,imm):
    @dasm(binary)
    def _(): 
        return f"acc {int(utils.to_strbin(imm), 2)}"
        
for imm in immediates_4:
    binary = f"0111{imm}"
    localizer(binary, imm)

# ======================================================


# Type 8 (68) # b-bit <k> <imm>

def localizer(binary, k, imm):
    @dasm(binary)
    def _(): 
        return f"b-bit {int(utils.to_strbin(k), 2)}{int(utils.to_strbin(imm), 2)}"
        
for k in immediates_k:
    for imm in immediates_11:
        binary = f"100{k}{imm}"
        localizer(binary, k, imm)
        
# ======================================================

# Type 9-13 (69-76)

def localizer(binary, branch, imm):
    @dasm(binary)
    def _(): 
        return f"{branch} {int(utils.to_strbin(imm), 2)}"
        
for branch in branches.keys():
    for imm in immediates_11:
        binary = f"{branches[branch]}{imm}"
        localizer(binary, branch, imm)

# ======================================================

# Type 14-15

def localizer(binary, branch, imm):
    @dasm(binary)
    def _(): 
        if (branch == 0):
            return f"b {int(utils.to_strbin(imm), 2)}"
        elif (branch == 1):
            return f"call {int(utils.to_strbin(imm), 2)}"
        
for i in range(2):
    for imm in immediates_12:
        if (i == 0):
            binary = f"{1110}{imm}"
            localizer(binary, i, imm)
        elif (i == 1):
            binary = f"{1111}{imm}"
            localizer(binary, i, imm)

