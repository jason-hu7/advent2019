from typing import Tuple
import itertools

def check_requirements(password: int, part2: bool = True) -> bool:
    password_str = str(password)
    # 1st requirement - 6 digits
    assert len(password_str) == 6

    twin_neighbor = False
    never_decrease = True

    # 2nd requirement - matching adjacent digits
    running_twins = [sum(1 for _ in l) for n, l in itertools.groupby(password_str)]
    if max(running_twins) >= 2 and not part2:
        twin_neighbor = True
    elif 2 in running_twins and part2:
        twin_neighbor = True

    # 3rd requirement - never decrease
    for i in range(1, len(password_str)):
        # if password_str[i] == password_str[i-1]:
        #     twin_neighbor = True
        if int(password_str[i]) < int(password_str[i-1]):
            never_decrease = False

    if twin_neighbor and never_decrease:
        return True
    else:
        return False


def find_password(password_range: Tuple[int, int], part2:bool = True) -> int:
    passwords = []
    for password in range(password_range[0], password_range[1]):
        if check_requirements(password, part2):
            passwords.append(password)
        else:
            pass
    return passwords


if __name__ == "__main__":
    password_range = (153517, 630395)
    test1 = 111111
    test2 = 223450
    test3 = 123789

    assert check_requirements(test1, part2=False)
    assert not check_requirements(test2, part2=False)
    assert not check_requirements(test3, part2=False)
    
    answer1 = find_password(password_range, part2=False)
    print(len(answer1))

    # part 2 starts here
    print("----------------------------------------part 2 starts here:")

    test1 = 112233
    test2 = 123444
    test3 = 111122

    assert check_requirements(test1, part2=True)
    assert not check_requirements(test2, part2=True)
    assert check_requirements(test3, part2=True)

    answer2 = find_password(password_range, part2=True)
    print(len(answer2))

