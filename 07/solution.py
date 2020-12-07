SHINY_GOLD = "shiny gold"


def parse_rule(rule):
    parts1 = rule.split(" bags contain ")
    parts2 = parts1[1].split(", ")
    parts3 = [x.split(" ", 1) for x in parts2]
    for part in parts3:
        if part[0] == "no":
            parts3 = []
            break
        part[0] = int(part[0])
        part[1] = part[1].split(" bag")[0]
    return (parts1[0], parts3)


def solve(puzzle_input):
    rules = [parse_rule(x) for x in puzzle_input.strip().split("\n")]

    bags_by_contained = {}
    bags_by_container = {}
    for rule in rules:
        for contained in rule[1]:
            color = contained[1]
            if color not in bags_by_contained:
                x = set()
            else:
                x = bags_by_contained[color]
            x.add(rule[0])
            bags_by_contained[color] = x
        bags_by_container[rule[0]] = rule[1]

    # part 1
    can_contain_shiny_gold = list(
        bags_by_contained[SHINY_GOLD] if SHINY_GOLD in bags_by_contained else [])
    total_containable = set()
    while len(can_contain_shiny_gold) > 0:
        color = can_contain_shiny_gold.pop()
        total_containable.add(color)
        if color in bags_by_contained:
            can_contain_shiny_gold.extend(list(bags_by_contained[color]))
    print(len(total_containable))

    # part 2
    rule_queue = list(bags_by_container[SHINY_GOLD])
    total_required_bags = 0
    while len(rule_queue):
        rule = rule_queue.pop()
        total_required_bags += int(rule[0])
        next_required_bags = bags_by_container[rule[1]]
        for next_rule in next_required_bags:
            rule_queue.append([next_rule[0] * rule[0], next_rule[1]])
    print(total_required_bags)

    return


