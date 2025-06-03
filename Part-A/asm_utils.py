def fix_width(num: str, digits: int, ext: str): # extends
    assert len(num) <= digits
    return (ext * (digits-len(num))) + num
def to_bin(num: str, bits: int):
    num = int(num)
    assert len(bin(num)[2:]) <= bits
    num = format(num, f"0{bits}b")
    return num