from itertools import product


input = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

def getem():
    return open('src/day19.txt').read()

def game(input, part1):
    g1,g2 = input.split('\n\n')
    rules = {}
    for line in g1.split('\n'):
        a,b = line.split('{')
        b = b[:-1]
        r = b.split(',')
        rules[a] = r

    ratings = []
    for line in g2.split('\n'):
        line = line.strip('{}')
        rr = {}
        for r in line.split(','):
            rr[r[0]] = int(r[2:])
        ratings.append(rr)

    return (rules, ratings)

def play(rules, ratings):
    total = 0
    for rate in ratings:
        work = "in"

        while work not in ["R", "A"]:
            rule = rules[work]
            for r in rule:
                if ':' not in r:
                    work = r
                    break

                cond, target = r.split(':')
                var = cond[0]
                comp = cond[1]
                val = int(cond[2:])
                actual = rate[var]
                if comp == "<":
                    if actual < val:
                        work = target
                        break
                elif comp == ">":
                    if actual > val:
                        work = target
                        break
                elif comp == "=":
                    if actual == val:
                        work = target
                        break
                else:
                    print("Unknown condition", comp, " in ", r)
                    exit(1)
        if work == "A":
            value = sum([rate[r] for r in rate])
            total += value
        elif work == "R":
            pass
        else:
            print("Unknown result", work)
            exit(1)
    return total

# Find all paths that lead to "A" from a given node
def solve(rules, node, path):
    paths = []
    work = node

    if node in ["R", "A"]:
        return [path + [node]]

    rule = rules[work]
    for r in rule:
        if ':' not in r:
            paths.extend(solve(rules, r, path))
            break

        cond, target = r.split(':')
        next = solve(rules, target, path + [cond])

        paths.extend(next)

    return paths

def combos(path):
    map = {'x': (1,4001), 'm': (1,4001), 'a': (1,4001), 's': (1,4001)}

    for cond in path[:-1]:
        var = cond[0]
        comp = cond[1]
        val = int(cond[2:])
        mn,mx = map[var]
        if comp == "<":
            mx = min(mx, val)
        elif comp == ">":
            mn = max(mn, val+1)
        elif comp == "=":
            mn = val
            mx = val
        else:
            print("Unknown condition", comp, " in ", cond)
            exit(1)
        map[var] = (mn,mx)

    return [map[var] for var in "xmas"]

# Split two ranges into three disjoint ranges
def split(r1, r2):
    mn1,mx1 = r1
    mn2,mx2 = r2

    # Common range
    c1 = max(mn1, mn2)
    c2 = min(mx1, mx2)
    if c1 <= c2:
        left = [ a for a in [(mn1, c1), (c2, mx1), (c1,c2+1)] if a[0] <= a[1]]
        return left
    else:
        return [r1]

def disjoint(p1, p2):
    left = split(p1[0], p2[0])
    if len(p1) == 1:
        return [[a] for a in left]

    lr = disjoint(p1[1:], p2[1:])
    a = []
    for l in left:
        for l2 in lr:
            a.append([l] + l2)
    return a


# a = [(1,5),(2,4), (5,12), (12,20)]
# b = [(3,7),(1,3), (3,6), (1,8)]
# for i,j in zip(a,b):
#     print(i, j, " ==> ", split(i,j))

# x,y = disjoint(a,b)
# for i in x:
#     print(i)
# for i in y:
#     print(i)


# exit(1)

def count(p1):
    total = 1
    for i in range(4):
        mn,mx = p1[i]
        total *= (mx-mn)
    return total

def show(p):
    print(count(p), p)

def disjoint_1xn(p1, paths):
    pp = set([tuple(p1)])

    for path in paths:
        next = set()
        for p in pp:
            left = disjoint(p, path)
            for a in left:
                next.add(tuple(a))
        pp = next

    # ## Validate pp
    # a = count(p1)
    # b = 0
    # for p in pp:
    #     b += count(p)
    # assert a == b

    return pp

def disjoint_all(paths):
    pp = set()
    for i in range(len(paths)):
        pp |= disjoint_1xn(paths[i], paths)
    return pp

# a = [(1,5),(2,4), (5,12), (13,17)]
# b = [(3,7),(1,3), (3,6), (1,8)]

# show(a)
# show(b)
# c = disjoint_1xn(a, [b])
# for i in c:
#     show(i)
# print()
# d = disjoint_all([a,b])
# total = 0
# for i in d:
#     show(i)
#     total += count(i)
# print(total)
# exit(1)

# a = [(2663, 4000), (1, 4000), (1, 2005), (1, 1350)] #['s<1351', 'a<2006', 'x>2662', 'A']
# b = [(1, 4000), (1, 4000), (1, 2005), (1, 1350)]    #['s<1351', 'a<2006', 'R']
# c = [(1, 4000), (1, 4000), (1, 4000), (1, 1350)]    #['s<1351', 'A']

# show(a)
# show(b)
# show(c)
# print()


def disjoiner(path, vertices):
    # print(path)
    rang = [sorted([x for x in s if p[0] <= x <= p[1]]) for p, s in zip(path, vertices)]
    # print(rang)
    rang = [[(a,b) for a,b in zip(x[0:-1], x[1:])] for x in rang]
    # print(rang)
    return product(*rang)

# input = getem()

g = game(input, True)
g = play(*g)
print("Part 1: ", g)


rules, _ = game(input, True)
paths = solve(rules, "in", [])
# for p in paths:
#     print(combos(p), p)
# print()

comb = [combos(p) for p in paths]

# get a map of every parameter range for every path
vertices = []
for i in range(4):
    ps = set()
    for p in comb:
        ps.add(p[i][0])
        ps.add(p[i][1])
    vertices.append(ps)
# print(vertices)

# for p in comb:
#     print(len(disjoiner(p, vertices)))
#     print(disjoiner(p, vertices))
    # print(sorted(disjoint_1xn(p, comb)))

# dj = disjoint_all(comb)

## Validate all resulting paths are disjoint
# for p in dj:
#     for q in dj:
#         if p != q:
#             z = disjoint_1xn(p, [q])
#             assert len(z) == 1
#             assert p in z

print("Length of paths: ", len(paths))
print("Length of vertices: ", [len(x) for x in vertices])

seen = set()
total = 0
for i, (p, c) in enumerate(zip(paths, comb)):
    print(p, c)
    dis = disjoiner(c, vertices)

    for x in dis:
        x = tuple(x)
        # print(count(x), x)
        if p[-1] == "A":
            # remove paths already seen
            if x not in seen: #dis -= seen
                total += count(x)
        seen.add(x)
print(total)


# 206016000000000 - 167409079868000 = 38606920132000
# print(([combos(p) for p in paths if p[-1] == "A"]))

# print("Part 2: ", g)
