from typing import List, Tuple, Optional, Iterable
from day5_sunny_asteroids import intcodeProgram
import itertools


class amplifierProgram:
    def __init__(self, intcode: List[int], amplifier_num: int = 5) -> None:
        self.intcode = intcode.copy()
        self.amplifier_num = amplifier_num
        self.amplifiers = [
            intcodeProgram(self.intcode, [0], False) for i in range(amplifier_num)
        ]

    @property
    def last_amplifier(self) -> intcodeProgram:
        return self.amplifiers[-1]

    @property
    def halt_flag(self) -> bool:
        if self.last_amplifier.instruction == 99:
            return True
        else:
            return False
        # return all([amplifier.instruction == 99 for amplifier in self.amplifiers])

    def phase_setting(self, input_sequence: Iterable[int]) -> None:
        for amplifier, input_i in zip(self.amplifiers, input_sequence):
            amplifier.execute_intcode(input_i)
        # print("Phase setting is finished!")

    def calculate_signal(self, input_sequence: Iterable[int]) -> int:
        self.phase_setting(input_sequence)

        amplifier_input = 0
        run_ind = 0
        while not self.halt_flag:
            ind = run_ind % self.amplifier_num
            amplifier_i = self.amplifiers[ind]
            input_i = input_sequence[ind]
            amplifier_i.execute_intcode(amplifier_input)
            amplifier_input = amplifier_i.output[-1]
            run_ind += 1
        last_output = amplifier_input
        return last_output


def get_max_thrust(intcode: List[int], phase_range: List[int]):
    max_thrust = 0
    # possible_phases = [p for p in itertools.product(phase_range, repeat=5)]
    possible_phases = list(itertools.permutations(phase_range))
    for phase in possible_phases:
        amp_program = amplifierProgram(intcode)
        thrust = amp_program.calculate_signal(phase)
        if thrust > max_thrust:
            max_thrust = thrust
    return max_thrust


if __name__ == "__main__":
    # read data
    with open("data/input_day7.txt") as f:
        intcode = f.read()
    intcode = [int(i) for i in intcode.split(",")]

    # Unit test 1
    test1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    test2 = [
        3,
        23,
        3,
        24,
        1002,
        24,
        10,
        24,
        1002,
        23,
        -1,
        23,
        101,
        5,
        23,
        23,
        1,
        24,
        23,
        23,
        4,
        23,
        99,
        0,
        0,
    ]
    test3 = [
        3,
        31,
        3,
        32,
        1002,
        32,
        10,
        32,
        1001,
        31,
        -2,
        31,
        1007,
        31,
        0,
        33,
        1002,
        33,
        7,
        33,
        1,
        33,
        31,
        31,
        1,
        32,
        31,
        31,
        4,
        31,
        99,
        0,
        0,
        0,
    ]

    # unit tests
    amp_program1 = amplifierProgram(test1)
    signal1 = amp_program1.calculate_signal([4, 3, 2, 1, 0])
    assert signal1 == 43210

    amp_program2 = amplifierProgram(test2)
    signal2 = amp_program2.calculate_signal([0, 1, 2, 3, 4])
    assert signal2 == 54321

    amp_program3 = amplifierProgram(test3)
    signal3 = amp_program3.calculate_signal([1, 0, 4, 3, 2])
    assert signal3 == 65210

    max_thrust = get_max_thrust(intcode, phase_range=[0, 1, 2, 3, 4])
    print("The max thrust is: {}".format(max_thrust))

    print("-------------------------------------part 2 start here:")

    test4 = [
        3,
        26,
        1001,
        26,
        -4,
        26,
        3,
        27,
        1002,
        27,
        2,
        27,
        1,
        27,
        26,
        27,
        4,
        27,
        1001,
        28,
        -1,
        28,
        1005,
        28,
        6,
        99,
        0,
        0,
        5,
    ]
    test5 = [
        3,
        52,
        1001,
        52,
        -5,
        52,
        3,
        53,
        1,
        52,
        56,
        54,
        1007,
        54,
        5,
        55,
        1005,
        55,
        26,
        1001,
        54,
        -5,
        54,
        1105,
        1,
        12,
        1,
        53,
        54,
        53,
        1008,
        54,
        0,
        55,
        1001,
        55,
        1,
        55,
        2,
        53,
        55,
        53,
        4,
        53,
        1001,
        56,
        -1,
        56,
        1005,
        56,
        6,
        99,
        0,
        0,
        0,
        0,
        10,
    ]

    # unit tests
    amp_program4 = amplifierProgram(test4)
    signal4 = amp_program4.calculate_signal([9, 8, 7, 6, 5])
    assert signal4 == 139629729

    amp_program5 = amplifierProgram(test5)
    signal5 = amp_program5.calculate_signal([9, 7, 8, 5, 6])
    assert signal5 == 18216

    max_thrust = get_max_thrust(intcode, phase_range=[5, 6, 7, 8, 9])
    print("The max thrust is: {}".format(max_thrust))
