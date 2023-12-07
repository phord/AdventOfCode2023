time = [7,  15,   30]
distance = [9,  40,  200]
time = [ 41,     96  ,   88,     94]
distance = [ 214,   1789,   1127,   1055]


time = 71530
distance = 940200

time =  41968894
distance =  214178911271055

#distance = time * speed
#x = time + speed

# Binary search for the answer
# 1. Find the maximum distance
# 2. Find the minimum distance

low = 0
high = time // 2

while low < high:
    mid = (low + high) // 2

    rt = time - mid
    if rt * mid > distance:
        high = mid - 1
    else:
        low = mid + 1

    print (low,high)

a = low

low = time // 2
high = time

while low < high:
    mid = (low + high) // 2

    rt = time - mid
    if rt * mid > distance:
        low = mid + 1
    else:
        high = mid - 1

    print (low,high)

b = low

print(a, b)
print(b - a + 1)

# total = 1
# for i in range(len(time)):
#     t = time[i]
#     d = distance[i]
#     win = 0
#     for s in range(1, d):
#         rt = t - s
#         if rt * s > d:
#             win += 1
#     print(win)
#     total *= win

# print(total)
