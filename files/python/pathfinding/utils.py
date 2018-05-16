import math

class DiagonalMovement:
    always = 1
    never = 2
    if_at_most_one_obstacle = 3
    only_when_no_obstacle = 4

SQRT2 = math.sqrt(2)

def backtrace(node):
    path = [(node.x, node.y)]
    while node.parent:
        node = node.parent
        path.append((node.x, node.y))
    path.reverse()
    return path


def bi_backtrace(node_a, node_b):
    path_a = backtrace(node_a)
    path_b = backtrace(node_b)
    path_b.reverse()
    return path_a + path_b


def manhatten(dx, dy):
    """manhatten heuristics"""
    return dx + dy


def octile(dx, dy):
    f = SQRT2 - 1
    if dx < dy:
        return f * dx + dy
    else:
        return f * dy + dx
