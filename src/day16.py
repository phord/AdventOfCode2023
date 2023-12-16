input = '''.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''

def getem():
    return open('src/day16.txt').read()

def display(game, pos, height, width):
    for i in range(height):
        for j in range(width):
            c = game[i][j]
            if (j,i) in pos:
                print('#',end='')
            else:
                print(c,end='')
        print()
    print("="*width)


def score(game, height, width, beam):
    memo = set()
    beam = set(beam)
    while beam:
        beam = set([(p,b) for p,b in beam if p[0] >= 0 and p[1] >= 0 and p[0] < width and p[1] < height])

        next = set()
        for p in beam:
            x,y = p[0]
            b = p[1]
            memo.add(p)
            c = game[y][x]
            if c == '\\':
                b = (b[1], b[0])
            elif c == '/':
                b = (-b[1], -b[0])
            elif c == '-':
                if b[1] != 0:
                    b = (1,0)
                    next.add(((x,y),(-1,0)))
            elif c == '|':
                if b[0] != 0:
                    b = (0,1)
                    next.add(((x,y),(0,-1)))
            dx, dy = b
            p = ((x+dx, y+dy), b)
            if p not in memo:
                next.add(p)
        beam = next

    return len(set([p for p,_ in memo]))

input=getem()

game = input.split('\n')
height = len(game)
width = len(game[0])


print(score(game, height, width, [((0,0),(1,0))]))

## part2

most = 0
for i in range(width):
    s1 = score(game, height, width, [((i,0), (0,1))])
    s2 = score(game, height, width, [((i,height-1), (0,-1))])
    most = max(most, s1, s2)

for i in range(height):
    s1 = score(game, height, width, [((0,i), (1,0))])
    s2 = score(game, height, width, [((width-1,i), (-1,0))])
    most = max(most, s1, s2)

print(most)

def show(grid, height, width):
    for i in range(height):
        for j in range(width):
            if (j,i) in grid:
                print('#',end='')
            else:
                print('.',end='')
        print()
    print()


# show(energy, height, width)