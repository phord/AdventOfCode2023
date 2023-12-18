input = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

def getem():
    return open('src/day18.txt').read()

def extents(grid):
    minx = min([x for x,y in grid])
    miny = min([y for x,y in grid])
    maxx = max([x for x,y in grid])
    maxy = max([y for x,y in grid])
    return minx, miny, maxx, maxy

def flood(grid, pos):
    minx, miny, maxx, maxy = extents(grid)
    while pos:
        x,y = pos.pop()

        if x < minx or x > maxx or y < miny or y > maxy:
            continue

        if (x,y) in grid:
            continue

        grid.add((x,y))
        pos.append((x+1,y))
        pos.append((x-1,y))
        pos.append((x,y+1))
        pos.append((x,y-1))
    return grid

def show(grid):
    minx, miny, maxx, maxy = extents(grid)
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x,y) in grid:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print("===")

input = getem()
game = input.split('\n')

trench = []
x=0
y=0
trench.append((x,y))
for path in game:
    dir, dist, color = path.split(' ')
    for d in range(int(dist)*2):
        if dir == 'R':
            x += 1
        elif dir == 'L':
            x -= 1
        elif dir == 'U':
            y -= 1
        elif dir == 'D':
            y += 1
        else:
            print('?', dir)
        trench.append((x,y))

trench = set(trench)

new = flood(trench, [(1,1)])

trench = set([(x//2,y//2) for x,y in trench if x%2 == 0 and y%2 == 0])
show(trench)

print(len(set(trench)))
