from collections import deque


input='''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''


def descend(brick):
    id, cubes = brick
    return (id, tuple([(x,y,z-1) for x,y,z in cubes]))

def floored(brick):
     return any([z == 1 for _,_,z in brick[1]])

def removed(brick):
     return brick[1] == ((0,0,0),)


def intersecting(brick1, brick2):
    return any([a in brick2[1] for a in brick1[1]])

def touching(brick1, brick2):
    b1 = descend(brick1)
    return intersecting(b1, brick2)

def footprint(brick):
    return set([(x,y) for x,y,_ in brick[1]])

def above_colliding(brick1, brick2):
    z1 = min([z for _,_,z in brick1[1]])
    z2 = min([z for _,_,z in brick2[1]])
    if z1 <= z2:
        return False

    f1 = footprint(brick1)
    f2 = footprint(brick2)
    return len(f1.intersection(f2)) > 0

def settle(grid, colliding, supporting):
    candidates = list(range(len(grid)))
    while candidates:
        candidates = sorted(candidates, key=lambda i: min([z for _,_,z in grid[i][1]]))
        next = []
        for i in candidates:
            brick = grid[i]
            if floored(brick) or removed(brick):
                continue

            highest = [z for j in colliding[i] for _,_,z in grid[j][1]]
            highest = max(highest) if highest else 0
            bottom = min([z for _,_,z in brick[1]])
            assert bottom > highest
            if bottom == highest + 1:
                continue

            # move brick down as far as possible
            distance = bottom - highest - 1
            grid[i] = (i,tuple([(x,y,z-distance) for x,y,z in brick[1]]))
            next.extend([j for j in supporting[i] if touching(grid[i], grid[j])])
        candidates = set(next)
    return grid

input = open('src/day22.txt').read()

grid = input.split('\n')
width = len(grid[0])
height = len(grid)

def cubes(brick):
    (x,y,z),(t,u,v) = brick
    return tuple([(i,j,k) for i in range(x,t+1) for j in range(y,u+1) for k in range(z,v+1)])

for i,line in enumerate(grid):
    a,b = line.split('~')
    x,y,z = [int(c) for c in a.split(',')]
    t,u,v = [int(c) for c in b.split(',')]
    grid[i] = (i, cubes(((x,y,z),(t,u,v))))

print("pairing combatants...")
# Map of bricks a brick may land on
collide = {i: set() for i in range(len(grid))}
sgrid = sorted(grid, key=lambda brick: min([z for _,_,z in brick[1]]))
for i, brick in enumerate(sgrid):
    k = brick[0]
    for brick2 in sgrid[:i]:
        j = brick2[0]
        if above_colliding(brick, brick2):
            collide[k].add(j)

# If any lower bricks also collide with the same bricks as us, we can't land on them
print("reducing collisions...")
supporting = {i: [] for i in range(len(grid))}
for k,v in collide.items():
    redundant = set([i for j in v for i in collide[j]])
    collide[k] = v - redundant
    for j in collide[k]:
        supporting[j].append(k)

print("settling...")
grid = settle(grid, collide, supporting)

print("searching...")
# Set of bricks that can't be removed
ss = set()
for a in grid:
    # Find bricks supporting a
    za = min([z for _,_,z in a[1]])
    supp = set()
    for j in collide[a[0]]:
        b = grid[j]
        zb = max([z for _,_,z in b[1]])
        if zb+1 == za:
            supp.add(tuple(b))
    if len(supp) == 1:
        ss.add(supp.pop())

print("filtering...")
all = set(grid)
removeable = all - ss
print("part 1: ", len(removeable))

def count_diff(grid1, grid2):
    return len([1 for brick in grid if g2[brick[0]][1] != ((0,0,0),) and g2[brick[0]][1] != brick[1]])

print("disintegrating...")
## Part 2: Find how many bricks are supported by one brick
count = 0
for i, _ in ss:
    g2 = grid.copy()
    g2[i] = (i, ((0,0,0),))
    g2 = settle(g2, collide, supporting)
    count += count_diff(grid, g2)

print("Part2: ", count)