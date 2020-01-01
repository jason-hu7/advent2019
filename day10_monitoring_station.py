import numpy as np
from typing import List, Dict, Tuple
from itertools import permutations


def load_tests(input_file: str = "data/test_day10.txt") -> Dict:
    tests = {}
    with open(input_file) as f:
        # files = f.read()
        # print(files.split('\n'))
        for line in f:
            if "test" in line:
                key = line.strip("\n")
                tests[key] = []
            else:
                tests[key].append(list(line.strip("\n")))
    for key, item in tests.items():
        tests[key] = np.array(item)
    return tests


def find_asteroids(space_map: np.ndarray) -> List[Tuple[int, int]]:
    asteroid_coords = []
    for y in range(space_map.shape[0]):
        for x in range(space_map.shape[1]):
            if space_map[y][x] == "#":
                asteroid_coords.append((y, x))
    return asteroid_coords


def get_direct_connections(
    asteroid_coords: List[Tuple[int, int]]
) -> Dict[Tuple[int, int], int]:
    direct_connections = {}
    asteroid_pairs = list(permutations(asteroid_coords, 2))
    for asteroid_pair in asteroid_pairs:
        asteroid1, asteroid2 = asteroid_pair
        if examine_line(asteroid1, asteroid2, asteroid_coords):
            if asteroid1 in direct_connections.keys():
                direct_connections[asteroid1] += 1
            else:
                direct_connections[asteroid1] = 1
    return direct_connections


def examine_line(
    asteroid1: Tuple[int, int],
    asteroid2: Tuple[int, int],
    asteroid_coords: List[Tuple[int, int]],
) -> bool:
    asteroids_list = asteroid_coords.copy()
    asteroids_list.remove(asteroid1)
    asteroids_list.remove(asteroid2)
    y1, x1 = asteroid1
    y2, x2 = asteroid2
    
def distance(
    asteroid1: Tuple[int, int],
    asteroid2: Tuple[int, int]
) -> int:
    y1, x1 = asteroid1
    y2, x2 = asteroid2
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_between(
    asteroid1: Tuple[int, int],
    asteroid2: Tuple[int, int],
    asteroid3: Tuple[int, int],
) -> bool:
    return distance(asteroid1, asteroid3) + distance(asteroid3, asteroid2) == distance(asteroid1, asteroid2) 



if __name__ == "__main__":
    # read data
    space_map = np.array(
        [list(line.rstrip("\n")) for line in open("data/input_day10.txt")]
    )

    tests = load_tests()
    print(tests)
