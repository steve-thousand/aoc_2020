class Node:

    def __init__(self, value):
        self.value = value
        self.next = None
        return

    def set_next(self, next):
        self.next = next


class Circle:

    def __init__(self, numbers, part_2=False):
        self.numbers = numbers

        self.node_by_number = {}

        start = Node(numbers[0])
        self.node_by_number[numbers[0]] = start
        self.max = numbers[0]
        current = start
        for number in numbers[1:]:
            next = Node(number)
            self.node_by_number[number] = next
            current.set_next(next)
            current = next
            if number > self.max:
                self.max = number
        current.set_next(start)

        if part_2 == True:
            for number in range(self.max + 1, 1_000_000 + 1):
                next = Node(number)
                self.node_by_number[number] = next
                current.set_next(next)
                current = next
                if number > self.max:
                    self.max = number
        current.set_next(start)

        self.current = start
        return

    def __get_current(self):
        return self.current

    def __remove_pick_up(self, current):
        pick_up = current.next
        current.set_next(pick_up.next.next.next)
        return pick_up

    def __identify_destination(self, current, pick_up):
        pick_up_values = set()
        start = pick_up
        for i in range(0, 3):
            pick_up_values.add(start.value)
            start = start.next

        destination_value = current.value
        while True:
            destination_value -= 1
            if destination_value < 0:
                destination_value = self.max
            if destination_value not in pick_up_values and destination_value in self.node_by_number:
                return self.node_by_number[destination_value]

    def __insert_following(self, destination, to_insert):
        to_insert.next.next.set_next(destination.next)
        destination.next = to_insert
        return

    def __iterate_current(self):
        self.current = self.current.next
        return

    def move(self):
        current = self.__get_current()

        # get three following current
        pick_up = self.__remove_pick_up(current)

        # find destination
        destination = self.__identify_destination(current, pick_up)

        # insert three after destination
        self.__insert_following(destination, pick_up)

        # iterate current
        self.__iterate_current()
        return

    def print(self):
        start = self.node_by_number[1]
        values = []
        for i in range(0, 8):
            start = start.next
            values.append(start.value)
        print(''.join([str(x) for x in values]))

    @ staticmethod
    def parse(puzzle_input, part_2=False):
        return Circle([int(x) for x in puzzle_input.strip()], part_2)


def solve(puzzle_input):
    # part 1
    circle = Circle.parse(puzzle_input)
    for i in range(0, 100):
        circle.move()
    circle.print()

    # part 2
    circle = Circle.parse(puzzle_input, True)
    for i in range(0, 10_000_000):
        circle.move()
    print(circle.node_by_number[1].next.value *
          circle.node_by_number[1].next.next.value)
    return


solve("""
215694783
""")
