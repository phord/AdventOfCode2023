import re, collections, itertools as it

input='''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''
from functools import lru_cache


# Brick = collections.namedtuple('Brick', ['id', 'cells', 'minZ'])

input = open('src/day23.txt').read()

grid = tuple(input.split('\n'))
width = len(grid[0])
height = len(grid)

start = (1,0)
end = (width-2, height-1)

def dump(grid, path):
    for y in range(height):
        for x in range(width):
            if (x,y) in path:
                print('O', end='')
            else:
                print(grid[y][x], end='')
        print()

@lru_cache(maxsize=10000, typed=False)
def neighbors(grid, x,y):
    nbors = []
    for dx,dy in ((0,1),(1,0),(0,-1),(-1,0)):
        nx,ny = x+dx,y+dy
        if 0 <= nx < width and 0 <= ny < height:
            if grid[ny][nx] in '.<>^v':
                nbors.append((nx,ny))
    return tuple(nbors)

def trails(grid):
    # find every trail segment's start, end and length
    # where a trail segment has no branches

    seen = set()
    edges = {}
    for y in range(height):
        for x in range(width):
            if grid[y][x] in '.<>^v':
                edges[(x,y)] = neighbors(grid, x,y)

    trailheads = {}
    for k, v in edges.items():
        if len(v) > 2:
            for n in v:
                if len(edges[n]) == 2:
                    # Found a trailhead
                    trailheads[n] = k

    trail = {}
    for t, start in trailheads.items():
        if t in trail:
            continue
        tt = [t]
        next = [n for n in edges[t] if len(edges[n]) == 2]
        while len(next) == 1:
            if len(edges[next[0]]) > 2: break
            tt.append(next[0])
            next = [n for n in edges[next[0]] if n not in tt]

        # print(t, tt)
        last = tt[-1]
        assert last in trailheads or len(edges[last]) == 1
        if not next:
            next = [last]
            assert len(edges[last]) == 1

        trail[t] = (next[0], last, len(tt))
        trail[last] = (start, t, len(tt))

    graph = {}
    for k,v in edges.items():
        for n in v:
            if len(edges[n]) > 2:
                if k not in trail and n not in trail:

        assert v[0] in trail
        assert v[1] in trail

    return trail

# print(len(t))
# for k,v in t.items():
#     print(k, v)

# print(trails(grid))
# exit(1)

def dfs(grid, trails, start, end):
    seen = set([start])
    stack = [(start, 0, seen)]
    mx = 0
    while stack:
        # print(len(stack), end=' ')
        (x,y),dist, seen = stack.pop()
        seen = set(seen)

        # # Clear the screen and home cursor
        # print("\033[2J\033[H", end='')
        # dump(grid, seen)

        if (x,y) == end:
            mx = max(mx, dist)
            if mx == dist:
                print("End at", dist)
            # dump(grid, seen)
            # return dist
        if (x,y) in trails:
            (nx,ny),(x0, y0), l = trails[(x,y)]
            # print(trails[(x,y)])
            if (nx,ny) not in seen:
                seen.add((nx,ny))
                # seen.add(x0,y0)
                stack.append(((nx,ny), dist+l, tuple(seen)))
        else:
            for nx,ny in neighbors(grid, x,y):
                if (nx,ny) not in seen:
                    seen.add((nx,ny))
                    stack.append(((nx,ny), dist+1, tuple(seen)))

    return mx-1

print( dfs(grid, trails(grid), start, end))