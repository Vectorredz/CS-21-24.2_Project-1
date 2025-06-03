from dataclasses import dataclass
import disassembler as dasm
import asm_utils as asm_u
from pathlib import Path
import subprocess

INSTR_BITS = INSTR_IMM = 16
MEM_BITS = INSTR_8 = 8
PATH = "Arch242_output_file.asm"

@dataclass
# --- Register class
class Register:
    name: str
    val: int

@dataclass
# --- flags to signal the processor of the ALU result
class ALUFlag:
    zero: int # ALU result == 0
    sign: int # ALU most significant bit
    of: int # ALU result cannot fit inside the 4-bit register
    carry: int # ALU indicate when arithmetic carry or borrow is generated from MSB

@dataclass
class Instructions:
# --- Instruction class
    type: str # last 4-bits 
    val: str # actual instruction bits
    
class DataMemory:
    def __init__(self, size=2**MEM_BITS):
        self.Data = [] * size
        # --- a 1D array of data memory
    
class InstrMemory:
    def __init__(self, size=2**INSTR_BITS):
        self.Instr = [] * size
        # --- a 1D array of instruction memory

class Processor:
    def __init__(self):
        # --- Special Register
        self.PC = Register('PC', 0b0) # program counter
        self.SP = Register('SP', 0b0) # stack pointer
        self.GP = Register('GP', 0b0) # global pointer
        self.ACC = Register('ACC', 0b10000001) # accumulator
        self.CFACC = Register('CFACC', 0b0) # carry flag : accumulator 
        self.CF = Register('CF', 0b0) # carry flag
        self.EI = Register('EI', 0b0) # enable interrupts
        self.TIMER = Register('TIMER', 0b0) # timer
         
        # --- General Purpose Registers && I/O Registers
        reg_names = ['RA','RB','RC','RD','RE','RF', 'IOA', 'IOB', 'IOC']
        self.RegFile = {name: Register(name, 0b0) for name in reg_names}

        self.DataMemory = DataMemory().Data
        self.InstrMemory = InstrMemory().Instr

        # cycle 1
        self.clock_cycle()
    
    def clock_cycle(self):
        self.instr = self.fetch()
        self.decode(self.instr)
        
    def fetch(self):
        # Run the assembler first 
        subprocess.run(["python", Path("assembler.py")], check=True)

        with open(Path(PATH), "r") as f:
            self.InstrMemory.append(f.readline().strip()) # remove newline

        self.instr = self.InstrMemory[self.PC.val] # get the memory from the current pc
        return self.instr
    
    def decode(self, instr):
        fetched = dasm.instruction_map[instr]()

        if len(instr) == INSTR_8:
            typebits = instr[:4] # read from the left
            bin_instr = int(instr, 2)
            type = dasm.instr_type[typebits]
            
            decoded_instr = Instructions(type, bin_instr)
            self.execute(decoded_instr)

    def execute(self, decoded_instr): # alu
        match (decoded_instr.type):
            case "Type1":
                self._type1(decoded_instr.val)
            case "Type2":
                self._type2(decoded_instr.val)
            case "Type3":
                self._type3(decoded_instr.val)
            case "Type4":
                self._type4(decoded_instr.val)
            case "Type5":
                self._type5(decoded_instr.val)
            case "Type6":
                self._type6(decoded_instr.val)
            case "Type7":
                self._type7(decoded_instr.val)
            case "Type8":
                self._type8(decoded_instr.val)
            case "Type9":
                self._type9(decoded_instr.val)
            case "Type10":
                self._type10(decoded_instr.val)
            case "Type11":
                self._type11(decoded_instr.val)
            case "Type12":
                self._type12(decoded_instr.val)
            case "Type13":
                self._type13(decoded_instr.val)

    def _overflow(self, sum):
        mask = 0b100000000
        return bool(mask & sum)

    def _underflow(self, sum):
        # if msb is 1 there is an underflow
        # a < b
        mask = 0b10000000
        return bool(mask & sum)

    # instructions 1 - 16
    def _type1(self, instr):
        mask = 0b11111111
        if instr == 0b00000000: # 1. rot-r
            dacc = self.ACC.val >> 1
            self.ACC.val = (self.ACC.val & 0b1 << INSTR_8-1) | dacc

        elif instr == 0b00000001: # 2. rot-l
            dacc = self.ACC.val << 1
            self.ACC.val = (dacc & mask) | dacc >> INSTR_8
        
        elif instr == 0b00000010: # 3. rot-rc
            cfacc = self.CF << INSTR_8 | self.ACC
            dcfacc = cfacc >> 1
            self.CFACC = (cfacc & 0b1 << INSTR_8-1) | dcfacc 
       
        elif instr == 0b00000011: # 4. rot-lc
            cfacc = self.CF << INSTR_8 | self.ACC
            dcfacc = cfacc << 1
            self.CFACC = (dcfacc & mask) | dcfacc >> INSTR_8
        
        elif instr == 0b00000100: # 5. from-mba
            rbra = self.RegFile['RB'].val << INSTR_8 | self.RegFile['RA'].val
            self.ACC = self.DataMemory[rbra]
        
        elif instr == 0b00000101: # 6. to-mba
            self.DataMemory[rbra] = self.ACC
       
        elif instr == 0b00000110: # 7. from-mbc
            rdrc = self.RegFile['RD'].val << INSTR_8 | self.RegFile['RC'].val
            self.ACC = self.DataMemory[rdrc]
       
        elif instr == 0b00000111: # 8. to-mbc
            self.DataMemory[rdrc] = self.ACC

        elif instr == 0b00001000: # 9. addc-mba
            sum = self.ACC + self.DataMemory[rbra] + self.CF
            self.CF = self._overflow(sum)

        elif instr == 0b00001001: # 10. add-mba
            sum = self.ACC + self.DataMemory[rdrc]
            self.CF = self._overflow(sum)

        elif instr == 0b00001010: # 11. subc-mba
            sum = self.ACC + self.DataMemory[rbra] - self.CF
            self.CF = self._underflow(sum)

        elif instr == 0b00001011: # 12. sub-mba
            sum = self.ACC - self.DataMemory[rbra]
            self.CF = self._underflow(sum)

        elif instr == 0b00001100: # 13. inc*-mba
            self.DataMemory[rbra] = self.DataMemory[rbra] + 1
        
        elif instr == 0b00001101: # 14. dec*-mba
            self.DataMemory[rbra] = self.DataMemory[rbra] - 1

        elif instr == 0b00001110: # 15. inc*-mdc
            self.DataMemory[rdrc] = self.DataMemory[rdrc] + 1
        
        elif instr == 0b00001111: # 16. dec*-mdc
            self.DataMemory[rdrc] = self.DataMemory[rdrc] - 1
        
        self.PC.val += 1
    
    # instructions 17 - 24
    def _type2(self, instr):
        ...

    # instructions 25 - 48
    def _type3(self, instr):
        ...

    # instructions 49 - 64
    def _type4(self, instr):
        ...
    
    # instructions 65 - 66
    def _type5(self, instr):
        ...
    
    # instructions 67
    def _type6(self, instr):
        ...

    # instructions 68
    def _type7(self, instr):
        ...

    # instructions 69 - 70
    def _type8(self, instr):
        ...
    
    # instructions 71 - 72
    def _type9(self, instr):
        ...
    
    # instructions 73 - 74
    def _type10(self, instr):
        ...

    # instructions 75 - 76
    def _type11(self, instr):
        ...

    # instructions 77
    def _type12(self, instr):
        ...

    # instructions 78
    def _type13(self, instr):
        ...
  
Processor()
