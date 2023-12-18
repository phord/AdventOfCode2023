input = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

def getem():
    return open('src/day17.txt').read()

def turnright(dir):
    return (dir[1], -dir[0])

def turnleft(dir):
    return (-dir[1], dir[0])

def go(pos, dir):
    x,y = pos
    dx,dy = dir
    return (x+dx, y+dy)

def valid(pos, dir, dist, height, width):
    x,y = pos
    if dist < 4:
        dx,dy = dir
        x += dx * (4-dist)
        y += dy * (4-dist)
    return x >= 0 and y >= 0 and x < width and y < height


visited = {}

def dump(path):
    global game, height, width
    p = [ p for p,_ in path]
    path = set(p)
    for y in range(height):
        for x in range(width):
            if (x,y) in path:
                i = p.index((x,y))
                if i > 0:
                    prev = p[i-1]
                    dx = x - prev[0]
                    dy = y - prev[1]
                    if dx == 1:
                        print('>', end='')
                    elif dx == -1:
                        print('<', end='')
                    elif dy == 1:
                        print('v', end='')
                    elif dy == -1:
                        print('^', end='')
                    else:
                        print('?', end='')
                else:
                    print('.', end='')
            else:
                print(game[y][x], end='')
        print()
    print("="*width)

## Game tuple: (cost, pos, dir, dist)

import astar

def Node(pos, dir, dist, height, width):
    nbors = []
    if dir:
        if False:   ## part1
            nbors  = ((dir, dist + 1), (turnleft(dir), 1), (turnright(dir), 1))
            if dist == 3:
                nbors = nbors[1:]

            nbors = [(go(pos, dir), dir, dist) for dir, dist in nbors]
            nbors = [(pos, dir, dist) for pos, dir, dist in nbors if pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height]
        else:      ## part2
            nbors = [(dir, dist + 1)] if dist < 4 else ((dir, dist + 1), (turnleft(dir), 1), (turnright(dir), 1))
            if dist == 10:
                nbors = nbors[1:]

            nbors = [(go(pos, dir), dir, dist) for dir, dist in nbors]
            nbors = [(pos, dir, dist) for pos, dir, dist in nbors if valid(pos, dir, dist, height, width)]
            nbors = [(pos, dir, dist) for pos, dir, dist in nbors if pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height]

    return (pos, frozenset(nbors))


class Day17(astar.AStar):

    def __init__(self, game, height, width):
        self.game = game
        self.height = height
        self.width = width

    def heuristic_cost_estimate(self, current, goal):
        ## Position = 0
        x0,y0 = current[0]
        x1,y1 = goal[0]
        return abs(x0-x1) + abs(y0-y1)

    def distance_between(self, n1, n2):
        x,y = n2[0]
        try:
            return int(self.game[y][x])
        except:
            print(n1, n2)


    def neighbors(self, node):
        return [Node(pos, dir, dist, self.height, self.width) for pos, dir, dist in node[1] ]

    def is_goal_reached(self, current, goal):
        # print(current.position, goal.position)
        return current[0] == goal[0]


input2 = '''111111111111
999999999991
999999999991
999999999991
999999999991'''

input=getem()

game = input.split('\n')
height = len(game)
width = len(game[0])

start = ((0, 0), frozenset({((1, 0), (1, 0), 1), ((0, 1), (0, 1), 1)}))

goal = Node((width-1, height-1), None, None, height, width)
path = Day17(game, height, width).astar(start, goal)

path = list(path)
total = 0
for p in path:
    x,y = p[0]
    if x>0 or y>0: total += int(game[y][x])
print()
print(total)


# s,path = solve()
# print("PART1: ", s, len(path))

# 1421 too high
dump(path)