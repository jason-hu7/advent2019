from day5_sunny_asteroids import intcodeProgram
from typing import List, Tuple

if __name__ == "__main__":
    # read data
    with open("data/input_day9.txt") as f:
        intcode = f.read()
    intcode = [int(i) for i in intcode.split(",")]

    # unit test
    test1= [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    test2 = [1102,34915192,34915192,7,4,7,99,0]
    test3 = [104,1125899906842624,99]

    # test1_intcode = intcodeProgram(test1, [0])
    # test1_intcode.execute_intcode(None)
    # assert test1_intcode.output == test1

    # test2_intcode = intcodeProgram(test2, [0])
    # test2_intcode.execute_intcode(None)
    # assert len(str(test2_intcode.output[0])) == 16

    # test3_intcode = intcodeProgram(test3, [0])
    # test3_intcode.execute_intcode(None)
    # assert test3_intcode.output[0] == test3[1]
    part1 = intcodeProgram(intcode, [0])
    part1.execute_intcode(1)