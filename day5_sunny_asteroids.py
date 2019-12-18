from typing import List, Tuple


# print(data)
def opcode1_op(
    intcode: List[int],
    param1: int,
    param2: int,
    param3: int,
    position_ind: int,
    mode: Tuple[int, int] = (0, 0)
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
    position_ind += 4
    return intcode, position_ind


def opcode2_op(
    intcode: List[int],
    param1: int,
    param2: int,
    param3: int,
    position_ind: int,
    mode: Tuple[int, int] = (0, 0),
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
    position_ind += 4
    return intcode, position_ind


def opcode3_op(intcode: List[int], param1: int, input_code: int, position_ind: int) -> List[int]:
    """opcode 3 takes a single integer input and stores at position pos1"""
    intcode[param1] = input_code
    position_ind += 2
    return intcode, position_ind


def opcode4_op(intcode: List[int], param1: int, position_ind: int, mode: int = 0) -> int:
    """opcode 4 outputs the value of param1 in the intcode"""
    if mode == 1:
        print(param1)
        position_ind += 2
        return intcode, position_ind
    elif mode == 0:
        print(intcode[param1])
        position_ind += 2
        return intcode, position_ind
    else:
        raise Exception("Not implemented")


def opcode5_op(
    intcode: List[int], param1: int, param2: int, position_ind: int, mode: Tuple[int, int] = (0, 0)
) -> int:
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
        position_ind += 3
    else:
        position_ind = param2_value
    return intcode, position_ind


def opcode6_op(
    intcode: List[int], param1: int, param2: int, position_ind:int, mode: Tuple[int, int] = (0, 0)
) -> int:
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
        position_ind = param2_value
    else:
        position_ind += 3
    return intcode, position_ind


def opcode7_op(
    intcode: List[int],
    param1: int,
    param2: int,
    param3: int,
    position_ind: int,
    mode: Tuple[int, int] = (0, 0),
) -> List[int]:
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
    position_ind += 4
    return intcode, position_ind


def opcode8_op(
    intcode: List[int],
    param1: int,
    param2: int,
    param3: int,
    position_ind: int,
    mode: Tuple[int, int] = (0, 0),
) -> List[int]:
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
    position_ind += 4
    return intcode, position_ind


def parameter_mode_op(
    intcode: List[int], instruction_code: int, param1: int, param2: int, param3: int, position_ind: int
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
            intcode, position_ind = opcode4_op(intcode, param1, position_ind, parameter1)
            return intcode, position_ind
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
        intcode, position_ind = opcode1_op(intcode, param1, param2, param3, position_ind, mode)
    elif op_code == 2:
        intcode, position_ind = opcode2_op(intcode, param1, param2, param3, position_ind, mode)
    elif op_code == 5:
        intcode, position_ind = opcode5_op(intcode, param1, param2, position_ind, mode)
        # print(ptr_increase)
    elif op_code == 6:
        intcode, position_ind = opcode6_op(intcode, param1, param2, position_ind, mode)
    elif op_code == 7:
        intcode, position_ind = opcode7_op(intcode, param1, param2, param3, position_ind, mode)
    elif op_code == 8:
        intcode, position_ind = opcode8_op(intcode, param1, param2, param3, position_ind, mode)
    else:
        raise Exception("Not implemented")
    return intcode, position_ind


def run_intcode(intcode: List[int], input_code: int, mode: int) -> List[int]:
    intcode_copy = intcode.copy()
    position_ind = 0
    mode = (mode, mode)
    while position_ind < len(intcode_copy):
        instruction_code = intcode_copy[position_ind]
        # print("instruction code: ", instruction_code)
        if instruction_code == 99:
            break
        else:
            pos1 = intcode_copy[position_ind + 1]
            # print(instruction_code)
            # opcode 1
            if instruction_code == 1:
                pos2 = intcode_copy[position_ind + 2]
                pos3 = intcode_copy[position_ind + 3]
                intcode_copy, position_ind = opcode1_op(intcode_copy, pos1, pos2, pos3, position_ind, mode)
            # opcode 2
            elif instruction_code == 2:
                pos2 = intcode_copy[position_ind + 2]
                pos3 = intcode_copy[position_ind + 3]
                intcode_copy, position_ind = opcode2_op(intcode_copy, pos1, pos2, pos3, position_ind, mode)
            # opcode 3
            elif instruction_code == 3:
                intcode_copy, position_ind = opcode3_op(intcode_copy, pos1, input_code, position_ind)
            # opcode 4
            elif instruction_code == 4:
                intcode_copy, position_ind = opcode4_op(intcode_copy, pos1, position_ind)
            # opcode 5
            elif instruction_code == 5:
                pos2 = intcode_copy[position_ind + 2]
                intcode_copy, position_ind = opcode5_op(intcode_copy, pos1, pos2, position_ind, mode)
            # opcode 6
            elif instruction_code == 6:
                pos2 = intcode_copy[position_ind + 2]
                intcode_copy, position_ind = opcode6_op(intcode_copy, pos1, pos2, position_ind, mode)
            # opcode 7
            elif instruction_code == 7:
                pos2 = intcode_copy[position_ind + 2]
                pos3 = intcode_copy[position_ind + 3]
                intcode_copy, position_ind = opcode7_op(intcode_copy, pos1, pos2, pos3, position_ind, mode)
            # opcode 8
            elif instruction_code == 8:
                pos2 = intcode_copy[position_ind + 2]
                pos3 = intcode_copy[position_ind + 3]
                intcode_copy, position_ind = opcode8_op(intcode_copy, pos1, pos2, pos3, position_ind, mode)
            # parameter mode
            elif len(str(instruction_code)) in (3, 4):
                # print(position_ind)
                pos2 = intcode_copy[position_ind + 2]
                pos3 = intcode_copy[position_ind + 3]
                intcode_copy, position_ind = parameter_mode_op(
                    intcode_copy, instruction_code, pos1, pos2, pos3, position_ind
                )
            else:
                raise Exception("Not implemented")
    return intcode_copy


if __name__ == "__main__":
    # read data
    with open("data/input_day5.txt") as f:
        intcode = f.read()
    intcode = [int(i) for i in intcode.split(",")]

    test1 = [1002, 4, 3, 4, 33]
    ans1, _ = parameter_mode_op(test1, test1[0], test1[1], test1[2], test1[3], 0)
    assert ans1[4] == 99

    # result_code = run_intcode(intcode, 1)

    print("-------------------------------------part 2 start here:")
    
    test2 = [
        3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
    ]
    test3 = [3,9,8,9,10,9,4,9,99,-1,8]
    test4 = [3,9,7,9,10,9,4,9,99,-1,8]

    test5 = [3,3,1108,-1,8,3,4,3,99]
    test6 = [3,3,1107,-1,8,3,4,3,99]
    
    test7 = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    test8 = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

    print("Test 2 given input smaller than 8, answer should be 999")
    run_intcode(test2, 5, 0)
    print("Test 2 given input larger than 8, answer should be 1001")
    run_intcode(test2, 10, 0)
    print("Test 2 given input is equal to 8, answer should be 1000")
    run_intcode(test2, 8, 0)
    print("Test 3 given not 8, answer should be 0")
    run_intcode(test3, 5, 0)
    print("Test 3 given 8, answer should be 1")
    run_intcode(test3, 8, 0)
    print("Test 4 given less than 8, answer should be 1")
    run_intcode(test4, 5, 0)
    print("Test 4 given higher than 8, answer should be 0")
    run_intcode(test4, 10, 0)


    print("Test 5 given not 8, answer should be 0")
    run_intcode(test5, 5, 1)
    print("Test 5 given 8, answer should be 1")
    run_intcode(test5, 8, 1)
    print("Test 6 given less than 8, answer should be 1")
    run_intcode(test6, 5, 1)
    print("Test 6 given higher than 8, answer should be 0")
    run_intcode(test6, 10, 1)

    print("Test 7 given 0, answer should be 0")
    run_intcode(test7, 0, 0)
    print("Test 7 given not 0, answer should be 1")
    run_intcode(test7, 8, 0)
    print("Test 8 given 0, answer should be 0")
    run_intcode(test8, 0, 1)
    print("Test 8 given not 0, answer should be 1")
    run_intcode(test8, 10, 1)

    print("final run on intcode")
    run_intcode(intcode, 5, 0)