from typing import List, Tuple, Dict


def get_direct_orbits(orbits: List[str]) -> int:
    return len(set(orbits))


def get_indirect_orbits(orbits: List[str]) -> int:
    orbit_map = construct_orbit_map(orbits)
    # print(orbit_map)
    total_indirect_orbits = 0
    for _, connections in orbit_map.items():
        total_indirect_orbits += len(connections) - 1  # minus 1 because ignore direct
    return total_indirect_orbits


def construct_orbit_map(orbits: List[str]) -> Dict[str, List[str]]:
    orbiters = []
    orbitees = []
    for orbit in orbits:
        orbitee, orbiter = orbit.split(")")
        orbiters.append(orbiter)
        orbitees.append(orbitee)

    orbit_map = {}
    for i, orbiter in enumerate(orbiters):
        if orbiter in orbit_map:
            print("something might be wrong")
        else:
            orbitee = orbitees[i]
            orbit_map[orbiter] = [orbitee]
            new_orbitee = orbitee
            while new_orbitee in orbiters:
                new_orbiter = new_orbitee
                orbiter_index = orbiters.index(new_orbiter)
                new_orbitee = orbitees[orbiter_index]
                orbit_map[orbiter].append(new_orbitee)
    return orbit_map


def get_min_orbital_transfers(orbits: List[str]) -> int:
    orbit_map = construct_orbit_map(orbits)
    min_steps = 0
    you_path = orbit_map["YOU"]
    san_path = orbit_map["SAN"]
    # print(you_path, san_path)
    for i in you_path:
        j_to_common = 0
        for j in san_path:
            if i == j:
                # found the common connector
                return min_steps + j_to_common
            else:
                j_to_common += 1
        # if didn't find common connector step + 1 for YOU
        min_steps += 1
    return None

if __name__ == "__main__":
    # read data
    with open("data/input_day6.txt") as f:
        orbits = f.read().splitlines()

    test1 = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ]
    # print(get_indirect_orbits(test1))
    assert (get_direct_orbits(test1) + get_indirect_orbits(test1)) == 42

    total_relations = get_direct_orbits(orbits) + get_indirect_orbits(orbits)
    print("part 1 answer is: ", total_relations)

    print("-----------------------------------------------part 2 starts here.")
    test2 = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "K)YOU",
        "I)SAN",
    ]

    # print(get_min_orbital_transfers(test2))
    assert (get_min_orbital_transfers(test2) == 4)

    print("part 2 answer is: ", get_min_orbital_transfers(orbits))