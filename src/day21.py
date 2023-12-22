from collections import deque


input='''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''

input = open('src/day21.txt').read()

grid = input.split('\n')
width = len(grid[0])
height = len(grid)

for i,line in enumerate(grid):
    if 'S' in line:
        start = (line.index('S'), i)
        break

def cell(x,y):
    return grid[y%height][x%width]

def display(grid, visit):
    for y in range(-height*2,height*3):
        if y % height == 0:
            print()
        for x in range(-width*2,width*3):
            if x % width == 0:
                print('  ', end='')
            if (x,y) in visit:
                print("{:-3}".format(visit[(x,y)]), end='')
            else:
                print("...", end='')
        print()

def display_reach(grid, visit):
    for y in range(height*6):
        if y % height == 0:
            print()
        for x in range(width*6):
            if x % width == 0:
                print('   ', end='')
            if (x,y) in visit:
                print("{:-4}".format(visit[(x,y)]), end='')
            else:
                print(' .. ', end='')
        print()

def sgn(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def neighbors(x, y):
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        if -width*5 <= x+dx < width*6 and -height*5 <= y+dy < height*6:
            yield (x+dx, y+dy)

def bfs(start, steps):
    queue = deque([start])
    dist = { start: 0 }
    while queue:
        x,y = queue.popleft()
        for nx,ny in neighbors(x,y):
            if (nx,ny) not in dist and cell(nx,ny) != '#' and dist[(x,y)] < steps:
                dist[(nx,ny)] = dist[(x,y)] + 1
                queue.append((nx,ny))
    return dist


from functools import lru_cache

def delta(dist):
    return dist[(3,0)][(width*3,0)] - dist[(2,0)][(width*2,0)]

def delta2(dist):
    return dist[(4,0)][(width*4,0)] - dist[(3,0)][(width*3,0)]

def split_grids(dist):
    split = {}
    for x in range(-6, 7):
        for y in range(-6, 7):
            split[(x,y)] = {k:v for k,v in dist.items() if
                    width*x <= k[0] < width*(x+1)
                    and height*y <= k[1] < height*(y+1)}
    return split

# for each repeating grid in the x and y directions..
def reachable(dist, steps, x, y):
    # This delta only works because dx and dy are conveniently identical
    d = delta(dist)

    # offset = 0
    # if -5 <= x <= 5 and -5 <= y <= 5:
    #     offset = 0
    # else:
    #     xoff = d * (abs(x)-2)
    #     yoff = d * (abs(y)-2)
    #     offset = abs(xoff + yoff)

    ox,oy = (x,y)

    # print(f"({x},{y}) ", end='')
    if x > 4:   # 3
        x = 4 + (x%2)
    elif x < -4:  # -2
        x = -4 - (x%2)

    if y > 4:
        y = 4 + (y%2)
    elif y < -4:
        y = -4 - (y%2)

    offset = (abs(ox-x) + abs(oy-y)) * d

    dist = dist[(x,y)]
    # print(offset, x, y, end='')
    match = offset % 2

    r = {k:v for k,v in dist.items() if v%2 == match and v+offset <= steps}
    # print (f"==> {len(r)}")
    return len(r)

def find_all(start, steps):
    dist = bfs(start, steps)
    # Steps can be reached with an even number circuit
    reachable = {k:v for k,v in dist.items() if v%2 ==0}
    count = len(reachable)
    print("Steps", steps, "can reach", count, "cells")
    return reachable

# print(list(neighbors(0,0)))
# display(grid, dist)

# 26501365 = 5 * 11 * 481843
# for steps in (6, 10, 50, 100, 500, 1000, 5000):
#     find_all(start, steps)
def comment_block():
    pass
    # for i in range(1,10):
    #     print("height: At", i, "grids", r[(height*i,0)], "diff=", r[(height*i, 0)] - r[(height*(i-1), 0)])
    #     print("width:  At", i, "grids", r[(0,width*i)], "diff=", r[(0, width*i)] - r[(0, width*(i-1))])

    # We have an infinite grid of repeating patterns like this:
    #       0     1     2     3     4     5
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #  0  ooooo ooooo ooooo ooooo ooooo ooooo
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #  1  ooooo ooooo ooooo ooooo ooooo ooooo
    #     ooooo ooooo ooSoo ooooo ooooo ooooo
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #  2  ooooo ooooo ooooo ooooo ooooo ooooo
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #  3  ooooo ooooo ooooo ooooo ooooo ooooo
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #     ooooo ooooo ooooo ooooo ooooo ooooo
    #
    # The deltas between each cell in each neighbor grid is the same (131), except for the grids
    # adjacent to the center.  This means that for each grid we move in any direction, the odds/evens
    # will switch.  For example, if there are 30 gardens, and 12 are even in grid (x,y), then 18 will
    # be even in grid (x+1,y), and 18 in grid (x,y+1). So we need to manually count the center 9 grids,
    # and then we can divide by 131 to find the extent of the rest of the grids.
    #
    # for the last grids on the edge, we simply need to examine each item in the grid and subtract its
    # offsets from our target width.  But we need to calculate the grids in a diamond pattern.

steps = 5000
r = bfs(start, 2000)
print("---")

# rr = {k:v for k,v in r.items() if v%2 == 0 and v <= 10}
# print(len(rr), rr)

r = split_grids(r)
for k,v in sorted(r.items()):
    p = [ j for i,j in v.items() if j%2 == 0]
    if p: print(k, len(p))

d = delta(r)
assert d == delta2(r)

# for x in range(-5, 0):
#     print ([v+x*11 for k,v in sorted(r[(x, 0)].items())])
# print (sorted(r[(-3, 0)].items()))
for k,v in r[(-5, 0)].items():
    x,y=k
    # print(x,y)
    assert(r[(-3, 0)][(x+width*2,y)] == v-d*2)

def count_reachable(dist, steps):
    count = 0
    d = delta(dist)
    w = steps // d + 1
    for y in range(-w-2,w+2):
        for x in range(-w-2,w+2):
            c = reachable(r, steps, x, y)
            count += c
            # if c:
            #     print(c, end=' ')
        # print()
    print(f"In exactly {steps} steps, he can still reach {count} garden plots.")
    return count

def count_reachable2(dist, steps):
    count = 0
    d = delta(dist)
    w = steps // d + 1
    block0 = reachable(r, steps, 3, 0)
    block1 = reachable(r, steps, 4, 0)
    twoblocks = reachable(r, steps, 3, 0) + reachable(r, steps, 4, 0)

    for y in range(-w-2,w+2):
        wid = w - abs(y) + 1
        for x in range(-wid-2,1):
            # Count left edge
            c = reachable(r, steps, x, y)
            count += c
            # if c:
            #     print(c, end=' ')
            if x != 0:
                # Count right edge
                c2 = reachable(r, steps, -x, y)
                count += c2
                # if c2:
                #     print(c2, end=' ')
            if c == block0 and c2 == block0 and x < -4:
                break
        if x < -2:
            blocks = -x - 2
            blocks -= blocks%2
            if abs(y) < 5:
                blocks -= 4
            count += twoblocks * blocks
            # if blocks:
            #     print(f"[{twoblocks} * {blocks}] ", end=' ')

            xx = x + blocks + 1
            assert xx <= 0

            for x in range(xx, 1):
                c = reachable(r, steps, x, y)
                count += c
                # if c:
                #     print(c, end=' ')
                if x != 0:
                    c = reachable(r, steps, -x, y)
                    count += c
                    # if c:
                    #     print(c, end=' ')
        # print()

    print(f"In exactly {steps} steps, he can still reach {count} garden plots.")
    return count


# 617565665054331 is too low
# 617565692567199 is the right answer using someone elses code (quadratic polynomial)
# This is mine + 27512868
def count_reachable3(dist, steps):
    count = 0
    d = delta(dist)
    w = steps // d + 1
    block0 = reachable(r, steps, 3, 0)
    block1 = reachable(r, steps, 4, 0)
    twoblocks = reachable(r, steps, 3, 0) + reachable(r, steps, 4, 0)

    prev = count
    prevrow = 0
    for y in range(-w-2,w+2):
        row = count - prev
        diff = row - prevrow
        prev = count

        if -w+20 < y < -20:
            # Each successive row is the previous row + twoblocks
            assert row - prevrow == twoblocks
            prevrow = row
            count += row + twoblocks
            continue

        elif 20 < y < w-20:
            # Each successive row is the previous row - twoblocks
            assert row - prevrow == -twoblocks
            assert row > twoblocks
            prevrow = row
            count += row - twoblocks
            continue

        if diff:
            print(f"y={y-1} {diff}")
        prevrow = row

        wid = w - abs(y) + 1
        for x in range(-wid-2,1):
            # Count left edge
            c = reachable(r, steps, x, y)
            count += c
            # if c:
            #     print(c, end=' ')
            if x != 0:
                # Count right edge
                c2 = reachable(r, steps, -x, y)
                count += c2
                # if c2:
                #     print(c2, end=' ')
            if c == block0 and c2 == block0 and x < -4:
                break
        if x < -2:
            blocks = -x - 2
            blocks -= blocks%2
            if abs(y) < 5:
                blocks -= 4
            count += twoblocks * blocks
            # if blocks:
            #     print(f"[{twoblocks} * {blocks}] ", end=' ')

            xx = x + blocks + 1
            assert xx <= 0

            for x in range(xx, 1):
                c = reachable(r, steps, x, y)
                count += c
                # if c:
                #     print(c, end=' ')
                if x != 0:
                    c = reachable(r, steps, -x, y)
                    count += c
                    # if c:
                    #     print(c, end=' ')
        # print()

    print(f"In exactly {steps} steps, he can still reach {count} garden plots.")
    return count

# for steps in (6, 10, 50, 100, 500):#, 1000):
#     count_reachable(r,steps)

for steps in (6, 10, 50, 100, 500, 1000, 5000, 26501365):
    count_reachable3(r,steps)

# for i in range(-1,2):
#     for j in range(-1,2):
#         count +=
#             count += r[(width+i, height+j)] % 2
# dx =

# display_reach(grid, r)