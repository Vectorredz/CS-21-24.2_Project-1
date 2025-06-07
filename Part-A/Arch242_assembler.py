from pathlib import Path
from sys import argv
from assembler.asm_instructions import instruction_map
from assembler.asm_directives import directive_map, label_map
from assembler.asm_utils import to_bin, to_hex, to_strbin, hex_to_bin, get_label_name, is_label
from emulator.disassembler import instr_no_arg, instr_imm_arg, instr_reg_arg

INPUT_PATH = argv[1]
OUTPUT_PATH = "Arch242_output_file.asm"

comment = "--"
comment_1 = "--!"
comment_2 = "-!"
comment_3 = "------------------"
branch_comments = "------------"
func_comments = "----------------------------------------"
output_lines: list[str] = []

# First pass - collect labels

def _not_comment(token: str):
    if (token == func_comments or token == comment or token == comment_1 or token == branch_comments or token == comment_2 or token == '--' or token == '--------------------'):
        return False
    else:
        return True

def _encode_instructions(tokens: list[str], instr: int, op: int) -> None:
    operands: list[str] = []
    
    for token in tokens[op:3]:  # -- Only process operand positions first filter the garbages
        if not _not_comment(token):
            continue

        # 1. Check for numeric values first
        if token.isdigit():  # Decimal
            operands.append(token)
        elif token.startswith("0b"):  # Bin
            operands.append(token[2:])  # Strip 0b prefix
        elif token.startswith("0x"):  # Hex
            operands.append(str(int(token[2:], 16)))  # Convert to decimal string
        
        # # 2. Check for valid labels (inline)
        if token in label_map:
            operands.append(str(label_map[token]))  # Replace with address if known

   
    # print(tokens[instr], *operands)
    for token in tokens[instr:instr+1]:
        ...
    #     print(token, *operands)
        if token in instr_no_arg:
            # print(token, *operands)
            encoded = instruction_map[tokens[instr]]()
            if len(encoded) == 16:
                output_lines.extend([encoded[:8], encoded[8:]])
            else:
                output_lines.append(encoded)
        elif token in instr_reg_arg:
            # print(token, *operands)
            encoded = instruction_map[tokens[instr]](to_bin(int(*operands), 4))
            if len(encoded) == 16:
                output_lines.extend([encoded[:8], encoded[8:]])
            else:
                output_lines.append(encoded)
        elif token in instr_imm_arg:
            # print(token, *operands)
            encoded = instruction_map[tokens[instr]](*operands)
            if len(encoded) == 16:
                output_lines.extend([encoded[:8], encoded[8:]])
            else:
                output_lines.append(encoded)

           
        # print(encoded) 
        # if len(encoded) == 16:
        #     output_lines.extend([encoded[:8], encoded[8:]])
        # else:
        #     output_lines.append(encoded)
            
            
    # try:
        
    #     encoded = instruction_map[tokens[instr]](*operands)
    #     if len(encoded) == 16:
    #         output_lines.extend([encoded[:8], encoded[8:]])
    #     else:
    #         output_lines.append(encoded)

    # except KeyError:
    #     raise ValueError(f"Invalid instruction: {tokens[instr]}")
    # except Exception as e:
    #     raise ValueError(f"Error encoding {line}: {str(e)}")

current_address = 0x0000 # <---- PC
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        line = line.strip()
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
        current_address +=1
        
# print(current_address, label_map['GAME_LOOP_food_miss_queue-tail_dec']) 
# # Second pass - generate machine code

current_address = 0x0000
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        # First remove entire comment lines
        line = line.strip()
        if not line or any(line.startswith(c) for c in ['--', '----']):
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

        if is_label(line): 
            continue
        
        # inline label instructions 
        elif is_label(tokens[0]):
            if not tokens: continue
            _encode_instructions(tokens, instr=1, op=2)
        
        elif line.startswith(".byte"):
            output_lines.append(line)

        # normal instructions
        else:
            if not tokens: continue
            _encode_instructions(tokens, instr=0, op=1)

            
# # print(label_map)

bin_or_hex = argv[2]
assert bin_or_hex in ("bin", "hex")

if bin_or_hex == 'hex':
    output_lines = [to_hex(line) for line in output_lines]

# writes to destination ASM file
destination_file = open(OUTPUT_PATH, 'w+')

for line in output_lines:
    # If line is a list (e.g., [instruction, [operand1, operand2]]), join it
    if isinstance(line, list):
        line = ' '.join(map(str, line))
    destination_file.write(line + "\n")

    
