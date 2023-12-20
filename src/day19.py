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

# arg = (1015,3000)
# cond = "<1416"
# return (1015,1416)
def apply_single(cond, arg, neg):
    comp = cond[0]
    val = int(cond[1:])
    mn,mx = arg
    if comp == "<" and not neg:
        mx = min(mx, val)
    elif comp == ">" and neg:
        mx = min(mx, val+1)  ## <=
    elif comp == ">" and not neg:
        mn = max(mn, val+1)
    elif comp == "<" and neg:
        mn = max(mn, val)  ## >=
    else:
        print("Unknown condition", comp, " in ", cond)
        exit(1)
    if mn < mx:
        return [(mn,mx)]
    else:
        return []

# args = [(1,1000), (1015,3000), (3001,4001)]
# cond = "<1416"
# return [(1,1000), (1015,1416)]
def apply_range(cond, args, neg):
    return [x  for arg in args for x in apply_single(cond, arg, neg)]

# args = ([(1,4001)], [(1,4001)], [(1,4001)], [(1,4001)])
# cond = "x<1416"
# return ((1,1416), (1,4001), (1,4001), (1,4001))
def apply(cond, args, neg):
    i = "xmas".index(cond[0])
    new = tuple(apply_range(cond[1:], args[i], neg))
    return args[:i] + tuple((new,)) + args[i+1:]

# Find all arguments that lead to the "A" node
def solve(rules, node, args):
    work = node

    if node == "R":
        # yield args
        return None

    if node == "A":
        yield args
        return

    rule = rules[work]
    for r in rule:
        if ':' not in r:
            yield from solve(rules, r, args)
            break

        cond, target = r.split(':')
        yield from solve(rules, target, apply(cond, args, False))
        args = apply(cond, args, True)

    return

def count_intervals(i):
    return sum([mx-mn for mn,mx in i])

def count(p1):
    total = 1
    for iv in p1:
        total *= count_intervals(iv)
    return total

input = getem()

rules, _ = game(input, True)
total = 0
for args in solve(rules, "in", (((1,4001),), ((1,4001),), ((1,4001),), ((1,4001),))):
    print(count(args), args)
    total += count(args)
print(total)
exit(1)
