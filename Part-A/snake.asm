b GAME_LOOP ------------ BRANCH_TO: GAME_LOOP
--!
from-reg 0 -------------------- function NEXT_CELL(direction RE, CELL pointer RB:RA)
rcrd 242 -- temporarily store CELL pointer
--!
to-mdc
from-reg 1
rcrd 243
--!
to-mdc
from-reg 0 -- copy pointer to RD:RC
to-reg 2
from-reg 1
to-reg 3
from-reg 4 -- get direction (RE)
b-bit 0 NEXT_CELL_up ------------ BRANCH_TO: NEXT_CELL_up
--!
b-bit 1 NEXT_CELL_down ------------ BRANCH_TO: NEXT_CELL_down
--!
b-bit 2 NEXT_CELL_left ------------ BRANCH_TO: NEXT_CELL_left
--!
b-bit 3 NEXT_CELL_right ------------ BRANCH_TO: NEXT_CELL_right
--!
nop -- this should be unreachable
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
NEXT_CELL_up: acc 1 ------------ BRANCH: NEXT_CELL_up
rarb 242 -- move pointer to ID upper nibble first
--!
clr-cf
add-mba
to-mba
acc 0
rarb 243
--!
addc-mba
to-mba
acc 5 -- set sub-mba arg to 5
rarb 244
--!
to-mba
from-mdc -- get lower nibble
clr-cf
sub-mba -- move up 1 row (-5 IDs)
to-mdc -- store to lower nibble
r4 0
--!
bnez-cf NEXT_CELL_up_dec ------------ BRANCH_TO: NEXT_CELL_up_dec
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
NEXT_CELL_up_dec: rcrd 242 ------------ BRANCH: NEXT_CELL_up_dec
--! -- copy upper nibble address to RB:RA
from-mdc
to-reg 0
rcrd 243
--!
from-mdc
to-reg 1
dec*-mba -- decrease upper nibble if CF underflow bit is 1
nop
nop
nop
nop
nop
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
nop
nop
nop
nop
nop
NEXT_CELL_down: acc 1 ------------ BRANCH: NEXT_CELL_down
rarb 242 -- move pointer to ID upper nibble first
--!
clr-cf
add-mba
to-mba
acc 0
rarb 243
--!
addc-mba
to-mba
acc 5 -- set add-mba arg to 5
rarb 244
--!
to-mba
from-mdc -- get lower nibble
clr-cf
add-mba -- move up 1 row (+5 IDs)
to-mdc -- store to lower nibble
rcrd 242 -- copy upper nibble address to RB:RA
--!
from-mdc
to-reg 0
rcrd 243
--!
from-mdc
to-reg 1
addc-mba -- add any possible overflows
to-mba
r4 0
--!
nop
nop
ret
NEXT_CELL_left: from-reg 2 ------------ BRANCH: NEXT_CELL_left
rarb 245 -- store initial pointer for possible use later
--!
to-mba
from-reg 3
rarb 246
--!
to-mba
acc 2 -- move pointer to MASK first
rarb 242
--!
clr-cf
add-mba
to-mba
to-reg 2 -- copy to RC
acc 0
rarb 243
--!
addc-mba
to-mba
to-reg 3 -- copy to RD
from-mdc -- get MASK
rot-r -- move left 1 col
to-mdc
b-bit 3 NEXT_CELL_left_flow ------------ BRANCH_TO: NEXT_CELL_left_flow
--!
r4 0
--!
nop
nop
nop
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
NEXT_CELL_left_flow: rarb 245 ------------ BRANCH: NEXT_CELL_left_flow
--!
from-mba -- set pointer and RD:RC to initial
rarb 242
--!
to-mba
to-reg 2
rarb 246
--!
from-mba
rarb 243
--!
to-mba
to-reg 3
acc 1 -- move pointer to ID upper nibble first
rarb 242
--!
clr-cf
add-mba
to-mba
acc 0
rarb 243
--!
addc-mba
to-mba
acc 1 -- set sub-mba arg to 1
rarb 244
--!
to-mba
from-mdc -- get lower nibble
clr-cf
sub-mba -- decrease ID
to-mdc -- store to lower nibble
r4 1
--!
bnez-cf NEXT_CELL_left_flow_dec ------------ BRANCH_TO: NEXT_CELL_left_flow_dec
--!
nop
nop
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
nop
nop
NEXT_CELL_left_flow_dec: rcrd 242 ------------ BRANCH: NEXT_CELL_left_flow_dec
--! -- copy upper nibble address to RB:RA
from-mdc
to-reg 0
rcrd 243
--!
from-mdc
to-reg 1
dec*-mba -- decrease upper nibble if CF underflow bit is 1
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
NEXT_CELL_right: from-reg 2 ------------ BRANCH: NEXT_CELL_right
rarb 245 -- store initial pointer for possible use later
--!
to-mba
from-reg 3
rarb 246
--!
to-mba
acc 2 -- move pointer to MASK first
rarb 242
--!
clr-cf
add-mba
to-mba
to-reg 2 -- copy to RC
acc 0
rarb 243
--!
addc-mba
to-mba
to-reg 3 -- copy to RD
from-mdc -- get MASK
rot-l -- move right 1 col
to-mdc
b-bit 0 NEXT_CELL_right_flow ------------ BRANCH_TO: NEXT_CELL_right_flow
--!
r4 0
--!
nop
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
nop
NEXT_CELL_right_flow: rarb 245 ------------ BRANCH: NEXT_CELL_right_flow
--!
from-mba -- set pointer and RD:RC to initial
rarb 242
--!
to-mba
to-reg 2
rarb 246
--!
from-mba
rarb 243
--!
to-mba
to-reg 3
acc 1 -- move pointer to ID upper nibble first
rarb 242
--!
clr-cf
add-mba
to-mba
acc 0
rarb 243
--!
addc-mba
to-mba
acc 1 -- set add-mba arg to 1
rarb 244
--!
to-mba
from-mdc -- get lower nibble
clr-cf
add-mba -- increase ID
to-mdc -- store to lower nibble
rcrd 242 -- copy upper nibble address to RB:RA
--!
from-mdc
to-reg 0
rcrd 243
--!
from-mdc
to-reg 1
addc-mba -- add any possible underflows
to-mba
r4 1
--!
nop
nop
nop
nop
nop
nop
nop
nop
ret -------------------- NEXT_CELL end
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
GAME_LOOP: from-ioa ---------------------------------------- GAME_LOOP
rarb 253 -- store new direction to 253 (get current val first if input is 0b0000)
--!
beqz GAME_LOOP_input ------------ BRANCH_TO: GAME_LOOP_input
--!
from-mba
b __GAME_LOOP_input_skip
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
__GAME_LOOP_input_skip: nop
nop
nop
nop
nop
nop
GAME_LOOP_input: to-mba ------------ BRANCH: GAME_LOOP_input
to-reg 4 -- setup call args
rarb 5
--!
nop
nop
call 0 ------------ NEXT_CELL(input, &snake-head)
--!
from-reg 4
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
beqz GAME_LOOP_oob_row ------------ BRANCH_TO: GAME_LOOP_oob_row
--!
rarb 6 -- compare column borders if oob
--!
acc 0b1100 -- 192, 197, 202, 207
xor-ba
bnez GAME_LOOP_oob_col_1101 ------------ BRANCH_TO: GAME_LOOP_oob_col_1101
--!
rarb 5
--!
acc 0b0000 -- 1100 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1100_skip1
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
__GAME_LOOP_oob_col_1100_skip1: beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b0101 -- 1100 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1100_skip2
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
__GAME_LOOP_oob_col_1100_skip2: nop
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b1010 -- 1100 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1100_skip3
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
__GAME_LOOP_oob_col_1100_skip3: nop
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b1111 -- 1100 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1100_skip4
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
__GAME_LOOP_oob_col_1100_skip4: nop
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
nop
nop
b GAME_LOOP_oob_row ------------ BRANCH_TO: GAME_LOOP_oob_row
--!
nop
nop
nop
nop
GAME_LOOP_oob_col_1101: acc 0b1101 -- 212, 217, 222 ------------ BRANCH: GAME_LOOP_oob_col_1101
xor-ba
bnez GAME_LOOP_oob_col_1110 ------------ BRANCH_TO: GAME_LOOP_oob_col_1110
--!
rarb 5
--!
acc 0b0100 -- 1101 + (lower nibble)
xor-ba
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b1001 -- 1101 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1101_skip1
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
__GAME_LOOP_oob_col_1101_skip1: nop
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b1110 -- 1101 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1101_skip2
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
__GAME_LOOP_oob_col_1101_skip2: nop
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
nop
nop
b GAME_LOOP_oob_row ------------ BRANCH_TO: GAME_LOOP_oob_row
--!
nop
nop
nop
nop
nop
nop
GAME_LOOP_oob_col_1110: acc 0b1110 GAME_LOOP_oob_col_1110 -- 227. 232, ------------ BRANCH: GAME_LOOP_oob_col_1110
xor-ba
b __GAME_LOOP_oob_col_1110_skip1
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
__GAME_LOOP_oob_col_1110_skip1: nop
nop
nop
nop
nop
nop
bnez GAME_LOOP_oob_row ------------ BRANCH_TO: GAME_LOOP_oob_row
--!
rarb 5
--!
acc 0b0011 -- 1110 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1110_skip2
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
__GAME_LOOP_oob_col_1110_skip2: nop
nop
nop
nop
nop
nop
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b1000 -- 1110 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1110_skip3
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
__GAME_LOOP_oob_col_1110_skip3: nop
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b1101 -- 1110 + (lower nibble)
xor-ba
b __GAME_LOOP_oob_col_1110_skip4
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
__GAME_LOOP_oob_col_1110_skip4: nop
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
beqz GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
nop
nop
GAME_LOOP_oob_row: acc 0b1100 ------------ BRANCH: GAME_LOOP_oob_row
rarb 243 -- check if lower than 192: subtract 0b1100 and check if underflow (upper nibble of 192)
--!
to-mba
rarb 6
--!
from-mba
rarb 243
--!
clr-cf
sub-mba
b __GAME_LOOP_oob_row_skip
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
__GAME_LOOP_oob_row_skip: nop
bnez-cf GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0b1111 -- check if upper nibble is 1111
rarb 6
--!
xor-ba
bnez GAME_LOOP_food ------------ BRANCH_TO: GAME_LOOP_food
--!
rarb 5 -- check if lower nibble > 0b0001 (higher than 241)
--!
from-mba
rarb 242
--!
to-mba
acc 0b0001
clr-cf
sub-mba
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
bnez-cf GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
nop
nop
nop
nop
GAME_LOOP_food: acc 0 ------------ BRANCH: GAME_LOOP_food
rarb 244
--!
to-mba
rarb 5 -- to check if its same as food address, keep spamming xor and doing OR operation on MEM[244]. its equal if and only if MEM[244] == 0
--! -- lower nibble
from-mba
rarb 2
--!
xor-ba
rarb 244
-!
or*-mba
rarb 6 -- upper nibble
--!
from-mba
rarb 3
--!
xor-ba
rarb 244
-!
or*-mba
rarb 7 -- MASK
--!
from-mba
rarb 4
--!
xor-ba
rarb 244
-!
or*-mba
from-mba -- only copies lower nibble of this address, no need to worry about upper 0b1111 due to xor + or
beqz GAME_LOOP_food_ate ------------ BRANCH_TO: GAME_LOOP_food_ate
--! -- food was missed
rcrd 5
--! -- check if snake-head LED is already 1
from-mdc
to-reg 0
rcrd 6
--!
from-mdc
to-reg 1
rcrd 7
--!
from-mdc
and-ba
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
bnez GAME_DEATH ------------ BRANCH_TO: GAME_DEATH
--!
acc 0 -- set food-ate to 0
rarb 255
--!
to-mba
rcrd 8 -- get snake-tail ID
--!
from-mdc
to-reg 0
rcrd 9
--!
from-mdc
to-reg 1
rcrd 10 -- get snake-tail MASK
--!
from-mdc
and*-mba -- update snake-tail LED
rarb 13 -- get queue-head dir and store to r4
--!
from-mba
to-reg 4
rarb 8 -- set to snake-tail CELL pointer
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
call 0 -- NEXT_CELL(queue-head dir, &snake-tail)
--!
rarb 12 -- copy queue-tail address to 242-243
--!
from-mba
to-reg 3 -- while copying, copy to RD:RC as well (to store direction at queue-tail to r4 later)
rarb 243
--!
to-mba
acc 1 -- while copying, lets also subtract 1 first for shifting later
rarb 242 -- set sub-mba arg to 1
--!
to-mba
rarb 11 -- get lower nibble
--!
from-mba
to-reg 2
rarb 242 -- subtract 1
--!
clr-cf
sub-mba
to-mba
from-mdc -- copy dir to r4
to-reg 4
bnez-cf GAME_LOOP_food_miss_queue-tail_dec ------------ BRANCH_TO: GAME_LOOP_food_miss_queue-tail_dec
--!
nop
b GAME_LOOP_food_miss_shift ------------ BRANCH_TO: GAME_LOOP_food_miss_shift
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
nop
nop
nop
nop
nop
nop
GAME_LOOP_food_miss_queue-tail_dec: rarb 243 ------------ BRANCH: GAME_LOOP_food_miss_queue-tail_dec
--!
dec*-mba
b GAME_LOOP_food_miss_shift ------------ BRANCH_TO: GAME_LOOP_food_miss_shift
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
GAME_LOOP_food_miss_shift: acc 0b0000 ------------ BRANCH: GAME_LOOP_food_miss_shift
rarb 243 -- if upper nibble is not 0b0000 then just skip lower nibble check
--!
xor-ba
bnez GAME_LOOP_food_miss_shift_cont ------------ BRANCH_TO: GAME_LOOP_food_miss_shift_cont
--!
acc 0b1101 -- set sub-mba arg to 0b1101
rarb 244
--!
to-mba
rarb 242 -- subtract 0b1101 from lower nibble
--!
from-mba
rarb 244
--!
clr-cf
sub-mba -- check if less than 13
bnez-cf GAME_LOOP_enqueue ------------ BRANCH_TO: GAME_LOOP_enqueue
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
GAME_LOOP_food_miss_shift_cont: rarb 242 ------------ BRANCH: GAME_LOOP_food_miss_shift_cont
--! -- copy current queue pointer to RD:RC
from-mba -- assume that r4 = dir from pointer + 1
to-reg 2
rarb 243
--!
from-mba
to-reg 3
from-mdc -- store dir at this pointer to r0
to-reg 0
from-reg 4 -- get dir from pointer + 1 and store it into this pointer
to-mdc
from-reg 0 -- get dir that was just changed and store to r4 for next iteration
to-reg 4
acc 1 -- set sub-mba arg to 1
rarb 244
--!
to-mba
rarb 242 -- get lower nibble
--!
from-mba
rarb 244 -- subtract 1
--!
clr-cf
sub-mba
to-mba
bnez-cf GAME_LOOP_food_miss_shift_dec ------------ BRANCH_TO: GAME_LOOP_food_miss_shift_dec
--!
b GAME_LOOP_food_miss_shift ------------ BRANCH_TO: GAME_LOOP_food_miss_shift
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
nop
nop
nop
nop
nop
nop
nop
GAME_LOOP_food_miss_shift_dec: rarb 243 ------------ BRANCH: GAME_LOOP_food_miss_shift_dec
--!
dec*-mba
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
b GAME_LOOP_food_miss_shift ------------ BRANCH_TO: GAME_LOOP_food_miss_shift
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
GAME_LOOP_food_ate: acc 1 ------------ BRANCH: GAME_LOOP_food_ate
rarb 255 -- set food-ate to 1
--!
to-mba
acc 1 -- length += 1
rarb 0
--!
clr-cf
add-mba
to-mba
rarb 1
--!
addc-mba
to-mba
acc 1 -- queue-tail address += 1
rarb 11
--!
clr-cf
add-mba
to-mba
rarb 12
--!
addc-mba
to-mba
rarb 254 -- score += 1
--!
inc*-mba
b __GAME_LOOP_food_ate_skip
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
__GAME_LOOP_food_ate_skip: nop
nop
nop
GAME_LOOP_enqueue: rcrd 11 ------------ BRANCH: GAME_LOOP_enqueue
--! -- get queue-tail address
from-mdc
to-reg 0
rcrd 12
--!
from-mdc
to-reg 1
rcrd 253 -- get new dir
--!
from-mdc
to-mba -- store new dir to queue-tail address
rcrd 5 -- get snake-head ID
--!
from-mdc
to-reg 0
rcrd 6
--!
from-mdc
to-reg 1
rcrd 7 -- get snake-head MASK
--!
from-mdc
and*-mba -- update snake-head LED
rarb 255 -- finally, check food-ate and spawn new food if its 1
--!
from-mba
nop
nop
nop
nop
nop
nop
nop
beqz GAME_LOOP ------------ BRANCH_TO: GAME_LOOP
--!
b GAME_LOOP_food_spawn ------------ BRANCH_TO: GAME_LOOP_food_spawn
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
nop
nop
nop
nop
nop
nop
GAME_DEATH: shutdown ------------ BRANCH: GAME_DEATH
--!
nop
GAME_LOOP_food_spawn: rarb 253 ------------ BRANCH: GAME_LOOP_food_spawn
--! -- spawn new food (final operation yay!!! >_<)
from-mba -- get new dir again
rarb 250 -- add to RNG
--!
add-mba
to-mba
rarb 252 -- add to RNG
--!
add-mba
to-mba
rarb 251 -- add to RNG
--!
add-mba
to-mba
acc 0b1100
and*-mba -- set upper nibble upper two bits to 1 (since 192-241 are all 11XX)
.byte 0x03  ---- length (lower nibble)
.byte 0x00  ---- length (upper nibble)
.byte 0x00  ---- food address ID (lower nibble)
.byte 0xda  -- food address ID (upper nibble)
.byte 0x01  -- food address MASK
.byte 0x00  ---- snake-tail address ID (lower nibble) = 192
.byte 0x0c  -- snake-tail address ID (upper nibble) = 192
.byte 0x01  -- snake-tail address MASK = 0b0001
.byte 0x00  ---- snake-head address ID (lower nibble) = 192
.byte 0x0c  -- snake-head address ID (upper nibble) = 192
.byte 0x04  -- snake-head address MASK = 0b0100
.byte 0x0e  ---- queue-tail address (lower nibble)
.byte 0x00  -- queue-tail address (upper nibble)
.byte 0x04  ---- queue (0b1000 = right)
.byte 0x04  ---- queue (0b1000 = right)

