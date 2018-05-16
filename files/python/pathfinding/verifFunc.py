try:
    from files.pathfinding.a_star import AStarFinder
    from files.pathfinding.utils import DiagonalMovement
    from files.pathfinding.grid import Grid
except ImportError:
    from a_star import AStarFinder
    from utils import DiagonalMovement
    from grid import Grid

def isObstacle(titleMap, x, y):
    if x == 1 and y == 0:
        if titleMap[1][0] != 0:
            return 1
    elif x == 8 and y == 0:
        if titleMap[1][9] != 0:
            return 1
    elif x == 0 and y == 1:
        if titleMap[0][1] != 0:
            return 1
    elif x == 9 and y == 1:
        if titleMap[0][8] != 0:
            return 1
    elif x == 8 and y == 9:
        if titleMap[8][9] != 0:
            return 1
    elif x == 0 and y == 8:
        if titleMap[9][1] != 0:
            return 1
    elif x == 1 and y == 9:
        if titleMap[8][0] != 0:
            return 1
    elif x == 9 and y == 8:
        if titleMap[9][8] != 0:
            return 1
    elif x == 9:
        if y == 9:
            return 1
        elif y == 0:
            return 1
        elif titleMap[y-1][x] != 0 or titleMap[y+1][x] != 0:
            return 1
        elif y == 1 and titleMap[y+2][x] != 0:
            return 1
        elif y == 8 and titleMap[y-2][x] != 0:
            return 1
        elif titleMap[y-2][x] != 0 and titleMap[y+2][x] != 0:
            return 1
    elif x == 1:
        if y == 9:
            return 1
        elif y == 0:
            return 1
        elif titleMap[y-1][x] != 0 or titleMap[y+1][x] != 0:
            return 1
        elif y == 1 and titleMap[y+2][x] != 0:
            return 1
        elif y == 8 and titleMap[y-2][x] != 0:
            return 1
        elif titleMap[y-2][x] != 0 and titleMap[y+2][x] != 0:
            return 1
    elif y == 1:
        if x == 9:
            return 1
        elif x == 0:
            return 1
        elif titleMap[y][x-1] != 0 or titleMap[y][x+1] != 0:
            return 1
        elif x == 1 and titleMap[y][x+2] != 0:
            return 1
        elif x == 8 and titleMap[y][x-2] != 0:
            return 1
        elif titleMap[y][x-2] != 0 and titleMap[y][x+2] != 0:
            return 1
    elif y == 9:
        if x == 9:
            return 1
        elif x == 0:
            return 1
        elif titleMap[y][x-1] != 0 or titleMap[y][x+1] != 0:
            return 1
        elif x == 1 and titleMap[y][x+2] != 0:
            return 1
        elif x == 8 and titleMap[y][x-2] != 0:
            return 1
        elif titleMap[y][x-2] != 0 and titleMap[y][x+2] != 0:
            return 1
    elif x == 8 and y >= 1 and y <= 8:
        if titleMap[y][x-2] != 0 or titleMap[y][x-1]:
            if titleMap[y-1][x] != 0 or titleMap[y+1][x] != 0:
                return 1
            if y >= 2:
                if y <= 7:
                    if titleMap[y-2][x] and titleMap[y+2][x] != 0:
                        return 1
                else:
                    if titleMap[y-2][x] != 0:
                        return 1
    elif x == 2 and y >= 1 and y <= 8:
        if titleMap[y][x+2] != 0 or titleMap[y][x+1]:
            if titleMap[y-1][x] != 0 or titleMap[y+1][x] != 0:
                return 1
            if y >= 2:
                if y <= 7:
                    if titleMap[y-2][x] and titleMap[y+2][x] != 0:
                        return 1
                else:
                    if titleMap[y-2][x] != 0:
                        return 1
    elif y == 8 and x >= 1 and x <= 8:
        if titleMap[y-2][x] != 0 or titleMap[y-2][x]:
            if titleMap[y][x-1] != 0 or titleMap[y][x+1] != 0:
                return 1
            if x >= 2:
                if x <= 7:
                    if titleMap[y][x-2] and titleMap[y][x+2] != 0:
                        return 1
                else:
                    if titleMap[y][x-2] != 0:
                        return 1
    elif y == 2 and x >= 1 and x <= 8:
        if titleMap[y+2][x] != 0 or titleMap[y+2][x]:
            if titleMap[y][x-1] != 0 or titleMap[y][x+1] != 0:
                return 1
            if x >= 2:
                if x <= 7:
                    if titleMap[y][x-2] and titleMap[y][x+2] != 0:
                        return 1
                else:
                    if titleMap[y][x-2] != 0:
                        return 1
    elif titleMap[y-1][x] != 0 or titleMap[y+1][x] != 0:
        if titleMap[y][x-1] != 0 or titleMap[y][x+1] != 0:
            return 1
        elif titleMap[y][x-2] != 0 and titleMap[y][x+2] != 0:
            return 1
    elif titleMap[y-2][x] != 0 and titleMap[y+2][x] != 0:
        if titleMap[y][x-1] != 0 or titleMap[y][x+1] != 0:
            return 1
        elif titleMap[y][x-2] != 0 and titleMap[y][x+2] != 0:
            return 1
    elif titleMap[y][x-1] != 0 or titleMap[y][x+1] != 0:
        if titleMap[y-1][x] != 0 or titleMap[y+1][x] != 0:
            return 1
        elif titleMap[y+2][x] != 0 and titleMap[y-2][x] != 0:
            return 1
    elif titleMap[y][x-2] != 0 and titleMap[y][x+2] != 0:
        if titleMap[y-1][x] != 0 or titleMap[y+1][x] != 0:
            return 1
        elif titleMap[y-2][x] != 0 and titleMap[y+2][x] != 0:
            return 1
    return 0


