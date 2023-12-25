import sys

input='''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''

def parse(input):
    game = input.split('\n')
    hail = []
    for g in game:
        l,r = g.split(' @ ')
        x,y,z = l.split(',')
        vx,vy,vz = r.split(', ')
        hail.append((int(x),int(y),int(z),int(vx),int(vy),int(vz)))

    return hail


def slope_int(a):
    x,y,_,vx,vy,_ = a
    return (vy / vx, y - vy / vx * x)

# find path intersections in just x and y axes, regardless of time
def intersect(l1,l2):
    x,y,_,vx,vy,_ = l1
    x2,y2,_,vx2,vy2,_ = l2

    # y = mx + b
    m,b = slope_int(l1)
    m2,b2 = slope_int(l2)

    # mx + b = m2x + b2
    # mx - m2x = b2 - b
    # x(m - m2) = b2 - b
    # x = (b2 - b) / (m - m2)
    if m == m2 and b != b2:
        return None
    if m == m2 and b == b2:
        raise Exception("same line")
        # rmin, rmax = (200000000000000, 400000000000000)
        # # Find where line crosses the box betweem rmin and rmax
        # y0 = m * rmin + b
        # y1 = m * rmax + b
        # if y0 < rmin and y1 >= rmin:
        #     return (rmin, rmax)

    x0 = (b2 - b) / (m - m2)
    y0 = m * x0 + b

    # When do they cross?
    # x + vx * t = x0
    # t = (x0 - x) / vx
    t = (x0 - x) / vx
    t2 = (x0 - x2) / vx2
    if t < 0 or t2 < 0:
        return None

    return (x0,y0)


def score(hail, rmin, rmax):
    count = 0
    for i in range(len(hail)):
        for j in range(i+1, len(hail)):
            a = hail[i]
            b = hail[j]
            sec = intersect(a,b)
            if sec:
                x,y = sec
                if rmin <= x <= rmax and rmin <= y <= rmax:
                    count += 1
                    # print(i,j,sec[0], sec[1])
    return count



rmin = 7
rmax = 27

# Check for args on cmdline
if len(sys.argv) > 1:
    print(sys.argv[1])
    input = open(sys.argv[1]).read()
    rmin = 200000000000000
    rmax = 400000000000000

hail = parse(input)

print(score(hail, rmin, rmax))

# Ints take about 50 seconds for Z3 to solve
# Reals take about 50ms.  Crazy!

from z3 import *
x, y, z, vx, vy, vz = Reals('x y z vx vy vz')
t = Real('t')
px = x + vx * t
py = y + vy * t
pz = z + vz * t

s = z3.Solver()
# Solving for 6 unknowns. How many equations do we need?
# Seems to work with 3, but I'm not sure why.
for i,h in enumerate(hail[:3]):
    x_i, y_i, z_i, vx_i, vy_i, vz_i = h
    t_i = z3.Real(f"t_{i}")
    s.add(x_i + vx_i * t_i == x + vx * t_i)
    s.add(y_i + vy_i * t_i == y + vy * t_i)
    s.add(z_i + vz_i * t_i == z + vz * t_i)

print(s.check())
m = s.model()
print(m[x], m[y], m[z])
print(m[x].as_long() + m[y].as_long() + m[z].as_long())
