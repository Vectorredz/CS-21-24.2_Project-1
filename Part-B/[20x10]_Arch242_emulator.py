import emulator.disassembler as dasm
from emulator import emu_utils as emu_u
from emulator.emu_instructions import EmulatorInstructions
from assembler import asm_utils as asm_u
from sys import argv
from dataclasses import dataclass
from pathlib import Path
import pyxel

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
    opcode: str # last 4-bits 
    bin: str 
    dec: str

@dataclass
class MatrixCell:
    memAddr: int
    mapbit: int
    state: int

class DataMemory:
    def __init__(self, size=2**emu_u.MEM_BITS):
        self.Data: list[int] = []
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
        self.rows = 20
        self.cols = 10
        self.mem_addr = 192
        self.emulator = emulator
        self.score = 0 
        pyxel.init(self.screen_width, self.screen_height, fps=30)
        pyxel.load(str(Path("assets/snake.pyxres")))
        self._build_matrix()
        pyxel.run(self.update, self.draw)

    def _build_matrix(self):
        mmio_addr = [data for data in range(192, 242)]
        self.led_matrix = [[None for _ in range(self.cols)] for _ in range(self.rows)]
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

    def _write_cell(self, mem_addr, val):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.led_matrix[row][col]
                if (cell.memAddr == mem_addr) & (cell.mapbit == val):
                    self.led_matrix[row][col].state = 1

    # def print_matrix(self):
    #     for row in self.led_matrix:
    #         print("".join("1" if cell.state else "0" for cell in row))  

    def update(self):
        self._write_cell(self.mem_addr, self.emulator.RegFile['IOA'])
        self.emulator.clock_tick()
    
    def draw(self):
        self._draw_cell()
      
    def _draw_cell(self):
        pyxel.rect(0, 0, emu_u.GAME_WIDTH, emu_u.SCREEN_HEIGHT, 3)
        self._draw_hud()
        matrix_width = self.cols * emu_u.DIM
        matrix_height = self.rows * emu_u.DIM
        
        offset_x = (emu_u.GAME_WIDTH - matrix_width) // 2
        offset_y = (emu_u.SCREEN_HEIGHT - matrix_height) // 2
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * emu_u.DIM
                y = offset_y + row * emu_u.DIM
                print(x, y)
                pyxel.blt(x,y,0,12,0,12,12)
                # pyxel.rectb(x, y, emu_u.DIM, emu_u.DIM, 0)
                # color = 11 if self.led_matrix[row][col].state == 1 else 6
                # pyxel.rect(x, y, emu_u.DIM - 1, emu_u.DIM - 1, color)        
        
    def _draw_title(self):
          # S
        pyxel.blt(emu_u.GAME_WIDTH + 10, 10, 0, 0,24,16,16)
        # N
        pyxel.blt(emu_u.GAME_WIDTH + 26, 10, 0, 16,24,16,16)
        # # A
        pyxel.blt(emu_u.GAME_WIDTH + 41, 10, 0, 32,24,16,16)
        # # K
        pyxel.blt(emu_u.GAME_WIDTH + 56, 10, 0, 48,24,16,16)
        # # E
        pyxel.blt(emu_u.GAME_WIDTH + 72, 10, 0, 64,24,16,16)
        # # G
        pyxel.blt(emu_u.GAME_WIDTH + 16, 26, 0, 0,40,16,16)
        # A
        pyxel.blt(emu_u.GAME_WIDTH + 32, 26, 0, 16,40,16,16)
        # M
        pyxel.blt(emu_u.GAME_WIDTH + 48, 26, 0, 32,40,16,16)
        # E
        pyxel.blt(emu_u.GAME_WIDTH + 64, 26, 0, 48,40,16,16)

    def _draw_snake(self, x, y):
        pyxel.blt(5,5, 0,0,56,11,11, 0)

    def _center(self, text):
        text_width = len(text) * 4  
        return emu_u.GAME_WIDTH + ((emu_u.SCREEN_WIDTH - emu_u.GAME_WIDTH) - text_width) // 2

    def _draw_hud(self):
        
        pyxel.rect(emu_u.GAME_WIDTH, 0, (emu_u.SCREEN_WIDTH - emu_u.GAME_WIDTH), emu_u.SCREEN_HEIGHT, 1) 
        self._draw_title()
        pyxel.blt(emu_u.GAME_WIDTH + 22, 58, 0, 31,0,10,12,0)
        pyxel.text(self._center("SCORE:") - 5, 60, "SCORE:", 7)
        pyxel.text(self._center(f"{self.score}") + 10, 60, f"{self.score}", 7)
        pyxel.text(self._center("HOW TO PLAY"), 76, "HOW TO PLAY", 7)
        pyxel.text(self._center("press arrow keys"), 110, "Press arrow keys", 7)
        pyxel.text(self._center("to change direction"), 120, "to change direction", 7)
        pyxel.blt(emu_u.GAME_WIDTH + 35, 86, 0, 10,57,40,20, 0)
  

class Arch242Emulator: # CPU
    def __init__(self):  
        # # --- Special Registers,General Purpose Registers, I/O Registers
        self.PC: int = 0
        reg_names: list[int] = ['ACC', 'CF','TEMP','RA','RB','RC','RD','RE', 'IOA']
        self.rbra: int = 0
        self.rdrc: int = 0

        self.RegFile: dict[str, int] = {name: 0 for name in reg_names}
        self.clock_cycle: int = 0
        self.emuState = EmulatorState(False, False)
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

        self.instr = Instructions(type, self.instr, int(asm_u.to_strbin(self.instr), 2))
        
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


def main():
    cpu = Arch242Emulator()
    Pyxel(cpu)

if __name__ == "__main__":
    main()