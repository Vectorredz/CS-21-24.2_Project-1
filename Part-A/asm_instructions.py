from typing import Callable
from asm_utils import fix_width, to_bin

type InstEncoder = Callable

instruction_map: dict[str, InstEncoder] = {}
def new_i(name: str):
    def _new(f: InstEncoder):
        instruction_map[name] = f
    return _new

''' THIS IS THE IDEA
@new_i(name="dec*_reg")
def _(reg: str):
    return "000" + reg + "1"

line = "dec*_reg 001"
tokens = line.split(" ") # ["dec*_reg", "001"]
instruction_map[tokens[0]](tokens[1:])
'''


@new_i("rot-r")
def _(): return "00000000"

@new_i("rot-l")
def _(): return "00000001"

@new_i("rot-rc")
def _(): return "00000010"

@new_i("rot-lc")
def _(): return "00000011"

@new_i("from-mba")
def _(): return "00000100"

@new_i("to-mba")
def _(): return "00000101"

@new_i("from-mdc")
def _(): return "00000110"

@new_i("to-mdc")
def _(): return "00000111"

@new_i("addc-mba")
def _(): return "00001000"

@new_i("add-mba")
def _(): return "00001001"

@new_i("subc-mba")
def _(): return "00001010"

@new_i("sub-mba")
def _(): return "00001011"

@new_i("inc*-mba")
def _(): return "00001100"

@new_i("dec*-mba")
def _(): return "00001101"

@new_i("inc*-mdc")
def _(): return "00001110"

@new_i("dec*-mdc")
def _(): return "00001111"

@new_i("inc*-reg")
def _(reg):
    reg = fix_width(reg, 3, "0")
    assert reg in ("000", "001", "010", "011", "100")
    return f"0001{reg}0"

@new_i("dec*-reg")
def _(reg):
    reg = fix_width(reg, 3, "0")
    assert reg in ("000", "001", "010", "011", "100")
    return f"0001{reg}1"

@new_i("and-ba")
def _(): return "00011010"

@new_i("xor-ba")
def _(): return "00011011"

@new_i("or-ba")
def _(): return "00011100"

@new_i("and*-mba")
def _(): return "00011101"

@new_i("xor*-mba")
def _(): return "00011110"

@new_i("or*-mba")
def _(): return "00011111"

@new_i("to-reg")
def _(reg):
    reg = fix_width(reg, 3, "0")
    assert reg in ("000", "001", "010", "011", "100")
    return f"0010{reg}0"

@new_i("from-reg")
def _(reg):
    reg = fix_width(reg, 3, "0")
    assert reg in ("000", "001", "010", "011", "100")
    return f"0010{reg}1"

@new_i("clr-cf")
def _(): return "00101010"

@new_i("set-cf")
def _(): return "00101011"

@new_i("set-ei")
def _(): return "00101100"

@new_i("clr-ei")
def _(): return "00101101"

@new_i("ret")
def _(): return "00101110"

@new_i("retc")
def _(): return "00101111"

@new_i("from-ioa")
def _(): return "00110000"

@new_i("inc")
def _(): return "00110001"

@new_i("to-ioa")
def _(): return "00110010"

@new_i("to-iob")
def _(): return "00110011"

@new_i("to-ioc")
def _(): return "00110100"

@new_i("bcd")
def _(): return "00110110"

@new_i("shutdown")
def _(): return "0011011100111110"

@new_i("timer-start")
def _(): return "00111000"

@new_i("timer-end")
def _(): return "00111001"

@new_i("from-timerl")
def _(): return "00111010"

@new_i("from-timerh")
def _(): return "00111011"

@new_i("to-timerl")
def _(): return "00111100"

@new_i("to-timerh")
def _(): return "00111101"

@new_i("nop")
def _(): return "00111110"

@new_i("dec")
def _(): return "00111111"

@new_i("add")
def _(imm):
    return f"010000000000{to_bin(imm, 4)}"

@new_i("sub")
def _(imm):
    return f"010000010000{to_bin(imm, 4)}"

@new_i("and")
def _(imm):
    return f"010000100000{to_bin(imm, 4)}"

@new_i("xor")
def _(imm):
    return f"010000110000{to_bin(imm, 4)}"

@new_i("or")
def _(imm):
    return f"010001000000{to_bin(imm, 4)}"

@new_i("r4")
def _(imm):
    return f"010001100000{to_bin(imm, 4)}"

@new_i("timer")
def _(imm):
    return f"010001110000{to_bin(imm, 4)}"




# ======================================================
# TODO wtf is this? (nops + rarb/rcrd same encoding)

@new_i("–")                                      # instruction 38
def _(): return "00110101"

@new_i("-")                                      # instruction 54
def _(imm):
    return f"010001010000{to_bin(imm, 4)}"

@new_i("–")                                      # instructions 57 - 64
def _(): return "01001000"

@new_i("–")
def _(): return "01001001"

@new_i("–")
def _(): return "01001010"

@new_i("–")
def _(): return "01001011"

@new_i("YYY")
def _(): return "01001100"

@new_i("YYY")
def _(): return "01001101"

@new_i("YYY")
def _(): return "01001110"

@new_i("YYY")
def _(): return "01001111"


@new_i("rarb")
def _(imm):
    imm = to_bin(imm, 8)
    YYYY = imm[:5]
    XXXX = imm[5:]
    return f"0101{XXXX}0000{YYYY}"

@new_i("rcrd")
def _(imm):
    imm = to_bin(imm, 8)
    YYYY = imm[:5]
    XXXX = imm[5:]
    return f"0110{XXXX}0000{YYYY}"

# ======================================================

@new_i("acc")
def _(imm): return f"0111{to_bin(imm, 4)}"

@new_i("b-bit")
def _(k, imm): return f"100{to_bin(k, 2)}{to_bin(imm, 11)}"

@new_i("bnz-a")
def _(imm): return f"10100{to_bin(imm, 11)}"

@new_i("bnz-b")
def _(imm): return f"10101{to_bin(imm, 11)}"

@new_i("beqz")
def _(imm):
    return f"10110{to_bin(imm, 11)}"

@new_i("bnez")
def _(imm):
    return f"10111{to_bin(imm, 11)}"

@new_i("beqz-cf")
def _(imm):
    return f"11000{to_bin(imm, 11)}"

@new_i("bnez-cf")
def _(imm):
    return f"11001{to_bin(imm, 11)}"

@new_i("b-timer")
def _(imm):
    return f"11010{to_bin(imm, 11)}"

@new_i("bnz-d")
def _(imm):
    return f"11011{to_bin(imm, 11)}"

@new_i("b")
def _(imm):
    return f"1110{to_bin(imm, 12)}"

@new_i("call")
def _(imm):
    return f"1111{to_bin(imm, 12)}"