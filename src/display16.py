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

class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    HOME = "\033[H"
    CLEAR = "\033[2J"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"


prev = set()
def display(game, pos, memo, height, width):
    print(Colors.HIDE_CURSOR + Colors.HOME, end='')
    if not memo:
        ## Draw the board
        for i in range(height):
            for j in range(width):
                c = game[i][j]
                beams = [b for p,b in memo if p == (j,i)]
                poss = [b for p,b in pos if p == (j,i)]

                if poss:
                    print(Colors.BOLD + Colors.YELLOW, end='')
                    if len(poss) > 1:
                        print('*',end='')
                    elif poss == [(1,0)]:
                        print('>',end='')
                    elif poss == [(-1,0)]:
                        print('<',end='')
                    elif poss == [(0,1)]:
                        print('v',end='')
                    elif poss == [(0,-1)]:
                        print('^',end='')
                elif beams and c == '.':
                    print(Colors.BOLD + Colors.LIGHT_RED, end='')
                    if len(beams) > 1:
                        x = len(beams)
                        if x > 9:
                            print('*',end='')
                        else:
                            print(x,end='')
                    else:
                        b = beams[0]
                        if b == (1,0):
                            print('>',end='')
                        elif b == (-1,0):
                            print('<',end='')
                        elif b == (0,1):
                            print('v',end='')
                        elif b == (0,-1):
                            print('^',end='')
                else:
                    print(Colors.GREEN, end='')
                    print(c,end='')
        print(Colors.END)

print(Colors.CLEAR, end='')
import time

def score(game, height, width, beam):
    delay = 1
    memo = set()
    beam = set(beam)
    while beam:
        beam = set([(p,b) for p,b in beam if p[0] >= 0 and p[1] >= 0 and p[0] < width and p[1] < height])

        display(game, beam, memo, height, width)
        time.sleep(delay)
        delay *= .9

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


# print(score(game, height, width, [((0,0),(1,0))]))

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

# print(most)

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