from typing import List
# opcode indicates what to do, opcode means something went wrong
# 99 means program is finished and should halt
# 1 adds numbers from 2 positions and store in 3rd position
# 2 multiplies the 2 inputs instead of adding
opcodes = [1, 2, 99]

# read data
with open('data/input_day2.txt') as f:
    intcode = f.read()
intcode = [int(i) for i in intcode.split(',')]

# print(data)
def opcode1_op(intcode: List[int], pos1: int, pos2: int) -> int:
    return intcode[pos1] + intcode[pos2]

def opcode2_op(intcode: List[int], pos1: int, pos2: int) -> int:
    return intcode[pos1] * intcode[pos2]

def run_intcode(intcode: List[int], opcodes: List[int] = opcodes) -> List[int]:
    intcode_copy = intcode.copy()
    position_ind = 0
    while position_ind < len(intcode_copy):
        opcode = intcode_copy[position_ind]
        assert (opcode in opcodes)

        if intcode_copy[position_ind] == 99:
            break
        else:
            pos1 = intcode_copy[position_ind + 1]
            pos2 = intcode_copy[position_ind + 2]
            pos3 = intcode_copy[position_ind + 3]    
            if intcode_copy[position_ind] == 1:
                intcode_copy[pos3] = opcode1_op(intcode_copy, pos1, pos2)
            elif intcode_copy[position_ind] == 2:
                intcode_copy[pos3] = opcode2_op(intcode_copy, pos1, pos2)
            position_ind += 4
    return intcode_copy

# unit test
data_1 = [1,9,10,3,2,3,11,0,99,30,40,50]
data_2 = [1,0,0,0,99]
data_3 = [2,3,0,3,99]
data_4 = [2,4,4,5,99,0]
data_5 = [1,1,1,4,99,5,6,0,99]


data_1_ans = [3500,9,10,70,2,3,11,0,99,30,40,50]
data_2_ans = [2,0,0,0,99]
data_3_ans = [2,3,0,6,99]
data_4_ans = [2,4,4,5,99,9801]
data_5_ans = [30,1,1,4,2,5,6,0,99]

assert run_intcode(data_1, opcodes) == data_1_ans
assert run_intcode(data_2, opcodes) == data_2_ans
assert run_intcode(data_3, opcodes) == data_3_ans
assert run_intcode(data_4, opcodes) == data_4_ans
assert run_intcode(data_5, opcodes) == data_5_ans
print('all tests passed!')

# precrash restoration
intcode_copy = intcode.copy()
intcode_copy[1] = 12
intcode_copy[2] = 2
print(run_intcode(intcode_copy, opcodes))


# part 2
print("-------------------part2 starts below: \n")

target = 19690720


def brute_force_search(intcode: List[int], opcodes: List[int], target: int) -> None:
    for i in range(100):
        for j in range(100):
            intcode_cpy = intcode.copy()
            intcode_cpy[1] = i
            intcode_cpy[2] = j
            output = run_intcode(intcode_cpy, opcodes)[0]
            if output == target:
                print("Found target!")
                print("The result input is: {} at position 1, {} at position 2.".format(i, j))
                print("The answer is {}".format(100 * i + j))
                break

brute_force_search(intcode, opcodes, target)
