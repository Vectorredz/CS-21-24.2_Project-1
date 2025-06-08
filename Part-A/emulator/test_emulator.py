import sys
import os
import pytest
from pathlib import Path

# Add *this* (emulator/) directory to sys.path
sys.path.append(os.path.dirname(__file__))

# Add parent directory to path (optional, if importing from parent)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import shared.utils as utils
from emu import Instructions, Arch242Emulator, DataMemory, InstructionMemory
from emu_instructions import EmulatorInstructions

@pytest.fixture
def cpu(): return Arch242Emulator()

@pytest.fixture
def emu_instr(cpu): return EmulatorInstructions(cpu)

@pytest.fixture
def data_mem(): return DataMemory()

@pytest.fixture
def instr_mem(): return InstructionMemory()

class TestMemory:
    def test_data_memory_init(self, data_mem):
        assert len(data_mem.mem) == 2 ** 8
        assert isinstance(data_mem.mem, list)

    def test_instr_memory_init(self, instr_mem):
        assert len(instr_mem.mem) == 2 ** 16
        assert isinstance(instr_mem.mem, list)

class TestCPUInitialState:
    def test_cpu_init(self, cpu: Arch242Emulator):
        assert cpu.PC == 0
        assert len(cpu.RegFile.REG) == 9
        assert cpu.clock_cycle == 0
        assert cpu.instr == " "

