from typing import List, Tuple, Optional


def run_instruction(
    intcode: List[int], position_ind: int, input_code: int, modes: List[int] = [0]
) -> Tuple[List[int], int]:
    """opcode 1 sums two integers at 2 position parameters"""
    instruction = intcode[position_ind]

    # if length of instruction is 1 then individual mode
    if len(str(instruction)) == 1:
        intcode, position_ind = run_opcode(intcode, position_ind, modes, input_code)
    # if length of instruction is bigger than 1 then parameter mode
    else:
        intcode, position_ind = parameter_mode(intcode, position_ind)
    return intcode, position_ind


def get_parameters(
    intcode: List[int],
    position_ind: int,
    modes: List[int],
    opcode: int,
    parameter_mode: bool,
) -> List[int]:
    param1 = intcode[position_ind + 1]
    if opcode in (1, 2, 7, 8):
        param2 = intcode[position_ind + 2]
        param3 = intcode[position_ind + 3]
        params = [param1, param2, param3]
        if len(modes) == 1:
            modes = modes * 2
    elif opcode in (5, 6):
        param2 = intcode[position_ind + 2]
        params = [param1, param2]
        if len(modes) == 1:
            modes = modes * 2
    elif opcode == 3:
        params = [param1]
        return params
    elif opcode == 4:
        if not parameter_mode:
            return [intcode[param1]]
        else:
            params = [param1]
    else:
        raise Exception("Not implemented.")
    for i, mode in enumerate(modes):
        if mode == 0:
            params[i] = intcode[params[i]]
    return params


def run_opcode(
    intcode: List[int],
    position_ind: int,
    modes: List[int],
    input_code: Optional[int] = None,
    parameter_mode: bool = False,
) -> Tuple[List[int], int]:
    opcode = intcode[position_ind]
    if len(str(opcode)) > 1:
        opcode = int(str(opcode)[-1])
    params = get_parameters(intcode, position_ind, modes, opcode, parameter_mode)
    if opcode == 1:
        intcode = opcode1_op(intcode, params)
        position_ind += 4
    elif opcode == 2:
        intcode = opcode2_op(intcode, params)
        position_ind += 4
    elif opcode == 3:
        if input_code == None:
            raise Exception("you need to provide an input code")
        intcode = opcode3_op(intcode, params, input_code)
        position_ind += 2
    elif opcode == 4:
        intcode = opcode4_op(intcode, params)
        position_ind += 2
    elif opcode == 5:
        position_ind = opcode5_op(intcode, params, position_ind)
    elif opcode == 6:
        position_ind = opcode6_op(intcode, params, position_ind)
    elif opcode == 7:
        intcode = opcode7_op(intcode, params, position_ind)
        position_ind += 4
    elif opcode == 8:
        intcode = opcode8_op(intcode, params, position_ind)
        position_ind += 4
    else:
        raise Exception("Not implemented.")
    return intcode, position_ind


def opcode1_op(intcode: List[int], params: List[int],) -> List[int]:
    """opcode 1 sums two integers at 2 position parameters"""
    param1, param2, param3 = params
    intcode[param3] = param1 + param2
    return intcode


def opcode2_op(intcode: List[int], params: List[int],) -> List[int]:
    """opcode 2 multiplies two integers at 2 position parameters"""
    param1, param2, param3 = params
    intcode[param3] = param1 * param2
    return intcode


def opcode3_op(
    intcode: List[int], params: List[int], input_code: Optional[int]
) -> List[int]:
    """opcode 3 takes a single integer input and stores at position pos1"""
    if input_code == None:
        raise Exception("No input provided.")
    param1 = params[0]
    intcode[param1] = input_code
    return intcode


def opcode4_op(intcode: List[int], params: List[int]) -> int:
    """opcode 4 outputs the value of param1 in the intcode"""
    param1 = params[0]
    print(param1)
    return intcode


def opcode5_op(intcode: List[int], params: List[int], position_ind: int) -> int:
    """Jump if true"""
    param1, param2 = params
    if param1 == 0:
        position_ind += 3
    else:
        position_ind = param2
    return position_ind


def opcode6_op(intcode: List[int], params: List[int], position_ind: int) -> int:
    """Jump if false"""
    param1, param2 = params
    if param1 == 0:
        position_ind = param2
    else:
        position_ind += 3
    return position_ind


def opcode7_op(intcode: List[int], params: List[int], position_ind: int,) -> List[int]:
    """Less than"""
    param1, param2, param3 = params
    if param1 < param2:
        intcode[param3] = 1
    else:
        intcode[param3] = 0
    return intcode


def opcode8_op(intcode: List[int], params: List[int], position_ind: int,) -> List[int]:
    """Equals"""
    param1, param2, param3 = params
    if param1 == param2:
        intcode[param3] = 1
    else:
        intcode[param3] = 0
    return intcode


def parameter_mode(intcode: List[int], position_ind: int) -> List[int]:
    instruction_code = intcode[position_ind]
    instruction_code_str = str(instruction_code)
    op_code = int(instruction_code_str[-2:])  # rightmost 2 digits
    parameters_reversed = instruction_code_str[:-2][::-1]
    param1_mode = int(parameters_reversed[0])  # hundreds digit
    if len(instruction_code_str) == 4:
        param2_mode = int(parameters_reversed[1])  # thousands digit
    elif len(instruction_code_str) == 3:
        if op_code == 3:
            raise Exception("This number does not look right.")
        elif op_code == 4:
            intcode, position_ind = run_opcode(
                intcode, position_ind, [param1_mode], parameter_mode=True
            )
            return intcode, position_ind
        else:
            param2_mode = 0
    else:
        raise Exception("Not implemented.")
    assert param1_mode in (0, 1)
    assert param2_mode in (0, 1)

    modes = (param1_mode, param2_mode)
    intcode, position_ind = run_opcode(
        intcode, position_ind, modes, parameter_mode=True
    )
    return intcode, position_ind


def execute_intcode(intcode: List[int], input_code: int, modes: List[int]) -> List[int]:
    intcode_copy = intcode.copy()
    position_ind = 0
    while position_ind < len(intcode_copy):
        instruction_code = intcode_copy[position_ind]
        # print("instruction code: ", instruction_code)
        if instruction_code == 99:
            break
        elif instruction_code == 3:
            instruction_code, position_ind = run_instruction(
                intcode_copy, position_ind, input_code, modes
            )
        else:
            intcode_copy, position_ind = run_instruction(
                intcode_copy, position_ind, None, modes
            )
    return intcode_copy


if __name__ == "__main__":
    # read data
    with open("data/input_day7.txt") as f:
        intcode = f.read()
    intcode = [int(i) for i in intcode.split(",")]

    test1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    test2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    test3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    ans1 = 43210
    ans2 = 54321
    ans3 = 65210

    intcode_copy = execute_intcode(test1, 4, [0])
    print(intcode_copy)

