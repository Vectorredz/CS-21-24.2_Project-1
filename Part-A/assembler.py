from typing import Callable
from pathlib import Path

type InstEncoder = Callable

instruction_map: dict[str, InstEncoder] = {}

def new(name: str):
    def _new(f: InstEncoder):
        instruction_map[name] = f
    return _new
def fix_width(num: str, digits: int): #sign extends
    assert len(num) <= digits
    return (num[0] * (len(num)-digits)) + num
def to_bin(num: str, digits: int):
    return fix_width(bin(int(num))[2:], digits)
def to_dec(num: str, digits: int):
    return fix_width(num, digits)


@new("rot_r")
def _(): return "00000000"

@new("rot_l")
def _(): return "00000001"

@new("rot_rc")
def _(): return "00000010"

@new("rot_lc")
def _(): return "00000011"

@new("from-mba")
def _(): return "00000100"

@new("to-mba")
def _(): return "00000101"

@new("from-mdc")
def _(): return "00000110"

@new("to-mdc")
def _(): return "00000111"

@new("addc-mba")
def _(): return "00001000"

@new("add-mba")
def _(): return "00001001"

@new("subc-mba")
def _(): return "00001010"

@new("sub-mba")
def _(): return "00001011"

@new("inc*-mba")
def _(): return "00001100"

@new("dec*-mba")
def _(): return "00001101"

@new("inc*-mdc")
def _(): return "00001110"

@new("dec*-mdc")
def _(): return "00001111"

@new("inc*-reg")
def _(reg):
    return f"0001{to_bin(reg, 3)}0"

@new("dec*-reg")
def _(reg):
    return f"0001{to_bin(reg, 3)}1"

@new("and-ba")
def _(): return "00011010"

@new("xor-ba")
def _(): return "00011011"

@new("or-ba")
def _(): return "00011100"

@new("and*-mba")
def _(): return "00011101"

@new("xor*-mba")
def _(): return "00011110"

@new("or*-mba")
def _(): return "00011111"

@new("to-reg")
def _(reg):
    return f"0010{to_bin(reg, 3)}0"

@new("from-reg")
def _(reg):
    return f"0010{to_bin(reg, 3)}1"

@new("clr-cf")
def _(): return "00101010"

@new("set-cf")
def _(): return "00101011"

@new("set-ei")
def _(): return "00101100"

@new("clr-ei")
def _(): return "00101101"

@new("ret")
def _(): return "00101110"

@new("retc")
def _(): return "00101111"

@new("from-pa")
def _(): return "00110000"

@new("inc")
def _(): return "00110001"

@new("to-ioa")
def _(): return "00110010"

@new("to-iob")
def _(): return "00110011"

@new("to-ioc")
def _(): return "00110100"

@new("bcd")
def _(): return "00110110"

@new("shutdown")
def _(): return "0011011100111110"

@new("timer-start")
def _(): return "00111000"

@new("timer-end")
def _(): return "00111001"

@new("from-timerl")
def _(): return "00111010"

@new("from-timerh")
def _(): return "00111011"

@new("to-timerl")
def _(): return "00111100"

@new("to-timerh")
def _(): return "00111101"

@new("nop")
def _(): return "00111110"

@new("dec")
def _(): return "00111111"

@new("add")
def _(imm):
    return f"010000000000{to_bin(imm, 4)}"

@new("sub")
def _(imm):
    return f"010000010000{to_bin(imm, 4)}"

@new("and")
def _(imm):
    return f"010000100000{to_bin(imm, 4)}"

@new("xor")
def _(imm):
    return f"010000110000{to_bin(imm, 4)}"

@new("or")
def _(imm):
    return f"010001000000{to_bin(imm, 4)}"

@new("r4")
def _(imm):
    return f"010001100000{to_bin(imm, 4)}"

@new("timer")
def _(imm):
    return f"010001110000{to_bin(imm, 4)}"




# ======================================================
# TODO wtf is this? (nops + rarb/rcrd same encoding)

@new("–")                                      # instruction 38
def _(): return "00110101"

@new("-")                                      # instruction 54
def _(imm):
    return f"010001010000{to_bin(imm, 4)}"

@new("–")                                      # instructions 57 - 64
def _(): return "01001000"

@new("–")
def _(): return "01001001"

@new("–")
def _(): return "01001010"

@new("–")
def _(): return "01001011"

@new("YYY")
def _(): return "01001100"

@new("YYY")
def _(): return "01001101"

@new("YYY")
def _(): return "01001110"

@new("YYY")
def _(): return "01001111"


@new("rarb")
def _(imm):
    imm = to_bin(imm, 8)
    YYYY = imm[:5]
    XXXX = imm[5:]
    return f"0101{XXXX}0000{YYYY}"

@new("rcrd")
def _(imm):
    imm = to_bin(imm, 8)
    YYYY = imm[:5]
    XXXX = imm[5:]
    return f"0101{XXXX}0000{YYYY}"

# ======================================================

@new("acc")
def _(imm): return f"0111{to_dec(imm, 4)}"

@new("b-bit")
def _(k, imm): return f"100{to_dec(k, 2)}{to_bin(imm, 11)}"

@new("bnz-a")
def _(imm): return f"10100{to_bin(imm, 11)}"

@new("bnz-b")
def _(imm): return f"10101{to_bin(imm, 11)}"

@new("beqz")
def _(imm):
    return f"10110{to_bin(imm, 11)}"

@new("bnez")
def _(imm):
    return f"10111{to_bin(imm, 11)}"

@new("beqz-cf")
def _(imm):
    return f"11000{to_bin(imm, 11)}"

@new("bnez-cf")
def _(imm):
    return f"11001{to_bin(imm, 11)}"

@new("b-timer")
def _(imm):
    return f"11010{to_bin(imm, 11)}"

@new("bnz-d")
def _(imm):
    return f"11011{to_bin(imm, 11)}"

@new("b")
def _(imm):
    return f"1110{to_bin(imm, 12)}"

@new("call")
def _(imm):
    return f"1111{to_bin(imm, 12)}"



''' THIS IS THE IDEA
@new(name="dec*_reg")
def _(reg: str):
    return "000" + reg + "1"

line = "dec*_reg 001"
tokens = line.split(" ") # ["dec*_reg", "001"]
instruction_map[tokens[0]](tokens[1:])
'''
# ==============================  Reading from ASM File

output_lines: list[str] = []
initial_file = open(Path("Arch242_example_code.asm"), "r") # Change filename to final
while True:
    line: str = initial_file.readline()
    if not line: break

    tokens = line.split(" ")
    machine_code = instruction_map[tokens[0]](*tokens[1:])
    assert len(machine_code) in (8, 16)

    output_lines.append(machine_code)

binary = True
if not binary:
    output_lines = [hex(int(line))[2:] for line in output_lines]

# writes to destination ASM fil
destination_file = open(Path("Arch242_output_file.asm"), 'w')
while True:
    for line in output_lines:
        destination_file.write(line)