class TestType1Instructions:

    def _rot_r_tick(self, cpu: Arch242Emulator, expected_acc, expected_pc):
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000000"
        cpu.decode()
        assert cpu.instr.bin == "00000000"
        assert cpu.instr.opcode == "Type1"
        assert cpu.instr.dec == 0b00000000
        cpu.execute()
        assert cpu.RegFile['ACC'] == expected_acc
        assert cpu.PC == expected_pc

    def _rot_l_tick(self, cpu: Arch242Emulator, expected_acc, expected_pc):
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000001"
        cpu.decode()
        assert cpu.instr.bin == "00000001"
        assert cpu.instr.opcode == "Type1"
        assert cpu.instr.dec == 0b00000001
        cpu.execute()
        assert cpu.RegFile['ACC'] == expected_acc
        assert cpu.PC == expected_pc

    def _rot_rc_tick(self, cpu: Arch242Emulator, expected_cfacc, expected_pc):
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000010"
        cpu.decode()
        assert cpu.instr.bin == "00000010"
        assert cpu.instr.opcode == "Type1"
        assert cpu.instr.dec == 0b00000010
        cpu.execute()
        assert cpu.CFACC == expected_cfacc
        assert cpu.PC == expected_pc

    def _rot_lc_tick(self, cpu: Arch242Emulator, expected_cfacc, expected_pc):
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000011"
        cpu.decode()
        assert cpu.instr.bin == "00000011"
        assert cpu.instr.opcode == "Type1"
        assert cpu.instr.dec == 0b00000011
        cpu.execute()
        assert cpu.CFACC == expected_cfacc
        assert cpu.PC == expected_pc

    def assert_type(self, cpu: Arch242Emulator, bin, dec, opcode):
        assert cpu.instr.bin == bin
        assert cpu.instr.dec == dec
        assert cpu.instr.opcode == opcode

    def test_rot_r(self, cpu: Arch242Emulator):
        for addr in range(4):
            cpu.InstMem.mem[addr] = "00000000"
        cpu.RegFile['ACC'] = 0b1001
        assert cpu.PC == 0
        self._rot_r_tick(cpu, expected_acc=0b1100, expected_pc=1)
        self._rot_r_tick(cpu, expected_acc=0b0110, expected_pc=2)
        self._rot_r_tick(cpu, expected_acc=0b0011, expected_pc=3)
        self._rot_r_tick(cpu, expected_acc=0b1001, expected_pc=4)

    def test_rot_l(self, cpu: Arch242Emulator):
        for addr in range(4):
            cpu.InstMem.mem[addr] = "00000001"
        cpu.RegFile['ACC'] = 0b1001
        assert cpu.PC == 0
        self._rot_l_tick(cpu, expected_acc=0b0011, expected_pc=1)
        self._rot_l_tick(cpu, expected_acc=0b0110, expected_pc=2)
        self._rot_l_tick(cpu, expected_acc=0b1100, expected_pc=3)
        self._rot_l_tick(cpu, expected_acc=0b1001, expected_pc=4)

    def test_rot_rc(self, cpu: Arch242Emulator):
        for addr in range(4):
            cpu.InstMem.mem[addr] = "00000010"
        cpu.RegFile['ACC'] = 0b0011
        cpu.RegFile['CF'] = 0b1
        assert cpu.PC == 0
        self._rot_rc_tick(cpu, expected_cfacc=0b11001, expected_pc=1)
        self._rot_rc_tick(cpu, expected_cfacc=0b11100, expected_pc=2)
        self._rot_rc_tick(cpu, expected_cfacc=0b01110, expected_pc=3)
        self._rot_rc_tick(cpu, expected_cfacc=0b00111, expected_pc=4)

    def test_rot_lc(self, cpu: Arch242Emulator):
        for addr in range(4):
            cpu.InstMem.mem[addr] = "00000011"
        cpu.RegFile['ACC'] = 0b0011
        cpu.RegFile['CF'] = 0b1
        assert cpu.PC == 0
        self._rot_lc_tick(cpu, expected_cfacc=0b00111, expected_pc=1)
        self._rot_lc_tick(cpu, expected_cfacc=0b01110, expected_pc=2)
        self._rot_lc_tick(cpu, expected_cfacc=0b11100, expected_pc=3)
        self._rot_lc_tick(cpu, expected_cfacc=0b11001, expected_pc=4)

    def test_from_mba(self, cpu: Arch242Emulator):
        cpu.InstMem.mem[0] = "00000100"
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.RBRA == 33
        assert cpu.DataMem.mem[cpu.RBRA] == 0
        assert cpu.RegFile['ACC'] == 0

    def test_to_mba(self, cpu: Arch242Emulator):
        cpu.InstMem.mem[0] = "00000101"
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.RBRA == 33
        assert cpu.DataMem.mem[cpu.RBRA] == 1
        assert cpu.RegFile['ACC'] == 1

    def test_from_mbc(self, cpu: Arch242Emulator):
        cpu.InstMem.mem[0] = "00000110"
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.RDRC == 33
        assert cpu.DataMem.mem[cpu.RDRC] == 0
        assert cpu.RegFile['ACC'] == 0

    def test_to_mbc(self, cpu: Arch242Emulator):
        cpu.InstMem.mem[0] = "00000111"
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.RDRC == 33
        assert cpu.DataMem.mem[cpu.RDRC] == 1
        assert cpu.RegFile['ACC'] == 1

    def test_addc_mba(self, cpu: Arch242Emulator):
        cpu.InstMem.mem[0] = "00001000"
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['CF'] = 0b0
        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010
        cpu.RBRA = cpu.RegFile['RB'] << utils.INSTR_4 | cpu.RegFile['RA']
        cpu.DataMem.mem[cpu.RBRA] = 33
        cpu.instr = cpu.fetch()
        cpu.decode()
        self.assert_type(cpu, bin="00001000", dec=8, opcode="Type1")
        cpu.execute()
        assert cpu.RegFile['CF'] == 0

    def test_add_mba(self, cpu: Arch242Emulator):
        cpu.InstMem.mem[0] = "00001001"
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['CF'] = 0b0
        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010
        cpu.RDRC = cpu.RegFile['RD'] << utils.INSTR_4 | cpu.RegFile['RC']
        cpu.DataMem.mem[cpu.RDRC] = 15
        cpu.instr = cpu.fetch()
        cpu.decode()
        self.assert_type(cpu, bin="00001001", dec=9, opcode="Type1")
        cpu.execute()
        assert cpu.RegFile['CF'] == 1  # Overflow

