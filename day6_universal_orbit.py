from typing import List, Tuple, Dict

def get_direct_orbits(orbits: List[str]) -> int:
    return len(set(orbits))

def get_indirect_orbits(orbits: List[str]) -> int:
    orbit_map = construct_orbit_map(orbits)
    total_indirect_orbits = 0
    for key, connections in orbit_map.items():
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




if __name__ == "__main__":
    # read data
    with open("data/input_day6.txt") as f:
        orbits = f.read().splitlines()

    test1 = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"]
    # print(get_indirect_orbits(test1))
    assert (get_direct_orbits(test1)+get_indirect_orbits(test1)) == 42

    total_relations = get_direct_orbits(orbits)+get_indirect_orbits(orbits)
    print("part 1 answer is: ", total_relations)