import sys


def get_buses(puzzle_input):
    x = puzzle_input.strip().split("\n")[1].split(",")
    buses = []
    for i, val in enumerate(x):
        if val != "x":
            buses.append((int(val), i))
    return buses


def get_lowest_common_multiple(a, b):
    da = a
    db = b
    while da != db:
        if da > db:
            db += b
        else:
            da += a
    return da


def solve(puzzle_input):
    arrive_time = int(puzzle_input.strip().split("\n")[0])
    buses = get_buses(puzzle_input)

    print("buses: " + str(buses))

    min_arrive_time = sys.maxsize
    earliest_bus = None
    for bus in buses:
        bus_id = bus[0]
        time = bus_id
        while time < arrive_time:
            time += bus_id
        if time < min_arrive_time:
            min_arrive_time = time
            earliest_bus = bus_id
    wait_time = min_arrive_time - arrive_time

    # part 1
    print(earliest_bus * wait_time)

    # part 2 down here is a mess, kind of amazed by assumptions turned out to be right

    # find required intervals between our buses
    intervals = []
    bus0 = buses[0]
    for i in range(1, len(buses)):
        bus_other = buses[i]
        # find how often bus_other time = bus time + n
        time = 0
        while True:
            time += bus0[0]
            if not (time + bus_other[1]) % bus_other[0]:
                break
        intervals.append([time, bus0[0] * bus_other[0]])

    while len(intervals) > 1:
        new_intervals = []
        interval0 = intervals[0]
        for i in range(1, len(intervals)):
            interval1 = intervals[i]
            time0 = interval0[0]
            time1 = interval1[0]
            while time1 != time0:
                if time1 > time0:
                    time0 += interval0[1]
                else:
                    time1 += interval1[1]
            new_intervals.append(
                (time0, get_lowest_common_multiple(interval0[1], interval1[1])))
        intervals = new_intervals

    print(intervals[0][0])
    return


solve("""
1000507
29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,631,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,23,x,x,x,x,x,x,x,383,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,17
""")
