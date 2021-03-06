import enum


class TokenType(enum.Enum):
    INT = 1
    ADDITION = 2
    MULTIPLICATION = 3
    PARENTHESES_OPEN = 4
    PARENTHESES_CLOSE = 5


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        return


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        return

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def solve(self):
        if self.value == TokenType.ADDITION:
            return self.left.solve() + self.right.solve()
        elif self.value == TokenType.MULTIPLICATION:
            return self.left.solve() * self.right.solve()
        else:
            return self.value


def get_tokens(problem):
    tokens = []
    current_term = ""
    for i in problem:
        if i == " ":
            continue
        elif i == "(":
            tokens.append(Token(TokenType.PARENTHESES_OPEN))
        elif i == ")":
            if current_term:
                tokens.append(Token(TokenType.INT, int(current_term)))
                current_term = ""
            tokens.append(Token(TokenType.PARENTHESES_CLOSE))
        elif i == "+":
            if current_term:
                tokens.append(Token(TokenType.INT, int(current_term)))
                current_term = ""
            tokens.append(Token(TokenType.ADDITION))
        elif i == "*":
            if current_term:
                tokens.append(Token(TokenType.INT, int(current_term)))
                current_term = ""
            tokens.append(Token(TokenType.MULTIPLICATION))
        else:
            current_term += i
    if current_term:
        tokens.append(Token(TokenType.INT, int(current_term)))
    return tokens


def build_tree(tokens_queue, precedence):
    """
    backus-naur form (for NO precedence):
    <expression> ::= <term> ( ("*"| "+") <term> )
    <term> ::= "(" + <expression> + ") | <int>
    <int> ::= /\\d+/

    backus-naur form (for precedence):
    <expression> ::= <additive> ( "*" <additive> )
    <additive> ::= <term> ( "+" <term> )
    <term> ::= "(" + <expression> + ") | <int>
    <int> ::= /\\d+/
    """

    def get_int(tokens_queue):
        return Node(tokens_queue.pop().value) if tokens_queue[-1].type == TokenType.INT else None

    def get_term(tokens_queue):
        if len(tokens_queue) > 0 and tokens_queue[-1].type == TokenType.PARENTHESES_OPEN:
            # parentheses
            tokens_queue.pop()  # (
            expression = get_expression(tokens_queue)
            tokens_queue.pop()  # )
            return expression
        else:
            return get_int(tokens_queue)

    def get_additive(tokens_queue):
        left_hand = get_term(tokens_queue)
        if len(tokens_queue) > 0 and tokens_queue[-1].type == TokenType.ADDITION:
            node = None
            while len(tokens_queue) > 0 and tokens_queue[-1].type == TokenType.ADDITION:
                tokens_queue.pop()
                right_hand = get_term(tokens_queue)
                node = Node(TokenType.ADDITION)
                node.set_left(left_hand)
                node.set_right(right_hand)
                left_hand = node
            return node
        else:
            return left_hand

    def get_expression(tokens_queue):
        if precedence:
            left_hand = get_additive(tokens_queue)
            if len(tokens_queue) > 0 and tokens_queue[-1].type == TokenType.MULTIPLICATION:
                node = None
                while len(tokens_queue) > 0 and tokens_queue[-1].type == TokenType.MULTIPLICATION:
                    tokens_queue.pop()
                    right_hand = get_additive(tokens_queue)
                    node = Node(TokenType.MULTIPLICATION)
                    node.set_left(left_hand)
                    node.set_right(right_hand)
                    left_hand = node
                return node
            else:
                return left_hand
        else:
            left_hand = get_term(tokens_queue)
            if len(tokens_queue) > 0 and (tokens_queue[-1].type == TokenType.ADDITION or tokens_queue[-1].type == TokenType.MULTIPLICATION):
                node = None
                while len(tokens_queue) > 0 and (tokens_queue[-1].type == TokenType.ADDITION or tokens_queue[-1].type == TokenType.MULTIPLICATION):
                    operation = tokens_queue.pop().type
                    right_hand = get_term(tokens_queue)
                    node = Node(operation)
                    node.set_left(left_hand)
                    node.set_right(right_hand)
                    left_hand = node
                return node
            else:
                return left_hand

    return get_expression(tokens_queue)


def solve_for_terms(terms):
    total = 0
    current_operator = "+"
    for term in terms:
        if isinstance(term, list):
            inner_total = solve_for_terms(term)
            if current_operator == "+":
                total += inner_total
            elif current_operator == "*":
                total *= inner_total
            current_operator = None
        elif term == "+" or term == "*":
            current_operator = term
        else:
            if current_operator == "+":
                total += term
            elif current_operator == "*":
                total *= term
            current_operator = None
    return total


def solve_problem(problem, precedence=False):
    tokens = get_tokens(problem)
    tokens.reverse()
    tree = build_tree(tokens, precedence)
    return tree.solve()


def solve(puzzle_input):
    problems = puzzle_input.strip().split("\n")

    # part 1
    total = 0
    for problem in problems:
        total += solve_problem(problem)
    print(total)

    # part 2
    total = 0
    for problem in problems:
        total += solve_problem(problem, True)
    print(total)
    return


