b-bit 0 1   -------------------- NEXT_CELL(direction ACC, address RB:RA, addres RD:RC) -> MEM[RB:RA], MEM[RD:RC]
--!         ------------ BRANCH: NEXT_CELL_up -- note that for the following branches, it is guaranteed that no row/col overflows/underflows, since an invalid address wouldve been caught in the snake head update stage anyway
b-bit 1 1   ------------ BRANCH: NEXT_CELL_down
--!
b-bit 2 1   ------------ BRANCH: NEXT_CELL_left
--!
nop
nop
nop
b-bit 3 1   ------------ BRANCH: NEXT_CELL_right
--!
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
dec*-mba    ------------ BRANCH_RECEIVER: NEXT_CELL_up
ret
inc*-mba    ------------ BRANCH_RECEIVER: NEXT_CELL_down
ret
rot-r       ------------ BRANCH_RECEIVER: NEXT_CELL_left
to-mba      -- sub 1 to col and update
b-bit 3 2   ------------ BRANCH: NEXT_CELL_left_dec (if it happens that MSB is 1 after rotation (column is too low for current row), then we decrease row address by 1)
--!
ret
rot-l       ------------ BRANCH_RECEIVER: NEXT_CELL_right
to-mba      -- add 1 to col and update
and 1       -- if it happens that LSB is 1 after rotation (column is too high for current row), then we increase row address by 1
add-mba     -- only increases if previous operation made ACC = 1
ret
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
dec*-mba    ------------ BRANCH_RECEIVER: NEXT_CELL_left_dec
ret         -------------------- NEXT_CELL end
acc 0b0111  -------------------- INIT: 3-length snake at topmost row
rarb 192
--!
to-mba
rarb 9      -------------------- BRANCH_RECEIVER: game_loop
--!         -------------------- move snake-tail to next address
from-mba    -- ACC = queue[0]
rarb 6      -- RB:RA = snake-tail ADDRESS (row)
--!
rcrd 7      -- RD:RC = snake-tail NIBBLE (col)
--!
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
call 0      -- NEXT_CELL(queue[0], 6, 7)
--!
-------------------- shift queue down once
-------------------- create new snake-head according to input
-------------------- end game if hit border/own body
-------------------- BRANCH: game_loop



















.byte 0x00  ---- score
.byte 0x03  ---- length (3)
.byte 0x00  ---- food address
.byte 0x00
.byte 0xc0  ---- snake-tail address (192, 0b0000)
.byte 0x00
.byte 0xc0  ---- snake-head address (192, 0b0100)
.byte 0x04
.byte 0x0a  ---- queue-tail address
.byte 0x04  ---- queue (0b1000 = right)
.byte 0x04  ---- queue (0b1000 = right)

-- 0: score
-- 1: length
-- 2-3: food        (ADDRESS (row), NIBBLE (col))
-- 4-5: snake head  (ADDRESS (row), NIBBLE (col))
-- 6-7: snake tail  (ADDRESS (row), NIBBLE (col))
-- 8: queue tail
-- 9 onwards: queue
-- in order to save space, the queue will only save the next direction to take (up, down, left, right) for the next cell
-- i.e. queue element is a 4-bit number that represents an implicit pointer to the next cell of the snake
-- example: 0001 means from the snake tail address, we move up once, that is the next cell of the snake
-- lines with "--!" are padding for 16-bit instructions (split into two) for easier reading