class TestType2Instructions:
    def test_inc_reg_ra(self, cpu: Arch242Emulator):
        """Test increment RA register (17)"""
        # Setup
        cpu.InstMem.mem[0] = "00010000"  # inc RA
        cpu.RegFile['RA'] = 5
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        
        # Verify decoding
        assert cpu.instr.bin == "00010000"
        assert cpu.instr.opcode == "Type2"
        assert cpu.instr.dec == 0b00010000
        
        # Execute instruction
        cpu.execute()
        
        # Verify results
        assert cpu.RegFile['RA'] == 6
        assert cpu.PC == 1

    def test_inc_reg_rb(self, cpu: Arch242Emulator):
        """Test increment RB register (17)"""
        # Setup
        cpu.InstMem.mem[0] = "00010010"  # inc RB
        cpu.RegFile['RB'] = 10
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RB'] == 11
        assert cpu.PC == 1

    def test_inc_reg_rc(self, cpu: Arch242Emulator):
        """Test increment RC register (17)"""
        # Setup
        cpu.InstMem.mem[0] = "00010100"  # inc RC
        cpu.RegFile['RC'] = 15
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RC'] == 0 # overflow
        assert cpu.PC == 1

    def test_inc_reg_rd(self, cpu: Arch242Emulator):
        """Test increment RD register (17)"""
        # Setup
        cpu.InstMem.mem[0] = "00010110"  # inc RD
        cpu.RegFile['RD'] = 0
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        assert cpu.instr.bin == "00010110" 
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RD'] == 1
        assert cpu.PC == 1

    def test_inc_reg_re(self, cpu: Arch242Emulator):
        """Test increment RE register (17)"""
        # Setup
        cpu.InstMem.mem[0] = "00011000"  # inc RE
        cpu.RegFile['RE'] = 0
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RE'] == 1 
        assert cpu.PC == 1

    def test_dec_reg_ra(self, cpu: Arch242Emulator):
        """Test decrement RA register (18)"""
        # Setup
        cpu.InstMem.mem[0] = "00010001"  # dec RA
        cpu.RegFile['RA'] = 5
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RA'] == 4
        assert cpu.PC == 1

    def test_dec_reg_rb(self, cpu: Arch242Emulator):
        """Test decrement RB register (18)"""
        # Setup
        cpu.InstMem.mem[0] = "00010011"  # dec RB
        cpu.RegFile['RB'] = 1
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RB'] == 0
        assert cpu.PC == 1

    def test_dec_reg_rc(self, cpu: Arch242Emulator):
        """Test decrement RC register (18)"""
        # Setup
        cpu.InstMem.mem[0] = "00010101"  # dec RC
        cpu.RegFile['RC'] = 0
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RC'] == -1
        assert cpu.PC == 1

    def test_dec_reg_rd(self, cpu: Arch242Emulator):
        """Test decrement RD register (18)"""
        # Setup
        cpu.InstMem.mem[0] = "00010111"  # dec RD
        cpu.RegFile['RD'] = 100
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RD'] == 3
        assert cpu.PC == 1

    def test_dec_reg_re(self, cpu: Arch242Emulator):
        """Test decrement RE register (18)"""
        # Setup
        cpu.InstMem.mem[0] = "00011001"  # dec RE
        cpu.RegFile['RE'] = 0
        
        # Execute
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Verify
        assert cpu.RegFile['RE'] == -1  # Should wrap around
        assert cpu.PC == 1

    def test_and_ba(self, cpu: Arch242Emulator):
        """Test AND with memory (19)"""
        cpu.InstMem.mem[0] = "00011010"
        cpu.RegFile['ACC'] = 0b1010
        cpu.RegFile['RA'] = 1
        cpu.RegFile['RB'] = 0
        cpu.RBRA = 1  # mem[1]
        cpu.DataMem.mem[cpu.RBRA] = 0b1100
        cpu.instr = cpu.fetch()
        cpu.decode()
        assert cpu.RegFile['ACC'] == 0b1010
        assert cpu.RBRA == 0b1
        cpu.execute()
        assert cpu.RegFile['ACC'] == 0b1000  # 1010 AND 1100
        assert cpu.PC == 1

    def test_xor_ba(self, cpu: Arch242Emulator):
        """Test XOR with memory (20)"""
        cpu.InstMem.mem[0] = "00011011"
        cpu.RegFile['ACC'] = 0b1010
        cpu.RegFile['RA'] = 1
        cpu.RegFile['RB'] = 0
        cpu.RBRA = 1  # mem[1]
        cpu.DataMem.mem[1] = 0b1100
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.RegFile['ACC'] == 0b0110  # 1010 XOR 1100
        assert cpu.PC == 1

    def test_or_ba(self, cpu: Arch242Emulator):
        """Test OR with memory (21)"""
        cpu.InstMem.mem[0] = "00011100"
        cpu.RegFile['ACC'] = 0b1010
        cpu.RegFile['RA'] = 1
        cpu.RegFile['RB'] = 0
        cpu.RBRA = 1  # mem[1]
        cpu.DataMem.mem[1] = 0b1100
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.RegFile['ACC'] == 0b1110  # 1010 OR 1100
        assert cpu.PC == 1

    def test_and_star_mba(self, cpu: Arch242Emulator):
        """Test AND to memory (22)"""
        cpu.InstMem.mem[0] = "00011101"
        cpu.RegFile['ACC'] = 0b1010
        cpu.RegFile['RA'] = 1
        cpu.RegFile['RB'] = 0
        cpu.RBRA = 1  # mem[1]
        cpu.DataMem.mem[1] = 0b1100
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.DataMem.mem[1] == 0b1000  # 1010 AND 1100
        assert cpu.PC == 1

    def test_xor_star_mba(self, cpu: Arch242Emulator):
        """Test XOR to memory (23)"""
        cpu.InstMem.mem[0] = "00011110"
        cpu.RegFile['ACC'] = 0b1010
        cpu.RegFile['RA'] = 1
        cpu.RegFile['RB'] = 0
        cpu.RBRA = 1  # mem[1]
        cpu.DataMem.mem[1] = 0b1100
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.DataMem.mem[1] == 0b0110  # 1010 XOR 1100
        assert cpu.PC == 1

    def test_or_star_mba(self, cpu: Arch242Emulator):
        """Test OR to memory (24)"""
        cpu.InstMem.mem[0] = "00011111"
        cpu.RegFile['ACC'] = 0b1010
        cpu.RegFile['RA'] = 1
        cpu.RegFile['RB'] = 0
        cpu.RBRA = 1  # mem[1]
        cpu.DataMem.mem[1] = 0b1100
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.DataMem.mem[1] == 0b1110  # 1010 OR 1100
        assert cpu.PC == 1

