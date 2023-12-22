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

def intersecting(brick1, brick2):
    return any([a in brick2[1] for a in brick1[1]])

def touching(brick1, brick2):
    b1 = descend(brick1)
    return intersecting(b1, brick2)

def settle(grid):
    while True:
        # sort by min z
        grid = sorted(grid, key=lambda x: min([a[2] for a in x[1]]))

        moved = False
        # for each brick, try to fall
        for i in range(len(grid)):
            brick = grid[i]
            if floored(brick):
                continue
            b = descend(brick)
            if any([intersecting(b, b2) for b2 in grid[:i]]):
                continue
            # move brick one level down
            grid[i] = b
            moved = True

        if not moved:
            break
    return grid


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

print("settling...")
grid = settle(grid)

print("searching...")
# Set of bricks that can't be removed
ss = set()
for a in grid:
    # Find bricks supporting a
    za = min([z for _,_,z in a[1]])
    supp = set()
    for b in grid:
        if a == b:
            continue
        zb = min([z for _,_,z in b[1]])
        if zb != za+1:
            continue
        if touching(b,a):
            supp.add(tuple(b))
    if len(supp) == 1:
        ss.add(supp.pop())

print("filtering...")
all = set([tuple(brick) for brick in grid])
removeable = all - ss
print(len(removeable))
# for i in sorted(list(removeable)):
#     print(i)
