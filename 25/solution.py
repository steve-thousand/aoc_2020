DATE_I_THINK = 20201227


def calculate_key(subject_number, loop_size):
    value = 1
    for i in range(0, loop_size):
        value *= subject_number
        value %= 20201227
    return value


def calculate_loop_size(key):
    value = 1
    subject_number = 7
    loop_size = 1
    while True:
        value *= subject_number
        value %= 20201227
        if value == key:
            return loop_size
        loop_size += 1


def solve(puzzle_input):
    public_keys = [int(x) for x in puzzle_input.strip().split("\n")]
    loop_sizes = [calculate_loop_size(x) for x in public_keys]
    print(calculate_key(public_keys[0], loop_sizes[1]))
    return


solve("""
3469259
13170438
""")
