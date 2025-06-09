from pathlib import Path

def fix_width(value, width, pad_char='0'):
    """Ensure a string has specific width by padding or truncating"""
    value = str(value)
    if len(value) > width:
        return value[-width:]
    return value.rjust(width, pad_char)

def to_bin(value, bits):
    """Convert integer or numeric string to binary string of given bits"""
    return format(value & ((1 << bits) - 1), f"0{bits}b")

def to_strbin(num: str):
    """Convert to binary string for easy conversion"""
    return f"0b{num}"

def to_hex(value):
    """Convert to hex string for easy conversion"""
    return f"0x{int(to_strbin(value), 2):02x}"
def hex_to_bin(value):
    """Convert to hex string to binary literal for easy conversion"""
    return to_bin(int(f"0x{value}", 16), 8)


def is_label(line):
    """Check if line is a label definition"""
    line = line.strip()
    return line.endswith(':')

def get_label_name(line):
    """Extract label name from label definition"""
    return line[:-1].strip()

INSTR_BITS = INSTR_16 = 16
MEM_BITS = INSTR_8 = 8
INSTR_4 = 4

SCREEN_WIDTH = 380
SCREEN_HEIGHT = 280
GAME_HEIGHT = 220
SYS_WIDTH = 220

DIM = 16
BASE_DIR = Path(__file__).resolve().parent.parent

# MASKS
HEX_16U4 = 0xF000
HEX_16U12 = 0xFFF0
HEX_16L12 = 0x0FFF
HEX_16L4 = 0x000F
HEX_16L5 = 0x001F
HEX_16U8 = 0xFF00
HEX_16U5 = 0xF800
BIN_13 = 0b001000000000
HEX_8L4 = 0x0F
HEX_8U4 = 0xF0

def is_binary_string(s):
    s = str(s)
    return len(s) > 0 and all(c in '01' for c in s)

instr_16_bit: list[str] = [
    "add", "sub", "and", "xor", "or",
    "r4", "rarb", "rcrd",
    "b-bit", "bnz-a", "bnz-b", "beqz", "bnez",
    "beqz-cf", "bnez-cf",
    "bnz-d", "b", "call", "shutdown"
]

