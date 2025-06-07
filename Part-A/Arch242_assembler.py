from pathlib import Path
from sys import argv
from assembler.asm_instructions import instruction_map
from assembler.asm_directives import directive_map, label_map
from assembler import asm_utils as asm_u

INPUT_PATH = argv[1]
OUTPUT_PATH = "Arch242_output_file.asm"

comment = "--"
output_lines: list[str] = []

# First pass - collect labels

def _encode_instructions(tokens: list[int], instr: int, op: int) -> None:
    # getting the immediate values 
    # Replace labels with their addresses or immediates
    operands: list[str] = []
    
    for token in tokens[op:]:
        if token in label_map:
            operands.append(str(label_map[token]))
        else:
            operands.append(token)
    
    try:
        encoded = instruction_map[tokens[instr]](*operands)
        if len(encoded) == 16:
            output_lines.extend([encoded[:8], encoded[8:]])
        else:
            output_lines.append(encoded)

    except KeyError:
        raise ValueError(f"Invalid instruction: {tokens[instr]}")
    except Exception as e:
        raise ValueError(f"Error encoding {line}: {str(e)}")

current_address = 0x0000 # <---- PC
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        line = line.strip()
        tokens = line.split()

        
        if not line or line.startswith("--"):
            continue
            
        
        # Remove comments
        if comment in line:
            line = line.split("--")[0].strip()
            

        # Create label
        if asm_u.is_label(line):
            label_name = asm_u.get_label_name(line)
            label_map[label_name] = current_address
        
        # Create inline label
        elif asm_u.is_label(tokens[0]):
            label_name = asm_u.get_label_name(tokens[0])
            label_map[label_name] = current_address
            
        elif line.startswith(".byte"):
            current_address += 1 # <-- increment
            
        current_address += 1
# Second pass - generate machine code

current_address = 0x0000 # <--- Restart PC 
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        line = line.strip()
        tokens = line.split()

        if not line or line.startswith("--"): continue
    
        # Remove comments
        if "--" in line: line = line.split("--")[0].strip()

        if asm_u.is_label(line): 
            continue
        
        elif asm_u.is_label(tokens[0]):
            if not tokens: continue
            _encode_instructions(tokens, instr=1, op=2)
        
        elif line.startswith(".byte"):
            output_lines.append(line)

        else:
            if not tokens: continue
            _encode_instructions(tokens, instr=0, op=1)

            
# print(label_map)

# TODO: Implement command line arguments for filename and bin/hex
# check if binary
bin_or_hex = argv[2]
assert bin_or_hex in ("bin", "hex")

if bin_or_hex == 'hex':
    output_lines = [asm_u.to_hex(line) for line in output_lines]

# writes to destination ASM file
destination_file = open(OUTPUT_PATH, 'w+')

for line in output_lines:
    destination_file.write(line+"\n")
    
