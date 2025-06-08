from sys import argv
from assembler.asm_instructions import instruction_map
from shared import utils
from emulator.disassembler import instr_branch_imm

INPUT_PATH = argv[1]
OUTPUT_PATH = "out.asm"
COMMENT = "--"

# This setup takes care of cases where a branch instruction to a LABEL was read before the LABEL itself recorded its own address.
label_address: dict[str, int] = {}
pending_tokens: list[list[str]] = [] # list[tokens]
pending_labels: dict[str, list[tuple[int, list, list[int]]]] = {} # pending_labels[LABEL] = [ (tokens, i, address) ]
output_lines: list[str] = []


def _record_tokens(tokens: list[str], address: int, label: str | None):
    instr = tokens[0]
    
    # Normal instruction
    if instr not in instr_branch_imm:
        for i in range(1, len(tokens)):  # -- Only process operand positions first filter the garbages
            token = tokens[i]

            # Check for numeric values first
            op = token
            if op.isdigit():  # Decimal
                op = int(token)
            elif op.startswith("0b"):  # Bin
                op = int(token[2:], 2)  # Convert to decimal
            elif op.startswith("0x"):  # Hex
                op = int(token[2:], 16)  # Convert to decimal
            tokens[i] = op

    else: # Branch instruction
        # All NUMERICAL operands are of the form (int, is_label_addr) for the function to use
        for i in range(1, len(tokens)):  # -- Only process operand positions first filter the garbages
            token = tokens[i]

            # Check for numeric values first
            op = token
            if op.isdigit():  # Decimal
                tokens[i] = (int(token), False)
            elif op.startswith("0b"):  # Bin
                tokens[i] = (int(token[2:], 2), False)  # Convert to decimal
            elif op.startswith("0x"):  # Hex
                tokens[i] = (int(token[2:], 16), False)  # Convert to decimal
            else:
                if op in label_address:
                    tokens[i] = (label_address[op], True)
                    if not ((label_address[op] & 0b1111 == address & 0b1111) or (label_address[op] & 0b11111 == address & 0b11111)):
                        print("FAIL", address, tokens)

                # (If it's not a real target label it's fine)
                else:
                    if op not in pending_labels: pending_labels[op] = []
                    pending_labels[op].append((tokens, i, address)) # Modified later if the target label's line is finally read
    
    # If this line itself has a label, then propagate changes to all of pending_labels[label]
    if label is not None:
        label_address[label] = address
        if label in pending_labels:
            while len(pending_labels[label]) > 0:
                (other_tokens, i, other_address) = pending_labels[label].pop()
                other_tokens[i] = (address, True)
                if not ((label_address[label] & 0b1111 == other_address & 0b1111) or (label_address[label] & 0b11111 == other_address & 0b11111)):
                    print("FAIL", other_address, other_tokens)
    
    pending_tokens.append(tokens)

    

def _encode_instruction(tokens: list[str]):
    instr = tokens[0]
    operands = tokens[1:]
    encoded = instruction_map[instr](*operands)
    if instr in utils.instr_16_bit:
        assert len(encoded) == 16
        output_lines.extend([encoded[:8], encoded[8:]])
    else:
        assert len(encoded) == 8
        output_lines.append(encoded)

# First pass: Record tokens
current_address: int = 0x0000
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        _c = line.find(COMMENT)
        if _c != -1: line = line[:_c]
        line = line.strip()
        if not line: continue
        
        tokens = line.split(" ")
        if line.startswith(".byte"):
            pending_tokens.append(tokens)
        else:
            
            # strip label
            label = None
            if utils.is_label(tokens[0]):
                label = utils.get_label_name(tokens[0])
                tokens = tokens[1:]
            
            instr = tokens[0]
            _record_tokens(tokens, current_address, label)
            current_address += 1 if instr not in utils.instr_16_bit else 2

# Second pass: Encode instructions
for tokens in pending_tokens:
    if tokens[0] == ".byte":
        output_lines.append(" ".join(tokens))
    else:
        _encode_instruction(tokens)


bin_or_hex = argv[2]
assert bin_or_hex in ("bin", "hex")

def _is_byte(line):
    return False if (line.startswith(".byte")) else True

if bin_or_hex == "hex":
    output_lines = [(utils.to_hex(line))[2:] if (_is_byte(line)) else line for line in output_lines]

# write to destination ASM file
destination_file = open(OUTPUT_PATH, "w+")

for line in output_lines:
    # If line is a list (e.g., [instruction, [operand1, operand2]]), join it
    if isinstance(line, list):
        line = " ".join(map(str, line))
    destination_file.write(line + "\n")

    
