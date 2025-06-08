import emulator.disassembler as dasm
from emulator.emu_instructions import EmulatorInstructions
from shared import utils
from sys import argv
from dataclasses import dataclass
from pathlib import Path
import pyxel

BASE_DIR = Path(__file__).resolve().parent
ASM_PATH = BASE_DIR / argv[1]

@dataclass
class Instructions:
# --- Instruction class
    opcode: str # last 4-bits 
    bin: str 
    dec: str
    is_branch: bool

@dataclass
class MatrixCell:
    memAddr: int
    mapbit: int
    state: int

class RegisterFile:
    def __init__(self):
        self.REG = {
            'RA': 0, 'RB': 0, 'RC': 0, 'RD': 0,
            'RE': 0, 'RF': 0, 'ACC': 0, 'CF': 0, 'IOA': 0
        }
    def __getitem__(self, key):
        return self.REG[key]

    def __setitem__(self, key, value):
        self.REG[key] = value 
        
    def get(self, key, default=None):
        return self.REG.get(key, default)

    def __repr__(self):
        return repr(self.REG)

class DataMemory:
    def __init__(self, size=2**utils.MEM_BITS):
        self.mem: list[int] = [0x00] * size
        self.addr: int = 0x00 # 8-bit memory address
        # --- a 1D array of data memory

class InstructionMemory:
    def __init__(self, size=2**utils.INSTR_BITS):
        self.mem: list[int] = [0x000] * size
        self.addr: int = 0x0000 # 16-bit instruction address
        self.instr_16: bool = False
        # --- a 1D array of instruction memory

