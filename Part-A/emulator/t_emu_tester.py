import sys
import os
import pytest
from pathlib import Path
import emu_utils as emu_u 

# Add parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Arch242_emulator import Instructions, Arch242Emulator, DataMemory, InstrMemory
from emu_instructions import EmulatorInstructions

@pytest.fixture
def cpu(): return Arch242Emulator()

@pytest.fixture
def emu_instr(cpu): return EmulatorInstructions(cpu)

@pytest.fixture
def data_mem(): return DataMemory()

@pytest.fixture
def instr_mem(): return InstrMemory()

class TestMemory:
    def test_data_memory_init(self, data_mem):
        """Test DataMemory initialization"""
        assert len(data_mem.Data) == 256
        assert isinstance(data_mem.Data, list)
        
    def test_instr_memory_init(self, instr_mem):
        """Test InstrMemory initialization"""
        assert len(instr_mem.Instruction) == 0
        assert isinstance(instr_mem.Instruction, list)

class TestCPUInitialState:
    def test_cpu_init(self, cpu: Arch242Emulator):
        """Test CPU registers are initialized correctly"""
        # # --- Init registers 
        assert cpu.PC == 0
        assert len(cpu.RegFile) == 9
        # for reg, val in cpu.RegFile.items():
        #     assert val == 0


        # # --- Init system
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

    def assert_type(self,  cpu: Arch242Emulator, bin, dec, opcode):
        assert cpu.instr.bin == bin
        assert cpu.instr.dec == dec
        assert cpu.instr.opcode == opcode

    def test_rot_r(self, cpu: Arch242Emulator):
        """Test ROTR (rotate right) instruction - repeated 4 times"""

        cpu.InstrMemory.extend(["00000000"] * 4)
        cpu.RegFile['ACC'] = 0b1001  # Initial ACC
        assert cpu.PC == 0

        # Clock Tick 1
        self._rot_r_tick(cpu, expected_acc=0b1100, expected_pc=1)
   
        # Clock Tick 2
        self._rot_r_tick(cpu, expected_acc=0b0110, expected_pc=2)
  
        # Clock Tick 3
        self._rot_r_tick(cpu, expected_acc=0b0011, expected_pc=3)

        # # Clock Tick 4
        self._rot_r_tick(cpu, expected_acc=0b1001, expected_pc=4)

    def test_rot_l(self, cpu: Arch242Emulator):
        """Test ROTR (rotate right) instruction - repeated 4 times"""

        cpu.InstrMemory.extend(["00000001"] * 4)
        cpu.RegFile['ACC'] = 0b1001  # Initial ACC
        assert cpu.PC == 0

         # Clock Tick 1
        self._rot_l_tick(cpu, expected_acc=0b0011, expected_pc=1)

        # Clock Tick 2
        self._rot_l_tick(cpu, expected_acc=0b0110, expected_pc=2)

        # Clock Tick 3
        self._rot_l_tick(cpu, expected_acc=0b1100, expected_pc=3)

        # # Clock Tick 4
        self._rot_l_tick(cpu, expected_acc=0b1001, expected_pc=4)
    
    def test_rot_rc(self, cpu: Arch242Emulator):
        """Test ROTRC (rotate right) instruction - repeated 4 times"""

        cpu.InstrMemory.extend(["00000010"] * 4)
        cpu.RegFile['ACC'] = 0b0011  # Initial ACC
        cpu.RegFile['CF'] = 0b1
        assert cpu.PC == 0

         # Clock Tick 1
        self._rot_rc_tick(cpu, expected_cfacc=0b11001, expected_pc=1)

        # Clock Tick 2
        self._rot_rc_tick(cpu, expected_cfacc=0b11100, expected_pc=2)

        # # Clock Tick 3
        self._rot_rc_tick(cpu, expected_cfacc=0b01110, expected_pc=3)

        # # # Clock Tick 4
        self._rot_rc_tick(cpu, expected_cfacc=0b00111, expected_pc=4)

    def test_rot_lc(self, cpu: Arch242Emulator):
        """Test ROTRC (rotate right) instruction - repeated 4 times"""

        cpu.InstrMemory.extend(["00000011"] * 4)
        cpu.RegFile['ACC'] = 0b0011  # Initial ACC
        cpu.RegFile['CF'] = 0b1
        assert cpu.PC == 0

         # Clock Tick 1
        self._rot_lc_tick(cpu, expected_cfacc=0b00111, expected_pc=1)

        # Clock Tick 2
        self._rot_lc_tick(cpu, expected_cfacc=0b01110, expected_pc=2)

        # # Clock Tick 3
        self._rot_lc_tick(cpu, expected_cfacc=0b11100, expected_pc=3)

        # # # Clock Tick 4
        self._rot_lc_tick(cpu, expected_cfacc=0b11001, expected_pc=4)

    def test_from_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00000100"])
        cpu.RegFile['ACC'] = 0b0001
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010

        assert cpu.RegFile['RA'] == 0b0001
        assert cpu.RegFile['RB'] == 0b0010
        
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000100"
        cpu.decode()
        assert cpu.instr.bin == "00000100"
        assert cpu.instr.dec == 0b00000100
        assert cpu.instr.opcode == "Type1"
        cpu.execute()
        assert cpu.RBRA == 33
        assert cpu.DataMemory[cpu.RBRA] == 0
        assert cpu.RegFile['ACC'] == 0

    def test_to_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00000101"])
        cpu.RegFile['ACC'] = 0b0001
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010

        assert cpu.RegFile['RA'] == 0b0001
        assert cpu.RegFile['RB'] == 0b0010
        
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000101"
        cpu.decode()
        assert cpu.instr.bin == "00000101"
        assert cpu.instr.dec == 0b00000101
        assert cpu.instr.opcode == "Type1"
        cpu.execute()
        assert cpu.RBRA == 33
        assert cpu.DataMemory[cpu.RBRA] == 1
        assert cpu.RegFile['ACC'] == 1
    
    def test_from_mbc(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00000110"])
        cpu.RegFile['ACC'] = 0b0001
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010

        assert cpu.RegFile['RC'] == 0b0001
        assert cpu.RegFile['RD'] == 0b0010
        
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000110"
        cpu.decode()
        assert cpu.instr.bin == "00000110"
        assert cpu.instr.dec == 0b00000110
        assert cpu.instr.opcode == "Type1"
        cpu.execute()
        assert cpu.RDRC == 33
        assert cpu.DataMemory[cpu.RDRC] == 0
        assert cpu.RegFile['ACC'] == 0

    def test_to_mbc(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00000111"])
        cpu.RegFile['ACC'] = 0b0001
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010

        assert cpu.RegFile['RC'] == 0b0001
        assert cpu.RegFile['RD'] == 0b0010
        
        cpu.instr = cpu.fetch()
        assert cpu.instr == "00000111"
        cpu.decode()
        assert cpu.instr.bin == "00000111"
        assert cpu.instr.dec == 0b00000111
        assert cpu.instr.opcode == "Type1"
        cpu.execute()
        assert cpu.RDRC == 33
        assert cpu.DataMemory[cpu.RDRC] == 1
        assert cpu.RegFile['ACC'] == 1
    
    def test_addc_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001000"])
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['CF'] = 0b0
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010

        assert cpu.RegFile['RA'] == 0b0001
        assert cpu.RegFile['RB'] == 0b0010

        cpu.RBRA = cpu.RegFile['RB'] << (emu_u.INSTR_4) | cpu.RegFile['RA']

        assert cpu.RBRA == 33

        cpu.DataMemory[cpu.RBRA] = 33

        assert cpu.DataMemory[cpu.RBRA] == 33

        assert cpu.RegFile['CF'] == 0

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001000"
        cpu.decode()

        self.assert_type(cpu, bin="00001000", dec=8, opcode="Type1")

        cpu.execute()
        assert cpu.RegFile['CF'] == 0
        
    def test_add_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001001"])
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['CF'] = 0b0
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010

        assert cpu.RegFile['RC'] == 0b0001
        assert cpu.RegFile['RD'] == 0b0010

        cpu.RDRC = cpu.RegFile['RD'] << (emu_u.INSTR_4) | cpu.RegFile['RC']

        assert cpu.RDRC == 33

        cpu.DataMemory[cpu.RDRC] = 15

        assert cpu.DataMemory[cpu.RDRC] == 15

        assert cpu.RegFile['CF'] == 0

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001001"
        cpu.decode()

        self.assert_type(cpu, bin="00001001", dec=9, opcode="Type1")

        cpu.execute()
        assert cpu.RegFile['CF'] == 1  # 1 + 15 = 16 (overflow)

    def test_subc_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001010"])
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['CF'] = 0b1
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010

        assert cpu.RegFile['RA'] == 0b0001
        assert cpu.RegFile['RB'] == 0b0010

        cpu.RBRA = cpu.RegFile['RB'] << (emu_u.INSTR_4) | cpu.RegFile['RA']

        assert cpu.RBRA == 33

        cpu.DataMemory[cpu.RBRA] = 2

        assert cpu.DataMemory[cpu.RBRA] == 2

        assert cpu.RegFile['CF'] == 1

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001010"
        cpu.decode()

        self.assert_type(cpu, bin="00001010", dec=10, opcode="Type1")

        cpu.execute()
        assert cpu.RegFile['CF'] == 0  # 1 - 2 + 1 = 0 (no underflow)

    def test_sub_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001011"])
        cpu.RegFile['ACC'] = 0b0001
        cpu.RegFile['CF'] = 0b0
        assert cpu.RegFile['ACC'] == 0b0001

        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010

        assert cpu.RegFile['RA'] == 0b0001
        assert cpu.RegFile['RB'] == 0b0010

        cpu.RBRA = cpu.RegFile['RB'] << (emu_u.INSTR_4) | cpu.RegFile['RA']

        assert cpu.RBRA == 33

        cpu.DataMemory[cpu.RBRA] = 2

        assert cpu.DataMemory[cpu.RBRA] == 2

        assert cpu.RegFile['CF'] == 0

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001011"
        cpu.decode()

        self.assert_type(cpu, bin="00001011", dec=11, opcode="Type1")

        cpu.execute()
        assert cpu.RegFile['CF'] == 1  # 1 - 2 = -1 (underflow)

    def test_inc_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001100"])
        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010

        assert cpu.RegFile['RA'] == 0b0001
        assert cpu.RegFile['RB'] == 0b0010

        cpu.RBRA = cpu.RegFile['RB'] << (emu_u.INSTR_4) | cpu.RegFile['RA']

        assert cpu.RBRA == 33

        cpu.DataMemory[cpu.RBRA] = 15

        assert cpu.DataMemory[cpu.RBRA] == 15

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001100"
        cpu.decode()

        self.assert_type(cpu, bin="00001100", dec=12, opcode="Type1")

        cpu.execute()
        assert cpu.DataMemory[cpu.RBRA] == 0 # truncate

    def test_dec_mba(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001101"])
        cpu.RegFile['RA'] = 0b0001
        cpu.RegFile['RB'] = 0b0010

        assert cpu.RegFile['RA'] == 0b0001
        assert cpu.RegFile['RB'] == 0b0010

        cpu.RBRA = cpu.RegFile['RB'] << (emu_u.INSTR_4) | cpu.RegFile['RA']

        assert cpu.RBRA == 33

        cpu.DataMemory[cpu.RBRA] = 1

        assert cpu.DataMemory[cpu.RBRA] == 1

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001101"
        cpu.decode()

        self.assert_type(cpu, bin="00001101", dec=13, opcode="Type1")

        cpu.execute()
        assert cpu.DataMemory[cpu.RBRA] == 0

    def test_inc_mdc(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001110"])
        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010

        assert cpu.RegFile['RC'] == 0b0001
        assert cpu.RegFile['RD'] == 0b0010

        cpu.RDRC = cpu.RegFile['RD'] << (emu_u.INSTR_4) | cpu.RegFile['RC']

        assert cpu.RDRC == 33

        cpu.DataMemory[cpu.RDRC] = 15

        assert cpu.DataMemory[cpu.RDRC] == 15

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001110"
        cpu.decode()

        self.assert_type(cpu, bin="00001110", dec=14, opcode="Type1")

        cpu.execute()
        assert cpu.DataMemory[cpu.RDRC] == 0

    def test_dec_mdc(self, cpu: Arch242Emulator):
        cpu.InstrMemory.extend(["00001111"])
        cpu.RegFile['RC'] = 0b0001
        cpu.RegFile['RD'] = 0b0010

        assert cpu.RegFile['RC'] == 0b0001
        assert cpu.RegFile['RD'] == 0b0010

        cpu.RDRC = cpu.RegFile['RD'] << (emu_u.INSTR_4) | cpu.RegFile['RC']

        assert cpu.RDRC == 33

        cpu.DataMemory[cpu.RDRC] = 1

        assert cpu.DataMemory[cpu.RDRC] == 1

        cpu.instr = cpu.fetch()
        assert cpu.instr == "00001111"
        cpu.decode()

        self.assert_type(cpu, bin="00001111", dec=15, opcode="Type1")

        cpu.execute()
        assert cpu.DataMemory[cpu.RDRC] == 0

class TestType2Instructions:
    ...