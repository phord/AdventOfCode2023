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

def settle(grid, colliding):
    while True:
        moved = False
        # for each brick, try to fall
        for i in range(len(grid)):
            brick = grid[i]
            if floored(brick) or removed(brick):
                continue

            highest = 0
            for j in colliding[i]:
                z = max([z for _,_,z in grid[j][1]])
                if z > highest:
                    highest = z

            bottom = min([z for _,_,z in brick[1]])
            assert bottom > highest
            if bottom == highest + 1:
                continue

            # move brick down as far as possible
            distance = bottom - highest - 1
            b = tuple([(x,y,z-distance) for x,y,z in brick[1]])

            grid[i] = (i,b)
            moved = True

        if not moved:
            break
    return grid

# 808 is too high!

input = open('src/day22.txt').read()

grid = input.split('\n')
width = len(grid[0])
height = len(grid)

def cubes(brick):
    (x,y,z),(t,u,v) = brick
    out = []
    for i in range(x,t+1):
        for j in range(y,u+1):
            for k in range(z,v+1):
                out.append((i,j,k))
    return tuple(out)

for i,line in enumerate(grid):
    a,b = line.split('~')
    x,y,z = [int(c) for c in a.split(',')]
    t,u,v = [int(c) for c in b.split(',')]
    grid[i] = (i, cubes(((x,y,z),(t,u,v))))

print("pairing combatants...")
# Map of bricks a brick may land on
collide = {i: [] for i in range(len(grid))}
for i, brick in enumerate(grid):
    for j, brick2 in enumerate(grid):
        if i == j:
            continue
        if above_colliding(brick, brick2):
            collide[i].append(j)

print("settling...")
grid = settle(grid, collide)

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
        if zb+1 != za:
            continue
        supp.add(tuple(b))
    if len(supp) == 1:
        ss.add(supp.pop())

print("filtering...")
all = set([tuple(brick) for brick in grid])
removeable = all - ss
print("part 1: ", len(removeable))
# for i in sorted(list(removeable)):
#     print(i)

def count_diff(grid1, grid2):
    count = 0
    for brick in grid:
        # print(brick, g2[brick[0]])
        if g2[brick[0]][1] != ((0,0,0),) and g2[brick[0]][1] != brick[1]:
            count += 1
    return count


print("disintegrating...")
## Part 2: Find how many bricks are supported by one brick
count = 0
ii = 0
for i, _ in ss:
    ii += 1
    g2 = grid.copy()
    g2[i] = (i, ((0,0,0),))
    g2 = settle(g2, collide)
    count += count_diff(grid, g2)
    print(ii,count)

print("Part2: ", count)