-- 0: length (lower nibble)
-- 1: length (upper nibble)
-- 2-4: food-CELL       (ID (8-bits), MASK (4-bits))
-- 5-7: snake-head CELL (ID (8-bits), MASK (4-bits))
-- 8-10: snake-tail CELL (ID (8-bits), MASK (4-bits))
-- 11-12: queue tail address
-- 13 onwards: queue

-- temp storage (for NEXT_CELL/GAME_LOOP)
    -- 242: address (lower nibble)
    -- 243: address (upper nibble)
    -- 244: temp storage for add/sub-mba/other
    -- 245: address2 (lower nibble) for over/underflows
    -- 246: address2 (upper nibble) for over/underflows
-- 250-252: food spawn RNG (ID, MASK)
-- 253: direction
-- 254: score
-- 255: food-ate

-- NOTES:
-- A CELL is an intended modification on the grid to light up a single cell, made up of two types: ID (8-bit data address), and MASK (4-bit address), both according to the table
-- ID points to the cell row, as well as the 4 possible columns it is assigned to (according to the table). MASK represents the bitmask to AND with the current value at that ID.
-- For example, if MEM[192] == 0b0011 (0th and 1st column lit up in row 1), and you want to modify the grid with ID=192 and MASK=0b1011, you are saying that you want to set MEM[192] = MEM[192] & MASK, which results in MEM[192] == 0b1011 (you have modified the grid to also light up the 4th column assigned to that ID.)

