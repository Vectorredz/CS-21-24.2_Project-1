from dataclasses import dataclass
import emulator.disassembler as dasm
from emulator import emu_utils as emu_u
from emulator.emu_instructions import EmulatorInstructions
from assembler import asm_utils as asm_u
from pathlib import Path
import pyxel
import subprocess

BASE_DIR = Path(__file__).resolve().parent
ASM_PATH = BASE_DIR / "assembler" / "asm_assembler.py"

"""
TODO:
    - shutdown
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
    type: str # last 4-bits 
    bin: str 
    dec: str

@dataclass
class MatrixCell:
    memAddr: int
    mapbit: int
    state: int

class DataMemory:
    def __init__(self, size=2**emu_u.MEM_BITS):
        self.Data: list[int] = [] * size
        # --- a 1D array of data memory

class InstrMemory:
    def __init__(self, size=2**emu_u.INSTR_BITS):
        self.Instruction: list[int] = [] * size
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
        pyxel.init(self.screen_width, self.screen_height, fps=30)
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
      
    def _draw_cell(self):
        pyxel.rect(0, 0, emu_u.SCREEN_WIDTH, emu_u.SCREEN_HEIGHT, 0)

        matrix_width = self.cols * emu_u.DIM
        matrix_height = self.rows * emu_u.DIM

        offset_x = (emu_u.SCREEN_WIDTH - matrix_width) // 2
        offset_y = (emu_u.SCREEN_HEIGHT - matrix_height) // 2

        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * emu_u.DIM
                y = offset_y + row * emu_u.DIM
                color = 11 if self.led_matrix[row][col].state == 1 else 6
                pyxel.rect(x, y, emu_u.DIM - 1, emu_u.DIM - 1, color)

    def draw(self):
        self._draw_cell()

class Arch242Emulator: # CPU
    def __init__(self):  
        # # --- Special Registers,General Purpose Registers, I/O Registers
        self.PC: int = 0
        reg_names: list[int] = ['ACC', 'CF','TEMP','RA','RB','RC','RD','RE', 'IOA']
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
        # self.iohardware()
        # if (self.instr):
        #     self.decode()
        #     self.execute()
        
        self.clock_cycle += 1
        
        return
    
    def load_instructions(self):
        # Run the assembler first 
        subprocess.run(["python", ASM_PATH], check=True)

        with open(Path(emu_u.PATH), "r") as f:
            assembled = f.readlines()

        for line in assembled:
            self.DataMemory.append(line.strip()) if (line[:5] == ".byte") else self.InstrMemory.append(line.strip())
            print(line)
        return
        
    def fetch(self):
        if (self.InstrMemory):
            instruction = self.InstrMemory[self.PC] 
            return instruction
    
    def decode(self):
        typebits = self.instr[:4]
        typebits = "100X" if typebits == "1001" or typebits == "1000" else typebits
        type = dasm.instr_type[typebits]
            
        self.instr = Instructions(type, self.instr, int(asm_u.to_strbin(self.instr), 2))
        
    def execute(self): # alu
        match (self.instr.type):
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

cpu = Arch242Emulator()
Pyxel(cpu)
