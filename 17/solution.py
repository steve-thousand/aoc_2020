from sys import maxsize
minsize = -maxsize - 1


def get_neighbor_cubes(state, dimensions):
    possible_spaces = [
        [dimensions[0] - 1],
        [dimensions[0] - 0],
        [dimensions[0] + 1]
    ]
    for value in dimensions[1:]:
        new_possible_spaces = []
        for possible_space in possible_spaces:
            new_possible_space = possible_space.copy()
            new_possible_space.append(value - 1)
            new_possible_spaces.append(new_possible_space)
            new_possible_space = possible_space.copy()
            new_possible_space.append(value - 0)
            new_possible_spaces.append(new_possible_space)
            new_possible_space = possible_space.copy()
            new_possible_space.append(value + 1)
            new_possible_spaces.append(new_possible_space)
        possible_spaces = new_possible_spaces

    number_neighboring_active = 0
    for possible_space in possible_spaces:
        if possible_space == dimensions:
            continue
        number_neighboring_active += 1 if state.is_active(
            possible_space) else 0

    return number_neighboring_active


class State:
    def __init__(self, dimensions=3):
        self.map = {}
        self.dimensions = dimensions
        self.mins = [(maxsize, minsize)] * dimensions

    @staticmethod
    def from_input(puzzle_input, dimensions=3):
        space = [[[y for y in x] for x in puzzle_input.strip().split("\n")]]
        origin_z = len(space) - (len(space) // 2 + 1)
        origin_y = len(space[0]) - (len(space[0]) // 2 + 1)
        origin_x = len(space[0][0]) - (len(space[0][0]) // 2 + 1)
        state = State(dimensions)
        for z in range(0, len(space)):
            for y in range(0, len(space[z])):
                for x in range(0, len(space[z][y])):
                    if space[z][y][x] == "#":
                        values = [
                            z - origin_z,
                            y - origin_y,
                            x - origin_x
                        ]
                        if dimensions == 4:
                            values.append(0)
                        state.push_active_cube(values)
        return state

    def push_active_cube(self, dimensions):
        current_map = self.map
        for dimension, value in enumerate(dimensions):
            if value not in current_map:
                current_map[value] = {}
            current_map = current_map[value]
            if value < self.mins[dimension][0]:
                self.mins[dimension] = (value, self.mins[dimension][1])
            if value > self.mins[dimension][1]:
                self.mins[dimension] = (self.mins[dimension][0], value)

    def is_active(self, dimensions):
        current_map = self.map
        for value in dimensions:
            if value in current_map:
                current_map = current_map[value]
            else:
                return False
        return True

    def cycle(self):
        next_state = State(self.dimensions)

        cells_to_check = [[]]

        for dimension in range(0, self.dimensions):
            new_cells_to_check = []
            for i in range(self.mins[dimension][0] - 1, self.mins[dimension][1] + 2):
                for cell_to_check in cells_to_check:
                    new_cell_to_check = cell_to_check.copy()
                    new_cell_to_check.append(i)
                    new_cells_to_check.append(new_cell_to_check)
            cells_to_check = new_cells_to_check

        for cell_to_check in cells_to_check:
            active = self.is_active(cell_to_check)
            neighbor_cubes = get_neighbor_cubes(self, cell_to_check)
            if active and (neighbor_cubes == 2 or neighbor_cubes == 3):
                # make inactive (skip)
                next_state.push_active_cube(cell_to_check)
            elif not active and neighbor_cubes == 3:
                # make active
                next_state.push_active_cube(cell_to_check)

        return next_state

    def count_active(self):
        active = 0
        maps = [self.map]
        for i in range(0, self.dimensions - 1):
            new_maps = []
            for map_to_crawl in maps:
                new_maps.extend(list(map_to_crawl.values()))
            maps = new_maps

        for map_to_crawl in maps:
            active += len(map_to_crawl)

        return active


def solve(puzzle_input):

    state = State.from_input(puzzle_input)
    cycles = 6
    for i in range(0, cycles):
        state = state.cycle()

    # part 1
    print(state.count_active())

    state = State.from_input(puzzle_input, 4)
    cycles = 6
    for i in range(0, cycles):
        state = state.cycle()

    # part 2
    print(state.count_active())

    return


solve("""
#.#.#.##
.####..#
#####.#.
#####..#
#....###
###...##
...#.#.#
#.##..##
""")
