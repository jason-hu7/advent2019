from typing import Tuple




def check_requirements(password: int) -> bool:
    password_str = str(password)
    # 1st requirement - 6 digits
    assert len(password_str) == 6

    twin_neighbor = False
    never_decrease = True

    for i in range(1, len(password_str)):
        if password_str[i] == password_str[i-1]:
            twin_neighbor = True
        if int(password_str[i]) < int(password_str[i-1]):
            never_decrease = False

    if twin_neighbor and never_decrease:
        return True
    else:
        return False


def find_password(password_range: Tuple[int, int]) -> int:
    passwords = []
    for password in range(password_range[0], password_range[1]):
        if check_requirements(password):
            passwords.append(password)
        else:
            pass
    return passwords


if __name__ == "__main__":
    password_range = (153517, 630395)
    test1 = 111111
    test2 = 223450
    test3 = 123789

    assert check_requirements(test1)
    assert not check_requirements(test2)
    assert not check_requirements(test3)
    
    answer1 = find_password(password_range)
    print(len(answer1))