solve("""
plaid fuchsia bags contain 5 light violet bags, 1 light yellow bag.
striped aqua bags contain 2 striped teal bags.
clear coral bags contain 2 plaid green bags, 5 mirrored gold bags.
dull tan bags contain 4 faded blue bags, 3 faded olive bags, 5 dull salmon bags.
plaid green bags contain 3 faded green bags.
light tomato bags contain 1 drab chartreuse bag, 1 dotted tomato bag, 3 striped red bags, 2 vibrant violet bags.
dim tomato bags contain 4 striped gold bags, 5 bright lavender bags, 1 pale beige bag, 4 pale tan bags.
vibrant green bags contain 4 faded teal bags.
shiny crimson bags contain 2 dull green bags.
vibrant black bags contain 5 dark beige bags, 3 dark bronze bags.
light tan bags contain 1 striped tomato bag.
vibrant teal bags contain 1 shiny silver bag.
pale chartreuse bags contain 2 dotted plum bags.
plaid coral bags contain 2 pale green bags, 2 faded tomato bags, 2 dark salmon bags, 1 vibrant magenta bag.
dull gray bags contain 1 dark tan bag, 3 dotted tan bags.
muted gray bags contain 5 bright indigo bags, 5 dotted purple bags.
vibrant red bags contain 4 bright tomato bags, 4 shiny orange bags.
faded tan bags contain 1 dull crimson bag, 5 faded red bags.
pale magenta bags contain 3 posh chartreuse bags, 4 vibrant purple bags.
shiny gray bags contain 2 wavy purple bags.
light crimson bags contain 5 clear teal bags.
striped turquoise bags contain 3 pale tomato bags, 2 posh teal bags.
striped purple bags contain 4 dark silver bags, 4 vibrant gray bags, 2 dim bronze bags, 2 clear aqua bags.
muted magenta bags contain 4 striped tomato bags.
light teal bags contain 2 faded brown bags, 2 posh purple bags, 1 faded olive bag.
clear cyan bags contain 1 clear coral bag, 5 clear aqua bags.
dull cyan bags contain 5 wavy crimson bags, 1 pale orange bag.
shiny tan bags contain 2 bright red bags, 4 plaid cyan bags.
light brown bags contain 3 dim yellow bags, 4 dull orange bags, 1 vibrant yellow bag.
pale tan bags contain 2 striped orange bags, 5 dull plum bags.
wavy salmon bags contain 2 dark blue bags, 5 dim plum bags.
mirrored cyan bags contain 2 plaid turquoise bags, 5 dull plum bags, 3 muted indigo bags, 2 plaid white bags.
dark aqua bags contain 3 bright red bags, 2 wavy purple bags, 2 plaid tan bags.
wavy purple bags contain 5 wavy brown bags.
clear magenta bags contain 4 muted green bags, 3 dull cyan bags, 4 striped teal bags, 2 faded blue bags.
bright red bags contain 5 vibrant tomato bags, 2 dull orange bags.
pale purple bags contain 3 plaid turquoise bags, 4 light tan bags, 1 faded black bag, 5 light yellow bags.
bright orange bags contain 1 mirrored orange bag, 2 faded bronze bags, 1 wavy turquoise bag, 1 bright yellow bag.
faded lavender bags contain 1 plaid brown bag.
dark salmon bags contain 3 dotted crimson bags, 1 posh bronze bag.
mirrored coral bags contain 3 dark red bags, 1 dull fuchsia bag, 2 drab magenta bags, 4 dull indigo bags.
clear black bags contain 5 mirrored salmon bags, 3 drab gold bags, 3 muted fuchsia bags.
faded fuchsia bags contain 1 shiny silver bag, 2 posh orange bags, 5 plaid bronze bags.
dotted red bags contain 4 faded yellow bags, 5 dull brown bags, 3 clear red bags.
light purple bags contain 2 plaid magenta bags, 3 vibrant coral bags, 2 wavy black bags.
faded beige bags contain no other bags.
dull fuchsia bags contain 3 dim lavender bags, 1 dull aqua bag, 2 pale fuchsia bags.
wavy olive bags contain 5 dotted cyan bags, 1 dull lime bag.
dim teal bags contain 1 dull green bag.
dull orange bags contain 5 striped tomato bags, 5 drab blue bags, 5 faded blue bags, 2 pale brown bags.
muted brown bags contain 3 dotted orange bags, 1 bright tan bag.
vibrant coral bags contain 2 wavy turquoise bags.
clear aqua bags contain 5 posh bronze bags, 5 dim orange bags, 5 posh chartreuse bags.
dull plum bags contain 4 drab tan bags.
wavy tomato bags contain 4 wavy cyan bags, 1 bright silver bag, 3 dotted gray bags, 1 dark tomato bag.
shiny fuchsia bags contain 1 dotted silver bag, 5 dull lime bags, 3 drab teal bags.
pale fuchsia bags contain 3 pale beige bags.
plaid plum bags contain 4 dotted plum bags, 1 mirrored brown bag, 3 dim yellow bags, 2 vibrant bronze bags.
posh green bags contain 5 plaid indigo bags, 1 wavy red bag, 5 dim indigo bags, 4 wavy indigo bags.
muted aqua bags contain 3 bright tan bags, 3 dull yellow bags, 1 faded blue bag.
mirrored white bags contain 5 dark coral bags, 1 plaid red bag, 4 dull violet bags, 5 clear gray bags.
dotted aqua bags contain 4 drab aqua bags, 3 faded tomato bags.
bright indigo bags contain 4 faded tan bags, 3 clear turquoise bags, 1 plaid indigo bag, 4 bright gray bags.
posh silver bags contain 5 striped red bags, 3 faded blue bags, 3 dim plum bags, 3 vibrant beige bags.
bright olive bags contain 3 dull silver bags, 5 drab tomato bags.
muted beige bags contain 1 drab crimson bag.
shiny beige bags contain 3 clear blue bags.
wavy brown bags contain 2 striped coral bags, 2 light purple bags.
wavy black bags contain 4 faded beige bags, 2 striped red bags, 2 pale brown bags, 3 dull yellow bags.
faded salmon bags contain 1 light indigo bag, 5 plaid cyan bags, 2 pale salmon bags.
dark gold bags contain 1 mirrored plum bag, 2 dark tomato bags, 5 dull green bags, 2 light lime bags.
mirrored lavender bags contain 5 muted brown bags, 1 shiny blue bag, 5 dull blue bags, 3 wavy indigo bags.
wavy beige bags contain 3 mirrored purple bags, 3 posh yellow bags, 4 plaid green bags.
striped fuchsia bags contain 5 drab bronze bags, 4 posh tomato bags, 1 drab maroon bag, 1 dim beige bag.
faded blue bags contain 1 striped tomato bag, 3 dark olive bags, 2 drab tan bags.
drab gray bags contain 1 posh teal bag.
dim cyan bags contain 4 dark fuchsia bags, 3 wavy maroon bags, 5 posh silver bags, 4 posh chartreuse bags.
dotted purple bags contain 3 wavy white bags.
shiny brown bags contain 5 light silver bags, 4 light turquoise bags, 4 posh bronze bags.
vibrant tomato bags contain 3 dotted cyan bags, 3 posh teal bags, 1 clear magenta bag, 5 dull lime bags.
dark bronze bags contain 2 vibrant maroon bags, 2 mirrored olive bags.
wavy silver bags contain 4 striped magenta bags, 3 dim fuchsia bags.
striped yellow bags contain 5 faded black bags, 5 light beige bags, 1 vibrant beige bag, 2 mirrored beige bags.
faded chartreuse bags contain 4 clear gray bags, 5 dotted gray bags.
faded tomato bags contain 5 faded gray bags, 4 faded fuchsia bags, 3 drab teal bags.
dull gold bags contain 1 dark plum bag, 4 striped black bags.
muted turquoise bags contain 1 mirrored bronze bag, 5 shiny aqua bags, 1 clear plum bag.
dotted lime bags contain 1 dark black bag, 5 pale brown bags.
vibrant violet bags contain 5 faded lime bags, 1 pale fuchsia bag, 5 dull plum bags.
faded black bags contain 2 striped teal bags, 5 faded beige bags, 4 wavy black bags, 1 striped lavender bag.
drab teal bags contain 1 clear gold bag, 4 muted crimson bags, 1 light teal bag.
dull purple bags contain 1 posh crimson bag, 2 clear blue bags.
dotted teal bags contain 2 dark tan bags.
dark red bags contain 3 dotted cyan bags, 3 posh red bags, 2 bright red bags, 3 faded magenta bags.
light black bags contain 5 dull yellow bags.
light salmon bags contain 3 faded beige bags.
dull brown bags contain 1 light indigo bag, 4 mirrored yellow bags, 5 faded silver bags.
dark black bags contain 5 dull yellow bags, 3 dull lime bags, 5 posh aqua bags.
faded crimson bags contain 3 light fuchsia bags, 5 muted chartreuse bags.
drab yellow bags contain 5 drab indigo bags, 2 shiny brown bags, 4 muted lime bags.
muted tomato bags contain 3 posh salmon bags, 2 plaid indigo bags, 5 striped aqua bags.
pale teal bags contain 2 muted red bags, 5 mirrored brown bags, 4 mirrored tan bags.
posh violet bags contain 4 posh tomato bags.
dim plum bags contain 1 faded magenta bag, 5 drab silver bags, 1 pale brown bag.
light fuchsia bags contain 2 dotted silver bags, 3 dotted lavender bags, 3 shiny gold bags, 5 clear magenta bags.
vibrant orange bags contain 5 shiny blue bags, 5 dull maroon bags.
shiny white bags contain 5 mirrored yellow bags, 2 pale fuchsia bags, 4 shiny turquoise bags.
drab green bags contain 1 mirrored lavender bag, 3 posh tan bags.
faded silver bags contain 5 vibrant coral bags, 3 striped lavender bags, 4 dotted cyan bags, 5 plaid turquoise bags.
faded gold bags contain 4 faded magenta bags.
dark coral bags contain 3 light maroon bags, 1 drab silver bag.
striped olive bags contain 4 dotted maroon bags, 3 wavy brown bags, 1 wavy crimson bag, 5 shiny silver bags.
wavy lavender bags contain 3 mirrored yellow bags, 5 shiny crimson bags, 4 dark indigo bags.
bright fuchsia bags contain 2 vibrant green bags, 5 drab blue bags.
dotted turquoise bags contain 3 striped red bags.
drab black bags contain 1 faded tan bag.
pale silver bags contain 1 faded yellow bag, 1 drab tan bag, 5 muted salmon bags, 3 shiny white bags.
striped magenta bags contain 4 dark turquoise bags, 4 shiny blue bags, 3 shiny crimson bags.
dotted beige bags contain 2 mirrored black bags, 2 faded brown bags, 1 bright red bag, 2 clear coral bags.
clear maroon bags contain 5 bright bronze bags.
shiny olive bags contain 2 dull blue bags.
pale violet bags contain 1 light purple bag, 1 pale tomato bag, 4 plaid aqua bags, 4 light magenta bags.
dotted white bags contain 3 bright purple bags, 4 dull orange bags, 2 plaid salmon bags.
plaid blue bags contain 5 faded blue bags, 4 muted green bags, 4 bright bronze bags.
mirrored lime bags contain 1 faded green bag, 4 striped black bags, 1 mirrored purple bag.
wavy violet bags contain 1 muted bronze bag.
light silver bags contain 2 dull cyan bags, 1 drab tan bag.
dark tomato bags contain 1 vibrant tomato bag, 1 striped tomato bag.
wavy teal bags contain 5 wavy red bags, 2 drab brown bags, 1 posh olive bag.
dim green bags contain 2 striped teal bags, 1 drab blue bag.
wavy crimson bags contain no other bags.
mirrored aqua bags contain 3 posh tan bags, 5 muted teal bags, 3 light violet bags.
light cyan bags contain 4 vibrant chartreuse bags, 1 faded lime bag, 2 drab purple bags, 2 shiny white bags.
shiny gold bags contain 4 drab blue bags, 4 posh purple bags, 2 drab silver bags, 4 wavy turquoise bags.
plaid chartreuse bags contain 5 mirrored olive bags, 2 vibrant orange bags, 2 shiny purple bags.
dim yellow bags contain 1 faded green bag, 4 wavy fuchsia bags.
pale turquoise bags contain 1 drab turquoise bag.
clear red bags contain 1 pale bronze bag, 4 drab tan bags.
shiny teal bags contain 3 bright aqua bags.
dotted tomato bags contain 3 dotted orange bags, 5 light silver bags, 2 dull green bags, 5 wavy chartreuse bags.
striped tan bags contain 1 light turquoise bag, 2 dotted salmon bags, 4 shiny orange bags, 2 clear red bags.
dim bronze bags contain 1 wavy gold bag.
posh crimson bags contain 4 posh aqua bags.
plaid salmon bags contain 2 dull tan bags.
mirrored salmon bags contain 2 muted aqua bags, 5 muted salmon bags.
striped blue bags contain 3 wavy white bags, 4 drab blue bags, 1 drab chartreuse bag, 4 dull orange bags.
pale red bags contain 1 striped red bag.
muted black bags contain 4 faded gold bags.
clear orange bags contain 2 faded red bags.
mirrored maroon bags contain 2 plaid tan bags.
dull aqua bags contain 4 pale gold bags.
posh coral bags contain 3 striped gold bags.
posh purple bags contain 4 pale orange bags, 5 dull salmon bags, 2 striped teal bags.
muted tan bags contain 3 clear coral bags, 4 pale salmon bags.
mirrored orange bags contain 5 pale bronze bags.
striped teal bags contain no other bags.
dark blue bags contain no other bags.
clear bronze bags contain 4 vibrant gray bags.
light magenta bags contain 4 dim green bags.
drab coral bags contain 5 dotted chartreuse bags, 4 vibrant crimson bags, 2 muted green bags.
drab brown bags contain 2 dull tomato bags, 5 vibrant bronze bags.
bright coral bags contain 1 posh plum bag, 1 wavy gold bag, 2 drab lavender bags, 2 muted lavender bags.
dim white bags contain 4 shiny aqua bags.
plaid bronze bags contain 4 drab tan bags, 3 plaid salmon bags, 4 striped coral bags.
faded teal bags contain 1 vibrant white bag, 5 wavy purple bags.
drab turquoise bags contain 3 pale tomato bags, 1 bright indigo bag.
muted white bags contain 3 striped brown bags, 1 light blue bag.
clear crimson bags contain 1 dark magenta bag.
shiny magenta bags contain 4 wavy tomato bags, 4 shiny bronze bags, 4 vibrant coral bags, 5 bright lime bags.
bright magenta bags contain 3 wavy brown bags.
bright tomato bags contain 4 vibrant fuchsia bags, 1 clear aqua bag.
wavy coral bags contain 4 striped gold bags, 1 light purple bag, 4 vibrant purple bags.
muted indigo bags contain 2 posh purple bags, 2 light gold bags, 3 striped lavender bags.
clear violet bags contain 2 wavy cyan bags, 5 pale brown bags, 4 faded magenta bags, 2 bright purple bags.
dull white bags contain 4 wavy olive bags, 3 mirrored olive bags, 3 faded magenta bags, 4 dull green bags.
dull magenta bags contain 4 dim beige bags.
dotted blue bags contain 4 posh beige bags, 1 pale purple bag, 4 shiny red bags.
dotted lavender bags contain 3 posh purple bags.
light white bags contain 4 striped lavender bags.
dark turquoise bags contain 5 light teal bags.
faded turquoise bags contain 5 striped violet bags, 4 dull crimson bags, 2 dim purple bags, 1 light silver bag.
striped chartreuse bags contain 3 pale white bags, 3 dim fuchsia bags.
pale gold bags contain 2 clear teal bags, 3 wavy turquoise bags, 5 light gold bags.
posh blue bags contain 4 muted yellow bags, 1 dull crimson bag, 3 wavy violet bags, 5 mirrored fuchsia bags.
dotted gray bags contain 3 wavy fuchsia bags.
plaid magenta bags contain 3 plaid black bags.
pale beige bags contain 1 pale white bag, 2 dim salmon bags, 5 mirrored gold bags.
striped bronze bags contain 2 dull yellow bags, 2 dark blue bags.
dark lime bags contain 2 pale magenta bags, 4 clear cyan bags.
bright turquoise bags contain 2 light white bags, 3 plaid salmon bags, 2 clear aqua bags, 5 dull silver bags.
posh salmon bags contain 1 drab turquoise bag.
muted bronze bags contain 1 pale bronze bag, 3 clear maroon bags.
faded coral bags contain 1 clear gray bag, 5 plaid gray bags, 3 bright silver bags, 4 posh yellow bags.
mirrored gray bags contain 1 dark coral bag, 2 plaid blue bags, 4 mirrored coral bags, 1 mirrored olive bag.
vibrant olive bags contain 5 pale chartreuse bags, 4 plaid green bags, 4 dark coral bags.
dotted magenta bags contain 4 light chartreuse bags, 3 plaid indigo bags, 2 dull tan bags.
light violet bags contain 2 muted green bags.
dim fuchsia bags contain 5 dim tan bags, 5 faded black bags, 1 drab white bag.
dotted black bags contain 3 bright gold bags, 2 faded gold bags.
striped indigo bags contain 3 posh aqua bags.
posh cyan bags contain 5 dull fuchsia bags.
vibrant turquoise bags contain 2 muted chartreuse bags, 2 clear magenta bags, 5 drab chartreuse bags.
mirrored magenta bags contain 1 dull lime bag.
mirrored violet bags contain 2 posh magenta bags, 1 plaid white bag, 4 wavy turquoise bags, 5 dull salmon bags.
pale tomato bags contain 4 wavy maroon bags, 3 clear aqua bags, 2 striped lavender bags.
clear fuchsia bags contain 5 dark cyan bags, 1 plaid cyan bag.
drab orange bags contain 3 mirrored purple bags, 1 striped orange bag.
bright blue bags contain 1 bright cyan bag, 4 plaid green bags.
muted chartreuse bags contain 4 faded beige bags, 3 faded green bags.
plaid teal bags contain 2 mirrored orange bags, 5 plaid plum bags.
light blue bags contain 4 faded silver bags, 3 light turquoise bags, 2 dim aqua bags, 5 posh silver bags.
bright tan bags contain 4 striped coral bags, 1 dark fuchsia bag.
shiny black bags contain 1 light green bag.
plaid violet bags contain 1 faded magenta bag, 1 shiny bronze bag, 2 vibrant tomato bags.
posh bronze bags contain 4 shiny gold bags, 1 bright yellow bag, 1 dull cyan bag.
light red bags contain 3 dotted black bags, 5 pale coral bags.
striped red bags contain no other bags.
clear tan bags contain 2 faded brown bags, 1 bright brown bag, 2 bright gold bags.
dull turquoise bags contain 5 mirrored yellow bags, 3 wavy red bags, 5 faded purple bags, 4 clear green bags.
plaid yellow bags contain 4 dark red bags, 3 dull tomato bags, 5 faded violet bags.
dotted gold bags contain 2 dotted lime bags, 2 faded gray bags, 3 clear coral bags.
dull bronze bags contain 2 pale red bags, 3 dim indigo bags.
shiny green bags contain 2 pale red bags, 1 mirrored silver bag, 4 bright lime bags, 5 pale indigo bags.
bright black bags contain 2 striped plum bags, 1 clear black bag, 4 clear olive bags.
bright gold bags contain 3 wavy cyan bags, 1 dotted magenta bag, 1 muted salmon bag, 4 light maroon bags.
muted violet bags contain 5 wavy cyan bags, 4 dim tan bags, 1 posh gray bag, 5 vibrant brown bags.
dim turquoise bags contain 1 pale tomato bag, 2 dotted silver bags, 5 mirrored coral bags.
drab lime bags contain 5 shiny gold bags.
wavy bronze bags contain 1 shiny red bag, 4 dotted cyan bags.
vibrant purple bags contain 4 drab chartreuse bags, 4 dotted yellow bags.
plaid purple bags contain 2 drab beige bags, 3 pale aqua bags, 3 muted magenta bags.
faded brown bags contain 3 faded beige bags, 1 light chartreuse bag, 4 mirrored gold bags.
pale lavender bags contain 1 mirrored tomato bag, 5 wavy maroon bags, 4 wavy lime bags.
posh fuchsia bags contain 5 posh orange bags.
drab fuchsia bags contain 1 dim plum bag, 1 dark coral bag, 3 dark red bags.
striped crimson bags contain 5 pale orange bags, 5 faded beige bags, 5 faded brown bags.
wavy lime bags contain 5 dull crimson bags.
vibrant fuchsia bags contain 2 wavy white bags.
vibrant plum bags contain 4 dim salmon bags, 2 plaid tan bags, 3 dull blue bags.
muted cyan bags contain 3 striped beige bags.
clear teal bags contain 2 wavy aqua bags, 3 dotted plum bags.
dark maroon bags contain 1 light violet bag, 3 clear plum bags, 5 dotted fuchsia bags, 2 vibrant tomato bags.
dull black bags contain 5 muted olive bags.
light yellow bags contain 1 dull white bag, 5 dark aqua bags, 3 light purple bags, 4 dim green bags.
pale bronze bags contain 1 wavy aqua bag.
plaid red bags contain 5 pale plum bags, 2 muted brown bags, 2 dull bronze bags.
dim gray bags contain 2 muted lavender bags.
plaid gray bags contain 5 muted aqua bags.
vibrant blue bags contain 4 light tomato bags, 1 plaid beige bag.
clear blue bags contain 5 clear plum bags, 5 drab chartreuse bags.
dotted green bags contain 5 plaid white bags, 5 vibrant turquoise bags, 1 drab silver bag.
dull crimson bags contain 3 mirrored yellow bags, 3 posh red bags, 3 faded brown bags.
striped maroon bags contain 1 shiny magenta bag, 2 light brown bags, 4 dull green bags.
dark yellow bags contain 4 faded silver bags, 5 shiny lavender bags, 4 dim crimson bags, 2 plaid bronze bags.
pale indigo bags contain 4 plaid salmon bags, 3 striped purple bags, 5 pale magenta bags, 1 dotted lime bag.
faded maroon bags contain 5 light silver bags, 5 dim bronze bags, 4 faded tan bags, 5 striped crimson bags.
pale green bags contain 4 vibrant white bags.
muted maroon bags contain 2 light black bags, 2 mirrored fuchsia bags.
pale yellow bags contain 2 dull bronze bags, 4 bright maroon bags, 5 wavy cyan bags, 4 dotted lavender bags.
posh white bags contain 3 mirrored turquoise bags, 3 shiny aqua bags, 2 striped blue bags, 4 faded coral bags.
wavy orange bags contain 4 wavy crimson bags, 2 bright brown bags, 3 bright magenta bags, 1 dotted gold bag.
dark beige bags contain 3 muted white bags.
dotted salmon bags contain 5 dim bronze bags, 5 striped orange bags.
dotted fuchsia bags contain 1 striped red bag, 4 bright purple bags.
pale cyan bags contain 1 dull blue bag.
mirrored purple bags contain 5 light turquoise bags, 2 faded silver bags.
drab violet bags contain 1 vibrant turquoise bag, 2 muted chartreuse bags, 5 pale bronze bags.
wavy gray bags contain 1 dark purple bag, 4 muted green bags.
wavy magenta bags contain 5 dark white bags, 4 vibrant black bags, 4 muted coral bags.
pale plum bags contain 5 mirrored brown bags, 2 pale red bags.
light plum bags contain 4 dark tomato bags, 4 wavy gold bags.
pale aqua bags contain 1 striped red bag, 2 dim crimson bags, 3 mirrored orange bags.
muted green bags contain 1 mirrored yellow bag.
bright purple bags contain 5 light violet bags, 5 clear magenta bags, 1 faded lime bag.
dark green bags contain 2 shiny aqua bags.
dark orange bags contain 3 striped coral bags.
dotted chartreuse bags contain 1 bright lime bag, 1 light olive bag, 4 muted red bags, 1 posh chartreuse bag.
shiny chartreuse bags contain 1 bright salmon bag, 1 plaid indigo bag.
clear gold bags contain 5 dull lime bags, 4 shiny brown bags, 1 dull plum bag, 4 dull salmon bags.
shiny salmon bags contain 2 muted salmon bags, 2 dotted lavender bags.
striped cyan bags contain 3 drab tan bags, 5 dotted cyan bags, 1 posh aqua bag, 1 plaid magenta bag.
dark plum bags contain 1 clear orange bag, 2 striped black bags.
vibrant magenta bags contain 1 plaid tan bag, 3 muted bronze bags, 3 bright chartreuse bags.
clear beige bags contain 4 muted tan bags, 1 clear turquoise bag, 4 mirrored turquoise bags, 2 bright silver bags.
drab lavender bags contain 1 dotted cyan bag, 4 clear plum bags.
shiny coral bags contain 2 drab beige bags.
light bronze bags contain 2 mirrored plum bags, 2 light black bags.
vibrant yellow bags contain 4 vibrant coral bags, 5 mirrored olive bags, 1 light lime bag, 2 muted crimson bags.
vibrant salmon bags contain 4 faded beige bags, 2 faded olive bags, 1 pale brown bag.
dim tan bags contain 3 faded beige bags, 4 light tan bags.
vibrant silver bags contain 1 dark tomato bag.
striped salmon bags contain 5 faded brown bags.
shiny purple bags contain 1 pale lavender bag, 3 plaid black bags, 1 drab indigo bag.
light turquoise bags contain 4 dark silver bags.
dark chartreuse bags contain 5 dark silver bags.
mirrored indigo bags contain 5 mirrored gold bags, 1 dotted white bag.
faded olive bags contain 1 pale brown bag, 3 faded beige bags, 2 light chartreuse bags.
mirrored black bags contain 5 posh purple bags.
clear green bags contain 2 dark magenta bags, 5 faded gold bags, 4 striped teal bags, 4 dark purple bags.
bright beige bags contain 3 light olive bags, 3 wavy orange bags, 4 dotted lavender bags.
plaid brown bags contain 4 dull lavender bags, 3 drab gold bags.
vibrant chartreuse bags contain 1 bright bronze bag, 5 wavy crimson bags.
posh aqua bags contain 5 muted green bags, 2 dim green bags, 1 dim crimson bag, 1 posh red bag.
vibrant gold bags contain 5 wavy chartreuse bags, 3 drab gold bags, 2 striped blue bags, 3 posh yellow bags.
posh tan bags contain 1 shiny chartreuse bag, 2 drab bronze bags.
bright violet bags contain 1 pale lavender bag, 5 mirrored olive bags, 1 posh turquoise bag.
faded lime bags contain 5 pale brown bags, 4 faded black bags, 1 faded beige bag.
vibrant gray bags contain 3 vibrant chartreuse bags, 3 bright purple bags.
dull silver bags contain 5 pale tomato bags, 5 shiny turquoise bags, 2 mirrored yellow bags.
pale maroon bags contain 3 posh red bags, 1 plaid bronze bag, 5 striped red bags.
dull lavender bags contain 4 vibrant violet bags, 1 bright yellow bag, 3 bright aqua bags.
light aqua bags contain 5 vibrant turquoise bags.
striped violet bags contain 4 drab silver bags, 3 posh magenta bags, 3 wavy turquoise bags.
bright green bags contain 3 drab teal bags.
light coral bags contain 5 dotted violet bags, 4 pale chartreuse bags.
muted salmon bags contain 4 vibrant turquoise bags, 5 clear chartreuse bags, 1 dark fuchsia bag, 5 bright bronze bags.
wavy cyan bags contain 4 dim orange bags, 1 dull orange bag, 4 plaid indigo bags, 4 dim salmon bags.
shiny red bags contain 1 dim blue bag, 4 clear plum bags.
vibrant beige bags contain 3 posh red bags.
shiny maroon bags contain 3 striped tomato bags, 2 faded lime bags.
shiny aqua bags contain 3 bright yellow bags.
bright aqua bags contain 5 wavy lavender bags, 4 striped coral bags, 5 dotted cyan bags, 3 drab cyan bags.
dim olive bags contain 2 posh blue bags, 5 vibrant violet bags, 3 drab brown bags, 1 dull purple bag.
shiny silver bags contain 5 dim green bags, 4 dull cyan bags.
dim brown bags contain 1 wavy brown bag, 3 drab black bags.
dotted brown bags contain 3 drab crimson bags, 1 shiny red bag.
striped coral bags contain 4 striped red bags, 1 dotted cyan bag.
dotted plum bags contain 3 faded lime bags, 2 striped lavender bags, 2 wavy crimson bags, 2 faded brown bags.
light gold bags contain 1 light silver bag, 3 posh teal bags, 3 dark orange bags, 4 bright bronze bags.
dark tan bags contain 5 drab black bags, 2 plaid cyan bags, 3 faded yellow bags, 1 dim blue bag.
posh olive bags contain 4 drab olive bags, 5 dull tan bags, 1 wavy chartreuse bag, 5 muted magenta bags.
dull red bags contain 1 vibrant teal bag, 4 dim salmon bags, 1 bright violet bag, 1 dark lavender bag.
plaid turquoise bags contain 3 faded green bags, 5 wavy crimson bags.
plaid cyan bags contain 2 dull yellow bags, 2 dotted cyan bags, 1 light chartreuse bag, 2 faded green bags.
dull indigo bags contain 2 faded silver bags.
pale brown bags contain no other bags.
striped plum bags contain 5 dull lime bags, 2 muted white bags, 3 striped teal bags.
dotted coral bags contain 4 faded silver bags, 2 wavy aqua bags, 2 light chartreuse bags, 5 posh indigo bags.
mirrored beige bags contain 1 plaid black bag, 2 plaid tan bags, 2 pale bronze bags.
vibrant cyan bags contain 4 wavy beige bags, 1 shiny orange bag.
wavy fuchsia bags contain 5 pale maroon bags, 3 drab violet bags, 2 shiny orange bags.
drab silver bags contain 2 dark blue bags, 3 light chartreuse bags, 3 mirrored gold bags.
wavy turquoise bags contain 5 posh red bags, 4 striped teal bags.
bright cyan bags contain 4 bright silver bags, 1 muted gray bag, 5 faded aqua bags, 3 wavy aqua bags.
wavy green bags contain 4 clear violet bags, 4 dark olive bags, 2 clear magenta bags, 1 mirrored black bag.
mirrored gold bags contain 2 dark olive bags.
wavy gold bags contain 4 plaid indigo bags.
dotted yellow bags contain 3 dull orange bags, 2 faded green bags.
light beige bags contain 4 dull cyan bags.
bright crimson bags contain 1 faded tan bag, 1 faded chartreuse bag, 5 vibrant brown bags.
dotted bronze bags contain 5 striped white bags.
mirrored yellow bags contain 3 wavy crimson bags, 4 dark olive bags, 5 drab tan bags.
plaid lavender bags contain 1 light tomato bag, 5 dull blue bags, 2 wavy indigo bags, 3 bright gray bags.
drab purple bags contain 3 dotted plum bags, 5 drab olive bags, 1 drab tan bag, 3 dark black bags.
shiny lime bags contain 2 plaid bronze bags, 1 shiny gold bag.
drab chartreuse bags contain 2 bright bronze bags, 4 light teal bags, 1 mirrored yellow bag.
bright plum bags contain 3 drab turquoise bags.
light orange bags contain 1 shiny lavender bag, 2 dark fuchsia bags, 1 muted olive bag, 4 wavy olive bags.
striped beige bags contain 4 dull crimson bags, 5 dotted fuchsia bags.
wavy chartreuse bags contain 2 bright salmon bags, 5 faded green bags, 1 mirrored black bag.
striped tomato bags contain no other bags.
plaid aqua bags contain 1 light magenta bag, 3 pale white bags, 3 clear blue bags, 4 dull crimson bags.
plaid tan bags contain 3 dull green bags, 1 light silver bag, 5 dim orange bags, 1 dark blue bag.
dotted cyan bags contain 2 wavy black bags, 3 striped teal bags.
dull green bags contain 1 plaid magenta bag, 3 dull plum bags, 4 dim green bags.
faded purple bags contain 5 mirrored cyan bags, 1 dull beige bag, 4 vibrant purple bags.
dotted maroon bags contain 1 vibrant beige bag, 3 plaid magenta bags.
faded aqua bags contain 4 plaid gold bags, 1 plaid yellow bag, 2 bright lime bags.
pale lime bags contain 1 light blue bag.
dark indigo bags contain 1 light gold bag.
shiny orange bags contain 2 plaid black bags, 2 faded brown bags, 4 plaid indigo bags.
muted olive bags contain 1 wavy chartreuse bag.
muted purple bags contain 4 dotted silver bags.
plaid black bags contain 3 drab silver bags.
striped lavender bags contain 5 wavy crimson bags.
posh chartreuse bags contain 5 drab chartreuse bags.
clear purple bags contain 3 faded green bags, 2 bright gold bags.
dark crimson bags contain 4 plaid teal bags, 4 muted cyan bags.
clear silver bags contain 3 pale beige bags, 2 mirrored tomato bags.
dotted indigo bags contain 2 dark plum bags, 2 clear magenta bags, 3 light olive bags.
dull chartreuse bags contain 2 light turquoise bags, 3 drab brown bags.
bright brown bags contain 4 light purple bags, 1 vibrant coral bag.
dim salmon bags contain 2 dull salmon bags.
muted lime bags contain 4 muted violet bags, 5 shiny white bags.
vibrant lime bags contain 2 mirrored bronze bags, 1 dotted crimson bag, 5 dim yellow bags, 2 mirrored gold bags.
muted silver bags contain 1 striped orange bag, 3 drab purple bags.
mirrored bronze bags contain 4 dull bronze bags.
light olive bags contain 4 mirrored olive bags, 2 dim lime bags, 1 clear magenta bag.
vibrant tan bags contain 2 shiny teal bags.
posh red bags contain 2 bright bronze bags, 5 striped teal bags, 5 faded beige bags, 4 faded olive bags.
faded red bags contain 4 striped lavender bags, 4 posh red bags.
mirrored brown bags contain 3 dim salmon bags, 4 drab chartreuse bags, 1 wavy tomato bag.
dark gray bags contain 1 muted tan bag, 4 faded blue bags, 2 dim chartreuse bags.
dark white bags contain 4 vibrant lime bags, 4 pale olive bags.
striped silver bags contain 4 dim cyan bags.
clear salmon bags contain 5 pale magenta bags, 1 mirrored salmon bag.
pale white bags contain 5 wavy crimson bags, 4 plaid indigo bags, 5 striped crimson bags, 3 drab violet bags.
vibrant indigo bags contain 1 mirrored gold bag, 1 striped turquoise bag, 3 posh beige bags.
drab aqua bags contain 5 faded crimson bags, 3 wavy gold bags, 3 striped tomato bags.
clear brown bags contain 5 bright lavender bags.
posh indigo bags contain 5 mirrored red bags, 5 clear coral bags.
posh black bags contain 4 dim fuchsia bags, 5 muted olive bags, 3 mirrored red bags.
shiny lavender bags contain 2 muted aqua bags, 3 striped black bags, 3 wavy salmon bags, 3 mirrored purple bags.
vibrant bronze bags contain 1 bright tan bag, 5 faded beige bags, 5 pale red bags, 1 plaid cyan bag.
clear chartreuse bags contain 2 shiny gold bags, 1 wavy turquoise bag, 2 muted crimson bags.
drab tan bags contain no other bags.
posh gold bags contain 5 dotted beige bags, 1 striped crimson bag, 5 drab purple bags, 1 bright gray bag.
clear olive bags contain 3 dark tomato bags.
dim aqua bags contain 4 wavy black bags, 5 clear chartreuse bags, 5 clear aqua bags.
pale coral bags contain 2 shiny orange bags, 5 dark black bags, 3 vibrant coral bags.
drab blue bags contain 5 dull salmon bags.
vibrant white bags contain 2 mirrored yellow bags.
faded indigo bags contain 5 clear aqua bags.
posh turquoise bags contain 1 light purple bag, 4 mirrored salmon bags.
dotted orange bags contain 5 dark blue bags, 1 shiny lavender bag, 2 dim plum bags, 3 clear violet bags.
muted crimson bags contain 4 wavy crimson bags, 1 light magenta bag, 3 clear plum bags.
dim coral bags contain 1 vibrant red bag, 2 vibrant magenta bags.
mirrored plum bags contain 5 light olive bags.
dull violet bags contain 2 dim aqua bags.
faded violet bags contain 5 clear violet bags, 5 muted indigo bags, 3 clear red bags, 1 posh tan bag.
vibrant crimson bags contain 1 shiny crimson bag.
muted plum bags contain 3 drab beige bags, 4 posh maroon bags.
dim orange bags contain 5 bright salmon bags.
dim blue bags contain 1 mirrored black bag, 3 faded blue bags.
mirrored tan bags contain 5 plaid plum bags.
pale crimson bags contain 4 dim green bags, 2 pale fuchsia bags.
bright white bags contain 2 drab gold bags, 2 shiny maroon bags, 5 mirrored lime bags.
dim indigo bags contain 1 mirrored cyan bag, 1 wavy purple bag, 1 drab brown bag.
dotted violet bags contain 4 bright teal bags, 2 vibrant plum bags.
wavy indigo bags contain 2 drab silver bags, 1 muted chartreuse bag, 1 drab aqua bag, 3 mirrored teal bags.
dark cyan bags contain 1 muted magenta bag, 3 vibrant violet bags, 4 mirrored aqua bags, 5 drab violet bags.
posh maroon bags contain 5 muted chartreuse bags, 4 dark olive bags.
drab tomato bags contain 2 plaid tan bags, 2 posh purple bags, 2 posh beige bags.
wavy tan bags contain 5 light cyan bags, 5 muted brown bags, 5 mirrored coral bags, 5 light chartreuse bags.
faded bronze bags contain 4 dotted magenta bags.
pale blue bags contain 5 pale purple bags.
dim magenta bags contain 5 posh aqua bags, 5 dim crimson bags, 4 wavy gold bags, 2 shiny orange bags.
dark fuchsia bags contain 2 drab silver bags.
wavy white bags contain 4 vibrant turquoise bags, 2 clear violet bags, 1 dull salmon bag.
drab maroon bags contain 3 pale tomato bags, 2 dim chartreuse bags, 5 mirrored orange bags, 4 drab violet bags.
muted fuchsia bags contain 4 muted bronze bags, 4 plaid brown bags, 1 faded white bag.
plaid gold bags contain 3 vibrant bronze bags, 5 striped chartreuse bags.
faded green bags contain 2 dull cyan bags, 5 posh purple bags.
light indigo bags contain 5 mirrored tomato bags.
striped white bags contain 5 clear plum bags.
posh magenta bags contain 5 wavy crimson bags, 3 striped coral bags.
drab olive bags contain 4 striped orange bags.
plaid indigo bags contain 1 plaid turquoise bag.
dark brown bags contain 2 faded tan bags, 5 wavy green bags.
faded cyan bags contain 2 bright violet bags, 3 mirrored salmon bags.
dim lavender bags contain 2 mirrored fuchsia bags, 3 pale magenta bags, 2 dotted tan bags, 4 posh bronze bags.
dull maroon bags contain 3 dark silver bags, 5 dim plum bags.
dull teal bags contain 3 pale green bags.
shiny yellow bags contain 4 dotted fuchsia bags.
mirrored crimson bags contain 5 dotted plum bags.
drab beige bags contain 3 faded orange bags, 3 dark orange bags, 4 clear orange bags.
dull olive bags contain 2 vibrant bronze bags, 4 shiny chartreuse bags.
wavy red bags contain 2 wavy brown bags, 1 wavy olive bag, 3 striped cyan bags.
light gray bags contain 1 pale salmon bag, 2 plaid bronze bags, 5 dull yellow bags.
faded gray bags contain 4 muted green bags, 5 faded red bags, 3 muted magenta bags, 5 bright magenta bags.
drab indigo bags contain 1 posh gold bag, 2 dull lime bags, 1 pale orange bag.
bright yellow bags contain 4 posh red bags, 4 shiny gold bags.
drab bronze bags contain 4 dark indigo bags.
striped gold bags contain 3 faded yellow bags, 2 mirrored tomato bags, 1 bright lime bag.
muted gold bags contain 4 dim violet bags.
plaid olive bags contain 3 wavy fuchsia bags.
bright gray bags contain 4 bright bronze bags, 1 plaid white bag, 1 pale bronze bag.
clear turquoise bags contain 2 mirrored purple bags, 2 light gold bags, 4 dim cyan bags, 5 wavy olive bags.
wavy plum bags contain 4 bright yellow bags.
dull blue bags contain 4 dotted lavender bags.
posh gray bags contain 4 faded blue bags, 2 dull brown bags, 1 clear cyan bag.
pale black bags contain 5 dim cyan bags, 4 bright white bags.
wavy blue bags contain 3 faded olive bags, 5 bright lavender bags, 1 wavy black bag, 2 posh magenta bags.
posh beige bags contain 2 light cyan bags, 1 wavy violet bag, 1 muted olive bag.
clear plum bags contain 3 dull cyan bags.
drab cyan bags contain 5 plaid green bags.
vibrant aqua bags contain 5 posh maroon bags.
dim silver bags contain 5 shiny gold bags, 5 posh magenta bags, 1 light white bag.
posh brown bags contain 4 plaid salmon bags, 2 vibrant blue bags, 2 posh olive bags.
dark teal bags contain 1 faded brown bag.
clear white bags contain 5 vibrant tan bags, 5 light purple bags, 3 posh tan bags, 4 faded beige bags.
dim maroon bags contain 2 plaid chartreuse bags, 1 dim gray bag, 2 drab gold bags, 5 light white bags.
dull salmon bags contain 5 striped teal bags, 3 dark blue bags, 3 drab tan bags, 5 wavy crimson bags.
dull coral bags contain 1 faded red bag, 2 shiny teal bags, 3 bright gray bags, 1 pale brown bag.
dark violet bags contain 1 clear cyan bag, 4 mirrored beige bags, 2 vibrant turquoise bags.
vibrant maroon bags contain 1 muted magenta bag, 3 muted olive bags, 2 shiny turquoise bags.
posh orange bags contain 5 dark black bags, 3 pale maroon bags, 5 dull plum bags.
clear indigo bags contain 4 faded tan bags, 3 clear orange bags, 1 vibrant aqua bag.
clear gray bags contain 4 dull salmon bags, 5 dark magenta bags.
shiny turquoise bags contain 4 muted green bags, 4 vibrant beige bags, 5 mirrored cyan bags, 4 striped blue bags.
pale salmon bags contain 1 dark silver bag, 4 dim green bags.
striped gray bags contain 3 dark lavender bags.
dull yellow bags contain 2 dark blue bags, 4 striped tomato bags, 2 striped red bags, 3 pale brown bags.
posh yellow bags contain 1 dull green bag, 1 dull plum bag.
plaid white bags contain 3 plaid turquoise bags, 4 dotted cyan bags, 3 shiny gold bags, 5 clear plum bags.
faded orange bags contain 1 dull silver bag, 4 clear gray bags, 1 posh tomato bag, 2 wavy yellow bags.
dim violet bags contain 4 drab silver bags, 1 dull yellow bag, 3 faded blue bags.
light green bags contain 3 drab gold bags, 4 wavy purple bags.
dark magenta bags contain 2 light gold bags, 5 drab violet bags.
dark purple bags contain 5 plaid beige bags.
mirrored blue bags contain 2 plaid tan bags.
dim lime bags contain 1 dotted beige bag, 2 striped white bags, 5 dim blue bags, 5 wavy blue bags.
bright chartreuse bags contain 3 clear orange bags.
vibrant brown bags contain 3 mirrored violet bags, 5 dull green bags, 2 pale magenta bags.
drab salmon bags contain 4 muted magenta bags.
muted teal bags contain 5 dark black bags, 5 light gold bags.
striped lime bags contain 1 dim orange bag.
plaid crimson bags contain 4 dim teal bags, 3 dull salmon bags.
posh plum bags contain 5 pale gray bags.
light maroon bags contain 4 drab violet bags, 2 faded brown bags, 2 striped black bags, 3 striped coral bags.
pale gray bags contain 1 dark aqua bag, 3 mirrored tomato bags.
light chartreuse bags contain no other bags.
dim crimson bags contain 5 faded blue bags, 1 dark blue bag, 2 striped teal bags.
dim beige bags contain 5 wavy silver bags, 1 wavy orange bag, 1 dim lime bag, 2 mirrored lime bags.
bright teal bags contain 1 dull violet bag, 1 faded beige bag, 3 faded orange bags.
striped green bags contain 2 drab gold bags, 5 posh olive bags, 4 light indigo bags, 1 clear yellow bag.
striped black bags contain 4 striped crimson bags, 1 pale red bag.
plaid beige bags contain 3 pale tomato bags.
drab plum bags contain 4 striped coral bags, 3 dotted crimson bags.
plaid orange bags contain 4 bright aqua bags.
wavy maroon bags contain 1 dim orange bag, 1 dim violet bag, 4 posh chartreuse bags, 5 plaid tan bags.
dim purple bags contain 1 mirrored black bag, 1 plaid plum bag, 4 striped teal bags, 1 posh aqua bag.
mirrored red bags contain 2 shiny salmon bags, 3 bright salmon bags, 1 vibrant salmon bag.
striped brown bags contain 3 light lime bags, 1 drab black bag, 2 dull white bags, 5 drab lavender bags.
dim red bags contain 2 mirrored black bags.
clear lavender bags contain 5 pale fuchsia bags.
bright bronze bags contain 2 striped teal bags, 4 clear plum bags, 3 dim crimson bags, 5 faded black bags.
shiny violet bags contain 2 dark gold bags, 3 posh maroon bags.
bright lime bags contain 2 clear magenta bags, 3 dark blue bags, 4 striped lavender bags, 1 dull crimson bag.
mirrored silver bags contain 1 vibrant tomato bag, 4 dull salmon bags, 5 plaid green bags, 4 wavy brown bags.
dotted olive bags contain 5 faded beige bags.
posh tomato bags contain 2 faded purple bags.
posh teal bags contain 2 drab tan bags, 3 striped red bags, 3 dull salmon bags, 1 striped lavender bag.
shiny tomato bags contain 3 posh indigo bags.
dotted crimson bags contain 1 pale gray bag.
shiny indigo bags contain 1 pale beige bag.
plaid lime bags contain 1 light maroon bag.
mirrored turquoise bags contain 5 faded bronze bags.
drab crimson bags contain 1 vibrant plum bag.
dim black bags contain 3 muted tan bags, 3 drab silver bags, 4 dull white bags.
faded yellow bags contain 5 faded black bags.
faded white bags contain 2 wavy lavender bags, 1 shiny orange bag.
plaid tomato bags contain 2 shiny brown bags, 3 clear red bags.
drab white bags contain 5 dark yellow bags.
mirrored tomato bags contain 2 light gold bags, 1 mirrored gold bag, 4 dim plum bags.
plaid maroon bags contain 2 mirrored lime bags, 3 plaid salmon bags, 2 shiny chartreuse bags.
drab gold bags contain 1 dim plum bag, 2 mirrored violet bags.
muted orange bags contain 3 mirrored lime bags, 1 muted maroon bag, 5 drab violet bags, 2 posh green bags.
mirrored fuchsia bags contain 3 dim plum bags, 2 muted olive bags, 2 wavy white bags, 1 dotted cyan bag.
plaid silver bags contain 3 pale violet bags, 5 striped purple bags, 5 dull purple bags.
dotted silver bags contain 2 vibrant coral bags.
shiny cyan bags contain 4 mirrored teal bags, 4 faded magenta bags, 4 bright lime bags, 1 vibrant teal bag.
clear yellow bags contain 1 muted brown bag, 5 wavy lime bags.
muted red bags contain 5 muted coral bags, 2 light violet bags, 2 muted indigo bags, 4 dotted tan bags.
dull beige bags contain 5 plaid black bags, 2 pale white bags, 2 light violet bags, 1 pale crimson bag.
vibrant lavender bags contain 3 dark chartreuse bags, 4 bright lavender bags.
posh lime bags contain 1 shiny cyan bag, 4 dotted blue bags, 3 mirrored chartreuse bags.
shiny blue bags contain 1 dotted magenta bag.
muted yellow bags contain 4 plaid salmon bags, 4 dull tomato bags.
muted blue bags contain 5 wavy magenta bags, 3 vibrant gray bags.
dotted tan bags contain 1 wavy green bag, 1 dim plum bag.
drab red bags contain 2 dark olive bags, 5 mirrored tan bags, 3 dull coral bags, 4 plaid yellow bags.
dull tomato bags contain 2 clear aqua bags, 2 dark fuchsia bags, 2 light teal bags.
bright salmon bags contain 5 dark blue bags.
pale olive bags contain 1 light violet bag, 3 shiny bronze bags, 2 dotted magenta bags, 4 posh silver bags.
mirrored teal bags contain 4 posh chartreuse bags, 5 vibrant bronze bags.
mirrored chartreuse bags contain 3 striped olive bags, 3 mirrored maroon bags, 5 faded black bags, 3 pale plum bags.
pale orange bags contain 4 mirrored gold bags, 3 faded brown bags, 2 dark olive bags.
dark olive bags contain no other bags.
faded plum bags contain 5 bright green bags, 5 shiny beige bags, 2 vibrant indigo bags, 1 mirrored orange bag.
drab magenta bags contain 5 dark fuchsia bags, 5 striped salmon bags.
dark lavender bags contain 5 mirrored red bags, 4 vibrant aqua bags, 2 dotted tan bags.
shiny bronze bags contain 2 clear aqua bags, 2 dull salmon bags, 1 plaid turquoise bag, 3 plaid bronze bags.
faded magenta bags contain 2 mirrored gold bags, 5 dim orange bags.
light lavender bags contain 3 striped magenta bags, 5 light yellow bags.
clear tomato bags contain 3 dark bronze bags, 5 plaid aqua bags, 2 faded lime bags, 2 bright salmon bags.
clear lime bags contain 1 mirrored lavender bag, 3 bright silver bags, 3 pale teal bags.
light lime bags contain 4 dim crimson bags, 2 vibrant tomato bags, 4 posh red bags.
wavy yellow bags contain 3 muted chartreuse bags, 3 drab teal bags, 4 striped tomato bags.
dark silver bags contain 5 posh magenta bags, 1 plaid black bag, 3 faded brown bags.
bright maroon bags contain 5 dotted turquoise bags, 3 wavy silver bags, 2 dotted lime bags.
striped orange bags contain 5 striped coral bags, 3 posh teal bags.
bright silver bags contain 3 mirrored violet bags, 5 striped gold bags, 1 striped white bag, 4 clear chartreuse bags.
mirrored olive bags contain 4 light silver bags, 1 muted crimson bag.
dim gold bags contain 3 clear magenta bags.
shiny plum bags contain 5 muted olive bags, 5 dark turquoise bags, 2 dull green bags, 1 plaid magenta bag.
mirrored green bags contain 5 striped magenta bags, 1 light lime bag, 2 dim cyan bags.
wavy aqua bags contain 4 dull tan bags, 5 vibrant beige bags.
posh lavender bags contain 4 muted black bags.
dull lime bags contain 2 plaid black bags.
dim chartreuse bags contain 4 bright red bags.
muted lavender bags contain 5 faded red bags, 5 drab brown bags, 5 clear bronze bags.
muted coral bags contain 4 clear red bags, 3 vibrant maroon bags.
bright lavender bags contain 4 striped blue bags.
""")