class Pyxel:
    def __init__(self, emulator: "Arch242Emulator"):
        # --- Pyxel
        self.screen_width = utils.SCREEN_WIDTH
        self.screen_height = utils.SCREEN_HEIGHT
        self.mid = utils.SCREEN_WIDTH // 2

        self.rows = 10
        self.cols = 20
        self.emulator = emulator
        self.score = 0 
        
        # -- Initialize
        self._build_matrix()
        pyxel.init(self.screen_width, self.screen_height, fps=400)
        pyxel.load(str(Path("assets/snake.pyxres")))
        pyxel.run(self.update, self.draw)

    def _build_matrix(self):
        mmio_addr = [data for data in range(192, 242)]
        self.led_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        k = j = 0
        for row in range(self.rows):
            for col in range(self.cols):
                cell = MatrixCell(mmio_addr[k], 2**(j % 4), 0)
                self.led_matrix[row][col] = cell
                if (j <= 2):
                    j+=1
                else: 
                    k+=1
                    j=0
                    
    def _write_cell(self):
        for mem_addr in range(192, 242):
            val = self.emulator.DataMem.mem[mem_addr]
            row = (mem_addr-192)//5
            col_start = (mem_addr-192) % 5
            for i in range(4):
                col = col_start*4 + i
                state = val & 1 
                self.led_matrix[row][col].state = state
                val >>= 1

    def print_matrix(self):
        for row in self.led_matrix:
            print("".join("1" if cell.state else "0" for cell in row))  

    def update(self):
        self._write_cell()
        self.emulator.clock_tick()
      
    def _draw_cell(self):
        self._draw_hud()
        matrix_width = self.cols * utils.DIM
        matrix_height = self.rows * utils.DIM
        
        offset_x = (utils.SCREEN_WIDTH - matrix_width) // 2
        offset_y = (utils.GAME_HEIGHT- matrix_height) // 2
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * utils.DIM
                y = offset_y + row * utils.DIM
                if (self.led_matrix[row][col].state == 1):
                    pyxel.blt(x,y,0,0,88,16,16)
                else:
                    pyxel.blt(x,y,0,16,88,16,16)
      
    def _draw_title(self):
           # S
        pyxel.blt(self.mid - 72, 6, 0, 0,24,16,16)
        # # N
        pyxel.blt(self.mid - 56, 6, 0, 16,24,16,16)
        # # # A
        pyxel.blt(self.mid - 41, 6, 0, 32,24,16,16)
        # # # K
        pyxel.blt(self.mid - 25, 6, 0, 48,24,16,16)
        # # # E
        pyxel.blt(self.mid - 9, 6, 0, 64,24,16,16)
        # # # G
        pyxel.blt(self.mid + 5, 6, 0, 0,40,16,16)
        # # A
        pyxel.blt(self.mid + 21, 6, 0, 16,40,16,16)
        # # M
        pyxel.blt(self.mid + 37, 6, 0, 32,40,16,16)
        # # E
        pyxel.blt(self.mid + 53, 6, 0, 48,40,16,16)

    def _draw_snake(self, x, y):
        pass

    def _center(self, text):
        text_width = len(text) * 4  
        return ((utils.SCREEN_WIDTH) - text_width) // 2

    def _draw_benchmark(self):
        # Layout constants
        left = utils.SCREEN_WIDTH - utils.SYS_WIDTH
        top = utils.GAME_HEIGHT
        line_height = 8
        text_color = 7
        bg_color = 0
        border_color = 7

        # Determine the far-right drawing position for register values
        bar_x = left + 165
        content_right = bar_x + 70  # Enough for "|   REG: VALUE"

        panel_width = content_right - left + 10  # Slight margin to the right
        panel_height = utils.SCREEN_HEIGHT - top + 20

        # Draw border and background fill
        pyxel.rectb(left, top - 20, panel_width - 25, panel_height, border_color)
        pyxel.rect(left + 1, top - 19, panel_width - 20, panel_height - 2, bg_color)

        # Header
        pyxel.text(left + 10, top - 14, "Arch242 CPU Emulator", text_color)
        pyxel.text(left + 8, top - 8, "-" * 49, text_color)

        # Instruction and PC
        pyxel.text(left + 10, top, "INSTRUCTION:", text_color)
        
        if (self.emulator.instr):
            pyxel.text(left + 85, top + line_height, f"{self.emulator.instr.bin}", text_color)
            pyxel.text(left + 85, top, f"{dasm.instruction_map[self.emulator.instr.bin]()}", text_color)
        else:
            pyxel.text(left + 90, top, "no fetched", text_color)
      
        pyxel.text(left + 10, top + 2 *  line_height, "PROGRAM COUNTER:", text_color)
        pyxel.text(left + 110, top + 2 * line_height, f"{self.emulator.PC}", text_color)
        
        print(f"{self.emulator.PC}:: {_XD[self.emulator.PC]}")
        
        pyxel.text(left + 10, top + 3 * line_height, "LINE:", text_color)
        # pyxel.text(left + 110, top + 2 * line_height, f"{self.emulator.RBRA}", text_color)

        # Visual register marker
        for i in range(7):  # enough for RA–CF
            pyxel.text(bar_x - 10, top + i * line_height, "|", text_color)

        # Register display beside the markers
        reg_labels = ["RA", "RB", "RC", "RD", "RE", "ACC", "CF"]
        for i, reg in enumerate(reg_labels):
            y = top + i * line_height
            value = self.emulator.RegFile.get(reg, 0)
            pyxel.text(bar_x, y, f"{reg}: {value:02d}", text_color)
            pyxel.text(bar_x + 30, y, f"{utils.to_bin(value, 4)}", text_color)
        

    def _draw_hud(self):
        # Clear HUD area (keep original background)
        pyxel.rect(-utils.SYS_WIDTH, utils.GAME_HEIGHT - 20, utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT, 1)

        # --- LEFT: INSTRUCTIONS (unchanged) ---
        pyxel.text(23, utils.GAME_HEIGHT - 9, "HOW TO PLAY", 7)
        pyxel.blt(30, utils.GAME_HEIGHT + 10, 0, 10, 57, 40, 20, 0)
        pyxel.text(15, utils.GAME_HEIGHT + 35, "Press arrow keys", 7)
        pyxel.text(8, utils.GAME_HEIGHT + 45, "to change direction", 7)

        center_left = utils.SCREEN_WIDTH // 3  # Shifted left from absolute center

        # Score (aligned with icons)
        pyxel.blt(center_left - 35, utils.GAME_HEIGHT - 12, 0, 32, 88, 16, 16, 0)
        pyxel.text(center_left - 15, utils.GAME_HEIGHT - 6, "SCORE:", 7)
        pyxel.text(center_left + 15, utils.GAME_HEIGHT - 6, f"{self.emulator.DataMem.mem[254]}", 7)
        
        # LED ON
        pyxel.blt(center_left - 35, utils.GAME_HEIGHT + 12, 0, 0, 88, 16, 16, 0)
        pyxel.text(center_left - 15, utils.GAME_HEIGHT + 18, "LED ON:", 7)

        # LED OFF
        pyxel.blt(center_left - 35, utils.GAME_HEIGHT + 36, 0, 16, 88, 16, 16, 0)
        pyxel.text(center_left - 15, utils.GAME_HEIGHT + 40, "LED OFF:", 7)
        
    def draw(self):
        self._draw_cell()
        self._draw_hud()
        self._draw_benchmark()
        self._draw_title()