class TestType3Instructions:
    """Test suite for Type 3 instructions (opcodes 25-48)"""
    
    def test_to_reg_ra(self, cpu: Arch242Emulator):
        """Test move ACC to RA (25)"""
        cpu.InstMem.mem[0] = "00100000"  # to RA
        cpu.RegFile['ACC'] = 0x1
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['RA'] == 0x1
        assert cpu.PC == 1

    def test_to_reg_rb(self, cpu: Arch242Emulator):
        """Test move ACC to RB (25)"""
        cpu.InstMem.mem[0] = "00100010"  # to RB
        cpu.RegFile['ACC'] = 0x55

        assert cpu.RegFile['ACC'] == 0x5 # truncated

        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['RB'] == 0x5
        assert cpu.PC == 1

    def test_from_reg_rc(self, cpu: Arch242Emulator):
        """Test move RC to ACC (26)"""
        cpu.InstMem.mem[0] = "00100101"  # from RC
        cpu.RegFile['RC'] = 0x33
        
        assert cpu.RegFile['RC'] == 0x3
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0x3
        assert cpu.PC == 1

    def test_from_reg_rd(self, cpu: Arch242Emulator):
        """Test move RD to ACC (26)"""
        cpu.InstMem.mem[0] = "00100111"  # from RD
        cpu.RegFile['RD'] = 0x77

        assert cpu.RegFile['RD'] == 0x7
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0x7
        assert cpu.PC == 1

    def test_clr_cf(self, cpu: Arch242Emulator):
        """Test clear carry flag (27)"""
        cpu.InstMem.mem[0] = "00101010"
        cpu.RegFile['CF'] = 1
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['CF'] == 0
        assert cpu.PC == 1

    def test_set_cf(self, cpu: Arch242Emulator):
        """Test set carry flag (28)"""
        cpu.InstMem.mem[0] = "00101011"
        cpu.RegFile['CF'] = 0
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['CF'] == 1
        assert cpu.PC == 1

    def test_ret(self, cpu: Arch242Emulator):
        """Test return instruction (31)"""
        cpu.InstMem.mem[0xFFFF] = "00101110"
        assert cpu.InstMem.mem[0xFFFF] == "00101110"
        cpu.TEMP = 0xF000
        cpu.PC = 0xFFFF

        cpu.instr = cpu.fetch()
        # assert cpu.instr == "00101110"
        cpu.decode()
        cpu.execute()
   
        assert cpu.PC == 0xF00F  # Combined upper ACC and lower TEMP
        assert cpu.TEMP == 0

