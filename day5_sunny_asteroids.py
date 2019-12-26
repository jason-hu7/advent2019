from typing import List, Tuple, Optional


class intcodeProgram:
    def __init__(self, intcode: List[int], modes: List[int], verbose: bool = True) -> None:
        self.intcode = intcode.copy()
        self.modes = modes
        self.position_ind: int = 0
        self.output: List[Optional[int]] = []
        self.phase_set_flag: bool = False
        self.verbose = verbose
        self.not_enough_input: bool = False
        self.input_used: bool = False

    @property
    def instruction(self) -> int:
        return self.intcode[self.position_ind]

    @property
    def parameter_mode_flag(self) -> bool:
        if len(str(self.instruction)) == 1:
            return False
        else:
            return True

    def execute_intcode(self, input_code: int) -> List[int]:
        while self.position_ind < len(self.intcode):
            # print("instruction code: ", self.instruction)
            if self.instruction == 99:
                break
            elif self.not_enough_input:
                # reset the flag
                self.not_enough_input = False
                self.input_used = False
                break
            else:
                self.run_instruction(input_code)

    def run_instruction(self, input_code: int) -> None:
        """opcode 1 sums two integers at 2 position parameters"""
        if self.parameter_mode_flag:
            self.run_parameter_mode(self.instruction)
        else:
            self.run_opcode(self.instruction, input_code, self.modes.copy())

    def run_parameter_mode(self, opcode: int) -> List[int]:
        instruction_code_str = str(self.instruction)
        opcode = int(instruction_code_str[-2:])  # rightmost 2 digits
        parameters_reversed = instruction_code_str[:-2][::-1]
        param1_mode = int(parameters_reversed[0])  # hundreds digit
        if len(instruction_code_str) == 4:
            param2_mode = int(parameters_reversed[1])  # thousands digit
        elif len(instruction_code_str) == 3:
            if opcode == 3:
                raise Exception("This number does not look right.")
            elif opcode == 4:
                self.run_opcode(opcode, input_code=None, modes=[param1_mode])
                return
            else:
                param2_mode = 0
        else:
            raise Exception("Not implemented.")
        assert param1_mode in (0, 1)
        assert param2_mode in (0, 1)

        modes = [param1_mode, param2_mode]
        self.run_opcode(opcode, input_code=None, modes=modes)

    def run_opcode(
        self, opcode: int, input_code: int, modes: List[int]
    ) -> None:
        if len(str(opcode)) > 1:
            opcode = int(str(opcode)[-1])
        params = self.get_parameters(opcode, modes)
        if opcode == 1:
            self.opcode1_op(params)
            self.position_ind = self.position_ind + 4
        elif opcode == 2:
            self.opcode2_op(params)
            self.position_ind = self.position_ind + 4
        elif opcode == 3:
            if input_code is None:
                raise Exception("you need to provide an input code")
            if self.input_used:
                self.not_enough_input = True
            else:
                self.opcode3_op(params, input_code)
                self.input_used = True
                self.position_ind = self.position_ind + 2
        elif opcode == 4:
            self.opcode4_op(params)
            self.position_ind = self.position_ind + 2
        elif opcode == 5:
            self.opcode5_op(params)
        elif opcode == 6:
            self.opcode6_op(params)
        elif opcode == 7:
            self.opcode7_op(params)
            self.position_ind = self.position_ind + 4
        elif opcode == 8:
            self.opcode8_op(params)
            self.position_ind = self.position_ind + 4
        else:
            raise Exception("Not implemented.")

    def get_parameters(self, opcode: int, modes: List[int]) -> List[int]:
        param1 = self.intcode[self.position_ind + 1]
        # opcode 1, 2, 7, 8 requires 3 parameters
        if opcode in (1, 2, 7, 8):
            param2 = self.intcode[self.position_ind + 2]
            param3 = self.intcode[self.position_ind + 3]
            params = [param1, param2, param3]
            # if length of modes is 1 then same parameter mode for all inputs
            if len(modes) == 1:
                modes = modes * 2
        # opcode 5, 6 requires 2 parameters as inputs
        elif opcode in (5, 6):
            param2 = self.intcode[self.position_ind + 2]
            params = [param1, param2]
            if len(modes) == 1:
                modes = modes * 2
        # opcode 3, 4 reuires 1 parameter
        elif opcode == 3:
            params = [param1]
            return params
        elif opcode == 4:
            if self.parameter_mode_flag:
                params = [param1]
            else:
                return [self.intcode[param1]]
        else:
            raise Exception("Not implemented.")
        # print(params, modes)
        for i, mode in enumerate(modes):
            if mode == 0:
                params[i] = self.intcode[params[i]]
        return params

    def opcode1_op(self, params: List[int]) -> None:
        """opcode 1 sums two integers at 2 position parameters"""
        param1, param2, param3 = params
        self.intcode[param3] = param1 + param2

    def opcode2_op(self, params: List[int]) -> None:
        """opcode 2 multiplies two integers at 2 position parameters"""
        param1, param2, param3 = params
        self.intcode[param3] = param1 * param2

    def opcode3_op(self, params: List[int], input_code: Optional[int]) -> None:
        """opcode 3 takes a single integer input and stores at position pos1"""
        if input_code == None:
            raise Exception("No input provided.")
        param1 = params[0]
        if self.verbose:
            print("Provide input {}".format(input_code))
        self.intcode[param1] = input_code
        # # If this is the first input then set phase setting to being finished
        # if not self.phase_set_flag:
        #     self.phase_set_flag = True

    def opcode4_op(self, params: List[int]) -> None:
        """opcode 4 outputs the value of param1 in the intcode"""
        param1 = params[0]
        self.output = self.output + [param1]
        if self.verbose:
            print("output from opcode 4 instruction: ", param1)

    def opcode5_op(self, params: List[int]) -> None:
        """Jump if true"""
        param1, param2 = params
        if param1 == 0:
            self.position_ind = self.position_ind + 3
        else:
            self.position_ind = param2

    def opcode6_op(self, params: List[int]) -> None:
        """Jump if false"""
        param1, param2 = params
        if param1 == 0:
            self.position_ind = param2
        else:
            self.position_ind = self.position_ind + 3

    def opcode7_op(self, params: List[int]) -> None:
        """Less than"""
        param1, param2, param3 = params
        if param1 < param2:
            self.intcode[param3] = 1
        else:
            self.intcode[param3] = 0

    def opcode8_op(self, params: List[int]) -> None:
        """Equals"""
        param1, param2, param3 = params
        if param1 == param2:
            self.intcode[param3] = 1
        else:
            self.intcode[param3] = 0


