from pathlib import Path
from sys import argv
from asm_instructions import instruction_map
from asm_directives import directive_map

# ==============================  Reading from ASM File

# read lines and convert to machine code

comment = "--"
output_lines: list[str] = []
initial_file = open(Path("Arch242_example_code.asm"), "r") # Change filename to final
while (line := initial_file.readline()) != "":
    line = line.lstrip().rstrip()
    if line == "": continue
    
    comment_idx = line.find(comment)
    if comment_idx != -1:
        line = line[:comment_idx]
    line.lstrip().rstrip()
    
    # directive
    if line[0] == ".":
        encoded = line
    
    # instruction
    else:
        tokens = line.split(" ")
        encoded = instruction_map[tokens[0]](*tokens[1:])
        assert len(encoded) in (8, 16)
        
    output_lines.append(encoded)


# TODO: Implement command line arguments for filename and bin/hex
# check if binary
bin_or_hex = "bin"
assert bin_or_hex in ("bin", "hex")
if bin_or_hex == 'hex':
    output_lines = [hex(int(line))[2:] for line in output_lines]

# writes to destination ASM file
destination_file = open(Path("Arch242_output_file.asm"), 'w+')

for line in output_lines:
    destination_file.write(line+"\n")