class TestType4Instructions:
    """Test suite for Type 4 instructions (opcodes 49-64)"""
    def test_from_ioa(self, cpu: Arch242Emulator):
        """Test read from IOA (33)"""
        cpu.InstMem.mem[0] = "00110010"
        cpu.RegFile['IOA'] = 0x55
        assert cpu.RegFile['IOA'] == 0x5
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0x5
        assert cpu.PC == 1

    def test_inc_acc(self, cpu: Arch242Emulator):
        """Test increment ACC (34)"""
        cpu.InstMem.mem[0] = "00110001"
        cpu.RegFile['ACC'] = 0xFF
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0x00  # Wraps around
        assert cpu.PC == 1

    def test_bcd_correction(self, cpu: Arch242Emulator):
        """Test BCD correction (39)"""
        # Case 1: ACC >= 10
        cpu.InstMem.mem[0] = "00110110"
        cpu.RegFile['ACC'] = 0x0F  # 15 in decimal
        cpu.RegFile['CF'] = 0
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0x5  # Corrected to BCD
        assert cpu.RegFile['CF'] == 1
        assert cpu.PC == 1
        

    def test_shutdown(self, cpu: Arch242Emulator):
        """Test shutdown instruction (40)"""
        cpu.InstMem.mem[0] = "00110111"
        cpu.InstMem.mem[1] = "00111110"  # Second half of 16-bit instruction
        
        with pytest.raises(SystemExit):
            cpu.instr = cpu.fetch()
            cpu.decode()
            cpu.execute()

    def test_nop(self, cpu: Arch242Emulator):
        """Test no-operation (47)"""
        cpu.InstMem.mem[0] = "00111110"
        initial_pc = cpu.PC
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.PC == initial_pc + 1  # Only PC increments
        # No other state changes

    def test_dec_acc(self, cpu: Arch242Emulator):
        """Test decrement ACC (48)"""
        cpu.InstMem.mem[0] = "00111111"
        cpu.RegFile['ACC'] = 0x00
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == -1  # Wraps around
        assert cpu.PC == 1

