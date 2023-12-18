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

def game(input, part1):
    trench = []
    x=0
    y=0
    trench.append((x,y))
    # First line is 1 cube longer than the rest because we count the starting point
    ofs = 1
    for path in input.split('\n'):
        dir, dist, color = path.split(' ')
        if part1:  #Part 1
            dist = int(dist)
        else:  #Part 2
            dist = int(color[2:7], 16)
            dir = "RDLU"[int(color[-2:-1])]

        if dir == 'R':
            x += dist + ofs
        elif dir == 'L':
            x -= dist - ofs
        elif dir == 'U':
            y -= dist - ofs
        elif dir == 'D':
            y += dist + ofs
        else:
            print('?', dir)
        trench.append((x,y))
        ofs = 0

    return trench

# Shoelace + perimeter
# calculate area of a polygon given its vertices
# Includes the area of the bounding box
# https://web.archive.org/web/20100405070507/http://valis.cs.uiuc.edu/~sariel/research/CG/compgeom/msg00831.html
# https://stackoverflow.com/questions/451426/how-do-i-calculate-the-area-of-a-2d-polygon
def area(p):
    segments = zip(p, p[1:] + [p[0]])
    #                    interior area   perimeter perimeter
    return 0.5 * abs(sum(x0*y1 - x1*y0 + abs(x1-x0) + abs(y1-y0)
                         for ((x0, y0), (x1, y1)) in segments))

input = getem()

trench = game(input, True)
print("Part 1: ", int(area(trench)))

trench = game(input, False)
print("Part 2: ", int(area(trench)))
