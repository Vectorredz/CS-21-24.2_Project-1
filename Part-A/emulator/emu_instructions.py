from __future__ import annotations
import emulator.disassembler as dasm
import emulator.emu_utils as emu_u
import assembler.asm_utils as asm_u
import sys
import os

# TODO: 2C OR SIGNED?

class EmulatorInstructions:
    def __init__(self, cpu) -> None:
        self.cpu = cpu

    def _overflow(self, result: int) -> bool:
        mask = 0b10000
        return bool(mask & result)
    
    def _truncate(self, result: int) -> int:
        return result & 0xF

    def _underflow(self, result: int) -> bool:
        # if msb is 1 there is an underflow // assumes signed borrow
        # a < b
        mask = 0b1000
        return bool(mask & result)
    
    def _readL4(self, addr: int) -> int:
        print(f"Reading memory at address: {addr}")
        # if 
        return int(self.cpu.DataMem.mem[addr]) & 0xF

    def _writeL4(self, addr: int, val: int) -> None:
        self.cpu.DataMem.mem[addr] = self._truncate(val) & 0xF

    def _PCNext(self, is_branch: bool) -> None:
       self.cpu.PC += 1 if not is_branch else 0

    # instructions 1 - 16
    def _type1(self):
        self.cpu.RBRA = self.cpu.RegFile['RB'] << (emu_u.INSTR_4) | self.cpu.RegFile['RA']
        self.cpu.RDRC = self.cpu.RegFile['RD'] << (emu_u.INSTR_4) | self.cpu.RegFile['RC']
        
        if self.cpu.instr.dec == 0b00000000: # 1. rot-r
            dacc = self.cpu.RegFile['ACC'] >> 1
            self.cpu.RegFile['ACC'] = ((self.cpu.RegFile['ACC'] & 0b1) << (emu_u.INSTR_4-1)) | dacc

        elif self.cpu.instr.dec == 0b00000001: # 2. rot-l
            dacc = self.cpu.RegFile['ACC'] << 1
            self.cpu.RegFile['ACC'] = (dacc & 0b1111) | dacc >> emu_u.INSTR_4

        elif self.cpu.instr.dec == 0b00000010:  # 3. rot-rc
            cfacc = (self.cpu.RegFile['CF'] << 4) | self.cpu.RegFile['ACC']  
            self.cpu.CFACC = ((cfacc & 1) << 4) | (cfacc >> 1)                     

            # update
            self.cpu.RegFile['CF'] = (self.cpu.CFACC >> 4) & 0b1           
            self.cpu.RegFile['ACC'] = self.cpu.CFACC & 0b1111        
       
        elif self.cpu.instr.dec == 0b00000011:  # 4. rot-lc
            cfacc = (self.cpu.RegFile['CF'] << 4) | self.cpu.RegFile['ACC']  
            self.cpu.CFACC = ((cfacc << 1) | (cfacc >> 4)) & 0b11111     
    
            # update          
            self.cpu.RegFile['CF'] = (self.cpu.CFACC >> 4) & 0b1                
            self.cpu.RegFile['ACC'] = self.cpu.CFACC & 0b1111                    
        
        elif self.cpu.instr.dec == 0b00000100: # 5. from-mba
            self.cpu.RegFile['ACC'] = self._readL4(self.cpu.RBRA)
        
        elif self.cpu.instr.dec == 0b00000101: # 6. to-mba
            self._writeL4(self.cpu.RBRA, self.cpu.RegFile['ACC'])
        
        elif self.cpu.instr.dec == 0b00000110: # 7. from-mbc
            self.cpu.RegFile['ACC'] = self._readL4(self.cpu.RDRC)
        
        elif self.cpu.instr.dec == 0b00000111: # 8. to-mbc
            self._writeL4(self.cpu.RDRC, self.cpu.RegFile['ACC'])

        elif self.cpu.instr.dec == 0b00001000: # 9. addc-mba
            result = self.cpu.RegFile['ACC'] + self._readL4(self.cpu.RBRA) + self.cpu.RegFile['CF']
            self.cpu.RegFile['ACC'] = result
            self.cpu.RegFile['CF'] = self._overflow(result)

        elif self.cpu.instr.dec == 0b00001001: # 10. add-mba
            result = self.cpu.RegFile['ACC'] + self._readL4(self.cpu.RDRC)
            self.cpu.RegFile['ACC'] = result
            self.cpu.RegFile['CF'] = self._overflow(result)

        elif self.cpu.instr.dec == 0b00001010: # 11. subc-mba
            result = self.cpu.RegFile['ACC'] - self._readL4(self.cpu.RBRA) + self.cpu.RegFile['CF']
            self.cpu.RegFile['ACC'] = result
            self.cpu.RegFile['CF'] = self._underflow(result)

        elif self.cpu.instr.dec == 0b00001011: # 12. sub-mba
            result = self.cpu.RegFile['ACC'] - self._readL4(self.cpu.RBRA)
            self.cpu.RegFile['ACC'] = result
            self.cpu.RegFile['CF'] = self._underflow(result)

        elif self.cpu.instr.dec == 0b00001100: # 13. inc*-mba
            self._writeL4(self.cpu.RBRA, self._readL4(self.cpu.RBRA) + 1)
        
        elif self.cpu.instr.dec == 0b00001101: # 14. dec*-mba
            self._writeL4(self.cpu.RBRA, self._readL4(self.cpu.RBRA) - 1)

        elif self.cpu.instr.dec == 0b00001110: # 15. inc*-mdc
            self._writeL4(self.cpu.RDRC, self._readL4(self.cpu.RDRC) + 1)
        
        elif self.cpu.instr.dec == 0b00001111: # 16. dec*-mdc
            self._writeL4(self.cpu.RDRC, self._readL4(self.cpu.RDRC) - 1)
        
        self.cpu.PC += 1

        return 

    # instructions 17 - 24
    def _type2(self):
        reg_bits = self.cpu.instr.bin[4:7]
        tag_bit = self.cpu.instr.bin[-1]
        self.cpu.RDRC = self.cpu.RegFile['RD'] << (emu_u.INSTR_4) | self.cpu.RegFile['RC']
        self.cpu.RBRA = self.cpu.RegFile['RB'] << (emu_u.INSTR_4) | self.cpu.RegFile['RA']

        if reg_bits in dasm.registers and tag_bit == '0': # 17. inc*-reg
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile[reg_name] = self._truncate(self.cpu.RegFile[reg_name] + 1)
            
            assert self.cpu.RegFile[reg_name] <= 0b1111
            
        elif reg_bits in dasm.registers and tag_bit == '1': # 18. dec*-reg
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile[reg_name] -=1 
            # self._truncate(self.cpu.RegFile[reg_name] -1)

            # assert self.cpu.RegFile[reg_name] <= 0b1111

        elif self.cpu.instr.dec == 0b00011010: # 19. and-ba
            accAndMem = self.cpu.RegFile['ACC'] & self._readL4(self.cpu.RBRA)
            self.cpu.RegFile['ACC'] = accAndMem

        elif self.cpu.instr.dec == 0b00011011: # 20. xor-ba
            accXorMem = self.cpu.RegFile['ACC'] ^ self._readL4(self.cpu.RBRA)
            self.cpu.RegFile['ACC'] = accXorMem
        
        elif self.cpu.instr.dec == 0b00011100: # 21. or-ba
            accOrMem = self.cpu.RegFile['ACC'] | self._readL4(self.cpu.RBRA)
            self.cpu.RegFile['ACC'] = accOrMem

        elif self.cpu.instr.dec == 0b00011101: # 22. and*-mba
            memAndAcc = self.cpu.RegFile['ACC'] & self._readL4(self.cpu.RBRA)
            self.cpu.DataMem.mem[self.cpu.RBRA] = memAndAcc
        
        elif self.cpu.instr.dec == 0b00011110: # 23. xor*-mba
            memXorAcc = self.cpu.RegFile['ACC'] ^ self._readL4(self.cpu.RBRA)
            self.cpu.DataMem.mem[self.cpu.RBRA] = memXorAcc
        
        elif self.cpu.instr.dec == 0b00011111: # 24. or*-mba
            memOrAcc = self.cpu.RegFile['ACC'] | self._readL4(self.cpu.RBRA)
            self.cpu.DataMem.mem[self.cpu.RBRA] = memOrAcc
        
        self.cpu.PC += 1

        return
    
    # instructions 25 - 48
    def _type3(self):
        reg_bits = self.cpu.instr.bin[4:7]
        tag_bit = self.cpu.instr.bin[-1]

        if reg_bits in dasm.registers and tag_bit == '0': # 25. to-reg    
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile[reg_name] = self.cpu.RegFile['ACC']

        elif reg_bits in dasm.registers and tag_bit == '1': # 26. from-reg
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile['ACC'] = self._truncate(self.cpu.RegFile[reg_name])

        elif self.cpu.instr.dec == 0b00101010: # 27. clr-cf
            self.cpu.RegFile['CF'] = 0
        
        elif self.cpu.instr.dec == 0b00101011: # 28. set-cf	
            self.cpu.RegFile['CF'] = 1

        elif self.cpu.instr.dec == 0b00101110: # 31. ret
            upperTemp = self.cpu.TEMP & emu_u.HEX_16U12 
            lowerPC = self.cpu.PC & emu_u.HEX_16L4 
            self.cpu.PC = upperTemp | lowerPC
            self.cpu.TEMP = 0

        self.cpu.PC += 1

    def _type4(self):
            
        if self.cpu.instr.dec == 0b00110010: # 33. from-ioa
            self.cpu.RegFile['ACC'] = self.cpu.RegFile['IOA']
        
        elif self.cpu.instr.dec == 0b00110001: # 34. inc
            self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] + 1

        
        elif self.cpu.instr.dec == 0b00110110: # 39. bcd
            if (self.cpu.RegFile['ACC'] >= 0b1010 or self.cpu.RegFile['CF'] == 1):
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] + 0b0110
                self.cpu.RegFile['CF'] = 1
            
        elif self.cpu.instr.dec == 0b0011011100111110: # 40. shutdown
            exit(0)

        elif self.cpu.instr.dec == 0b00111110: # 47. nop
            pass

        elif self.cpu.instr.dec == 0b00111111: # 48. dec
            self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] - 1

                    
        self.cpu.PC += 1

        return 

    # instructions 49 - 64
    def _type5(self):
        self.cpu.IMM = self.cpu.instr.dec & emu_u.HEX_16L4
        op = (self.cpu.instr.dec & emu_u.HEX_16U8) >> emu_u.INSTR_8 # get the logical op
        key_op = format(int(op) & ((1 << emu_u.INSTR_8) - 1), f"0{emu_u.INSTR_8}b")

        match (dasm.to_operation[key_op]):
            case "add": # 49 add <self.cpu.IMM>	
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] + self.cpu.IMM
                self.cpu.RegFile['CF'] = self._overflow(self.cpu.RegFile['ACC'])
                self.cpu.RegFile['ACC'] = self._truncate(self.cpu.RegFile['ACC'])
            case "sub": # 50 sub <self.cpu.IMM>
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] - self.cpu.IMM
            case "and": # 51 and s<self.cpu.IMM>
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] & self.cpu.IMM
            case "xor": # 52 xor <self.cpu.IMM>
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] ^ self.cpu.IMM
            case "or": # 53 or <self.cpu.IMM>
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] | self.cpu.IMM
            case "r4": # 55 r4 <self.cpu.IMM>
                self.cpu.RegFile['RE'] = self.cpu.IMM
                
        self.cpu.PC += 1

        return 

    # instructions 65 rarb <self.cpu.IMM>
    def _type6(self):
        rb_imm = int(asm_u.to_strbin(self.cpu.instr.bin[12:]), 2) << 4
        ra_imm = int(asm_u.to_strbin(self.cpu.instr.bin[4:8]) , 2)
        self.cpu.IMM = rb_imm | ra_imm
        self.cpu.RBRA = self.cpu.IMM
        self.cpu.RegFile['RA'] = ra_imm
        self.cpu.RegFile['RB'] = rb_imm

        self.cpu.PC += 1

        return 

    # instructions 66 rcrd <self.cpu.IMM>
    def _type7(self):
        rc_imm = int(asm_u.to_strbin(self.cpu.instr.bin[12:]), 2) << 4
        rd_imm = int(asm_u.to_strbin(self.cpu.instr.bin[4:8]) , 2)
        self.cpu.IMM = rc_imm | rd_imm

        self.cpu.RegFile['RC'] = rc_imm
        self.cpu.RegFile['RD'] = rd_imm
                
        self.cpu.PC += 1

        return 

    # instructions 67 acc <self.cpu.IMM>
    def _type8(self):
        self.cpu.IMM = self.cpu.instr.dec & emu_u.HEX_8L4 # 67. acc <self.cpu.IMM>	
        self.cpu.RegFile['ACC'] = self.cpu.IMM
        self.cpu.PC += 1

        return 

    # instructions 68 b-bit <k> <self.cpu.IMM>
    def _type9(self):
        k = int(self.cpu.instr.bin[3:5], 2)        # Bits 4–5: K (bit selector)
        b = int(self.cpu.instr.bin[5:8], 2)        # Bits 6–7: B
        a = int(self.cpu.instr.bin[8:], 2)         # Bits 8–15: A
        self.cpu.IMM = ((b << 8) | a) << 5         # 11-bit immediate: BBBAAAAAAAA

        acc = self.cpu.RegFile["ACC"]            # Get ACC value

        if ((acc >> k) & 1) == 1:
            # Check if bit K of ACC is 1
            lowerPC = self.cpu.PC & emu_u.HEX_16L5        # Keep lower 5 bits
            self.cpu.PC = lowerPC | self.cpu.IMM            # Replace lower 11 bits with self.cpu.IMM
        else:
            self.cpu.PC += 1          # Skip to next instruction
        

    # instructions 69 - 70
    def _type10(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        self.cpu.IMM = ((b << 8) | a) << 5
        print(self.cpu.IMM)
        tag = self.cpu.instr.bin[4]

        if (tag == '0' and self.cpu.RegFile['RA'] != 0):  # 69. bnz-a <self.cpu.IMM>
            lowerPC = self.cpu.PC & emu_u.HEX_16L5
            self.cpu.PC = lowerPC | self.cpu.IMM
        elif (tag == '1' and self.cpu.RegFile['RB'] != 0): # 70. bnz-b <self.cpu.IMM>
            lowerPC = self.cpu.PC & emu_u.HEX_16L5
            self.cpu.PC = lowerPC | self.cpu.IMM
        else:
            self.cpu.PC += 1
        # return   

    # instructions 71 - 72
    def _type11(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        self.cpu.IMM = ((b << 8) | a) << 5
        tag = self.cpu.instr.bin[4]

        if (tag == '0' and self.cpu.RegFile['ACC'] == 0): # 71. beqz <self.cpu.IMM>
            lowerPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = lowerPC | self.cpu.IMM
        elif (tag == '1' and self.cpu.RegFile['ACC'] != 0): # 72. bnez <self.cpu.IMM>
            lowerPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = lowerPC | self.cpu.IMM
        else:
            self.cpu.PC += 1
            
        return 

    # instructions 73 - 74
    def _type12(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        self.cpu.IMM = ((b << 8) | a) << 5
        tag = self.cpu.instr.bin[4]

        if (self.cpu.RegFile['CF'] == 0 and tag == '0'): # 73. beqz-cf <self.cpu.IMM>
            lowerPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = lowerPC | self.cpu.IMM
        elif (self.cpu.RegFile['CF'] != 0 and tag == '1'): # 74. bnez-cf <self.cpu.IMM>
            lowerPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = lowerPC | self.cpu.IMM
        else:
            self.cpu.PC += 1
        

        return 

    # instructions 75 - 76
    def _type13(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        self.cpu.IMM = ((b << 8) | a) << 5
        tag = self.cpu.instr.bin[4]

        if (self.cpu.RegFile['RD'] != 0 and tag == '1'): # 76. bnz-d <self.cpu.IMM>
            lowerPC = self.cpu.PC & emu_u.HEX_16L5
            self.cpu.PC = lowerPC | self.cpu.IMM
        else:
            self.cpu.PC += 1
        

        return 

    # instructions 77  -> 77. b <imm>
    def _type14(self):
        # upperPC = self.cpu.PC & emu_u.HEX_16U4         
        # self.cpu.IMM = int(asm_u.to_strbin(self.cpu.instr.bin[4:]), 2)  
        # self.cpu.PC = upperPC | self.cpu.IMM  
        lowerPC = self.cpu.PC & emu_u.HEX_16L4
        self.cpu.IMM = int(asm_u.to_strbin(self.cpu.instr.bin[4:]), 2) # immediate decimal
        self.cpu.PC = (self.cpu.IMM << 4) | lowerPC


    # instructions 78 -> 78. call <imm> 
    def _type15(self): 
        # self.cpu.TEMP = self.cpu.PC + 2
        # upper_pc = self.cpu.PC & 0xF000
        # imm_12bit = int(self.cpu.instr.bin[4:], 2)  
        # self.cpu.PC = upper_pc | imm_12bit
        
        self.cpu.TEMP = self.cpu.PC + 2
        lowerPC = self.cpu.PC & emu_u.HEX_16L4
        self.cpu.IMM = int(asm_u.to_strbin(self.cpu.instr.bin[4:]), 2)
        self.cpu.PC = self.cpu.IMM << 4 | lowerPC

        return 