class TestType5Instructions:
    """Test suite for Type 5 instructions (opcodes 49-64)"""
    
    def test_add_imm(self, cpu: Arch242Emulator):
        """Test ADD with immediate (49)"""
        # Binary: 0100 0001 0000 0101 (add imm=5)
        cpu.InstMem.mem[0] = "01000000" 
        cpu.InstMem.mem[1] = "00000001"

        cpu.RegFile['ACC'] = 10
        
        cpu.instr = cpu.fetch()
        assert cpu.instr == "01000000" 
        cpu.decode()
        # assert cpu.RegFile['ACC'] == 10
        assert cpu.instr.bin == "0100000000000001" 
        cpu.execute()
        assert cpu.IMM == 1
        
        assert cpu.RegFile['ACC'] == 11  # 10 + 5
        assert cpu.PC == 2  # 16-bit instruction

    def test_sub_imm(self, cpu: Arch242Emulator):
        """Test SUB with immediate (50)"""
        # Binary: 0100 0010 0000 1010 (sub imm=10)
        cpu.InstMem.mem[0] = "01000001" 
        cpu.InstMem.mem[1] =  "00001010"
        cpu.RegFile['ACC'] = 15
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 5  # 20 - 10
        assert cpu.PC == 2

    def test_and_imm(self, cpu: Arch242Emulator):
        """Test AND with immediate (51)"""
        # Binary: 0100 0011 0000 1100 (and imm=0b1100)
        cpu.InstMem.mem[0] = "01000010" 
        cpu.InstMem.mem[1] = "00001100"
        cpu.RegFile['ACC'] = 0b1010
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0b1000  # 1010 AND 1100
        assert cpu.PC == 2

    def test_xor_imm(self, cpu: Arch242Emulator):
        """Test XOR with immediate (52)"""
        # Binary: 0100 0100 0000 1111 (xor imm=0b1111)
        cpu.InstMem.mem[0] = "01000011" 
        cpu.InstMem.mem[1] = "00001111"
        cpu.RegFile['ACC'] = 0b1010
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0b0101  # 1010 XOR 1111
        assert cpu.PC == 2

    def test_or_imm(self, cpu: Arch242Emulator):
        """Test OR with immediate (53)"""
        # Binary: 0100 0101 0000 1100 (or imm=0b1100)
        cpu.InstMem.mem[0] = "01000100" 
        cpu.InstMem.mem[1] = "00001100"
        cpu.RegFile['ACC'] = 0b1010
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0b1110  # 1010 OR 1100
        assert cpu.PC == 2

    def test_r4_imm(self, cpu: Arch242Emulator):
        """Test load immediate to RE (55)"""
        # Binary: 0100 0111 0000 1111 (r4 imm=15)
        cpu.InstMem.mem[0] = "01000110" 
        cpu.InstMem.mem[1] = "00001111"
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['RE'] == 15
        assert cpu.PC == 2

    # def test_add_imm_overflow(self, cpu: Arch242Emulator):
    #     """Test ADD immediate with overflow"""
    #     # Binary: 0100 0001 1111 1111 (add imm=255)
    #     cpu.InstMem.mem[0] = "0100000111111111"
    #     cpu.RegFile['ACC'] = 1
    #     cpu.RegFile['CF'] = 0
        
    #     cpu.instr = cpu.fetch()
    #     cpu.decode()
    #     cpu.execute()
        
    #     assert cpu.RegFile['ACC'] == 0  # 1 + 255 wraps to 0
    #     assert cpu.RegFile['CF'] == 1  # Should set carry flag
    #     assert cpu.PC == 2

    # def test_sub_imm_underflow(self, cpu: Arch242Emulator):
    #     """Test SUB immediate with underflow"""
    #     # Binary: 0100 0010 0000 0001 (sub imm=1)
    #     cpu.InstMem.mem[0] = "0100001000000001"
    #     cpu.RegFile['ACC'] = 0
    #     cpu.RegFile['CF'] = 0
        
    #     cpu.instr = cpu.fetch()
    #     cpu.decode()
    #     cpu.execute()
        
    #     assert cpu.RegFile['ACC'] == 255  # 0 - 1 wraps to 255
    #     assert cpu.RegFile['CF'] == 1  # Should set carry flag
    #     assert cpu.PC == 2

    # def test_edge_cases(self, cpu: Arch242Emulator):
    #     """Test edge cases of immediate operations"""
    #     # Test zero immediate
    #     cpu.InstMem.mem[0] = "0100000100000000"  # add imm=0
    #     cpu.RegFile['ACC'] = 42
    #     cpu.instr = cpu.fetch()
    #     cpu.decode()
    #     cpu.execute()
    #     assert cpu.RegFile['ACC'] == 42
    #     assert cpu.PC == 2
        
    #     # Test max immediate (15)
    #     cpu.InstMem.mem[2] = "0100011110001111"  # r4 imm=15
    #     cpu.instr = cpu.fetch()
    #     cpu.decode()
    #     cpu.execute()
    #     assert cpu.RegFile['RE'] == 15
    #     assert cpu.PC == 4

class TestType6Instructions:
    """Test suite for Type 6 instructions (rarb <imm>)"""
    
    def test_rarb_imm(self, cpu: Arch242Emulator):
        """Test loading immediate to RA/RB (65)"""
        cpu.InstMem.mem[0] = "01011111"  # First byte
        cpu.InstMem.mem[1] = "00000000"  # Second byte 
        
        cpu.instr = cpu.fetch()  # Should get both bytes
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['RA'] == 0b1111  # 15
        assert cpu.RegFile['RB'] == 0b0000  # 2
        assert cpu.PC == 2  # 16-bit instruction

