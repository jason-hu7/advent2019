from typing import List, Tuple, Dict
import re

origin = (0, 0)

def get_line_coords(wire: List[str]) -> Dict[str, List[Tuple[int]]]:
    start_coord = (0, 0)
    line_coords = {"horizontal": [], "vertical": []}

    for line in wire:
        direction = re.findall(r"[A-Z]", line)[0]
        dist = int(re.findall(r"\d+", line)[0])
        if direction == "R":
            end_coord = (start_coord[0] + dist, start_coord[1])
        elif direction == "L":
            end_coord = (start_coord[0] - dist, start_coord[1])
        elif direction == "U":
            end_coord = (start_coord[0], start_coord[1] + dist)
        elif direction == "D":
            end_coord = (start_coord[0], start_coord[1] - dist)
        else:
            print("The wire format you provided is shitty.")
        line_coord = start_coord + end_coord
        if direction == "R" or direction == "L":
            line_coords["horizontal"].append(line_coord)
        else:
            line_coords["vertical"].append(line_coord)
        start_coord = end_coord
    return line_coords


def find_intersections(wire1: List[str], wire2: List[str]) -> List[Tuple[int, int]]:
    wire1_line_coords = get_line_coords(wire1)
    wire2_line_coords = get_line_coords(wire2)
    # print(wire1_line_coords, "\n", wire2_line_coords)
    intersections = []
    # horizontal lines in wire1 and vertical lines in wire2
    for horizontal_line_1 in wire1_line_coords["horizontal"]:
        for vertical_line_2 in wire2_line_coords["vertical"]:
            x1_start, y1_start, x1_end, y1_end = horizontal_line_1
            x2_start, y2_start, x2_end, y2_end = vertical_line_2
            assert y1_start == y1_end
            assert x2_start == x2_end
            # vertical line x coords should be between horizontal line x coords
            if x2_start <= max(x1_start, x1_end) and x2_start >= min(x1_start, x1_end):
                # horizontal line y coords should be between vertical y coords
                if y1_start <= max(y2_start, y2_end) and y1_start >= min(y2_start, y2_end):
                    intersection = (x2_start, y1_start)
                    if intersection != (0, 0):
                        intersections.append(intersection)

    # horizontal lines in wire2 and vertical lines in wire1
    for horizontal_line_2 in wire2_line_coords["horizontal"]:
        for vertical_line_1 in wire1_line_coords["vertical"]:
            x2_start, y2_start, x2_end, y2_end = horizontal_line_2
            x1_start, y1_start, x1_end, y1_end = vertical_line_1
            assert y2_start == y2_end
            assert x1_start == x1_end
            if x1_start <= max(x2_start, x2_end) and x1_start >= min(x2_start, x2_end):
                if y2_start <= max(y1_start, y1_end) and y2_start >= min(y1_start, y1_end):
                    intersection = (x1_start, y2_start)
                    if intersection != (0, 0):
                        intersections.append(intersection)
    return intersections


def find_closest_intersection_distance(
    wire1: List[str], wire2: List[str]
) -> Tuple[Tuple[int, int], int]:
    intersections = find_intersections(wire1, wire2)
    shortest_dist = 8888888
    closest_intersection = (None, None)
    # If there is no intersection
    if len(intersections) == 0:
        return (closest_intersection, shortest_dist)

    for intersection in intersections:
        x, y = intersection
        dist = abs(x - origin[0]) + abs(y - origin[0])
        if dist < shortest_dist:
            shortest_dist = dist
            closest_intersection = intersection
    return (closest_intersection, shortest_dist)


def find_closest_intersection_steps(
    wire1: List[str], wire2: List[str]
) -> Tuple[Tuple[int, int], int]:
    intersections = find_intersections(wire1, wire2)
    shortest_steps = 8888888
    closest_intersection = (None, None)
    # If there is no intersection
    if len(intersections) == 0:
        return (closest_intersection, shortest_steps)

    # Calculate the steps to each intersection
    return (closest_intersection, shortest_dist)


if __name__ == "__main__":
    wire1 = ["R8", "U5", "L5", "D3"]
    wire2 = ["U7", "R6", "D4", "L4"]
    answer1_1 = 6
    answer1_2 = 30

    wire3 = ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"]
    wire4 = ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]
    answer2_1 = 159
    answer2_2 = 610

    wire5 = ["R98", "U47", "R26", "D63", "R33", "U87", "L62", "D20", "R33", "U53", "R51"]
    wire6 = ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"]
    answer3_1 = 135
    answer3_2 = 410

    assert find_closest_intersection_distance(wire1, wire2)[1] == answer1_1
    assert find_closest_intersection_distance(wire3, wire4)[1] == answer2_1
    assert find_closest_intersection_distance(wire5, wire6)[1] == answer3_1

    # read data
    with open('data/input_day3.txt') as f:
        wires = f.readlines()
    wire_1 = wires[0].strip('\n').split(',')
    wire_2 = wires[1].strip('\n').split(',')

    # print(type(wire_1))
    print("answer is: ", find_closest_intersection_distance(wire_1, wire_2))


    print("---------------------------------------part2 starts here")


