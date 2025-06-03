from typing import Callable
from asm_utils import fix_width, to_bin

type DirEncoder = Callable

directive_map = dict[str, DirEncoder] = {}
def new_d(name: str):
    def _new(f: DirEncoder):
        directive_map[name] = f
    return _new

# Internal values/flags
mem_target = 0x0    # current target memory address for memwrite directives (in-case there's multiple)
mem_cap = 2**8

@new_d("byte")
def _(value):

    # split byte into two 4-bit values
    v1 = value[:-1]
    v2 = f"0x{value[-1]}"
    v1, v2 = int(v1), int(v2)

    # MEM[mem_target] = v1, MEM[mem_target+1] = v2
    # TODO check if memory is 4-bit data per address (currently) instead of 8-bit data
    encoded = [
        f"rarb {mem_target}",
        f"acc {v1}",
        "to-mba",
        f"rarb {mem_target+1}",
        f"acc {v2}",
        "to-mba"
    ]
    mem_target += 2
    assert mem_target < mem_cap
    return encoded