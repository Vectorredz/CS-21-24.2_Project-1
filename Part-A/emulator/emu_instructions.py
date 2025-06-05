
import emulator.disassembler as dasm
import emulator.emu_utils as emu_u
import assembler.asm_utils as asm_u

class EmulatorInstructions:
    def __init__(self, cpu):
        self.cpu = cpu

    def _overflow(self, result):
        mask = 0b100000000
        return bool(mask & self, result)

    def _underflow(self, result):
        # if msb is 1 there is an underflow // assumes signed borrow
        # a < b
        mask = 0b10000000
        return bool(mask & self, result)

    # instructions 1 - 16
    def _type1(self):
        mask = 0b11111111
        rbra = self.cpu.RegFile['RB'] << (emu_u.INSTR_4) | self.cpu.RegFile['RA']
        rdrc = self.cpu.RegFile['RD'] << (emu_u.INSTR_4) | self.cpu.RegFile['RC']
        if self.cpu.instr.dec == 0b00000000: # 1. rot-r
            dacc = self.cpu.RegFile['ACC'] >> 1
            self.cpu.RegFile['ACC'] = ((self.cpu.RegFile['ACC'] & 0b1) << (emu_u.INSTR_8-1)) | dacc

        elif self.cpu.instr.dec == 0b00000001: # 2. rot-l
            dacc = self.cpu.RegFile['ACC'] << 1
            self.cpu.RegFile['ACC'] = (dacc & mask) | dacc >> emu_u.INSTR_8

        elif self.cpu.instr.dec == 0b00000010: # 3. rot-rc
            cfacc = self.cpu.RegFile['CF'] << emu_u.INSTR_8 | self.cpu.RegFile['ACC']
            dcfacc = cfacc >> 1
            self.cpu.CFACC = (cfacc & 0b1 << emu_u.INSTR_8-1) | dcfacc 
        
        elif self.cpu.instr.dec  == 0b00000011: # 4. rot-lc
            cfacc = self.cpu.RegFile['CF'] << emu_u.INSTR_8 | self.cpu.RegFile['ACC']
            dcfacc = cfacc << 1
            self.cpu.CFACC = (dcfacc & mask) | dcfacc >> emu_u.INSTR_8
        
        elif self.cpu.instr.dec == 0b00000100: # 5. from-mba
            self.cpu.RegFile['ACC'] = self.cpu.DataMemory[rbra]
        
        elif self.cpu.instr.dec == 0b00000101: # 6. to-mba
            self.cpu.DataMemory[rbra] = self.cpu.RegFile['ACC']
        
        elif self.cpu.instr.dec == 0b00000110: # 7. from-mbc
            self.cpu.RegFile['ACC'] = self.cpu.DataMemory[rdrc]
        
        elif self.cpu.instr.dec == 0b00000111: # 8. to-mbc
            self.cpu.DataMemory[rdrc] = self.cpu.RegFile['ACC']

        elif self.cpu.instr.dec == 0b00001000: # 9. addc-mba
            self, result = self.cpu.RegFile['ACC'] + self.cpu.DataMemory[rbra] + self.cpu.RegFile['CF']
            self.cpu.RegFile['CF'] = self.cpu._overflow(self, result)

        elif self.cpu.instr.dec == 0b00001001: # 10. add-mba
            self, result = self.cpu.RegFile['ACC'] + self.cpu.DataMemory[rdrc]
            self.cpu.RegFile['CF'] = self.cpu._overflow(self, result)

        elif self.cpu.instr.dec == 0b00001010: # 11. subc-mba
            self, result = self.cpu.RegFile['ACC'] - self.cpu.DataMemory[rbra] + self.cpu.RegFile['CF']
            self.cpu.RegFile['CF'] = self.cpu._underflow(self, result)

        elif self.cpu.instr.dec == 0b00001011: # 12. sub-mba
            self, result = self.cpu.RegFile['ACC'] - self.cpu.DataMemory[rbra]
            self.cpu.RegFile['CF'] = self.cpu._underflow(self, result)

        elif self.cpu.instr.dec == 0b00001100: # 13. inc*-mba
            self.cpu.DataMemory[rbra] = self.cpu.DataMemory[rbra] + 1
        
        elif self.cpu.instr.dec == 0b00001101: # 14. dec*-mba
            self.cpu.DataMemory[rbra] = self.cpu.DataMemory[rbra] - 1

        elif self.cpu.instr.dec == 0b00001110: # 15. inc*-mdc
            self.cpu.DataMemory[rdrc] = self.cpu.DataMemory[rdrc] + 1
        
        elif self.cpu.instr.dec == 0b00001111: # 16. dec*-mdc
            self.cpu.DataMemory[rdrc] = self.cpu.DataMemory[rdrc] - 1
        
        self.cpu.PC += 1

        return 

    # instructions 17 - 24
    def _type2(self):
        reg_bits = self.cpu.instr.bin[4:7]
        tag_bit = self.cpu.instr.bin[-1]
        rdrc = self.cpu.RegFile['RD'] << (emu_u.INSTR_4) | self.cpu.RegFile['RC']
        rbra = self.cpu.RegFile['RB'] << (emu_u.INSTR_4) | self.cpu.RegFile['RA']

        if reg_bits in dasm.registers and tag_bit == 0: # 17. inc*-reg
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile[reg_name] += 1

        elif reg_bits in dasm.registers and tag_bit == 1: # 18. dec*-reg
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile[reg_name] -= 1
        elif self.cpu.instr == 0b00011010: # 19. and-ba
            accAndMem = self.cpu.RegFile['ACC'] & self.cpu.DataMemory[rbra]
            self.cpu.RegFile['ACC'] = accAndMem

        elif self.cpu.instr == 0b00011011: # 20. xor-ba
            accXorMem = self.cpu.RegFile['ACC'] ^ self.cpu.DataMemory[rbra]
            self.cpu.RegFile['ACC'] = accXorMem
        
        elif self.cpu.instr == 0b00011100: # 21. or-ba
            accOrMem = self.cpu.RegFile['ACC'] | self.cpu.DataMemory[rbra]
            self.cpu.RegFile['ACC'] = accOrMem

        elif self.cpu.instr == 0b00011101: # 22. and*-mba
            memAndAcc = self.cpu.RegFile['ACC'] & self.cpu.DataMemory[rbra]
            self.cpu.DataMemory[rbra] = memAndAcc
        
        elif self.cpu.instr == 0b00011110: # 23. xor*-mba
            memXorAcc = self.cpu.RegFile['ACC'] ^ self.cpu.DataMemory[rbra]
            self.cpu.DataMemory[rbra] = memXorAcc
        
        elif self.cpu.instr == 0b00011111: # 24. or*-mba
            memOrAcc = self.cpu.RegFile['ACC'] | self.cpu.DataMemory[rbra]
            self.cpu.DataMemory[rbra] = memOrAcc
        
        self.cpu.PC += 1

        return
    # instructions 25 - 48
    def _type3(self):
        reg_bits = self.cpu.instr.bin[4:7]
        tag_bit = self.cpu.instr.bin[-1]

        if reg_bits in dasm.registers and tag_bit == 0: # 25. to-ref     
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile[reg_name] = self.cpu.RegFile['ACC']

        elif reg_bits in dasm.registers and tag_bit == 1: # 26. from-reg
            reg_name = dasm.registers[reg_bits]
            self.cpu.RegFile['ACC'] = self.cpu.RegFile[reg_name]

        elif self.cpu.instr.dec == 0b00101010: # 27. clr-cf
            self.cpu.RegFile['CF'] = 0
        
        elif self.cpu.instr.dec == 0b00101011: # 28. set-cf	
            self.cpu.RegFile['CF'] = 1

        elif self.cpu.instr.dec == 0b00101110: # 31. ret
            lowerTemp = self.cpu.TEMP & emu_u.HEX_16L12 
            upperAcc = self.cpu.RegFile['ACC'] & emu_u.HEX_16U4
            self.cpu.RegFile['ACC'] = upperAcc | lowerTemp
            self.cpu.TEMP = 0
        
        elif self.cpu.instr.dec == 0b00110000: # 33. from-ioa
            self.cpu.RegFile['ACC'] = self.cpu.RegFile['IOA']
        
        elif self.cpu.instr.dec == 0b00110001: # 34. inc
            self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] + 1
        
        elif self.cpu.instr.dec == 0b00110001: # 34. inc
            self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] + 1
        
        elif self.cpu.instr.dec == 0b00110110: # 39. bcd
            if (self.cpu.RegFile['ACC'] >= 0b1010 | self.cpu.RegFile['CF'] == 1):
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] + 0b0110
                self.cpu.RegFile['CF'] = 1
            
        elif self.cpu.instr.dec == 0b0011011100111110: # 40. shutdown
            exit(self)

        elif self.cpu.instr.dec == 0b00111110: # 47. nop
            ...

        elif self.cpu.instr.dec == 0b00111111: # 48. dec
            self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] - 1

                    
        self.cpu.PC += 1

        return 

    # instructions 49 - 64
    def _type4(self):
        imm = self.cpu.instr.dec & emu_u.HEX_16L4
        op = (self.cpu.instr.dec & emu_u.HEX_16U8) >> emu_u.INSTR_8 # get the logical op
        key_op = asm_u.to_bin(op, emu_u.INSTR_8)
        match (dasm.to_operation[key_op]):
            case "add": # 49
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] + imm
            case "sub": # 50
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] - imm
            case "and": # 51
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] & imm
            case "xor": # 52
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] ^ imm

            case "or": # 53
                self.cpu.RegFile['ACC'] = self.cpu.RegFile['ACC'] | imm
            case "r4": # 55
                self.cpu.RegFile['RE'] = imm
                
        self.cpu.PC += 1

        return 

    # instructions 65
    def _type5(self):
        rb_imm = int(self.cpu.instr.bin[12:], 2) << 4
        ra_imm = int(self.cpu.instr.bin[4:8] , 2)
        imm = rb_imm | ra_imm

        self.cpu.RegFile['RA'] = ra_imm
        self.cpu.RegFile['RB'] = rb_imm

        self.cpu.PC += 1

        return 

    # instructions 66
    def _type6(self):
        rc_imm = int(self.cpu.instr.bin[12:], 2) << 4
        rd_imm = int(self.cpu.instr.bin[4:8] , 2)
        imm = rc_imm | rd_imm

        self.cpu.RegFile['RC'] = rc_imm
        self.cpu.RegFile['RD'] = rd_imm
                
        self.cpu.PC += 1

        return 

    # instructions 67
    def _type7(self):
        imm = self.cpu.instr & emu_u.HEX_8L4 # 67. acc <imm>	
        self.cpu.RegFile['ACC'] = imm

        self.cpu.PC += 1

        return 

    # instructions 68
    def _type8(self):
        k = int(self.cpu.instr.bin[3:5], 2)
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        if (self.cpu.PC & k == 1):
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm

        self.cpu.PC += 1

        return 
    # instructions 69 - 70
    def _type9(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.cpu.instr.bin[4]

        if (tag == 0):  # 69. bnz-a <imm>
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm
        elif (tag == 1): # 70. bnz-b <imm>
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm

        self.cpu.PC += 1

        return   

    # instructions 71 - 72
    def _type10(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.cpu.instr.bin[4]

        if (self.cpu.RegFile['ACC'] != 0 and tag == 0): # 71. beqz <imm>
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm
        elif (self.cpu.RegFile['ACC'] == 0 and tag == 1): # 72. bnez <imm>
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm

        self.cpu.PC += 1

        return 

    # instructions 73 - 74
    def _type11(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.cpu.instr.bin[4]

        if (self.cpu.RegFile['CF'] != 0 and tag == 0): # 73. beqz-cf <imm>
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm
        elif (self.cpu.RegFile['CF'] == 0 and tag == 1): # 74. bnez-cf <imm>
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm
        
        self.cpu.PC += 1

        return 

    # instructions 75 - 76
    def _type12(self):
        b = int(self.cpu.instr.bin[5:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        imm = (b << 8) | (a)
        tag = self.cpu.instr.bin[4]

        if (self.cpu.RegFile['RD'] != 0 and tag == 1): # 76. bnez-cf <imm>
            upperPC = self.cpu.PC & emu_u.HEX_16U5
            self.cpu.PC = upperPC | imm
        
        self.cpu.PC += 1

        return 

    # instructions 77
    def _type13(self):
        b = int(self.cpu.instr.bin[4:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        upperPC = self.cpu.PC & emu_u.HEX_16U4
        self.cpu.PC = upperPC | imm

        self.cpu.PC += 1

        return 

    # instructions 78
    def _type14(self):
        b = int(self.cpu.instr.bin[4:8], 2)
        a = int(self.cpu.instr.bin[8:], 2)    
        imm = (b << 8) | (a)

        self.cpu.TEMP = self.cpu.PC + 2
        upperPC = self.cpu.PC & emu_u.HEX_16U4
        self.cpu.PC = upperPC | imm

        self.cpu.PC += 1

        return 