if __name__ == "__main__":
    # read data
    with open("data/input_day5.txt") as f:
        intcode = f.read()
    intcode = [int(i) for i in intcode.split(",")]

    # Unit test 1
    test1 = [1002, 4, 3, 4, 33]
    test1_intcode = intcodeProgram(test1, [0])
    test1_intcode.run_parameter_mode(1002)
    assert test1_intcode.intcode[4] == 99

    part1_intcode = intcodeProgram(intcode, [0])
    part1_intcode.execute_intcode(1)

    print("-------------------------------------part 2 start here:")

    test2 = [
        3,
        21,
        1008,
        21,
        8,
        20,
        1005,
        20,
        22,
        107,
        8,
        21,
        20,
        1006,
        20,
        31,
        1106,
        0,
        36,
        98,
        0,
        0,
        1002,
        21,
        125,
        20,
        4,
        20,
        1105,
        1,
        46,
        104,
        999,
        1105,
        1,
        46,
        1101,
        1000,
        1,
        20,
        4,
        20,
        1105,
        1,
        46,
        98,
        99,
    ]
    test3 = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    test4 = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]

    test5 = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    test6 = [3, 3, 1107, -1, 8, 3, 4, 3, 99]

    test7 = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    test8 = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]

    print("Test 2 given input smaller than 8, answer should be 999")
    test2_intcode = intcodeProgram(test2, [0])
    test2_intcode.execute_intcode(5)
    print("Test 2 given input larger than 8, answer should be 1001")
    test2_intcode = intcodeProgram(test2, [0])
    test2_intcode.execute_intcode(10)
    print("Test 2 given input is equal to 8, answer should be 1000")
    test2_intcode = intcodeProgram(test2, [0])
    test2_intcode.execute_intcode(8)
    print("Test 3 given not 8, answer should be 0")
    test3_intcode = intcodeProgram(test3, [0])
    test3_intcode.execute_intcode(5)
    print("Test 3 given 8, answer should be 1")
    test3_intcode = intcodeProgram(test3, [0])
    test3_intcode.execute_intcode(8)
    print("Test 4 given less than 8, answer should be 1")
    test4_intcode = intcodeProgram(test4, [0])
    test4_intcode.execute_intcode(5)
    print("Test 4 given higher than 8, answer should be 0")
    test4_intcode = intcodeProgram(test4, [0])
    test4_intcode.execute_intcode(10)

    print("Test 5 given not 8, answer should be 0")
    test5_intcode = intcodeProgram(test5, [1])
    test5_intcode.execute_intcode(5)
    print("Test 5 given 8, answer should be 1")
    test5_intcode = intcodeProgram(test5, [1])
    test5_intcode.execute_intcode(8)
    print("Test 6 given less than 8, answer should be 1")
    test6_intcode = intcodeProgram(test6, [1])
    test6_intcode.execute_intcode(5)
    print("Test 6 given higher than 8, answer should be 0")
    test6_intcode = intcodeProgram(test6, [1])
    test6_intcode.execute_intcode(10)

    print("Test 7 given 0, answer should be 0")
    test7_intcode = intcodeProgram(test7, [0])
    test7_intcode.execute_intcode(0)
    print("Test 7 given not 0, answer should be 1")
    test7_intcode = intcodeProgram(test7, [0])
    test7_intcode.execute_intcode(8)
    print("Test 8 given 0, answer should be 0")
    test8_intcode = intcodeProgram(test8, [1])
    test8_intcode.execute_intcode(0)
    print("Test 8 given not 0, answer should be 1")
    test8_intcode = intcodeProgram(test8, [1])
    test8_intcode.execute_intcode(10)

    print("final run on intcode")
    part2_intcode = intcodeProgram(intcode, [0])
    part2_intcode.execute_intcode(5)
