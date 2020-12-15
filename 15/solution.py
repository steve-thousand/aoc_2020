import sys


def get_nth_number(starting_numbers, n):
    numbers_seen = {}
    turn = 0
    last_number = None
    while turn < n:
        sys.stdout.write('\r%d' % turn)
        sys.stdout.flush()
        if turn < len(starting_numbers):
            if last_number is not None:
                numbers_seen[last_number] = turn
            last_number = starting_numbers[turn]
        else:
            if last_number not in numbers_seen:
                numbers_seen[last_number] = turn
                last_number = 0
            else:
                last_turn = numbers_seen[last_number]
                numbers_seen[last_number] = turn
                last_number = turn - last_turn
        turn += 1
    sys.stdout.write('\n')
    sys.stdout.flush()
    return last_number


def solve(puzzle_input):
    starting_numbers = [int(x) for x in puzzle_input.strip().split(",")]

    # part 1
    print(get_nth_number(starting_numbers, 2020))

    # part 2, takes about a minute, whatever
    print(get_nth_number(starting_numbers, 30000000))

    return


solve("""
1,12,0,20,8,16
""")
