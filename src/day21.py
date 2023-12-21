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

# input = open('src/day21.txt').read()

grid = input.split('\n')
width = len(grid[0])
height = len(grid)

for i,line in enumerate(grid):
    if 'S' in line:
        start = (line.index('S'), i)
        break

def display(grid, visit):
    for y in range(height):
        for x in range(width):
            if (x,y) in visit:
                print(visit[(x,y)]%10, end='')
            else:
                print(grid[y][x], end='')
        print()


def neighbors(x, y):
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        yield ((x+dx + width) % width, (y+dy+height) % height)

def bfs(start):
    queue = deque([start])
    dist = { start: 0 }
    while queue:
        x,y = queue.popleft()
        for nx,ny in neighbors(x,y):
            if (nx,ny) not in dist and grid[ny][nx] != '#' and dist[(x,y)] < 64:
                dist[(nx,ny)] = dist[(x,y)] + 1
                queue.append((nx,ny))
    return dist

dist = bfs(start)
print(len([k for k,v in dist.items() if v%2 ==0]))
display(grid, dist)

# 5 * 11 * 481843