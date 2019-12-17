from typing import List, Tuple


# print(data)
def opcode1_op(
    intcode: List[int], param1: int, param2: int, param3: int, mode: Tuple[int, int] = (0, 0)
) -> List[int]:
    """opcode 1 sums two integers at 2 position parameters"""
    if mode[0] == 1:
        param1_value = param1
    elif mode[0] == 0:
        param1_value = intcode[param1]
    else:
        raise Exception("Not implemented")
    
    if mode[1] == 1:
        param2_value = param2
    elif mode[1] == 0:
        param2_value = intcode[param2]
    else:
        raise Exception("Not implemented")
    intcode[param3] = param1_value + param2_value
    return intcode


def opcode2_op(
    intcode: List[int], param1: int, param2: int, param3: int, mode: Tuple[int, int] = (0, 0)
) -> List[int]:
    """opcode 2 multiplies two integers at 2 position parameters"""
    if mode[0] == 1:
        param1_value = param1
    elif mode[0] == 0:
        param1_value = intcode[param1]
    else:
        raise Exception("Not implemented")
    
    if mode[1] == 1:
        param2_value = param2
    elif mode[1] == 0:
        param2_value = intcode[param2]
    else:
        raise Exception("Not implemented")
    intcode[param3] = param1_value * param2_value
    return intcode


def opcode3_op(intcode: List[int], param1: int, input_code: int) -> List[int]:
    """opcode 3 takes a single integer input and stores at position pos1"""
    intcode[param1] = input_code
    return intcode


def opcode4_op(intcode: List[int], param1: int, mode: int = 0) -> int:
    """opcode 4 outputs the value of param1 in the intcode"""
    if mode == 1:
        return param1
    elif mode == 0:
        return intcode[param1]
    else:
        raise Exception("Not implemented")

def opcode5_op(intcode: List[int], param1: int, param2: int, mode: Tuple[int, int] = (1, 1)) -> int:
    """Jump if true"""
    if mode[0] == 1:
        param1_value = param1
    elif mode[0] == 0:
        param1_value = intcode[param1]
    else:
        raise Exception("Not implemented")
    
    if mode[1] == 1:
        param2_value = param2
    elif mode[1] == 0:
        param2_value = intcode[param2]
    else:
        raise Exception("Not implemented")

    if param1_value == 0:
        return 2
    else:
        return param2_value

def opcode6_op(intcode: List[int], param1: int, param2: int, mode: Tuple[int, int] = (1, 1)) -> int:
    """Jump if false"""
    if mode[0] == 1:
        param1_value = param1
    elif mode[0] == 0:
        param1_value = intcode[param1]
    else:
        raise Exception("Not implemented")

    if mode[1] == 1:
        param2_value = param2
    elif mode[1] == 0:
        param2_value = intcode[param2]
    else:
        raise Exception("Not implemented")

    if param1_value == 0:
        return param2_value
    else:
        return 2

def opcode7_op(intcode: List[int], param1: int, param2: int, param3: int, mode: Tuple[int, int] = (0, 0)) -> List[int]:
    """Less than"""
    if mode[0] == 1:
        param1_value = param1
    elif mode[0] == 0:
        param1_value = intcode[param1]
    else:
        raise Exception("Not implemented")

    if mode[1] == 1:
        param2_value = param2
    elif mode[1] == 0:
        param2_value = intcode[param2]
    else:
        raise Exception("Not implemented")

    if param1_value < param2_value:
        intcode[param3] = 1
    else:
        intcode[param3] = 0
    return intcode

def opcode8_op(intcode: List[int], param1: int, param2: int, param3: int, mode: Tuple[int, int] = (0, 0)) -> List[int]:
    """Equals"""
    if mode[0] == 1:
        param1_value = param1
    elif mode[0] == 0:
        param1_value = intcode[param1]
    else:
        raise Exception("Not implemented")

    if mode[1] == 1:
        param2_value = param2
    elif mode[1] == 0:
        param2_value = intcode[param2]
    else:
        raise Exception("Not implemented")

    if param1_value == param2_value:
        intcode[param3] = 1
    else:
        intcode[param3] = 0
    return intcode


def parameter_mode_op(
    intcode: List[int], instruction_code: int, param1: int, param2: int, param3: int
) -> List[int]:
    instruction_code_str = str(instruction_code)
    op_code = int(instruction_code_str[-2:])  # rightmost 2 digits
    parameters_reversed = instruction_code_str[:-2][::-1]
    parameter1 = int(parameters_reversed[0])  # hundreds digit
    if len(instruction_code_str) == 4:
        parameter2 = int(parameters_reversed[1])  # thousands digit
    elif len(instruction_code_str) == 3:
        if op_code == 3:
            raise Exception("This number does not look right.")
        elif op_code == 4:
            print(opcode4_op(intcode, param1, parameter1))
            return intcode
        else:
            parameter2 = 0
    else:
        raise Exception("Not implemented.")
    # print(instruction_code)
    assert parameter1 in (0, 1)
    assert parameter2 in (0, 1)

    mode = (parameter1, parameter2)
    # Logics for op code
    if op_code == 1:
        intcode = opcode1_op(intcode, param1, param2, param3, mode)
    elif op_code == 2:
        final_value = opcode2_op(intcode, param1, param2, param3, mode)
    else:
        raise Exception("Not implemented")
    return intcode


def run_intcode(intcode: List[int], input_code: int) -> List[int]:
    intcode_copy = intcode.copy()
    position_ind = 0
    while position_ind < len(intcode_copy):
        opcode = intcode_copy[position_ind]

        if intcode_copy[position_ind] == 99:
            break
        else:
            pos1 = intcode_copy[position_ind + 1]
            pos2 = intcode_copy[position_ind + 2]
            pos3 = intcode_copy[position_ind + 3]
            instruction_code = intcode_copy[position_ind]
            # print(instruction_code)
            # opcode 1
            if instruction_code == 1:
                intcode_copy = opcode1_op(intcode_copy, pos1, pos2, pos3)
                position_ind += 4
            # opcode 2
            elif instruction_code == 2:
                intcode_copy = opcode2_op(intcode_copy, pos1, pos2, pos3)
                position_ind += 4
            # opcode 3
            elif instruction_code == 3:
                intcode_copy = opcode3_op(intcode_copy, pos1, input_code)
                position_ind += 2
            # opcode 4
            elif instruction_code == 4:
                print(opcode4_op(intcode_copy, pos1))
                position_ind += 2
            # parameter mode
            elif len(str(instruction_code)) in (3, 4):
                # print(position_ind)
                intcode_copy = parameter_mode_op(
                    intcode_copy, instruction_code, pos1, pos2, pos3
                )
                if int(str(instruction_code)[-1]) == 4:
                    position_ind += 2
                else:
                    position_ind += 4
            else:
                # print(instruction_code)
                raise Exception("Not implemented")
    return intcode_copy


if __name__ == "__main__":
    # read data
    with open("data/input_day5.txt") as f:
        intcode = f.read()
    intcode = [int(i) for i in intcode.split(",")]

    test1 = [1002, 4, 3, 4, 33]
    ans1 = parameter_mode_op(test1, test1[0], test1[1], test1[2], test1[3])
    assert ans1[4] == 99

    result_code = run_intcode(intcode, 1)

    print("-------------------------------------part 2 start here:")
