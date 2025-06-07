from typing import Callable
from assembler.asm_utils import fix_width, to_bin

type DirEncoder = Callable

label_map = {}
directive_map = {
    ".byte": lambda x: format(int(x) & 0xFF, '08b')
}

def new_d(name: str):
    def _new(f: DirEncoder):
        directive_map[name] = f
    return _new

# Internal values/flags
MEM_CAP = 1 << 8
mem_target = 0x0    # current target memory address for memwrite directives (in-case there's multiple)

# TODO this disrupts instruction addressing by being an instruction itself!
@new_d("byte")
def _(value):
    value = int(value)
    
    assert mem_target < MEM_CAP-1
    encoded = [
        # MEM[mem_target] = v1
        f"rarb {mem_target}",
        f"acc {value}",
        "to-mba",

        # clear register values
        "acc 0",
        "rarb 0"
    ]
    mem_target += 1
    return encoded