def hash_list(list):
    return hash(str(list))


def count_valid_arrangements(list, min_joltage, max_joltage, divide=True):
    last_boundary = 0
    joltage = min_joltage
    if divide:
        possible_arrangements = 1
        for i in range(0, len(list)):
            if list[i] - joltage == 3 or i == len(list) - 1:
                # BOUNDARY
                found_possible = count_valid_arrangements(
                    list[last_boundary:i], min_joltage, list[i], False)
                possible_arrangements *= found_possible
                min_joltage = list[i]
                last_boundary = i
            joltage = list[i]
        return possible_arrangements
    else:
        found_possible = set([hash_list(list)])
        possible_arrangement_queue = [list]
        while len(possible_arrangement_queue) > 0:
            possible_arrangement = possible_arrangement_queue.pop()
            for i in range(0, len(possible_arrangement)):
                new_possible_arrangement = possible_arrangement.copy()
                new_possible_arrangement.pop(i)
                if len(new_possible_arrangement) > 0 and hash_list(new_possible_arrangement) not in found_possible:
                    valid = is_valid_arrangement(
                        new_possible_arrangement, min_joltage, max_joltage)
                    if valid:
                        possible_arrangement_queue.append(
                            new_possible_arrangement)
                        found_possible.add(hash_list(new_possible_arrangement))
        return len(found_possible)


def count_ones_and_threes(adapters, min_joltage=0):
    joltage = min_joltage
    ones = 0
    threes = 0
    for adapter in adapters:
        if adapter - joltage == 1:
            ones += 1
        elif adapter - joltage == 3:
            threes += 1
        elif adapter - joltage > 3:
            return None
        joltage = adapter
    joltage += 3
    threes += 1
    return (ones, threes, joltage)


def is_valid_arrangement(adapters, min_joltage=0, max_joltage=None):

    if min(adapters) > min_joltage:
        return None

    result = count_ones_and_threes(adapters, min_joltage)
    if not result:
        return None

    if max_joltage and result[2] < max_joltage:
        return None

    return result


def solve(puzzle_input):
    adapters = [int(x) for x in puzzle_input.strip().split("\n")]
    adapters.sort()

    result = count_ones_and_threes(adapters)

    # part 1
    if result:
        print(result[0] * result[1])
    else:
        print("what")

    print(count_valid_arrangements(adapters, 3, max(adapters)))

    return


solve("""
83
69
170
56
43
111
117
135
136
176
154
65
107
169
141
151
158
134
108
143
114
104
49
55
72
73
144
13
35
152
98
133
31
44
150
70
118
64
39
137
142
28
130
167
101
100
120
79
153
157
89
163
177
3
1
38
16
128
18
62
76
78
17
63
160
59
175
168
54
34
22
174
53
25
129
90
42
119
92
173
4
166
19
2
121
7
71
99
66
46
124
86
127
159
12
91
140
52
80
45
33
9
8
77
147
32
95
""")
