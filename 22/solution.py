def parse_decks(puzzle_input):
    return [[int(y) for y in x.split("\n")[1:]] for x in puzzle_input.strip().split("\n\n")]


def calculate_score(decks):
    deck1 = decks[0]
    deck2 = decks[1]
    winning_deck = deck1 if len(deck1) > len(deck2) else deck2
    total = 0
    for i in range(0, len(winning_deck)):
        total += winning_deck[i] * (len(winning_deck) - i)
    return total


def combat(decks):
    deck1 = decks[0]
    deck2 = decks[1]
    while len(deck1) > 0 and len(deck2) > 0:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    return [deck1, deck2]


def recursive_combat(decks):
    deck1 = decks[0]
    deck2 = decks[1]
    deck_cache = set()
    while len(deck1) > 0 and len(deck2) > 0:

        # recursive prevention rule
        hand_key = ','.join([str(x) for x in deck1]) + \
            "!" + ','.join([str(x) for x in deck2])
        if hand_key in deck_cache:
            return ([deck1, deck2], 0)
        else:
            deck_cache.add(hand_key)

        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

        if len(deck1) >= card1 and len(deck2) >= card2:
            # RECURSIVE TIME!
            result = recursive_combat([
                deck1.copy()[:card1], deck2.copy()[:card2]])

            if result[1] == 0:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)

        else:
            if card1 > card2:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)

    return ([deck1, deck2], 0 if len(deck1) > len(deck2) else 1)


def solve(puzzle_input):
    decks = parse_decks(puzzle_input)
    decks = combat(decks)
    print(calculate_score(decks))

    decks = parse_decks(puzzle_input)
    decks = recursive_combat(decks)[0]
    print(calculate_score(decks))

    return


solve("""
Player 1:
20
28
50
36
35
15
41
22
39
45
30
19
47
38
25
6
2
27
5
4
37
24
42
29
21

Player 2:
23
43
34
49
13
48
44
18
14
9
12
31
16
26
33
3
10
1
46
17
32
11
40
7
8
""")
