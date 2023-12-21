from itertools import product


input = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

in2 = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''


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


def getem():
    return open('src/day20.txt').read()

def dump(machine):
    for k, v in sorted(machine.items()):
        print(k, v)

def state(machine):
    return frozenset([(k,v) for k, v in machine.items()])

def decode(machine, node):
    # Decode the binary number represented by flip-flops with lsb at node
    n = 1
    total = 0
    while node:
        if machine[node][2]:
            total += n
        n *= 2
        next = [ m for m in machine[node][0] if m in machine and machine[m][1] == '%' ]
        node = next[0] if next else None
    return total

def ordering(machine):
    order = ["broadcaster"]

    # # start with the flip-flops from broadcaster
    mods = [ m for m in machine["broadcaster"][0] if machine[m][1] == '%' ]
    while mods:
        mod = mods.pop()
        if mod not in order:
            order.append(mod)
            mods.extend([ m for m in machine[mod][0] if machine[m][1] == '%' ])

    # then the conjunctions
    mods = [ m for m in machine["broadcaster"][0] if machine[m][1] == '&' ]
    while mods:
        mod = mods.pop()
        if mod not in order:
            order.append(mod)
            mods.extend([ m for m in machine[mod][0] if machine[m][1] == '&' ])

    order.extend(sorted([ m for m in machine.keys() if m not in order and machine[m][1] == '&']))

    return order


def display(machine):
    for mod in [ m for m in machine["broadcaster"][0] if machine[m][1] == '%' ]:
        print(Colors.YELLOW + mod + '=' + Colors.LIGHT_BLUE + str(decode(machine, mod)), end=' ')

    for k in ordering(machine):
        v = machine[k]
        color = Colors.RED if v[2] else Colors.GREEN
        if v[1] == '&':
            color += Colors.BOLD
        print(color + k + ' ' + Colors.END, end='')
        if v[1] == '&':
            print("(", end='')
            for mod in v[3]:
                m = machine[mod]# if mod in machine else ([], '*', None)
                color = Colors.RED if m[2] else Colors.GREEN
                if m[1] == '&':
                    color += Colors.BOLD
                print(color + mod + Colors.END + ',', end='')
            print(")  ", end='')
    print()

def diff(m1, m2):
    for k,v in m1.items():
        if k not in m2:
            print(k, v[2], "null")
        elif v[2] != m2[k][2]:
            print(k, v[2], m2[k][2])


def game(input, part1):
    g1 = input.split('\n')

    machine = {}
    for g in g1:
        module, args = g.split(' -> ')
        args = [arg.strip() for arg in args.split(',')]
        if module[0] == '%':
            module = module[1:]
            machine[module] = (args, '%', False)
        elif module[0] == '&':
            module = module[1:]
            machine[module] = (args, '&')
        else:
            machine[module] = (args, 'B', False)

    for k,v in machine.items():
        if v[1] == '&':
            inputs = {inp: False for inp,val in machine.items() if k in val[0]}
            machine[k] = (v[0], v[1], False, inputs)

    return machine

def send(machine, cmd):
    next = machine.copy()
    pulses = [0, 0]
    finished = False
    while cmd and not finished:
        output = []
        # print("="*80)
        # print(cmd)

        for sender, module, pulse in cmd:
            # print("{} -{}-> {}".format(sender, "high" if pulse else "low", module))
            # Count pulses
            if pulse:
                pulses[1] += 1
            else:
                pulses[0] += 1

            orig = machine[module] if module in machine else ([], '*', None)

            if module == "broadcaster":
                next[module] = (orig[0], orig[1], pulse)
                output.extend([(module, mod, pulse) for mod in orig[0]])
                # print("Broacaster: ", output, orig[0])

            elif orig[1] == '%':
                # flipflop
                if not pulse:
                    next[module] = (orig[0], orig[1], not orig[2])
                    output.extend([(module, mod, not orig[2]) for mod in orig[0]])

            elif orig[1] == '&':
                # conjunction
                inputs = orig[3]
                inputs[sender] = pulse
                next[module] = (orig[0], orig[1], not all(inputs.values()), inputs)
                output.extend([(module, mod, next[module][2]) for mod in orig[0]])

            elif orig[1] == '*':
                # debug
                next[module] = (orig[0], orig[1], pulse)
                if module == "rx" and not pulse:
                    finished = True

            else:
                print("Unhandled module: ", module, orig)
                exit(1)

        cmd = output
        machine = next

    return machine, pulses


def button(machine):
    cmd = [("button", "broadcaster", False)]
    return send(machine, cmd)

input = in2

input = getem()

mach = game(input, True)
dump(mach)

if False:
    low, high = (0,0)
    for _ in range(1000):
        mach, pulses = button(mach)
        low += pulses[0]
        high += pulses[1]
        # dump(mach)
        # print(" =1=> ", pulses)

    print("Low: ", low, " High: ", high)
    print("Part 1: ", low * high)

## Part 2 is was decoded visually...

# for _ in range(1000):
press = 0
while True:
    press += 1
    print(f"{press:-12}  ", end='')
    display(mach)
    mach, _ = button(mach)
