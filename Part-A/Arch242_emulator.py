import emulator.disassembler as dasm
from emulator import emu_utils as emu_u
from emulator.emu_instructions import EmulatorInstructions
from assembler import asm_utils as asm_u

from dataclasses import dataclass
from pathlib import Path
import pyxel
import subprocess

BASE_DIR = Path(__file__).resolve().parent
ASM_PATH = BASE_DIR / "assembler" / "asm_assembler.py"

"""
TODO:
    - HUD
    - test instructions
# """

@dataclass
class EmulatorState:
    shutdown: bool
    start: bool

@dataclass
class Instructions:
# --- Instruction class
    opcode: str # first 4-bits 
    bin: str 
    dec: str

@dataclass
class MatrixCell:
    memAddr: int
    mapbit: int
    state: int

class DataMemory:
    def __init__(self, size=2**emu_u.MEM_BITS):
        self.Data: list[int] = [0] * size
        # --- a 1D array of data memory

class InstrMemory:
    def __init__(self, size=2**emu_u.INSTR_BITS):
        self.Instruction: list[int] = []
        # --- a 1D array of instruction memory

class Pyxel:
    def __init__(self, emulator: "Arch242Emulator"):
        # --- Pyxel
        self.screen_width = emu_u.SCREEN_WIDTH
        self.screen_height = emu_u.SCREEN_HEIGHT
        self.rows = 10
        self.cols = 20
        self.mid = emu_u.SCREEN_WIDTH // 2
        self.mem_addr = 192
        self.emulator = emulator
        self.score = 0 
        self._build_matrix()
        # self.print_matrix()
        pyxel.init(self.screen_width, self.screen_height, fps=1)
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
        # print(self.led_matrix)

    def _write_cell(self, mem_addr, val):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.led_matrix[row][col]
                if (cell.memAddr == mem_addr) & (cell.mapbit == val):
                    self.led_matrix[row][col].state = 1
                

    def print_matrix(self):
        for row in self.led_matrix:
            print("".join("1" if cell.state else "0" for cell in row))  

    def update(self):
        # print(self.emulator.RegFile['IOA'])
        self._write_cell(self.mem_addr, self.emulator.RegFile['IOA'])
        self.emulator.clock_tick()
      
    def _draw_cell(self):
        # pyxel.rect(0, 0, emu_u.GAME_HEIGHT, emu_u.SCREEN_HEIGHT, 3)
        self._draw_hud()
        matrix_width = self.cols * emu_u.DIM
        matrix_height = self.rows * emu_u.DIM
        
        offset_x = (emu_u.SCREEN_WIDTH - matrix_width) // 2
        offset_y = (emu_u.GAME_HEIGHT- matrix_height) // 2
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * emu_u.DIM
                y = offset_y + row * emu_u.DIM
                # print(x, y)
                if (self.led_matrix[row][col].state == 1):
                    pyxel.blt(x,y,0,0,88,16,16)
                else:
                    pyxel.blt(x,y,0,16,88,16,16)
                # pyxel.rectb(x, y, emu_u.DIM, emu_u.DIM, 0)
        # self._draw_snake(offset_x  * emu_u.DIM, offset_y  * emu_u.DIM)

    def _draw_title(self):
           # S
        pyxel.blt(self.mid - 72, 2, 0, 0,24,16,16)
        # # N
        pyxel.blt(self.mid - 56, 2, 0, 16,24,16,16)
        # # # A
        pyxel.blt(self.mid - 41, 2, 0, 32,24,16,16)
        # # # K
        pyxel.blt(self.mid - 25, 2, 0, 48,24,16,16)
        # # # E
        pyxel.blt(self.mid - 9, 2, 0, 64,24,16,16)
        # # # G
        pyxel.blt(self.mid + 5, 2, 0, 0,40,16,16)
        # # A
        pyxel.blt(self.mid + 21, 2, 0, 16,40,16,16)
        # # M
        pyxel.blt(self.mid + 37, 2, 0, 32,40,16,16)
        # # E
        pyxel.blt(self.mid + 53, 2, 0, 48,40,16,16)

    def _draw_snake(self, x, y):
        pass

    def _center(self, text):
        text_width = len(text) * 4  
        return ((emu_u.SCREEN_WIDTH) - text_width) // 2

    def _draw_benchmark(self):
        # Layout constants
        left = emu_u.SCREEN_WIDTH - emu_u.SYS_WIDTH
        top = emu_u.GAME_HEIGHT
        line_height = 8
        text_color = 7
        bg_color = 0
        border_color = 7

        # Determine the far-right drawing position for register values
        bar_x = left + 165
        content_right = bar_x + 70  # Enough for "|   REG: VALUE"

        panel_width = content_right - left + 10  # Slight margin to the right
        panel_height = emu_u.SCREEN_HEIGHT - top + 20

        # Draw border and background fill
        pyxel.rectb(left, top - 20, panel_width - 25, panel_height, border_color)
        pyxel.rect(left + 1, top - 19, panel_width - 40, panel_height - 2, bg_color)

        # Header
        pyxel.text(left + 10, top - 14, "Arch242 CPU Emulator", text_color)
        pyxel.text(left + 8, top - 8, "-" * 49, text_color)

        # Instruction and PC
        pyxel.text(left + 10, top, "INSTRUCTION:", text_color)
        pyxel.text(left + 90, top + line_height, f"{self.emulator.instr.bin}", text_color)
        pyxel.text(left + 90, top, f"{dasm.instruction_map[self.emulator.instr.bin]()}", text_color)

        pyxel.text(left + 10, top + 2 *  line_height, "PROGRAM COUNTER:", text_color)
        pyxel.text(left + 110, top + 2 * line_height, f"{self.emulator.PC}", text_color)

        pyxel.text(left + 10, top + 3 * line_height, "CPU CLOCK CYCLE:", text_color)
        # pyxel.text(left + 110, top + 2 * line_height, f"{self.emulator.clock}", text_color)

        # Visual register marker
        for i in range(7):  # enough for RA–CF
            pyxel.text(bar_x, top + i * line_height, "|", text_color)

        # Register display beside the markers
        reg_labels = ["RA", "RB", "RC", "RD", "RE", "ACC", "CF"]
        for i, reg in enumerate(reg_labels):
            y = top + i * line_height
            value = self.emulator.RegFile.get(reg, 0)
            pyxel.text(bar_x + 10, y, f"{reg}: {value:02X}", text_color)





    def _draw_hud(self):
        # Clear HUD area (keep original background)
        pyxel.rect(-emu_u.SYS_WIDTH, emu_u.GAME_HEIGHT - 20, emu_u.SCREEN_WIDTH, emu_u.SCREEN_HEIGHT, 1)

        # --- LEFT: INSTRUCTIONS (unchanged) ---
        pyxel.text(10, emu_u.GAME_HEIGHT - 14, "HOW TO PLAY", 7)
        pyxel.blt(15, emu_u.GAME_HEIGHT - 5, 0, 10, 57, 40, 20, 0)
        pyxel.text(15, emu_u.GAME_HEIGHT + 17, "Press arrow keys", 7)
        pyxel.text(8, emu_u.GAME_HEIGHT + 25, "to change direction", 7)

        center_left = emu_u.SCREEN_WIDTH // 3  # Shifted left from absolute center

        # Score (aligned with icons)
        pyxel.blt(center_left - 20, emu_u.GAME_HEIGHT - 12, 0, 32, 88, 16, 16, 0)
        pyxel.text(center_left, emu_u.GAME_HEIGHT - 6, "SCORE:", 7)

        # LED ON
        pyxel.blt(center_left - 20, emu_u.GAME_HEIGHT + 12, 0, 0, 88, 16, 16, 0)
        pyxel.text(center_left, emu_u.GAME_HEIGHT + 18, "LED ON:", 7)

        # LED OFF
        pyxel.blt(center_left - 20, emu_u.GAME_HEIGHT + 36, 0, 16, 88, 16, 16, 0)
        pyxel.text(center_left, emu_u.GAME_HEIGHT + 40, "LED OFF:", 7)
        
    def draw(self):
        self._draw_cell()
        self._draw_hud()
        self._draw_benchmark()
        self._draw_title()