def verifSaut(titleMap, posAndObjects):
    titleMapCaillou = titleMap
    for items in posAndObjects:
        if items[0] == "files/rocher.png":
            titleMapCaillou[items[2][1] - 1][items[2][0] - 1] = 2
        elif items[0] == "files/lave.png" or items[0] == "files/Mur.png" or items[0] == "files/Mur+.png" or items[0] == "files/MurH.png":
            titleMapCaillou[items[2][1] - 1][items[2][0] - 1] = 3
    for x in range(0, 10):
        for y in range(0, 10):
            if titleMapCaillou[y][x] == 2:
                titleMapCaillou[y][x] = isObstacle(titleMapCaillou, x, y)
    for x in range(0, 10):
        for y in range(0, 10):
            if titleMapCaillou[y][x] != 1:
                titleMapCaillou[y][x] = 0

    titleMapLave = titleMap
    for items in posAndObjects:
        if items[0] == "files/lave.png":
            titleMapLave[items[2][1] - 1][items[2][0] - 1] = 2
        elif items[0] == "files/Mur.png" or items[0] == "files/Mur+.png" or items[0] == "files/MurH.png":
            titleMapLave[items[2][1] - 1][items[2][0] - 1] = 3
    for x in range(0, 10):
        for y in range(0, 10):
            if titleMapLave[y][x] == 2:
                titleMapLave[y][x] = isObstacle(titleMapCaillou, x, y)
    for x in range(0, 10):
        for y in range(0, 10):
            if titleMapLave[y][x] != 1:
                titleMapLave[y][x] = 0

    for x in range(0, 10):
        for y in range(0, 10):
            if titleMapLave[y][x] == 1:
                titleMap[y][x] = 1
            if titleMapCaillou[y][x] == 1:
                titleMap[y][x] = 1
    return titleMap

def verif(posAndObjects):
    titleMapSimple = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ]
    titleMapSaut = verifSaut(titleMapSimple, posAndObjects)
    titleMapObstacle = titleMapSimple
    for items in posAndObjects:
        if items[0] == "files/Mur.png" or items[0] == "files/Mur+.png" or items[0] == "files/MurH.png":
            titleMapObstacle[items[2][1] - 1][items[2][0] - 1] = 1
    for x in range(0,10):
        for y in range(0,10):
            if titleMapSaut[y][x] == 1:
                titleMapObstacle[y][x] = 1
    grid = Grid(matrix=titleMapObstacle)
    start, end = 0, 0
    for items in posAndObjects:
        if items[0] == "files/robotB.png" or items[0] == "files/robotD.png" or items[0] == "files/robotG.png" or items[0] == "files/robotH.png":
            start = grid.node(items[2][0] - 1, items[2][1] - 1)
        elif items[0] == "files/finish.png":
            end = grid.node(items[2][0] - 1, items[2][1] - 1)
    if start == 0:
        if end == 0:
            return -1
        else:
            return -2
    elif end == 0:
        return -3
    else:
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        return len(path)
