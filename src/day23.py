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

def neighbors(grid, x,y):
    nbors = []
    for dx,dy in ((0,1),(1,0),(0,-1),(-1,0)):
        nx,ny = x+dx,y+dy
        if 0 <= nx < width and 0 <= ny < height:
            if grid[ny][nx] in '.<>^v':
                nbors.append((nx,ny))
    return tuple(nbors)

def measure(edges, start, head):
    count = 1
    while len(edges[head]) == 2:
        count += 1
        next = [n for _,n in edges[head] if n != start]
        assert len(next) == 1
        next = next[0]
        start = head
        head = next
    return (count, head)


def trails(grid):
    edges = {}
    for y in range(height):
        for x in range(width):
            if grid[y][x] in '.<>^v':
                edges[(x,y)] = [(1,n) for n in neighbors(grid, x,y)]

    # Collapse all trail segments into a single edge
    newedges = {}
    for k,v in edges.items():
        if len(v) != 2:
            newedges[k] = [measure(edges, k, n[1]) for n in v]

    return newedges

def dfs(grid, trails, start, end):
    seen = set([start])
    stack = [(start, 0, seen)]
    mx = 0
    while stack:
        pos, dist, seen = stack.pop()

        if pos == end:
            mx = max(mx, dist)
        for d, next in trails[pos]:
            if next not in seen:
                stack.append((next, dist+d, seen | set([next])))

    return mx

print( dfs(grid, trails(grid), start, end))