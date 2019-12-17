from typing import List

# read data
with open("data/input_day2.txt") as f:
    intcode = f.read()
intcode = [int(i) for i in intcode.split(",")]

# print(data)
def opcode1_op(intcode: List[int], pos1: int, pos2: int) -> int:
    return intcode[pos1] + intcode[pos2]


def opcode2_op(intcode: List[int], pos1: int, pos2: int) -> int:
    return intcode[pos1] * intcode[pos2]


def opcode3_op(intcode: List[int], pos1: int, input_code: int) -> List[int]:
    intcode[pos1] = input_code
    return intcode


def opcode4_op(intcode: List[int], pos1: int) -> int:
    return intcode[pos1]


def parameter_mode_op(intcode: List[int], instruction_code: int, pos1:int, pos2:int, pos3: int) -> int:
    instruction_code_str = str(instruction_code)
    op_code = int(instruction_code_str[-2:])
    parameters_reversed = instruction_code_str[:-2][::-1]
    parameter1 = int(parameters_reversed[0])
    parameter2 = int(parameters_reversed[1])
    # parameter3 = 0
    assert parameter1 in (0, 1)
    assert parameter2 in (0, 1)
    # if len(parameters_reversed) == 3:
    #     parameter3 = 1
    
    if parameter1 == 0:
        variable1 = intcode[pos1]
    elif parameter1 == 1:
        variable1 = pos1

    if parameter2 == 0:
        variable2 = intcode[pos2]
    elif parameter2 == 1:
        variable2 = pos2
    
    if op_code == 1:
        return variable1 + variable2
    elif op_code == 2:
        return variable1 * variable2




def run_intcode(intcode: List[int], opcodes: List[int] = opcodes) -> List[int]:
    intcode_copy = intcode.copy()
    position_ind = 0
    while position_ind < len(intcode_copy):
        opcode = intcode_copy[position_ind]
        assert opcode in opcodes

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