from pathlib import Path
from sys import argv
from assembler.asm_instructions import instruction_map
from assembler.asm_directives import directive_map, label_map
from assembler.asm_utils import to_bin, to_hex, to_strbin, hex_to_bin, get_label_name, is_label
from emulator.disassembler import instr_no_arg, instr_imm_arg, instr_branch_imm, instr_reg_imm, instr_reg_arg

INPUT_PATH = argv[1]
OUTPUT_PATH = "out.asm"

comments = ["--", "-!", "--!", "------------", "------------------", "--------------------", "----------------------------------------"]
output_lines: list[str] = []

def _not_comment(token: str) -> bool: return True if token not in comments else False

def _encode_instructions(tokens: list[str]) -> None:
    instr: str = tokens[0]
    operands: list[str | int] = []
    
    # Normal instruction
    if instr not in instr_branch_imm:
        for token in tokens[1:]:  # -- Only process operand positions first filter the garbages
            # Check for numeric values first
            op = token
            if op.isdigit():  # Decimal
                op = int(token)
            elif op.startswith("0b"):  # Bin
                op = int(token[2:], 2)  # Convert to decimal
            elif op.startswith("0x"):  # Hex
                op = int(token[2:], 16)  # Convert to decimal
            operands.append(op)

    else: # Branch instruction
        # All NUMERICAL operands are of the form (int, is_label_addr) for the function to use
        for token in tokens[1:]:  # -- Only process operand positions first filter the garbages
            # Check for numeric values first
            op = token
            if op.isdigit():  # Decimal
                op = (int(token), False)
            elif op.startswith("0b"):  # Bin
                op = (int(token[2:], 2), False)  # Convert to decimal
            elif op.startswith("0x"):  # Hex
                op = (int(token[2:], 16), False)  # Convert to decimal
            elif op in label_map:
                op = (label_map[op], True) # Get address from label
            operands.append(op)
    
    encoded = instruction_map[instr](*operands)
    if len(encoded) == 16:
        output_lines.extend([encoded[:8], encoded[8:]])
    else:
        output_lines.append(encoded)


current_address: int = 0x0000 # <---- PC
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        line: str = line.strip()
        tokens = line.split()
        
        if not line:
            continue              
        # Remove comments
        # if comment in line:
        #     line = line.split("--")[0].strip()
        
        # if comment_1 in line:
        #     continue
        
        # Create label
        if is_label(line):
            label_name = get_label_name(line)
            label_map[label_name] = current_address
            # print(line)
            
        # Create inline label
        elif is_label(tokens[0]):
            label_name = get_label_name(tokens[0])
            label_map[label_name] = current_address
            
        # else:
        #     current_address += 1 # <-- increment 
        current_address += 1
        
# print(current_address, label_map['GAME_LOOP_food_miss_queue-tail_dec']) 
# # Second pass - generate machine code

current_address: int = 0x0000
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        # First remove entire comment lines
        line = line.strip()
        if not line or any(line.startswith(c) for c in comments):
            continue
            
        # Remove inline comments
        if '--' in line:
            line = line.split('--')[0].strip()
            if not line:  # Case where whole line was a comment
                continue
                
        tokens = line.split()
        
        filtered_tokens = [t for t in tokens if _not_comment(t)]
        if not filtered_tokens:
            continue
        
        if line.startswith(".byte"):
            output_lines.append(line)
            
        else:
            # strip label
            if is_label(tokens[0]):
                tokens = tokens[1:]
            _encode_instructions(tokens)


bin_or_hex = argv[2]
assert bin_or_hex in ("bin", "hex")

if bin_or_hex == "hex":
    output_lines = [to_hex(line) for line in output_lines]

# writes to destination ASM file
destination_file = open(OUTPUT_PATH, "w+")

for line in output_lines:
    # If line is a list (e.g., [instruction, [operand1, operand2]]), join it
    if isinstance(line, list):
        line = " ".join(map(str, line))
    destination_file.write(line + "\n")

    