class TestType7Instructions:
    """Test suite for Type 7 instructions (rcrd <imm>)"""
    
    def test_rcrd_imm(self, cpu: Arch242Emulator):
        cpu.InstMem.mem[0] = "01101111"  # First byte
        cpu.InstMem.mem[1] = "00001111"  # Second byte 
        
        cpu.instr = cpu.fetch()  # Should get both bytes
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['RC'] == 0b0000  # 15
        assert cpu.RegFile['RD'] == 0b1111  # 2
        assert cpu.PC == 2  # 16-bit instruction

class TestType8Instructions:
    """Test suite for Type 8 instructions (acc <imm>)"""
    
    def test_acc_imm(self, cpu: Arch242Emulator):
        # Instruction format: 0111 imm (8-bit)
        cpu.InstMem.mem[0] = "01110101"  # imm=5
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['ACC'] == 0b0101  # 5
        assert cpu.PC == 1

class TestType9Instructions:
    """Test suite for Type 9 instructions (b-bit)"""
    
    def test_b_bit_branch_taken(self, cpu: Arch242Emulator):
        """Test jump taken when ACC bit k is 1"""
        cpu.PC = 0x0020
        cpu.InstMem.mem[0x20] = "10001000"  # 1000kkbb
        cpu.InstMem.mem[0x21] = "00000101"  # a = 0b00000101
        
        cpu.RegFile["ACC"] = 0b0100  # Bit 2 = 1 (k = 2)

        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        k = cpu.instr.bin[4:6]
        b = cpu.instr.bin[6:8]
        a = cpu.instr.bin[8:]

        assert k == "10"
        assert b == "00"
        assert a == "00000101"
        imm = (int(utils.to_strbin(b), 2) << 8) | int(utils.to_strbin(a), 2) # = 0x105
        expected_pc = ((cpu.PC - 2) & 0xF800) | imm
        assert cpu.PC == expected_pc, f"Expected PC = {hex(expected_pc)}, got {hex(cpu.PC)}"

    def test_b_bit_branch_not_taken(self, cpu: Arch242Emulator):
        """Test conditional jump is NOT taken when ACC bit K is 0"""

        # Same instruction: k=2, b=1, a=0x05 → imm = 0x105
        cpu.PC = 0x20
        cpu.InstMem.mem[0x20] = "10001000"
        cpu.InstMem.mem[0x21] = "10000101"

        cpu.RegFile["ACC"] = 0b00000000  # Bit 2 is 0 → should NOT jump

        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()

        # Should just move to next instruction (2-byte instr)
        expected_pc = 0x0022
        assert cpu.PC == expected_pc, f"Expected PC to be {hex(expected_pc)}, got {hex(cpu.PC)}"

class TestType10Instructions:
    """Test suite for Type 10 instructions (bnz)"""
    
    def test_bnz_a(self, cpu: Arch242Emulator):
        """Test bnz-a instruction (69)"""
        # Instruction format: 1001 0 b a (16-bit)
        cpu.InstMem.mem[0] = "10100010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # 
        cpu.RegFile['RA'] = 1

        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['RA'] == 1
        assert cpu.IMM == 592
        assert cpu.instr.bin[4] == '0'
        # Should always take the branch
        expected_pc = (cpu.PC & 0xF800) | (0b010 << 8) | cpu.IMM
        assert cpu.PC == expected_pc

    def test_bnz_a(self, cpu: Arch242Emulator):
        """Test bnz-a instruction (69)"""
        # Instruction format: 1001 0 b a (16-bit)
        cpu.InstMem.mem[0] = "10101010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # 
        cpu.RegFile['RB'] = 1

        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        assert cpu.RegFile['RB'] == 1
        assert cpu.IMM == 592
        assert cpu.instr.bin[4] == '1'
        # Should always take the branch
        expected_pc = (cpu.PC & 0xF800) | (0b010 << 8) | cpu.IMM
        assert cpu.PC == expected_pc