class Arch242Emulator: # CPU
    
    def __init__(self) -> None:  
        # # --- Special Registers,General Purpose Registers, I/O # Registers
        self.PC: int = 0x0000
        self.TEMP: int = 0x0000
        self.IMM: int = 0x000
        self.RegFile: RegisterFile = RegisterFile()

        self.CFACC: int = 0
        self.RDRC: int = 0
        self.RBRA: int = 0
        # Init System
        self.clock_cycle: int = 0
        self.instr: str = " "

        # Instantiation
        self.emu_i = EmulatorInstructions(self)
        self.DataMem = DataMemory()
        self.InstMem = InstructionMemory()
        
        self.load_instructions()

    def clock_tick(self) -> None:
        self.instr: str = self.fetch()
        self.iohardware()
        if (self.instr):
            self.decode()
            self.execute()
        self.clock_cycle += 1
        x = (int(bin(self.DataMem.mem[6])[2:], 2) << 4) | int(bin(self.DataMem.mem[5])[2:], 2)
        print("SNAKE-HEAD::", x, bin(self.DataMem.mem[7])[2:])
        for (name, value) in self.RegFile.REG.items():
            print(f"REG: {name} --> {bin(value)}")
        x = (int(bin(self.DataMem.mem[243])[2:], 2) << 4) | int(bin(self.DataMem.mem[242])[2:], 2)
        print("QUEUE-TAIL POINTER:", x)
        return
    
    def load_instructions(self) -> None:
        
        # first pass (.byte)
        with open(Path(ASM_PATH), "r") as f:
            assembled = f.readlines()

        for line in assembled:
            line = line.strip()
            if (line.startswith(".byte")):
                self.DataMem.mem[self.DataMem.addr] = int(line[6:], 16)
                self.DataMem.addr += 1
            else:
                continue
        
        # second pass (instructions)
        with open(Path(ASM_PATH), "r") as f:
            assembled = f.readlines()

        for line in assembled:
            line = line.strip()
            if (utils.is_binary_string(line)): 
                self.InstMem.mem[self.InstMem.addr] = line
                self.InstMem.addr += 1   
            elif not (utils.is_binary_string(line)) and not (line.startswith(".byte")):
                self.InstMem.mem[self.InstMem.addr] = utils.hex_to_bin(line)
                self.InstMem.addr += 1
        return
        
    def fetch(self) -> str:
        if (self.InstMem.mem):
            instruction: str = self.InstMem.mem[self.PC]
            return instruction
        
    def decode(self) -> None:
        
        opcode_bits = "100X" if self.instr[:4] == "1001" or self.instr[:4] == "1000" else self.instr[:4]

        type: str = dasm.instr_type[opcode_bits]

        if type in dasm.instr_16_bit_type or self.instr == "00110111": # shutdown
            self.instr += self.InstMem.mem[self.PC + 1]
        else: 
            self.instr = self.instr # pc += 1
        
        token: str = dasm.instruction_map[self.instr]().split()[0]

        is_branch = True if token in dasm.jump_or_branch else False
        self.instr: Instructions = Instructions(type, self.instr, int(utils.to_strbin(self.instr), 2), is_branch)
        
    def execute(self) -> None: # alu
        match (self.instr.opcode):
            case "Type1":
                self.emu_i._type1()
            case "Type2":
                self.emu_i._type2()
            case "Type3":
                self.emu_i._type3()
            case "Type4":
                self.emu_i._type4()
            case "Type5":
                self.emu_i._type5()
            case "Type6":
                self.emu_i._type6()
            case "Type7":
                self.emu_i._type7()
            case "Type8":
                self.emu_i._type8()
            case "Type9":
                self.emu_i._type9()
            case "Type10":
                self.emu_i._type10()
            case "Type11":
                self.emu_i._type11()
            case "Type12":
                self.emu_i._type12()
            case "Type13":
                self.emu_i._type13()
            case "Type14":
                self.emu_i._type14()
            case "Type15":
                self.emu_i._type15()
            case _:
                print(self.PC)
                
    def iohardware(self) -> None:
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0001 if pyxel.btn(pyxel.KEY_UP) else self.RegFile['IOA'] & 0b1110
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0010 if pyxel.btn(pyxel.KEY_DOWN) else self.RegFile['IOA'] & 0b1101
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0100 if pyxel.btn(pyxel.KEY_LEFT) else self.RegFile['IOA'] & 0b1011
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b1000 if pyxel.btn(pyxel.KEY_RIGHT) else self.RegFile['IOA'] & 0b0111

_XD = []
def main():
    with open("snake.asm") as file:
        for line in file.readlines():
            _XD.append(line.strip())

    
    cpu = Arch242Emulator()
    Pyxel(cpu)

if __name__ == "__main__":
    main()