-- Additionally, in order to save space, the queue will only save the next direction to take (up, down, left, right) for the next cell
-- i.e. queue element is a 4-bit number that represents an implicit pointer to the next cell of the snake
-- Example: 0001 means from the snake tail address, we move up once, that is the next cell of the snake
-- Note it is guaranteed that no queue element will result in overflows/underflows, since an invalid address wouldve been caught in the snake update stage anyway
-- Lines with "--!" are padding for 16-bit instructions (split into two) for easier reading

-- RNG for food spawn is based on directions taken.


-- PSEUDOCODE:
------ function NEXT_CELL definition
    -- if input is up: decrease row
        -- ID -= 5
    -- if input is down: increase row
        -- ID += 5
    -- if input is left: decrease column
        -- rotate MASK, decrease ID if underflow
    -- if input is right: decrease column
        -- rotate MASK, increase ID if overflow
    -- returns RE = 1 if left/right input caused ID to change (for column-wise OOB detection)
------ branch GAME_LOOP
    -- get input
    -- modify snake-head
    -- branch GAME_LOOP_oob
        -- if OOB:
            -- branch to GAME_DEATH
    -- branch GAME_LOOP_food
        -- if not touching food address:
            -- if snake-head LED is already 1:
                -- branch to GAME_DEATH
            -- change snake-tail, update LED
            -- shift queue down
                -- start from queue-tail and shift downwards (store dir from last iteration to current pointer)
        -- else: -- branch GAME_LOOP_food_ate
            -- set food-ate to 1
            -- change length
            -- increase queue-tail address by 1
            -- increase score
    -- branch GAME_LOOP_enqueue
        -- enqueue new direction
            -- insert new dir at queue-tail
            -- update snake-head LED
    -- if food-ate is 1:
        -- spawn new food
------ branch GAME_DEATH (multiple of 16)
    -- shutdown (?)