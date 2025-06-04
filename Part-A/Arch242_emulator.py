# TODO CHECK EVERY INSTRUCTIONS + 40-42 & 47

from dataclasses import dataclass
import disassembler as dasm
import asm_utils as asm_u
from pathlib import Path
import subprocess

INSTR_BITS = INSTR_16 = 16
MEM_BITS = INSTR_8 = 8
INSTR_4 = 4
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
    bin: str 
    dec: str
    
class DataMemory:
    def __init__(self, size=2**MEM_BITS):
        self.Data = [] * size
        # --- a 1D array of data memory
    
class InstrMemory:
    def __init__(self, size=2**INSTR_BITS):
        self.Instruction = [] * size
        # --- a 1D array of instruction memory

class Processor:
    def __init__(self):
        # --- Special Register
        self.PC = Register('PC', 0b0) # program counter // assume 16-bit
        self.PA = Register('PA', 0b0)
        self.SP = Register('SP', 0b0) # stack pointer
        self.GP = Register('GP', 0b0) # global pointer
        self.ACC = Register('ACC', 0b10000001) # accumulator
        self.CFACC = Register('CFACC', 0b0) # carry flag : accumulator 
        self.CF = Register('CF', 0b0) # carry flag
        self.EI = Register('EI', 0b0) # enable interrupts
        self.TEMP = Register('TEMP', 0b0) # temp // assume 16-bit
        self.TIMER = Register('TIMER', 0b0) # timer
         
        # --- General Purpose Registers && I/O Registers
        reg_names = ['RA','RB','RC','RD','RE','RF', 'IOA', 'IOB', 'IOC']
        self.RegFile = {name: Register(name, 0b0) for name in reg_names}

        self.DataMemory = DataMemory().Data
        self.InstrMemory = InstrMemory().Instruction

        # cycle 1
        self.clock_cycle()
    
    def clock_cycle(self):
        self.instr = self.fetch()
        self.decode()
        
    def fetch(self):
        # Run the assembler first 
        subprocess.run(["python", Path("assembler.py")], check=True)

        with open(Path(PATH), "r") as f:
            self.InstrMemory.append(f.readline().strip()) # remove newline

        instruction = self.InstrMemory[self.PC.val] # get the memory from the current pc
        return instruction
    
    def decode(self):
        # fetched = dasm.instruction_map[self.instr]() 

        typebits = self.instr[:4]
        typebits = "100X" if typebits == "1001" or typebits == "1000" else typebits
        type = dasm.instr_type[typebits]
            
        self.instr = Instructions(type, self.instr, int(asm_u.to_strbin(self.instr), 2))
        self.execute()
        
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
        rbra = self.RegFile['RB'].val << (INSTR_4) | self.RegFile['RA'].val
        rdrc = self.RegFile['RD'].val << (INSTR_4) | self.RegFile['RC'].val
        if self.instr.dec == 0b00000000: # 1. rot-r
            dacc = self.ACC.val >> 1
            self.ACC.val = ((self.ACC.val & 0b1) << (INSTR_8-1)) | dacc

        elif self.instr.dec == 0b00000001: # 2. rot-l
            dacc = self.ACC.val << 1
            self.ACC.val = (dacc & mask) | dacc >> INSTR_8

        elif self.instr.dec == 0b00000010: # 3. rot-rc
            cfacc = self.CF.val << INSTR_8 | self.ACC.val
            dcfacc = cfacc >> 1
            self.CFACC = (cfacc & 0b1 << INSTR_8-1) | dcfacc 
       
        elif self.instr.dec  == 0b00000011: # 4. rot-lc
            cfacc = self.CF.val << INSTR_8 | self.ACC.val
            dcfacc = cfacc << 1
            self.CFACC = (dcfacc & mask) | dcfacc >> INSTR_8
        
        elif self.instr.dec == 0b00000100: # 5. from-mba
            self.ACC.val = self.DataMemory[rbra]
        
        elif self.instr.dec == 0b00000101: # 6. to-mba
            self.DataMemory[rbra] = self.ACC.val
       
        elif self.instr.dec == 0b00000110: # 7. from-mbc
            self.ACC.val = self.DataMemory[rdrc]
       
        elif self.instr.dec == 0b00000111: # 8. to-mbc
            self.DataMemory[rdrc] = self.ACC.val

        elif self.instr.dec == 0b00001000: # 9. addc-mba
            result = self.ACC.val + self.DataMemory[rbra] + self.CF.val
            self.CF.val = self._overflow(result)

        elif self.instr.dec == 0b00001001: # 10. add-mba
            result = self.ACC.val + self.DataMemory[rdrc]
            self.CF.val = self._overflow(result)

        elif self.instr.dec == 0b00001010: # 11. subc-mba
            result = self.ACC.val - self.DataMemory[rbra] + self.CF.val
            self.CF.val = self._underflow(result)

        elif self.instr.dec == 0b00001011: # 12. sub-mba
            result = self.ACC.val - self.DataMemory[rbra]
            self.CF.val = self._underflow(result)

        elif self.instr.dec == 0b00001100: # 13. inc*-mba
            self.DataMemory[rbra] = self.DataMemory[rbra] + 1
        
        elif self.instr.dec == 0b00001101: # 14. dec*-mba
            self.DataMemory[rbra] = self.DataMemory[rbra] - 1

        elif self.instr.dec == 0b00001110: # 15. inc*-mdc
            self.DataMemory[rdrc] = self.DataMemory[rdrc] + 1
        
        elif self.instr.dec == 0b00001111: # 16. dec*-mdc
            self.DataMemory[rdrc] = self.DataMemory[rdrc] - 1
        
        self.PC.val += 1
    
    # instructions 17 - 24
    def _type2(self):
        reg_bits = self.instr.bin[4:7]
        tag_bit = self.instr.bin[-1]
        rdrc = self.RegFile['RD'].val << (INSTR_4) | self.RegFile['RC'].val
        rbra = self.RegFile['RB'].val << (INSTR_4) | self.RegFile['RA'].val

        if reg_bits in dasm.registers and tag_bit == 0: # 17. inc*-reg
            reg_name = dasm.registers[reg_bits]
            self.RegFile[reg_name].val += 1

        elif reg_bits in dasm.registers and tag_bit == 1: # 18. dec*-reg
            reg_name = dasm.registers[reg_bits]
            self.RegFile[reg_name].val -= 1

        elif self.instr == 0b00011010: # 19. and-ba
            accAndMem = self.ACC.val & self.DataMemory[rbra]
            self.ACC.val = accAndMem

        elif self.instr == 0b00011011: # 20. xor-ba
            accXorMem = self.ACC.val ^ self.DataMemory[rbra]
            self.ACC.val = accXorMem
        
        elif self.instr == 0b00011100: # 21. or-ba
            accOrMem = self.ACC.val | self.DataMemory[rbra]
            self.ACC.val = accOrMem

        elif self.instr == 0b00011101: # 22. and*-mba
            memAndAcc = self.ACC.val & self.DataMemory[rbra]
            self.DataMemory[rbra] = memAndAcc
        
        elif self.instr == 0b00011110: # 23. xor*-mba
            memXorAcc = self.ACC.val ^ self.DataMemory[rbra]
            self.DataMemory[rbra] = memXorAcc
        
        elif self.instr == 0b00011111: # 24. or*-mba
            memOrAcc = self.ACC.val | self.DataMemory[rbra]
            self.DataMemory[rbra] = memOrAcc

    # instructions 25 - 48
    def _type3(self):
        reg_bits = self.instr.bin[4:7]
        tag_bit = self.instr.bin[-1]

        if reg_bits in dasm.registers and tag_bit == 0: # 25. to-ref     
            reg_name = dasm.registers[reg_bits]
            self.RegFile[reg_name].val = self.ACC.val

        elif reg_bits in dasm.registers and tag_bit == 1: # 26. from-reg
            reg_name = dasm.registers[reg_bits]
            self.ACC.val = self.RegFile[reg_name].val

        elif self.instr.dec == 0b00101010: # 27. clr-cf
            self.CF.val = 0
        
        elif self.instr.dec == 0b00101011: # 28. set-cf	
            self.CF.val = 1
        
        elif self.instr.dec == 0b00101100: # 29. set-ei
            self.EI = 1

        elif self.instr.dec == 0b00101100: # 30. clr-ei
            self.EI = 0

        elif self.instr.dec == 0b00101110: # 31. ret
            lowerTemp = self.TEMP & HEX_16L12 
            upperAcc = self.ACC.val & HEX_16U4
            self.ACC.val = upperAcc | lowerTemp
            self.TEMP = 0

        elif self.instr.dec == 0b00101110: # 32. retc
            lowerTemp = self.TEMP & HEX_16L12 
            upperAcc = self.ACC.val & HEX_16U4
            self.ACC.val = upperAcc | lowerTemp
            self.CF.val = self.TEMP & BIN_13
            self.TEMP = 0
        
        elif self.instr.dec == 0b00110000: # 33. from-pa
            self.ACC.val = self.PA.val
        
        elif self.instr.dec == 0b00110001: # 34. inc
            self.ACC.val = self.ACC.val + 1
        
        elif self.instr.dec == 0b00110001: # 34. inc
            self.ACC.val = self.ACC.val + 1
        
        elif self.instr.dec == 0b00110010: # 35. to-ioa
            self.RegFile['IOA'].val = self.ACC.val 
        
        elif self.instr.dec == 0b00110011: # 36. to-iob
            self.RegFile['IOB'].val = self.ACC.val 
        
        elif self.instr.dec == 0b00110011: # 37. to-ioc
            self.RegFile['IOC'].val = self.ACC.val 

        elif self.instr.dec == 0b00110101: # 38. -
            ...
        
        elif self.instr.dec == 0b00110110: # 39. bcd
            if (self.ACC.val >= 0b1010 | self.CF.val == 1):
                self.ACC.val = self.ACC.val + 0b0110
                self.CF.val = 1
            
        elif self.instr.dec == 0b0011011100111110: # 40. shutdown
            exit()

        elif self.instr.dec == 0b00111000: # 41. timer-start
            ...

        elif self.instr.dec == 0b00111000: # 42. timer-send
            ...
        
        elif self.instr.dec == 0b00111010: # 43. from-timerl
            self.ACC.val = self.TIMER.val & HEX_8L4 

        elif self.instr.dec == 0b00111011: # 44. from-timerh
            self.ACC.val = (self.TIMER.val & HEX_8U4) >> 4

        elif self.instr.dec == 0b00111100: # 45. to-timerl
            lowerAcc =  self.ACC.val & HEX_8L4
            upperTimer =  self.TIMER.val & HEX_8U4
            self.TIMER.val = upperTimer | lowerAcc
        
        elif self.instr.dec == 0b00111101: # 46. to-timerh
            lowerAcc = HEX_8L4 & self.ACC.val
            upperTimer = (HEX_8U4 & self.TIMER.val) >> 4
            self.TIMER.val = upperTimer | lowerAcc

        elif self.instr.dec == 0b00111110: # 47. nop
            ...

        elif self.instr.dec == 0b00111111: # 48. dec
            self.ACC.val = self.ACC.val - 1

    # instructions 49 - 64
    def _type4(self):
        imm = self.instr.dec & HEX_16L4
        op = (self.instr.dec & HEX_16U8) >> INSTR_8 # get the logical op
        key_op = asm_u.to_bin(op, INSTR_8)
        match (dasm.to_operation[key_op]):
            case "add": # 49
                self.ACC.val = self.ACC.val + imm
            case "sub": # 50
                self.ACC.val = self.ACC.val - imm
            case "and": # 51
                self.ACC.val = self.ACC.val & imm
            case "xor": # 52
                self.ACC.val = self.ACC.val ^ imm
            case "or": # 53
                self.ACC.val = self.ACC.val | imm
            case "r4": # 55
                self.RegFile['RE'].val = imm
            case "timer": # 56
                self.TIMER.val = imm
        # 57 - 60 ???
    
    # instructions 65
    def _type5(self):
        rb_imm = int(self.instr.bin[12:], 2) << 4
        ra_imm = int(self.instr.bin[4:8] , 2)
        imm = rb_imm | ra_imm

        self.RegFile['RA'].val = ra_imm
        self.RegFile['RB'].val = rb_imm

    # instructions 66
    def _type6(self):
        rc_imm = int(self.instr.bin[12:], 2) << 4
        rd_imm = int(self.instr.bin[4:8] , 2)
        imm = rc_imm | rd_imm

        self.RegFile['RC'].val = rc_imm
        self.RegFile['RD'].val = rd_imm

    # instructions 67
    def _type7(self):
        imm = self.instr & HEX_8L4 # 67. acc <imm>	
        self.ACC.val = imm

    # instructions 68
    def _type8(self):
        k = int(self.instr.bin[3:5], 2)
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        if (self.PC.val & k == 1):
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm

    # instructions 69 - 70
    def _type9(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        if (tag == 0):  # 69. bnz-a <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm
        elif (tag == 1): # 70. bnz-b <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm
        
    # instructions 71 - 72
    def _type10(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        if (self.ACC.val != 0 and tag == 0): # 71. beqz <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm
        elif (self.ACC.val == 0 and tag == 1): # 72. bnez <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm

    # instructions 73 - 74
    def _type11(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        if (self.CF.val != 0 and tag == 0): # 73. beqz-cf <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm
        elif (self.CF.val == 0 and tag == 1): # 74. bnez-cf <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm

    # instructions 75 - 76
    def _type12(self):
        b = int(self.instr.bin[5:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.instr.bin[4]

        # if timer on
        if (tag == 0): # 75. b-timer <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm
        elif (self.RegFile['RD'].val != 0 and tag == 1): # 76. bnez-cf <imm>
            upperPC = self.PC.val & HEX_16U5
            self.PC.val = upperPC | imm

    # instructions 77
    def _type13(self):
        b = int(self.instr.bin[4:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        upperPC = self.PC.val & HEX_16U4
        self.PC.val = upperPC | imm

    # instructions 78
    def _type14(self):
        b = int(self.instr.bin[4:8], 2)
        a = int(self.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        self.TEMP.val = self.PC.val + 2
        upperPC = self.PC.val & HEX_16U4
        self.PC.val = upperPC | imm
    
Processor()