class TestType11Instructions:
    """Test suite for Type 11 instructions (beqz/bnez)"""
    
    def test_beqz(self, cpu: Arch242Emulator):
        """Test beqz instruction (71)"""
        # Instruction format: 1010 0 b a (16-bit)
        cpu.InstMem.mem[0] = "10110010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # Second byte (b=2, a=5)
        cpu.RegFile['ACC'] = 1  # Non-zero
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        assert cpu.IMM == 592
        # Should branch since ACC != 0 and tag=0
        expected_pc = (cpu.PC & 0xF800) | (0b010 << 8) | cpu.IMM
        assert cpu.PC == expected_pc
    
    def test_bnez(self, cpu: Arch242Emulator):
        """Test bnez instruction (72)"""
        # Instruction format: 1010 1 b a (16-bit)
        cpu.InstMem.mem[0] = "10111010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # Second byte (b=2, a=5)
        cpu.RegFile['ACC'] = 0  # Zero
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Should branch since ACC == 0 and tag=1
        expected_pc = (cpu.PC & 0xF800) | (0b010 << 8) | cpu.IMM
        assert cpu.PC == expected_pc

class TestType12Instructions:
    """Test suite for Type 12 instructions (beqz-cf/bnez-cf)"""
    
    def test_beqz_cf(self, cpu: Arch242Emulator):
        """Test beqz-cf instruction (73)"""
        # Instruction format: 1011 0 b a (16-bit)
        cpu.InstMem.mem[0] = "11000010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # Second byte (b=2, a=5)
        cpu.RegFile['CF'] = 1  # Non-zero
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Should branch since CF != 0 and tag=0
        expected_pc = (cpu.PC & 0xF800) | (0b010 << 8) | cpu.IMM
        assert cpu.PC == expected_pc
    
    def test_bnez_cf(self, cpu: Arch242Emulator):
        """Test bnez-cf instruction (74)"""
        # Instruction format: 1011 1 b a (16-bit)
        cpu.InstMem.mem[0] = "11001010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # Second byte (b=2, a=5)
        cpu.RegFile['CF'] = 0  # Zero
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Should branch since CF == 0 and tag=1
        expected_pc = (cpu.PC & 0xF800) | (0b010 << 8) | cpu.IMM
        assert cpu.PC == expected_pc

class TestType13Instructions:
    """Test suite for Type 13 instructions (branch on RD)"""
    
    def test_branch_rd(self, cpu: Arch242Emulator):
        """Test branch on RD instruction (76)"""
        # Instruction format: 1100 1 b a (16-bit)
        cpu.InstMem.mem[0] = "11001010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # Second byte (b=2, a=5)
        cpu.RegFile['RD'] = 1  # Non-zero
        
        cpu.instr = cpu.fetch()
        cpu.decode()
        cpu.execute()
        
        # Should branch since RD != 0 and tag=1
        expected_pc = (cpu.PC & 0xF800) | (0b010 << 8) | cpu.IMM
        assert cpu.PC == expected_pc

class TestType14Instructions:
    """Test suite for Type 14 instructions (branch on b)"""
    
    def test_b(self, cpu: Arch242Emulator):
        # Instruction format: 1100 1 b a (16-bit)
        cpu.InstMem.mem[0] = "11101010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # Second byte (b=2, a=5)
        imm = int(utils.to_strbin(cpu.InstMem.mem[0][4:] + cpu.InstMem.mem[1]),2)

        assert cpu.PC == 0
        cpu.instr = cpu.fetch()
        cpu.decode()
        assert cpu.PC == 1
        lowerPC = cpu.PC & utils.HEX_16L4
        expected_cpu = imm << 4 | lowerPC
        cpu.execute()
        assert cpu.PC == expected_cpu
        assert cpu.instr.bin == "1110101001010000"
        
class TestType14Instructions:
    """Test suite for Type 14 instructions (branch on b)"""
    
    def test_b(self, cpu: Arch242Emulator):
        # Instruction format: 1100 1 b a (16-bit)
        cpu.InstMem.mem[0] = "11111010"  # First byte
        cpu.InstMem.mem[1] = "01010000"  # Second byte (b=2, a=5)
        imm = int(utils.to_strbin(cpu.InstMem.mem[0][4:] + cpu.InstMem.mem[1]),2)

        assert cpu.PC == 0
        cpu.instr = cpu.fetch()
        cpu.decode()
        assert cpu.PC == 1
        lowerPC = cpu.PC & utils.HEX_16L4
        expected_cpu = imm << 4 | lowerPC
        cpu.execute()
        assert 1 + 2 == cpu.TEMP
        assert cpu.PC == expected_cpu
        assert cpu.instr.bin == "1111101001010000"
