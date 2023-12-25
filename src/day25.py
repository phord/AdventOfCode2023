input='''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''

def parse(input):
    for line in input.split('\n'):
        l,r = line.split(': ')
        r = r.split(' ')
        for x in r:
            yield (l,x)

def neighbors(graph, cut, node):
    for tup in graph:
        if node in tup:
            if tup not in cut and tuple(reversed(tup)) not in cut:
                yield [ n for n in tup if n != node ][0]

# traverse graph from start to every other node
def traverse(graph, cut):
    visited = set()
    start = list(graph)[0][0]

    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend([x for x in neighbors(graph, cut, node) if x not in visited])
    return visited

def shortest_path(graph, cut, start, end):
    visited = set()
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for n in neighbors(graph, cut, node):
                new_path = list(path)
                new_path.append(n)
                queue.append(new_path)

import sys
if len(sys.argv) > 1:
    input = open(sys.argv[1]).read()
graph = set(parse(input))
nodes = set([n[0] for n in graph]) | set([n[1] for n in graph])

def find_wires(graph, cut, start, end, common = set()):
    path = shortest_path(graph, cut, start, end)
    if path is None:
        assert len(cut) == 3
        return cut
    elif len(cut) == 3:
        # Wrong three wires
        return None
    edges = set(zip(path, path[1:]))
    for edge in edges:
        if edge in common:
            continue
        found = find_wires(graph, cut | set([edge]), start, end, common | edges)
        if found is not None:
            return found
    return None

import itertools
for start, end in itertools.combinations(nodes, 2):
    cut = find_wires(graph, set(), start, end)
    if cut is not None:
        seen = traverse(graph, cut)
        a,b = (len(seen), len(nodes)-len(seen))
        print(f"{a} * {b} = {a*b}")
        break
