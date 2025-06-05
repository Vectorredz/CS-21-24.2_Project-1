import sys
import os
import pytest
from emulator.emu_instructions import EmulatorInstructions

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Arch242_emulator import Arch242Emulator

# overrides pyxel 

@pytest.fixture
def cpu(): return Arch242Emulator()

@pytest.fixture
def emu_instr(): return EmulatorInstructions() 
        
class TestType1:

    def test_rot_r(self, cpu: Arch242Emulator, emu_instr: EmulatorInstructions):
        # test 
        cpu.RegFile['ACC']
        pass
    
        


