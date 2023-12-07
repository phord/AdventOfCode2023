time = [7,  15,   30]
distance = [9,  40,  200]
time = [ 41,     96  ,   88,     94]
distance = [ 214,   1789,   1127,   1055]


time = [71530]
distance = [940200]

time = [ 41968894]
distance = [ 214178911271055]

#distance = time * speed
#x = time + speed


total = 1
for i in range(len(time)):
    t = time[i]
    d = distance[i]
    win = 0
    for s in range(1, d):
        rt = t - s
        if rt * s > d:
            win += 1
    print(win)
    total *= win

print(total)
