from dataclasses import dataclass
import disassembler as dasm
import asm_utils as asm_u
from pathlib import Path
import pyxel
import subprocess

"""
TODO:
    - shutdown
    - HUD
    - test instructions

"""
INSTR_BITS = INSTR_16 = 16
MEM_BITS = INSTR_8 = 8
INSTR_4 = 4

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 300
DIM = 10
PATH = "Arch242_output_file.asm"

# MASKS
HEX_16U4 = 0xF000
HEX_16L12 = 0x0FFF
HEX_16L4 = 0x000F
HEX_16U8 = 0xFF00
HEX_16U5 = 0xF800
BIN_13 = 0b001000000000
HEX_8L4 = 0x0F
HEX_8U4 = 0xF0

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
    def __init__(self, size=2**MEM_BITS):
        self.Data: list[int] = [] * size
        # --- a 1D array of data memory
    
class InstrMemory:
    def __init__(self, size=2**INSTR_BITS):
        self.Instruction: list[int] = [] * size
        # --- a 1D array of instruction memory

class Pyxel:
    def __init__(self, emulator: "Arch242Emulator"):
        # --- Pyxel
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
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
        pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0)

        matrix_width = self.cols * DIM
        matrix_height = self.rows * DIM

        offset_x = (SCREEN_WIDTH - matrix_width) // 2
        offset_y = (SCREEN_HEIGHT - matrix_height) // 2

        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * DIM
                y = offset_y + row * DIM
                color = 11 if self.led_matrix[row][col].state == 1 else 6
                pyxel.rect(x, y, DIM - 1, DIM - 1, color)

    def draw(self):
        self._draw_cell()

