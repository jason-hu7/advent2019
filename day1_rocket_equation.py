import math


def find_fuel(mass: int) -> int:
    return int(math.floor(mass / 3) - 2)


def fuel_accum(mass: int) -> int:
    fuel = find_fuel(mass)
    fuel_total = fuel
    while fuel >= 0:
        fuel_fuel = find_fuel(fuel)
        if fuel_fuel <= 0:
            break
        else:
            fuel_total += fuel_fuel
        fuel = fuel_fuel
    return fuel_total


if __name__ == "__main__":
    fuel_req = 0
    # read data
    with open("data/input_day1.txt") as f:
        masses = f.read().splitlines()
        for mass in masses:
            fuel_req += find_fuel(int(mass))

    print("Part 1 answer is: ", fuel_req)

    # Part 2
    print("----------------------------------------------part 2 starts here: ")

    # Unit tests
    assert fuel_accum(14) == 2
    assert fuel_accum(1969) == 966
    assert fuel_accum(100756) == 50346

    fuel_req = 0
    for mass in masses:
        fuel_req += fuel_accum(int(mass))
    print("Part 2 answer is: ", fuel_req)
