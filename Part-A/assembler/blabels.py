from pathlib import Path


INPUT_PATH = "../snake2.asm"
output_lines = []
with open(INPUT_PATH, "r") as input_file:
    for line in input_file:
        if not line: continue
        # if "BRANCH_TO: " in line:
        #     s = line.split("BRANCH_TO: ")
        #     x = line.find("--")
        #     inst = s[0][:x].strip()
        #     comment_dashes = s[0][x:].strip()
        #     label = s[1].strip()
        #     line = f"{inst} {label} {comment_dashes} BRANCH_TO: {label}\n"
        # elif "BRANCH: "in line:
        #     s = line.split("BRANCH: ")
        #     x = line.find("--")
        #     inst = s[0][:x].strip()
        #     comment_dashes = s[0][x:].strip()
        #     label = s[1].strip()
        #     line = f"{label}: {inst} {label} {comment_dashes} BRANCH: {label}\n"
        # output_lines.append(line)
        if "BRANCH:" in line:
            x = line.find("--")
            s = line.split("------------ BRANCH:")
            s[0] = s[0].strip().split(" ")
            s[0].pop()
            s[0] = " ".join(s[0]) + " "
            line = "------------ BRANCH:".join(s)
        output_lines.append(line)

destination_file = open(INPUT_PATH, 'w+')

for line in output_lines:
    destination_file.write(line)

            