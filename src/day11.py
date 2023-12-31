input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

def getem():
    return '''......................#..................#................................#............#..........................#.........................
..........#....................................#.................#..........................................................................
................................#......................#..........................#.....................#................#..................
...........................#....................................................................#........................................#..
.....#..........#...................................................................................................................#.......
........................................................................................#...................................................
........................................#............#......................................................................................
.....................#....................................................#...................#.......................#.....................
..............................................................................................................................#...........#.
............................#.......#......................#................................................................................
...........#......................................#..............#............#.............................................................
.........................................................................................#..................................................
....#...............................................................................#.....................................#...........#.....
..................#...........#...............#..............................................#.......#........#.............................
........................................#...........................#.......................................................................
............................................................................................................................................
.........................#..........................#.........................#.........................#...................................
................#...................#..................................................................................#...................#
...#...........................................................#........#.............#..............................................#......
..................................................................................................#.........................................
.............#..............................#...............................................................................................
.....................#.........................................................................................#............................
............................#........................#............#.........................#..................................#............
.......#..............................................................................................................#.....................
........................................................................#........#..................#.......................................
...#......................................#.......#......................................................#........#...............#.........
...........................................................#.............................................................................#..
................................#..................................#........................................................................
.............#.................................#............................................................................................
#.......................#...............#.................................#...........#.........#...................................#.......
...........................................................................................#..................#.............................
........#....................#........................................................................................#......#..............
............................................................#......................................#......................................#.
..#.......................................#.................................................................................................
....................#................................................................#....................................#........#........
.............#......................#................#......................................#...............................................
.......#............................................................#................................................#......................
..............................#.................#.................................................#.........................................
.......................#...................................................................................#................................
..................#..........................................#..................................................#..............#.....#......
...................................................#...............................#.....#.............#....................................
...#..........#.............#........#......................................................................................................
............................................................................#..................#.............#...........................#..
......................................................#..............#......................................................................
#......#....................................................................................................................#...............
..............................................#.............................................................................................
...................#................#...................................#.......................................................#..........#
...........#............#.................................#.................................................#...........#...................
.....................................................................................#.....#........#............#.....................#....
....................................................#..........#............................................................................
............................................................................................................................................
.#.......#..................#..........#.............................#............#............#..........#................#..............#.
...............#.....#...................................................................#..................................................
.................................................#..........................#.........................................#........#.....#......
......#..........................................................#...............................................#..........................
............................................................................................................................................
.............................#................#.......................................#.....................#...............................
..................#..................#.......................#..........#.....................#.............................#...............
............................................................................................................................................
..................................................................................#.................#...................#..........#........
..................................#.....#..............#..........#.....................#...................................................
.....#.................#....................................................................................................................
#......................................................................................................................................#....
..................#..................#........#...........#..................#.................#............................................
.....................................................................#................................#.........#.............#.............
..........#..........................................................................#.....#................................................
............................#.......................#...........#...........................................................................
.#.................................#.............................................................#.................#........................
............................................................................#................................#..........................#...
......#..................................................................................................................#..................
...................#..............................#.................................................#.........................#.............
..............#................#.........................................................#..........................................#.......
............................................#....................#...............#..........................................................
.......................#................................................#.................................#.................................
..................................#.....#...........#...................................................................#...................
.#.....................................................................................#........#...........................................
.......#......................#................................#.......................................#....................................
...............................................#............................................................................................
..........................................................#................#.....................................#..........................
......................#.....................................................................................................................
............................................#.........#.......................................#..................................#..........
.#.........#........................................................#...................................#.....#.............................
.......................................#.............................................#..................................................#...
...............................#............................................................................................................
.............................................................................#..................#................#........#.................
......................#.....................................................................................................................
...#..............................................#.........#.....................#......................#...........................#......
..................................#.........................................................................................................
...........................................................................#...............#...................................#............
..........#..............#....................#.............................................................................................
...............................................................................................................#........................#...
....#.........#...............................................................#.....#.......................................................
.......................................................#..........#.......................................................#.................
..................................#...............#..............................................................................#..........
..............................................................#..........................#................#.........#.......................
........#............................................................#......................................................................
#...............................................................................................#...........................................
......................#....................................................................................................................#
.....#......................#..............................................#...........#..........................#.....#...................
................#.................................................#..............#..........................................................
...........#.........................................#......................................................................................
..#..................................#.............................................................................................#.....#..
..........................................#................................................#.....#........#.................................
..............#...............................................#.................................................#...........................
....................#.............#....................#..............................................#.....................................
.............................#..........................................#...................................................................
...........................................................#................................................................................
.......................#.........................#.....................................#...........#........................................
.................................................................#............................................#.......#.....................
........#.....#............................................................#........................................................#.......
.................................#...........................................................#..............................................
.#.................#......................#.................#.........#..................................#.......#........#................#
...........#................................................................................................................................
........................#..............................#.............................#......................................................
...................................#.....................................#.........................#.................................#......
............................................................................................................................................
....#..................................#.................................................#...............................#..................
.............................#....................#......................................................................................#..
.............................................................................#.........................#....................................
.............#.....#......................#.......................#.................#........................................#..............
......................................................................................................................................#.....
...#.................................................#...........................................#..........................................
......................#.....................................#...............................................................................
................#..........#..................................................................................#..........#..................
..........#.........................#............#.................#..........#............................................................#
............................................................................................................................................
.......................................................#............................................................#.......................
...#.........................................#.....................................#...............#..............................#.........
............#.........................#.....................................................................................................
.......................#...........................#.....................................................#..................................
..............................................................#............................#...............................#..........#.....
.........#......................#..........#.........................................#......................................................
...............#................................................................................#.....#.....................................
....#.......................#..................#....................#......................................#...................#............
..........................................................#.................................................................................
.....................................#.........................#.........................#..................................................
#..........................................................................#................................................................
...........................................#..................................................................#........#...........#........
......................#...........................................................#...................#.....................................
....#...........#................................................................................#..........................................'''

input = getem()

grid = input.split('\n')
width = len(grid[0])
height = len(grid)

galaxy=[]
for i,line in enumerate(grid):
    for j,c in enumerate(line):
        if c == '#':
            galaxy.append((j,i))

gx = set([x for x,y in galaxy])
gy = set([y for x,y in galaxy])

doublewide = [x for x in range(width) if x not in gx]
doublehigh = [y for y in range(height) if y not in gy]

def distance(a,b):
    dist = abs(a[0]-b[0])+abs(a[1]-b[1])
    for x in doublewide:
        if a[0] < x < b[0] or b[0] < x < a[0]:
            dist += 999999
    for y in doublehigh:
        if a[1] < y < b[1] or b[1] < y < a[1]:
            dist += 999999
    return dist

dist = 0
for i in range(len(galaxy)):
    for j in range(i+1,len(galaxy)):
        dist += distance(galaxy[i],galaxy[j])

# print(doublehigh)
# print(doublewide)
# print(galaxy)

print(dist)