class Arch242Emulator: # CPU
    def __init__(self):  
        # # --- Special Registers,General Purpose Registers, I/O Registers
        self.PC: int = 0
        reg_names: list[int] = ['ACC', 'CF','TEMP','RA','RB','RC','RD','RE', 'IOA']
        self.RegFile: dict[str, int] = {name: 0 for name in reg_names}
        self.clock_cycle: int = 0

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
        subprocess.run(["python", Path("assembler.py")], check=True)

        with open(Path(PATH), "r") as f:
            assembled = f.readlines()
        
        for instr in assembled:
            self.InstrMemory.append(instr.strip())
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
                self._type1()
            case "Type2":
                self._type2()
            case "Type3":
                self._type3()
            case "Type4":
                self._type4()
            case "Type5":
                self._type5()
            case "Type6":
                self._type6()
            case "Type7":
                self._type7()
            case "Type8":
                self._type8()
            case "Type9":
                self._type9()
            case "Type10":
                self._type10()
            case "Type11":
                self._type11()
            case "Type12":
                self._type12()
            case "Type13":
                self._type13()
            case "Type14":
                self._type14()

    def iohardware(self):
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0001 if pyxel.btn(pyxel.KEY_UP) else self.RegFile['IOA'] & 0b1110
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0010 if pyxel.btn(pyxel.KEY_DOWN) else self.RegFile['IOA'] & 0b1101
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b0100 if pyxel.btn(pyxel.KEY_LEFT) else self.RegFile['IOA'] & 0b1011
        self.RegFile['IOA'] = self.RegFile['IOA'] | 0b1000 if pyxel.btn(pyxel.KEY_RIGHT) else self.RegFile['IOA'] & 0b0111

    def _overflow(self, result):
        mask = 0b100000000
        return bool(mask & result)

    def _underflow(self, result):
        # if msb is 1 there is an underflow // assumes signed borrow
        # a < b
        mask = 0b10000000
        return bool(mask & result)

    # instructions 1 - 16
    def _type1(self):
        mask = 0b11111111
        rbra = self.RegFile['RB'] << (INSTR_4) | self.RegFile['RA']
        rdrc = self.RegFile['RD'] << (INSTR_4) | self.RegFile['RC']
        if self.instr.dec == 0b00000000: # 1. rot-r
            dacc = self.RegFile['ACC'] >> 1
            self.RegFile['ACC'] = ((self.RegFile['ACC'] & 0b1) << (INSTR_8-1)) | dacc

        elif self.instr.dec == 0b00000001: # 2. rot-l
            dacc = self.RegFile['ACC'] << 1
            self.RegFile['ACC'] = (dacc & mask) | dacc >> INSTR_8

        elif self.instr.dec == 0b00000010: # 3. rot-rc
            cfacc = self.RegFile['CF'] << INSTR_8 | self.RegFile['ACC']
            dcfacc = cfacc >> 1
            self.CFACC = (cfacc & 0b1 << INSTR_8-1) | dcfacc 
       
        elif self.instr.dec  == 0b00000011: # 4. rot-lc
            cfacc = self.RegFile['CF'] << INSTR_8 | self.RegFile['ACC']
            dcfacc = cfacc << 1
            self.CFACC = (dcfacc & mask) | dcfacc >> INSTR_8
        
        elif self.instr.dec == 0b00000100: # 5. from-mba
            self.RegFile['ACC'] = self.DataMemory[rbra]
        
        elif self.instr.dec == 0b00000101: # 6. to-mba
            self.DataMemory[rbra] = self.RegFile['ACC']
       
        elif self.instr.dec == 0b00000110: # 7. from-mbc
            self.RegFile['ACC'] = self.DataMemory[rdrc]
       
        elif self.instr.dec == 0b00000111: # 8. to-mbc
            self.DataMemory[rdrc] = self.RegFile['ACC']

        elif self.instr.dec == 0b00001000: # 9. addc-mba
            result = self.RegFile['ACC'] + self.DataMemory[rbra] + self.RegFile['CF']
            self.RegFile['CF'] = self._overflow(result)

        elif self.instr.dec == 0b00001001: # 10. add-mba
            result = self.RegFile['ACC'] + self.DataMemory[rdrc]
            self.RegFile['CF'] = self._overflow(result)

        elif self.instr.dec == 0b00001010: # 11. subc-mba
            result = self.RegFile['ACC'] - self.DataMemory[rbra] + self.RegFile['CF']
            self.RegFile['CF'] = self._underflow(result)

        elif self.instr.dec == 0b00001011: # 12. sub-mba
            result = self.RegFile['ACC'] - self.DataMemory[rbra]
            self.RegFile['CF'] = self._underflow(result)

        elif self.instr.dec == 0b00001100: # 13. inc*-mba
            self.DataMemory[rbra] = self.DataMemory[rbra] + 1
        
        elif self.instr.dec == 0b00001101: # 14. dec*-mba
            self.DataMemory[rbra] = self.DataMemory[rbra] - 1

        elif self.instr.dec == 0b00001110: # 15. inc*-mdc
            self.DataMemory[rdrc] = self.DataMemory[rdrc] + 1
        
        elif self.instr.dec == 0b00001111: # 16. dec*-mdc
            self.DataMemory[rdrc] = self.DataMemory[rdrc] - 1
        
        self.PC += 1

        return 
    
    # instructions 17 - 24
    def _type2(self):
        reg_bits = self.instr.bin[4:7]
        tag_bit = self.instr.bin[-1]
        rdrc = self.RegFile['RD'] << (INSTR_4) | self.RegFile['RC']
        rbra = self.RegFile['RB'] << (INSTR_4) | self.RegFile['RA']

        if reg_bits in dasm.registers and tag_bit == 0: # 17. inc*-reg
            reg_name = dasm.registers[reg_bits]
            self.RegFile[reg_name] += 1

        elif reg_bits in dasm.registers and tag_bit == 1: # 18. dec*-reg
            reg_name = dasm.registers[reg_bits]
            self.RegFile[reg_name] -= 1

        elif self.instr == 0b00011010: # 19. and-ba
            accAndMem = self.RegFile['ACC'] & self.DataMemory[rbra]
            self.RegFile['ACC'] = accAndMem

        elif self.instr == 0b00011011: # 20. xor-ba
            accXorMem = self.RegFile['ACC'] ^ self.DataMemory[rbra]
            self.RegFile['ACC'] = accXorMem
        
        elif self.instr == 0b00011100: # 21. or-ba
            accOrMem = self.RegFile['ACC'] | self.DataMemory[rbra]
            self.RegFile['ACC'] = accOrMem

        elif self.instr == 0b00011101: # 22. and*-mba
            memAndAcc = self.RegFile['ACC'] & self.DataMemory[rbra]
            self.DataMemory[rbra] = memAndAcc
        
        elif self.instr == 0b00011110: # 23. xor*-mba
            memXorAcc = self.RegFile['ACC'] ^ self.DataMemory[rbra]
            self.DataMemory[rbra] = memXorAcc
        
        elif self.instr == 0b00011111: # 24. or*-mba
            memOrAcc = self.RegFile['ACC'] | self.DataMemory[rbra]
            self.DataMemory[rbra] = memOrAcc
        
        self.PC += 1

        return
    # instructions 25 - 48
    def _type3(self):
        reg_bits = self.instr.bin[4:7]
        tag_bit = self.instr.bin[-1]

        if reg_bits in dasm.registers and tag_bit == 0: # 25. to-ref     
            reg_name = dasm.registers[reg_bits]
            self.RegFile[reg_name] = self.RegFile['ACC']

        elif reg_bits in dasm.registers and tag_bit == 1: # 26. from-reg
            reg_name = dasm.registers[reg_bits]
            self.RegFile['ACC'] = self.RegFile[reg_name]

        elif self.instr.dec == 0b00101010: # 27. clr-cf
            self.RegFile['CF'] = 0
        
        elif self.instr.dec == 0b00101011: # 28. set-cf	
            self.RegFile['CF'] = 1

        elif self.instr.dec == 0b00101110: # 31. ret
            lowerTemp = self.TEMP & HEX_16L12 
            upperAcc = self.RegFile['ACC'] & HEX_16U4
            self.RegFile['ACC'] = upperAcc | lowerTemp
            self.TEMP = 0
        
        elif self.instr.dec == 0b00110000: # 33. from-ioa
            self.RegFile['ACC'] = self.RegFile['IOA']
        
        elif self.instr.dec == 0b00110001: # 34. inc
            self.RegFile['ACC'] = self.RegFile['ACC'] + 1
        
        elif self.instr.dec == 0b00110001: # 34. inc
            self.RegFile['ACC'] = self.RegFile['ACC'] + 1
        
        elif self.instr.dec == 0b00110110: # 39. bcd
            if (self.RegFile['ACC'] >= 0b1010 | self.RegFile['CF'] == 1):
                self.RegFile['ACC'] = self.RegFile['ACC'] + 0b0110
                self.RegFile['CF'] = 1
            
        elif self.instr.dec == 0b0011011100111110: # 40. shutdown
            exit()

        elif self.instr.dec == 0b00111110: # 47. nop
            ...

        elif self.instr.dec == 0b00111111: # 48. dec
            self.RegFile['ACC'] = self.RegFile['ACC'] - 1

                   
        self.PC += 1

        return 

    # instructions 49 - 64
    def _type4(self):
        imm = self.instr.dec & HEX_16L4
        op = (self.instr.dec & HEX_16U8) >> INSTR_8 # get the logical op
        key_op = asm_u.to_bin(op, INSTR_8)
        match (dasm.to_operation[key_op]):
            case "add": # 49
                self.RegFile['ACC'] = self.RegFile['ACC'] + imm
            case "sub": # 50
                self.RegFile['ACC'] = self.RegFile['ACC'] - imm
            case "and": # 51
                self.RegFile['ACC'] = self.RegFile['ACC'] & imm
            case "xor": # 52
                self.RegFile['ACC'] = self.RegFile['ACC'] ^ imm
  
            case "or": # 53
                self.RegFile['ACC'] = self.RegFile['ACC'] | imm
            case "r4": # 55
                self.RegFile['RE'] = imm
               
        self.PC += 1

        return 
    
    # instructions 65
    def _type5(self):
        rb_imm = int(self.instr.bin[12:], 2) << 4
        ra_imm = int(self.instr.bin[4:8] , 2)
        imm = rb_imm | ra_imm

        self.RegFile['RA'] = ra_imm
        self.RegFile['RB'] = rb_imm

        self.PC += 1

        return 

    # instructions 66
    def _type6(self):
        rc_imm = int(self.instr.bin[12:], 2) << 4
        rd_imm = int(self.instr.bin[4:8] , 2)
        imm = rc_imm | rd_imm

        self.RegFile['RC'] = rc_imm
        self.RegFile['RD'] = rd_imm
               
        self.PC += 1

        return 

    # instructions 67
    def _type7(self):
        imm = self.instr & HEX_8L4 # 67. acc <imm>	
        self.RegFile['ACC'] = imm

        self.PC += 1

        return 

    # instructions 68
    def _type8(self):
        k = int(self.instr.bin[3:5], 2)
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        if (self.PC & k == 1):
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm

        self.PC += 1

        return 
    # instructions 69 - 70
    def _type9(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        if (tag == 0):  # 69. bnz-a <imm>
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm
        elif (tag == 1): # 70. bnz-b <imm>
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm

        self.PC += 1

        return   
    
    # instructions 71 - 72
    def _type10(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        if (self.RegFile['ACC'] != 0 and tag == 0): # 71. beqz <imm>
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm
        elif (self.RegFile['ACC'] == 0 and tag == 1): # 72. bnez <imm>
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm

        self.PC += 1

        return 

    # instructions 73 - 74
    def _type11(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        if (self.RegFile['CF'] != 0 and tag == 0): # 73. beqz-cf <imm>
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm
        elif (self.RegFile['CF'] == 0 and tag == 1): # 74. bnez-cf <imm>
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm
        
        self.PC += 1

        return 

    # instructions 75 - 76
    def _type12(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        if (self.RegFile['RD'] != 0 and tag == 1): # 76. bnez-cf <imm>
            upperPC = self.PC & HEX_16U5
            self.PC = upperPC | imm
        
        self.PC += 1

        return 

    # instructions 77
    def _type13(self):
        b = int(self.instr.bin[4:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        upperPC = self.PC & HEX_16U4
        self.PC = upperPC | imm

        self.PC += 1

        return 

    # instructions 78
    def _type14(self):
        b = int(self.instr.bin[4:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        self.TEMP = self.PC + 2
        upperPC = self.PC & HEX_16U4
        self.PC = upperPC | imm

        self.PC += 1

        return 

cpu = Arch242Emulator()
Pyxel(cpu)