class Arch242Emulator: # CPU
    def __init__(self):  
        # # --- Special Registers,General Purpose Registers, I/O # Registers
        self.PC: int = 0
        reg_names: list[int] = ['ACC', 'CF','TEMP','RA','RB','RC','RD','RE', 'IOA']
        self.RegFile: dict[str, int] = {name: 0 for name in reg_names}
        self.CFACC: int = 0
        self.RBRA: int = 0
        self.RDRC: int = 0
        self.RegFile['ACC'] = 0b1

        # Init System
        self.clock_cycle: int = 0
        self.instr: str = " "
        self.emuState = EmulatorState(False, False)

        # Instantiation
        self.emu_i = EmulatorInstructions(self)
        self.DataMemory = DataMemory().Data
        self.InstrMemory = InstrMemory().Instruction
        
    def clock_tick(self):
        # brief pause to start the game
        self.load_instructions()
        self.instr = self.fetch()
        self.iohardware()
        if (self.instr):
            self.decode()
            self.execute()
        
        self.clock_cycle += 1
        
        return
    
    def load_instructions(self):
        # Run the assembler first 
        subprocess.run(["python", ASM_PATH], check=True)

        with open(Path(emu_u.PATH), "r") as f:
            assembled = f.readlines()

        for line in assembled:
            self.DataMemory.append(line.strip()) if (line[:5] == ".byte") else self.InstrMemory.append(line.strip())
        return
        
    def fetch(self):
        if (self.InstrMemory):
            instruction = self.InstrMemory[self.PC]
            return instruction
        
    
    def decode(self):
        opcode_bits = self.instr[:4]

        opcode_bits = "100X" if opcode_bits == "1001" or opcode_bits == "1000" else opcode_bits

        type = dasm.instr_type[opcode_bits]
        
        if type in dasm.instr_16_bit or self.instr == "00110111": # shutdown
            self.PC += 1
            self.instr += self.fetch() # 16 bit instruction
        else: 
            self.instr = self.instr

        self.instr: Instructions = Instructions(type, self.instr, int(asm_u.to_strbin(self.instr), 2))
        # print(dasm.instruction_map[self.instr.bin]())        
        
    def execute(self): # alu
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

    def iohardware(self):
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0001 if pyxel.btn(pyxel.KEY_UP) else self.RegFile['IOA'] & 0b1110
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0010 if pyxel.btn(pyxel.KEY_DOWN) else self.RegFile['IOA'] & 0b1101
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0100 if pyxel.btn(pyxel.KEY_LEFT) else self.RegFile['IOA'] & 0b1011
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b1000 if pyxel.btn(pyxel.KEY_RIGHT) else self.RegFile['IOA'] & 0b0111

        # print(self.RegFile['IOA'])
def main():
    cpu = Arch242Emulator()
    Pyxel(cpu)

if __name__ == "__main__":
    main()