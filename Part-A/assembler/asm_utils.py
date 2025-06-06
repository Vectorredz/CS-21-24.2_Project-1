def fix_width(value, width, pad_char='0'):
    """Ensure a string has specific width by padding or truncating"""
    value = str(value)
    if len(value) > width:
        return value[-width:]
    return value.rjust(width, pad_char)

def to_bin(value, bits):
    """Convert integer or numeric string to binary string of given bits"""
    try:
        num = int(value)
    except ValueError:
        num = 0
    return format(num & ((1 << bits) - 1), f'0{bits}b')

def to_strbin(num: str):
    """Convert to binary string for easy conversion"""
    return f"0b{num}"

def is_label(line):
    """Check if line is a label definition"""
    return line.endswith(':')

def get_label_name(line):
    """Extract label name from label definition"""
    return line[:-1].strip()