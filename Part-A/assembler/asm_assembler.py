from pathlib import Path
from sys import argv
from asm_instructions import instruction_map
from asm_directives import directive_map, label_map
import asm_utils as asm_u


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "Arch242_example_code.asm"
OUTPUT_PATH = BASE_DIR / "Arch242_output_file.asm"

comment = "--"
output_lines: list[str] = []

# First pass - collect labels

current_address = 0x0000 # <---- PC
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        line = line.strip()
        if not line or line.startswith("--"):
            continue
        
        # Remove comments
        if comment in line:
            line = line.split("--")[0].strip()

        # Create label
        if asm_u.is_label(line):
            label_name = asm_u.get_label_name(line)
            label_map[label_name] = current_address

        # Ignore .byte directives
        elif not line.startswith(".byte"):
            current_address += 1 # <---- PC

# Second pass - generate machine code

current_address = 0x0000 # <--- Restart PC 
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        line = line.strip()
        if not line or line.startswith("--"): continue
    
        # Remove comments
        if "--" in line: line = line.split("--")[0].strip()

        if asm_u.is_label(line): continue

        elif line.startswith(".byte"):
            output_lines.append(line)

        else:
            tokens = line.split()
            if not tokens: continue
                
            # Replace labels with their addresses
            operands: list[str] = []
            for token in tokens[1:]:
                if token in label_map:
                    operands.append(str(label_map[token]))
                else:
                    operands.append(token)
            
            try:
                encoded = instruction_map[tokens[0]](*operands)
                if len(encoded) == 16:
                    output_lines.extend([encoded[:8], encoded[8:]])
                else:
                    output_lines.append(encoded)

            except KeyError:
                raise ValueError(f"Invalid instruction: {tokens[0]}")
            except Exception as e:
                raise ValueError(f"Error encoding {line}: {str(e)}")

# TODO: Implement command line arguments for filename and bin/hex
# check if binary
bin_or_hex = "bin"
assert bin_or_hex in ("bin", "hex")
if bin_or_hex == 'hex':
    output_lines = [hex(int(line))[2:] for line in output_lines]

# writes to destination ASM file
destination_file = open(OUTPUT_PATH, 'w+')

for line in output_lines:
    destination_file.write(line+"\n")