solve("""
(9 + (5 + 2 + 2 * 4) * (7 + 7 * 5 * 3) + 7) + 2 + 4 * 2 + 3 * (8 + 5)
3 + 5 + (9 + 2 * 5) + (6 * 4 + 8) * 9 + 3
6 + 4 * ((4 * 8 * 3 * 5) + 8 * 6 + 7 + 6 * (3 + 5 + 6 * 4)) * 2 * 7
4 * (9 * 2) + 2 + (3 + 2 * 5 * (5 * 3 + 9 * 5 * 9) + 4 + 9)
(9 * (7 * 7 * 2 + 3 + 8 + 8) + 5 + 5) + 9 * 6
4 + (2 + 2 * 6 + 3 * (9 * 8 * 3) * 2) * 2 * (8 + 7 * 3 * 9 + 2 + 4) + 7 + (4 * 7 + 3 + 2 + 4)
(2 * 3) * 4 + 9 * 7 + 5 + 9
9 * (9 + 4 + (6 + 2 + 8 + 6 * 4) * 6 + (7 + 7 + 9)) + 9
7 * (9 + 2 + 8) + 3 + (5 * 5) + 9
6 * ((8 + 9 * 9 * 5 * 5) * (4 * 9 + 5) + 3 + (2 + 9 * 4 + 5 * 6 * 3) * (9 + 8 + 3)) + 7 + 3 * 2 + 9
(2 * 9 * (9 + 3 * 3 * 3 * 7 * 4)) + 2 + ((3 + 5 + 7 + 9 + 7) * 2 + 5 * 5 * 9)
2 + 5 + 3 + (8 + (8 + 8 + 4 * 9 * 7) * (8 * 6 + 2) * 9 + 2 + 6) * 3
(8 * 8 * 7) + 5
(3 * 5 * 9 * (2 + 9 + 5 * 3)) + (7 + 2 + 8) + 2 * (8 * 2)
8 + 2 + (3 * 7 * 2 + 9 + 9) * 3 + ((3 + 2 * 6 + 8 * 6 * 8) + 3 * 8 + 7) + (2 * (7 + 7 + 7 * 6 * 9 + 5) * 3 + 3 + (7 + 9))
6 * (3 * 8 + 3 * 9 + 7 * 2) + 9 * 7 * 3 + (9 * 7 * 5 * 7 + (6 + 5) * 6)
4 * (6 * 3 * 9 + 5 + 2 * 2) * (2 * 5 * 2 * 6 * (9 + 9 * 7 + 6 * 8))
(9 + (2 + 7 + 8)) * 6 + 5 + 6
6 + ((4 + 5 * 9) + (9 + 4 * 7) * 6 * 7 + (3 * 2 + 9 + 4) * (6 * 3)) + 5 + 6
4 * 4 + 9 + 9
2 + 5 * (8 * 2 * 3 * (2 + 3 + 3 + 3 * 5) + (7 + 8)) * 6 + (9 + 8 * (9 + 8) * 3 * 3 * (2 * 8 * 5 + 6)) + 5
7 * (4 * (8 + 8 * 3) + 7 + 3 + 6 * (8 + 4)) + 2 * 8
5 * (3 + 7 * 4 * (4 + 8 + 8 * 2 + 6) + (5 * 6 + 8 * 5 + 8)) * 6
(9 * 2 + 7) + 9 + 9 * 6
3 + 6 + 7 * (7 + (7 * 9 + 5 + 5) * 7) * (7 * 9 * 9 * 2 * 2 + 7)
5 * (8 * 9) + 6
9 + (6 + 4 * 5) * (2 + 7 + 9 * 2 + 7) + 5 * (8 * 4 * 3 * 7 * 5 * 3)
6 * (9 * 6 + 4 * 8)
4 * (6 * 7 + (4 + 2 * 3 + 3 * 5) * 6 * 7)
6 * (5 + (2 * 4 * 5 + 7 * 8 * 5) * 6 * 2 + 6 * 3)
((7 + 2 + 8) + 2 + 7 + (4 * 3 * 4) + 3 * 6) + 6 + 2 * (8 + 8) + 2
7 + (6 * 9 * (9 * 5 * 2)) * 4 * (7 + 5) + 5
5 + 8
9 + 2 * 6 + (9 * 2 + 2) * ((9 * 4) + (9 + 9 + 8) + 3 * 4 * 8 * (9 + 8)) + 2
(8 * (5 + 8 * 4 * 2) * 5 * 5 + 5 * 3) + 4
4 + (2 * 4 * 9 * (6 * 8) * 8) + 6 * (3 * 2 * 8) + (5 + 2) * 9
((4 + 9 + 5 * 2) * 6 * 7 + 3 * 7 + 9) * 9 + 7 * 4
(5 + 9 * (7 + 3 * 4 * 5 * 3 * 6) + (8 + 8 * 8 + 8 + 2)) * 6
3 + 6 * 3 * (2 * 4 + 8) * 5
2 * 9 * 5 * (9 + (7 + 3 + 3 * 9 + 9 * 5) + (7 * 7 * 6)) * 3
6 * 9 * 7 * ((3 + 9 * 9) * 2) * 7 + (8 + (9 + 7 * 6 * 6 * 3) * 2 * 7 + (2 * 3 * 2 + 3) * (4 * 3 * 7))
(3 + (3 * 2) + 3) + 2
5 + (9 * (4 + 3 * 2 + 2 + 7) + 4 + (4 + 9) + 6) * 3 * (3 * (9 * 5 * 8 * 7 + 7 + 9) * 5) + (2 + 4 * (3 + 5 * 5 * 4 * 5 + 4) * 5 * 6 * 3) + ((2 + 7) * (8 + 2 + 4) + 8 + 7)
4 * 9 + 9 * (3 + 5)
(5 + 2 * 3 + 6) * 4
6 * (5 + 5 * 2) * 3 * (7 * 7 + 4 + 5 + 8 + (3 + 2 + 6 * 4 * 4 + 5)) + 8 * 8
6 * 2 * 9 + 2 + 9 + (8 * 9 + 8 + 7 * 3)
5 * 6 + 4 * (2 + 6 + 6 + 4 + 5)
(4 + 5 + 5 + 3 + 2) + 4
((8 + 9 + 9 + 9) + 7) + ((2 + 6 + 7 + 7 * 2) * 9 + 3 + (9 + 9) + 8 * 4)
6 * 5 + 6 * 9 * 4
8 + (4 * 6 + 8 + 8 + 3) + 5 + 9 * ((8 * 9 * 5 + 6) + 2 + 9) + 3
9 + (9 * 2 + 6 + 7 + 5 * (9 + 5 + 7 * 3 * 7 + 6)) * 3
((9 * 8) * 4) * 6 * 7 + 9 + (4 * (7 * 3 + 2 * 8 * 5 * 5) + 6 + 8 * 5 + 7)
3 * (6 + 2 + 2) * 8 + (5 + 4 + (5 + 4 + 6 * 9 + 2) + 9 + 7) * (9 + 2 * 7 * 6 + 4 * 5) * 9
(7 + 3 * 4 + 2 + 5) + (7 + 2 + 6 * 9 + 7) + (8 * 4 * 2 * 7 * 7 + 5) * 2 * 7 * 2
7 + 5 * 2 * (3 * 7 * 9 * 9) * (9 * 7 * 3 + 6 + 7)
3 * 4 * ((4 * 7 * 4 * 8) * (8 * 5 + 4 * 3 * 4 * 8) * 8 + 7) * ((6 * 5 * 5) + (6 + 4 * 6 + 3 + 5 * 8)) * 9
(8 + 2 * 5 + 9 * 8) + ((6 + 6 * 3 + 8 * 5) + (5 + 7) * 9 + 2) + 5 + 5 + 7 + 8
8 + 3 * 7 + (6 * 5 * 7) + 9 + 8
8 * ((3 * 7) + (8 + 6 + 5) + 4 * 4 * 7 + 3) + (4 * (8 * 4 + 5 + 8 * 2)) + 7 + 4 * 8
7 * 5 * 9 * 2 * ((3 + 3) * 5 + 4 + 2 * (5 * 5 * 6 + 4) * 5) * 3
7 * (8 + 6 + 2) * 3 * 9
8 * ((8 * 7 + 9 + 9 + 2) * 5 * (9 * 9 + 5 * 2 + 4 * 8)) + (5 + 2 * 9 + 6) * 5 + 9
2 + (5 + (2 + 3 * 5 * 5) * 7 * 8 * 7 + 4) * 2 + 7
9 * 6 * 2 * 2 * (3 + 3 + 3)
9 * (3 * (7 + 2 * 3) * (3 * 6 + 9) + 4)
5 * 9 + 4 + 3 + 6 + 3
3 * 6 * (6 * (6 * 2) + 7 * (4 * 6 * 2 * 3 + 7)) + 6 * 4 * 8
(2 + 3 * 4 + 6 + 6 + (4 * 3 * 8 + 6 + 2)) * 7 * 6
(2 * 6) + 2 * 6 * 4
8 + ((9 * 5 + 2 * 4 + 9) + 8) * 5 + 2
7 + 4 * (8 * 6 + (3 + 5 * 8 + 8) + 9) + 5 * 8
(5 * 9) * 9 + 8 * 6 + 5
((3 * 9 + 3 + 2 * 2) + 2 * 3 + 5 + 8) * 4 * ((7 + 9 * 2) + 5 * 6 * (3 * 7 + 2 + 9))
((9 + 5 + 9) + 7 + 9) + (3 * 7 + 6 * 5 * 8 * 3) + 8 * 7
4 + 4 * 4 + (5 + (3 + 4 + 6 + 9 * 5) + 7 * 8 * 2 * 2)
((4 + 4 * 5) * (3 + 4 * 7 * 9 + 2 + 4) + 8 * 4 * 5 + 8) * 7 + 3 + 3 * 9 * ((8 + 3 * 3 + 2) * 3)
((7 * 5 * 3 + 5 * 2 * 6) * 8 * 6 + 8) * 5 * 2 + 6 + 5 * (4 * (6 + 2 * 9 * 3 + 2) + (8 + 2 * 7))
3 + 7 * 6 + 9 * 9 + 2
9 + 8 * (9 + (2 * 6 * 4) * 7) + 3 + 6 * 5
(8 + 8 * (9 * 3 * 4 + 3)) + ((3 + 6 + 2) + 5 * 6 * 3 * 3 + 9) * 8
4 + 8 * (3 * (6 + 9) + (2 + 9 + 2) * 4 + 7 + 2)
9 * 7 + (2 * 8 * 5 * (2 * 7) * 2 * (3 + 2 * 7 + 4))
9 + 6 * (9 * 3 + 4) + 7 * 8 * (5 * 6 * 3 + 3 + 5 * 5)
8 * 7 * ((3 * 2 + 5 + 8 * 3 * 2) + 8 * 2)
(4 + 2 * (7 * 2 * 7) * 7 * 3) + 6 + 2 + 7 * 8
((4 * 9 * 3 + 7) + 5 * (2 * 6 * 8) + 9) + 3 + 9 + (2 * 8 * 5 * 6 * 5)
8 * ((2 * 4 + 2 + 7) * 5) * (8 * 8 + 7 * 9 + 4 + 4)
6 + (3 + 8 + 3 + 2) * 3 * (7 + 7 + 2 * 4 + 8)
3 + 6 * 6 + 2 + ((4 + 6 + 6 * 3) * 2) * 4
(6 * 4 + 4) * (9 + 2 * 4 + 5 + 5 + 5)
2 + 7 * 9 * ((2 * 4 + 5) * 9 * (5 + 6 * 5)) * (9 + 2 * 9 * 9 * 4 + 3) * 4
9 + ((6 + 7 * 8 * 6 * 6 + 7) + (7 + 5 * 7 + 7 * 4 * 3)) + (9 * (3 * 2 * 7 + 6 * 4 + 6) * 3 * 9 * 9)
6 + 7 * (8 + 5) + 3
(6 * (2 + 7 + 2 * 7 + 8) * (7 * 7 + 5 * 8 * 5) * 5 * 3 * (5 + 4 * 6 * 6 * 3 + 9)) + 6 * 7 + 4
5 * 9 * (5 * 4 + 6 * 7)
6 * 6 * 5 * (5 + (4 * 5 + 5 + 2) + (6 * 7 + 4) * 7) * (3 + 3 + 2 + 7 * (4 + 8 * 5 + 7 + 9))
(9 * 8 * 7 * 9 * 2 + 5) * 3
(9 + 6 * 8 + 9 * 8 * 8) + 3 + (9 * 2 * 9 * 5 + 2)
(4 * (4 + 6 + 6 * 9 + 8 + 2) * (6 * 2) + 2) + 4 * 8 * 6 * (6 * 6) + 8
8 * 7 * 5
9 + (5 + 3 * 7 * 7 + 3 + 4) * (9 * 5 + 8 + 7 * 4) * 7
9 + (8 * (8 + 7 * 4)) * 6 + 5 + 4 * 9
5 + 4 + (2 * 5 + (5 * 4 + 2 * 9 * 4)) + 5 * 2 * 6
3 * 9 + (5 + 3 + 4 * 8) * 6 + 8
8 * (8 * (3 * 6 * 4) * (3 + 6 * 5 * 9 + 3)) * (3 + 6 + (5 + 4) * (9 * 6)) + 7
8 * 2 + (9 * 6 * 4) + 7 * (4 * (9 * 4 * 4 * 9) * (5 * 9) * (3 * 4 * 3 * 6 * 3 * 6))
(2 * 8 * 2 + 3) * 6 + 9 + 7 * 5
(8 + 9 * 9 * (7 * 4 + 9 + 4 * 4 * 8)) + (2 + 6 + 4 + 2 * 6) + ((4 + 8 * 2) * 9 * (2 + 7 + 6 * 3 * 6 + 4) * 9 + (7 + 2 * 3 * 4) * 2) + 8 + 4 + 4
4 + 5 * (7 * 4 * (2 * 9 * 4 + 2 + 7 + 7) + 2)
8 * (2 + 3 + 8 + (2 * 5 + 6) + 3 * 6) * 9 * 8
8 + (2 + (3 + 2 * 3 + 9 * 2 + 7) * (7 * 5)) + 2 + 8 * 8
6 + 7 + 9 * (6 + 3 * 9) + (2 + 6) * 9
2 * ((6 * 4) * 8 * 8) + 2 * 4 * 6
9 + 6 + 4 * 7 * 4 + ((9 * 6 * 8) * 8 * 2 + 6 * 6)
3 + 3 + 7 * 8 + 5
4 + 2 + (2 + 7 * (4 + 6) + 3 * 4 * 9) * 2 + 8
5 * 9 * (3 * (8 * 8 + 2 * 5) * 3 * 9 + 3)
2 + 8 * 4 + (2 * 7) * 5
4 + (3 * 3) * ((3 * 8 + 6 * 4) + (4 + 6) * (2 + 6 + 4 + 3 + 9) * 9 * 5 * 6) * 7 * 9
3 * 9
4 + 8 + 2 * (6 + 4 + (8 * 4) * (9 + 4 + 2) + 7) * (9 * 7)
6 * 6 * (5 * (2 * 3 * 8)) + 3 + (8 * (9 + 6 * 2 + 8 * 4) * (2 * 8)) * 8
((7 + 5 * 4 + 8 * 6 + 3) * (8 + 9 * 2 * 7 + 7 + 3) * 9) * 5 + 7 + 7 * 5
5 * 4 + (5 + (2 + 7 * 9) * 2 + (4 * 7 + 8 * 9 * 5 + 7) * 9 * 4) * 4 * 5
4 * (2 * 9 + 9 * 9) * (9 * 2 * 3 + 8) * 3 + 5
9 + (3 * 8 + (9 * 6 * 3)) + 2 + ((5 * 8) + 5) * (5 + 5 + 2 * 7 + (4 + 4 + 5 + 9 * 2 * 2) * 7)
(2 + 4 + 4 + 6 * 5) + 2 * 8
5 * 5 * ((4 * 8) + 6 * 5) * 5
(6 * (4 + 9 * 3) * (2 * 8)) * 3 + 5
6 * 2 + 9 + (4 * 9 + 2 * 2) + (5 * 8 + 5 * 4 * 2 * (4 * 5 * 6 + 8)) + 4
(6 + 8 * 6 + 9 * 8) * (4 * 8 + 8) + 7 + 5
5 * (2 * 6 * 2 * 2) * 9 + (4 + (2 * 3 * 5) * 7 * 2)
5 + 3 + (7 * 4 * 8 + 6) + 9 * 4 + (5 * 8 + 6 + 9)
9 + 4 + (8 * (4 + 2 * 7)) + 9 * (4 * 7 + (5 * 7 * 8 + 6) * 5 * 2)
7 + 9 + 5 + 8 * 2 + ((4 + 3 * 9 + 8 + 3 * 7) * (5 * 6 * 7 + 4))
6 * (4 + (5 + 7 * 7 * 9 + 4) * 6 + 9 + 3)
(6 * (5 + 5 + 9 + 2 * 2) + 7 * 8 + 3 * 8) + 3
(2 * 9 + (5 + 7 + 2) + 6 * 5) + 4
9 + (7 + (8 * 9) * 4) * 6 * 4
((3 + 2 + 9) * (6 * 6) * 8 * 8) + 6 + 2 + 7 * 8 + ((3 * 7 + 5 * 2 + 7) * 5 + 8)
4 + 8 + (6 + 4) + 7 + (4 * 6 + (9 + 8 * 2 * 6 * 2 + 8) + 7 + 2)
(7 * 2 + (8 * 3)) + 3 + 5 * (4 + 9 + 9 + (9 + 6)) * 4 * 5
5 + ((2 * 2 * 2) * (7 * 7) * 6 + 6 + 8 * (3 + 3 + 2)) * 3 * 7
9 * 6 * 6 + 5 * 6 * (7 * 8 + 9 * 4 * 2 + 7)
2 + (8 * 3)
(4 * (4 * 2 * 9 * 9 + 6) + (6 + 6 * 9) * 2 + 2) + ((4 + 9 + 6 + 4 + 9) + 7 * 7 * 2 + 4 + 3) * 2
9 + 5 + 4 * 9 + 3 + (7 * (7 + 7 * 8) * 2 + (9 + 6 + 6 * 8))
2 * 8 + 6 + 4
4 * (7 + 4 * (6 * 6 * 8 * 9 * 2) + 6) + 9 + 7 + 7 * 4
7 + 2 * 3 * 3 * (6 * (8 + 3) * (5 * 6 * 7 * 6 * 9 * 6) * 8) * 9
7 + 4 + 5 * (5 * 4 + 9)
3 + 4 * 9 * 3 * 2 + 8
(2 * 6 * (7 * 3)) * 2 + (4 * 9 * (6 + 7)) * 2
4 + 5 + (3 + 9 + 8 * 3 * (6 * 4 * 4) * 2)
(9 * 3) + (7 * 7 + 2 + 4 + 2 * (9 * 9 * 5))
((9 + 7) * 9 * 4 + 5 + 5) * 5 + 7
3 + (2 + 5 * 6 * 2 * 5) * 4 + 2 + (9 * 9 * 6) * 8
(4 * 3 + 7) * 8 * 5
5 * (7 + (6 * 3 * 7 * 2 + 6) * 4 + 7 * (8 + 2 + 8 + 2)) * 8 * (8 + 7 * 5 + 3)
(3 * 7 * 7 + 8 * 4 * (2 * 9)) * 9 + 8 * 9
5 + (4 + (4 * 4 + 5) + (7 + 9 * 7 + 5 + 4) + 2)
8 + 6 + 6 + ((8 + 5) + 7 + 2)
9 + 2 + 3
7 + (4 * 6 + (9 + 6 * 6 + 8) * 6) + (6 * 4 + 2)
8 + (2 * 6 + (5 + 2 + 5) * 6 * (7 + 9 + 7 * 8 + 5 + 9) + 2) * 6 * (8 + 6 * 9 + 7 * 2) + 8
(6 + 7 * 6 + 9) + 3 * ((8 + 4 * 4 + 6) * 3 * 6 + 4)
2 * 2 * (8 + 2 * 5 * 9 * 9) + (9 + 3 * 6) + 7
2 * (7 + 3 * 3 + 4) * 8 * 9
6 * 7 * 2 * 8 + (5 * 7 + 7 * 9 * (4 + 3 + 9 + 4 * 8))
2 * (6 + 8 * (8 + 6 + 4 + 7) + 2 * 7 + 6)
9 + (9 * 4) + 9 * (9 + (2 * 4) + 3 + 9) * 7
8 * (6 + 7) * (9 + 4 * 3 * 7 * (7 * 4 + 3 * 2 + 8 + 4) * 6)
(6 + 3 + 3 + 3 * 8 + (8 + 6 + 9)) * (2 + 8 + 6 * 6 * 9 + 6) + 8
4 * 6 * 5 + (2 * 5 * (3 * 3 + 8 * 7)) + 8
5 * 9 + 5 * 2 * (5 * 8 + 4 + 2 * 7) * 8
(5 * 4) * 9
5 * 6 + 7 * 4
7 * (5 + 5) + ((3 + 4 * 2 + 4) * 7) * 9 * 4 * 3
3 + (5 * 8 * 8 * 4 + 5 * 8) * 9 * ((2 + 6 + 9 + 3) * 6)
5 * 5 * (2 * 7 + 9 * (5 + 3 + 3) * 4 * 9) * 8 * 3 * 3
6 + ((2 + 3 + 2) * 5 + 3 + 3) + (8 * 2 * 9) * 6
(5 + (2 * 5 * 9 + 3 * 8 + 2) + (5 + 4 * 2 * 9 * 9 * 4) * 7 * (9 + 5 + 2)) * 2 * 9 + 8 * 5
2 * (2 * 9 * 2 * 9 * 2 + 6) + 2 + (5 * 9 + 7 * 5 * 9) * 9
3 + (6 * 9) + 6 * 4 * 5
((9 + 4 * 6) + 9 + 4 + (6 + 4 * 6) + 4 + 5) + 9 * 7 + 6
(2 + 9 * 4 * 7 + 9 * 9) * 4 * 3 + 2
(2 * 7 + 7 + 9 + 4) * 5 + 7 * (6 * (5 * 8) * 4 + 4) + 7 + 3
8 * 5 * (6 + 3 * 3 * 9 * (5 * 4 + 4 + 5 + 5)) + 6 + 8 * 7
7 * 7 + ((8 * 7 * 4) + 7)
9 + 6 * ((4 * 8 * 5) + 4 + 4 * 6) + 7
9 + ((7 + 6 * 3 + 9 * 4) + 9) + (2 * 7 * 8 + 3 + 7 * 3) * 6
((2 + 4 * 9) * 9 + 7 + 7 * 5 * 6) * 6 + 8 + 5 * 6 * (6 * 9 * 3 * 5 + (9 * 6 * 5 * 8 * 9 * 2))
(9 * 3) * 3 + 4
(3 * (3 + 9 * 5 + 5 + 9 * 2) + 9) + (5 * 5 + 8) * 6 * 7 * 5
4 + ((3 * 2 * 5 + 9) * 8 * 9 + (8 + 9) * 7) + 9 * 8
(9 * 4 * 3 + 9 + 2) + 9 * (3 + 9 + 3) * ((7 * 6 * 4) + 7 + 9 * 8 * 4)
2 + 6 * (8 + 8 + 5 + 6) * (3 + 2 + 8 * 7 + 6)
3 + ((5 * 2) * 9 + 5 + 3 * 2 + 2)
7 + 8 + (2 + 4 + 2 + 5 + 3) * 9 + 4 * 6
2 + 2 + 5 + 3 + ((2 * 2 + 6 + 2 + 7 + 7) + (7 * 4))
5 + (8 * 8 * (4 + 5 + 5 * 9) * 7) + 8
(7 * 2 * (8 + 3 + 3 * 7 + 7) * 5) + 2 * 9 + (6 * 7 + 5 + 3 + 2) * (9 + 4 + (9 * 6 + 4) * 7) + 9
((9 * 2 + 6 * 3) + 2 * (4 * 3 * 8 * 8)) * (3 + 2 + 2 * 8 * (3 + 7) + 6) + 3 + 2
6 + 5 + 4
6 + ((4 * 8 + 8) + 7) * (3 * 2 * 6 + 9 + (5 * 6 + 6 + 6 + 6) * 9) * 3 + 6
6 + 9 * 2 + ((4 + 4 * 7 + 2) + 7 * (8 * 8 + 2 + 4) * 6 * 9 * 7) * 3
((7 + 4 * 5 * 6) + (8 + 8 * 6 * 5) * 4) * 2 + ((3 + 8 * 6) * 3 + (8 + 8) * 2)
7 + (9 + 7) + 3 + 9 + 4 * 8
6 * 5 * 8 + 9 * 9 * (9 + 8 * (9 * 5 + 9) * 3 * 4 + 2)
4 * (3 * (4 * 9 + 4 * 4 + 6 * 3))
(7 + 9 + 2 + 3 + (9 * 5 * 5)) * 8 + 4 + 9
(4 * 7 * (7 * 3) + 8 * 3) * 9
4 * 6 + 7 * 6 + ((3 + 5 * 9) + 8 * 2 + (7 * 4 + 6 + 6))
(2 + 4 + 7) * 7 * ((5 * 9 + 7 + 6 * 7) + 9 + 4 * (9 * 5)) * 7
4 + 7
(6 + 5 * 8) * 2 * 9 * 6 + 8 * 8
6 * 3 * 8 + (9 + (3 * 9 * 9 + 5) * 7 + 2 * 6) * 7 + (8 + 4 + 9 + 9)
(6 * (9 + 3) * 5) * 5 * 5
8 + ((9 + 9 * 7) + (6 + 8 * 3 + 7 * 3) * 5 * 4 + 5 + 7)
(4 + 6 + 2 * (6 * 5 * 3 + 6) * 7 * 3) + 4
4 * (5 * 2 + 5 + (7 + 9 + 9 * 6 * 6) + (3 + 2)) * 3 * (8 * 4 * (2 + 4 + 7 + 6) + 5) * 6 * 5
8 + 6 + 5 + 8
(7 * 4 + 3 + 5 + (2 * 9 + 7 * 8)) + ((3 * 9 + 4 + 7 + 9 * 2) * 4) * 5 * 5
8 * 4 + ((9 + 8 * 4 + 2 + 4) * 6 + 6 * 6)
4 * 6 + ((7 + 8 * 7) + (4 * 5 * 4))
7 + (3 * 2 * 2 + 3 * 7) + 7 + 3 + 4 + (8 * 8 * 7 + (5 * 2 + 9))
3 + 8 + (2 + 7 * 3 * 6) + 2
7 + ((5 + 6 * 6 + 3) + (6 + 9 + 7 * 3 + 7)) + 8 + (8 + 7)
((9 * 5 + 7 * 8 + 5) + 2 * 7 * 3) * 2 * 4 + (6 * 3 * (3 * 2 * 7 + 7 + 7))
(7 + (4 + 2 * 2) * 6 * 9 + (9 * 8) * 5) * 2
3 + (3 + 9 * 2 + 3) + 7 + 4 + 7 + (4 * 2 * (7 + 2 + 3 + 5) * 6)
9 * 8 + (8 * 6 * (9 * 8 * 9 * 6 * 6) + 6 * 3) * 2 + ((5 * 3) * 7 + 3 + 3 * 8 * 2)
4 + (5 + (5 * 6) + (8 * 9 + 9))
9 + 3 * 2
8 * (3 + 4 + 6 * (9 * 8 * 6))
4 * (2 + (5 + 7) * 8 * 6) * 7 * (3 * (8 + 2 + 8 + 5 + 7 * 7)) + (6 + 8 * 3 * 8 * 2 + 5) * 7
(5 * 7 + 4 * 6 + 4 * 8) * ((8 * 6 * 7 + 5) * 7 + 6 + 5) + 4 + 3 + (2 + (9 * 9 + 9 * 5 + 3) + 3 * 3 * 3)
9 + 9 + 9 * 6 + 8
3 + 7 * 5 + (6 * (6 + 6 + 5 + 6) * 3 * 2) + 3
(5 + 8 * 3 + 4) * 8 * (9 * 3 + 4 * 6 * (5 + 9 + 9 * 8) + 3)
2 * (9 * 2 * 6 + 2 * 6) + 5 * 7
(4 + 7) * 6 + 8 + 9 + (6 * 7) * 4
9 + 7 * (8 * 5 * 7 * (7 * 5 + 9 * 4 + 8)) * 7 + 4
3 * 6 + 6 + 2 + (2 * 5 * 8) * 8
(4 + 2 * 6) + 3 + (7 + (6 + 7 * 6 + 6)) * 6 + (4 * 6)
7 + 9 * (3 * (9 + 7 + 7 * 5) * (7 * 2))
((7 + 5 + 8) * (3 * 2 * 6 + 2 + 9 + 2) * 9 + (8 + 6 + 2 * 4 * 9) + (4 + 2 * 9 * 6 * 7 * 8) + 3) * 2 + 2 + (5 * 7 + 8 + 2 + 8)
((4 * 8) * 3 * 9 * 3 + 4) + (6 * 8) + 3
5 + 2 * (6 + 9 + 3)
5 * 4 + (6 + 2) * 4 + 8 + 6
(5 + 4 + 5 + (6 + 2 + 4)) + (7 * (2 + 5 * 9 * 8 + 3) + 4 + (3 * 9 * 5)) * (7 + 8 + 6 * 5 * 3) + (9 * 6 + 9 * 5 + 5 + 7) * (3 + 2 * 5 + 6 + 4 + 8)
2 + (8 + (5 * 4 * 2 * 4 + 6 * 8)) * 5 * 6
(2 * 6 * (5 * 8 * 8 + 7 + 4 + 6) * 6) + 6 + (6 * (6 + 3) + 5) + (3 * 8 + 4) * 6 * (5 + 5)
((3 * 7 + 4 + 5) * 6 + (6 + 4 + 2 + 8) * 9 + 7 * 6) * 9 * 5
2 + (5 * 8 + 6 + (3 + 4 * 5 * 5 * 8 + 4) * (7 * 9 * 6 + 3 + 4)) * 8 * 6
(7 + 6 * 5 * 6) * 3 + 4 * 7 * 4 * 8
7 * (7 * 9 * (9 + 3 * 4 * 8) + (2 * 9 * 5 * 9 + 9) * 6 + 3) * (2 * 5 + (9 + 3 * 9) + 9) * 6
2 + 5 + (7 + (4 * 9) * 2 * 5 * 9) * 4 * 2 * ((2 * 4) * 3 + 8 * 4 + 8 + 7)
4 + 2 + 3 + ((9 + 9 * 4 + 9) + 5 * 7 * (9 + 4 * 7 * 3) * (3 * 9))
(7 + 6 * 3 + (6 * 6 * 9 + 9 * 4 * 2)) + 8 * (4 * (9 * 6))
4 + (2 + 2 * 7 * 2) * 4 + 9 + 9
7 * 2 + 2 + 5 + ((4 + 6) + (8 * 6 * 2) * (2 + 6 * 5 + 4 + 9 * 6))
4 * (8 + 6 + 2) * 7
((5 * 9 * 2 + 3 * 8 * 4) + 9 * 7 + 7 * (2 * 3 + 4 + 6)) + 8 + 6 + 3 + 9
8 * (9 * (3 + 5 + 3 + 5) + 7 + 6 * 5 * 5) * 7
7 * 7 * (3 * 2)
4 + ((9 * 2 + 9 + 4 + 9 * 5) + 6 + 5 + 9 * 8) * (8 * (4 + 9 + 8 * 2) * 5 * 9 + (8 + 7 * 8 + 3 + 8) * 6) + 7 + ((5 + 2) * (2 + 7) * (4 * 9 + 6) + (6 + 8 + 5 + 2 + 2 + 2) + (6 + 6)) + 6
5 * (5 * (4 * 7) + (3 * 5 + 8 + 2 + 3 * 2) * 9 * 2 + 8) * (4 * 7 * 2 * 7 + 4 * 3) + 3 + (8 + 3 * 6 * 5 + 6)
3 * (9 * 2 + 9) + ((4 + 4) * 7 + 7 * 7 * 6 * (5 + 5 + 2 * 4 + 4)) * 7 * 8
((5 + 3) + 3 + 6 * 9) * 9 + (3 * 7 + (3 * 6 * 2) * 9 * 8 + 6) + (5 * 8) + (4 + 7 + 4 + 4) + 6
2 + 8 * 4 + (8 * 8 * 4 * 7)
2 * 4 * (5 + 3 + 6 + 5 + 2) * 3 * (2 + 4 * (2 + 8 * 6 + 2 + 2 * 3) * 3 + 9)
(2 + (8 * 4 * 8 + 4 + 8 + 7) * 3 + 9) * 5 + (3 + (3 * 8 * 4 * 4) + 3 * 9)
5 + 2 * 7 + (3 + 2 * 7 + 6 + 6) * 8 * (3 + 4 * (3 * 3 + 3 * 2))
(9 + 2) * (5 + 6) * 2
(8 * 6 * (9 * 9) * 5 + (8 * 6 + 4 * 2)) * (2 + 2 * (2 * 3 + 5 + 6))
((2 * 4) * 4 * (9 * 3 + 6) * 4 + (4 * 6) + 4) + 9 * (3 * 6 + 2 * 7 * 7 + 3)
3 * (6 + 9 * 7 * 8 + (7 * 8 * 5 * 7 * 2) + 8)
8 + 8 + (6 + (5 * 8 + 6 + 7 * 4 + 7) * (2 * 3) * 4 * 2 + 5) + 5 * (8 * 3 + (7 * 7 * 2)) * 7
3 * 5 * 7 + 6 * 9
((7 + 5) * 4) + 3 + 6
(4 + 2 * (6 * 7 + 3 + 6 + 5 + 2) + (9 * 5 * 2 * 3)) + 4
((7 + 6 + 6 * 2) * (9 * 9 + 7 * 9 * 3 * 3) * 2 + 2 * 9) + 3 * 2 + 7 * 7
((4 * 7 * 3 * 5 + 4 + 4) + 3 * 5 + 6) * (5 * 4) * 4
3 * 3 + 9 * 9 + (8 + 2 + 5 + 2)
3 + 6 + 3 * (2 + (2 * 9)) + 9 + 9
(9 + 6 * 6 * 8 * 4) + 4 + 4 + 2 * 5 + 5
(2 + 3 * 5 + 2 + 4) + (7 + (9 * 8 + 2) * 7 + (6 * 7)) * 9 + 4 * 3
6 + (9 * (5 * 2) + 5 * 2 + 5 * 2) + 6
4 + 5 * ((5 * 9) + 4 + 5 + 2) * 4
((4 + 7 + 3) * (4 * 5) + 9 + 4) * 7
2 * 9 + 8 + (6 * 5 + 9 + 6) * (6 * 7 + 6 + 6 + (7 * 8 + 5 + 2 + 6) + 4) + (5 * 6 + 5 + 2 * 5)
4 + (9 * 5 + 4 * 5 + 5) * 9 + (7 + (2 * 5 * 4 * 7 + 2 + 9) * 3)
2 + 3 * 4 + 2 * (9 * 2 + 2 * 7 + 6 * 3)
3 * (7 * 6 * 5 * 4) + ((7 * 8 * 4) * 6) * 3
7 * (9 * 8) * 2 * 2
(8 * 9 + 5) * 2 * 7 * (4 * 2 + 6 + (9 * 6 + 9 + 3 * 7 * 6))
6 * (8 + 9 * 4 * 2 * 8 * 5) + 3
2 * 2 * (5 * 9 + 8 * 8 * 5) * (9 + 9 * 4)
6 * 4
(3 + 2 * (9 + 8 + 6 * 8 + 5) * (9 * 4)) + (5 * 9) + 2 + 9
(4 + 4 + 8 + 9 * 8 + 4) * ((4 * 2) + 9 * 2)
3 * ((2 * 8) * (7 * 5 + 9 + 4 + 5 * 5) + 3 + 8 + 5) * 2 * (4 * 8) * 5
4 + (7 * 9) + (3 + 8) * 7 * 3 + 8
5 + 3 * 9 * 9 + (8 + 9 * 6 * (6 + 9 * 3 + 7) * (8 + 2) + 5)
6 + 8 * ((3 + 5) * 3) * 5
2 + ((6 + 5) + 7) + (5 + 6 + 3 * 7 + 7) * 4 + 7
(9 * (6 * 7) + (6 + 3 + 8 * 4) * 7 * 2) * ((7 + 8 + 5 * 7) * 7 * 2) * (7 + 6 + 5 * 7 + 9) + (2 + 7 * 9 + (9 + 4 * 4 + 5 * 8 * 9)) * 9
9 + (4 * 2) + 5 + (6 + 7 * 9) + 6
5 * 5 + 8 + 4 * 4 * 7
8 + 4 * ((8 * 2 + 8 + 2 * 5) * (3 + 8) * 6 * 5) + 3 + 9
9 + ((9 * 9 * 3 * 5) * 6 * 4) * 7 * (6 + 7 + 5)
8 * 9 * 8 * (6 + 2 * 7 + 4 + 2 + (5 * 5 * 7 + 2)) * 3
7 * 5 * 5 + (5 + 4 + (3 * 3 + 9 * 7 + 7 + 5)) * 6
(3 * 2 * 7 + 5) * 4 + 2 * (3 + 3 * 7 * 9 * 3 * 2)
6 + 2 + (3 + (9 * 6 + 8) * (5 + 9) + 3) + 5
((8 * 4 * 6) * 2 * (4 + 9 * 7 + 6 * 6 + 2) * 9 + 4) + 5 * (5 * 2 + 8) + 9 * 7 * ((5 * 6 + 5 * 7 + 9) + 2)
6 + 2 * ((3 + 5 * 7 + 2 * 8 * 8) + (5 * 3 + 4 + 2 + 4) * 3 * 5 + 5) * 8 + 9 * 6
6 * ((3 + 7 + 8 * 6 * 6 * 2) * 7)
((6 * 6 * 6 * 9 + 8 * 7) * 6 * 7 * 4 * 6 * 6) + 5 * 3 + 8
(5 + 8 + 3) + 6 * (5 + 5 + 3 + 6) * (9 + 2 + 4 + 4 * 3) * 4 + 6
4 * 7 * (6 * 3 * 5 * (4 + 2 + 3) * (2 + 3 * 9) * 2)
7 * (2 * 5 + 5) + 9 + 5 + (3 * 2 + 3)
(4 + 6 + 5) + (6 * (9 + 7 + 9 + 2 * 6 + 4) * (9 + 2 + 6 * 7) + 2 + 3 + 7) + 5 + ((3 + 2 * 5) + 3 + 7 + (6 + 9 * 6 + 3 + 4)) + 2
(7 + (5 * 7 * 6 * 9 * 3) + 3 + 9 + (6 * 5 * 4 * 6)) * 2 + 6 + (9 + 5 * 9 + 8 * 4)
(8 * (9 * 4 * 6 * 8 + 8 + 9) + 6 * 9 + (2 * 6)) * (5 + 8 + 8) * 2 + 8 * 4 + 2
(9 + (6 * 5 * 9 + 4) * 5 * (8 * 7 + 7) + 6 + 3) * 7 + 7
6 * 2 + 8 * 3 + 5 * 8
9 * 3 * ((4 * 2 + 5 * 5 + 2) + 4 * 4) + (6 + 6 * 7 + 9 * 9) + (9 * 8 + 5 + 4 * 9)
9 * 5 * 6 * (4 * 4) * (9 + (4 + 2 * 7 + 3) + 9) + 2
((2 * 3 + 6 + 5) * 2 * 9 + (9 + 8 * 7 + 3 * 2 + 6) + 8) * 7 + 3 + 9 * 9
(3 * 2 * 7 + 6 * 8) + 4 + ((7 + 2) * 7 * (8 * 6 + 4 + 4 * 2 + 5) + 4 * (9 * 9 * 6 + 4 + 5 * 8) * 2)
9 + 6 * 8 * 6 + (8 * 3 + 9 + 4) + 6
(5 * (9 + 9 + 3 + 5) * 6 + 7 * 4 * 6) * 7 + (6 + (2 + 9 + 2 * 5 + 4) + (9 * 5 * 7 * 8 + 4) * 4 + 8 * 5) * 9 + 4
3 * (2 * (8 * 4 + 7) + 6)
(8 + 9 * 5 + 3 * 9 * 5) + 6 * ((6 * 8 * 6 * 4 + 9) + (2 * 5) * 2) + 4 + 9 + 7
5 * 3 * (2 * 5 * 8 * 6 * 7 * (4 * 8 + 3 * 7))
3 + 9 * 4 + 5 * 9
6 * 7 * 4 * 6 * 9 + (4 + 2 + (3 + 5 * 9 * 2 + 8) * 3 + (8 * 6) * 8)
(7 + 7 * 5 * 2 + (3 * 4 + 8 * 2 * 9 + 4)) + 5
(4 + 2) * 4 * 2 + 9 + (9 + 9 + 4 + 3 * 4 + 9) + (4 + 8 + 2)
((9 + 8 * 4 + 3 + 8 * 9) + 4 * 5 * 7 + 7) * 5 + 2
(2 * 7 + 6 * 5 * 6 * 9) * 9 * 2 * 8 * 7
(8 + 2 * 7 * 5) * 4 + 7
6 * 6 + (7 + 7 + 6 + 4 * 7)
9 + 5 + 2 + 4 * 9 + (3 * 6 * 5 * 3)
8 * 8 + 4 * 6 * ((6 * 3 * 5 + 5 * 6) + 3 + 6 * 6 + 8) * (2 * 8 + 9)
2 + 5
2 * 2 + 7 * 4 + (6 * 8)
4 * ((6 * 3) * 7 * 6 * 2 * 7 * 9) + ((4 + 5 + 2 + 4 * 8 + 9) + 4 + (3 + 5 + 3 * 9 + 9) + 5 * 4 + (4 + 5 + 6 + 3)) + 5
3 + (6 + 5 + 2 * 5 + 8) + 4 + 2 * 3
9 + 9 + (4 + 6 * 9 * 2) * 2 + 6 * 6
4 + 9 * 9 + 4 + (5 * 6 + (8 + 5 * 3) + (7 + 6 + 7) * 3) * 9
(7 + 2) + (4 + 6 * 5 * 7 + 4)
5 * (4 + (4 + 9) + (6 + 7 * 7 + 3) + (4 * 5 + 5 * 9 * 6) * (2 + 9 * 7)) * 5 + 7 + 3 * 6
8 * 5 * (3 + 4) * 9 * 5
9 + ((2 * 8 + 4) + 6 * 4 + (2 * 9) * 9 + 6) + (3 * 2 * 5 + (4 * 8) + (8 * 2) * 9)
4 + 8 + 6 * 9 * ((6 + 8 * 5) + 6 * 9)
(8 * 9 + 5 * 9 * 3 * 3) * 6 * 2
5 * 5 + 4
9 + (7 * 5 + 4 + 2 + 8 * 5)
(9 + (2 * 4 + 8) * (4 * 9 + 7 * 2 + 2) + 4) + 3 * 5 + 7 * 7
(6 * 2 * 9 * 8 * (3 + 4 + 3 + 2 + 7)) * 7 + 4 * 6
9 + 7 + (3 + (5 + 9 * 2 * 4 * 9) * (9 + 6 + 5) + 9 * 7 * 9) * 5
7 + (2 + 5 * 7 * 4) + 6
6 * 3 + (6 + 5 * (4 + 8 + 8) + 6) * 3 * 9 * 7
3 * (9 + 2 * (8 * 5 + 9 * 6 + 2 + 3) * 4 + 4 * 6) * 2 + 3
8 + 6 + ((2 * 2 + 7) * 7 + (8 + 2 + 2)) + 6 * 5
7 * (9 * 3 + (4 * 4 + 4) * 6 * (8 + 8 + 2)) * (5 * 4 + 6 * 8 + 3)
3 + 5 * (4 * (8 + 8 * 8 + 2) + 6 + 9 * 4 + 8) * 7 + (4 + 5 + (6 + 8 * 8) + 5 * 6)
4 * 8 * 6 + 7 * (5 + (3 * 2 * 2 * 5 * 8 + 7)) * 9
((8 + 5 + 6) + 3) * 3 * 5
((9 * 7 * 4 * 4 * 9) + 3 + 9 + 9 + 3 + 2) + 8 + 5 * ((6 * 5 + 3 + 5 * 3) + 3 + (3 * 6 * 5))
7 * 2 * 4 + 9
""")
