import Image

I = Image.open('maze.png')
W, H = I.size
P = []
for x in range(W):
    P.append([I.getpixel((x,y)) for y in range(H)])

s = [set() for i in range(3)]
for x in range(W):
    for y in range(H):
        if x < 65 and y < 65: continue
        s[0].add(P[x][y][0])
        s[1].add(P[x][y][1:3])
        s[2].add(P[x][y][3])

print [len(si) for si in s]

def around(x_y):
    x, y = x_y
    nb = ((x+1, y), (x, y-1), (x, y+1), (x-1, y))
    return [p for p in nb if p[0] >= 0 and p[1] >= 0 and p[0] < W and p[1] < H and P[p[0]][p[1]] != (255,255,255,255)]

# top entry point
point_A, = [(x, 0) for x in range(60, W) if P[x][0] != (255,255,255,255)]
# bottom exit point
point_Z, = [(x, H-1) for x in range(W) if P[x][H-1] != (255,255,255,255)]
# remember dead ends
dead_ends = set()
alt = {}
def walk(seq):
    point = seq[-1]
    if point == point_Z:
        print 'We made it!'
        return seq
    if point in dead_ends:
        seq.pop()
        return walk(seq)
    next_points = [p for p in around(point) if p not in seq and p not in dead_ends]
    #print point, next_points
    if next_points:
        seq.append(next_points.pop())
        alt[seq[-1]] = next_points
        print 'Try alt', seq[-1]
        return walk(seq)
    else:
        dead_ends.add(seq.pop())
        print 'Backtracked to', seq[-1]
        return walk(seq)

seq = [point_A]
while True:
    try:
        seq = walk(seq)
    except:
        print 'Restart...', len(seq)
        continue
    break

# zip file hidden as red values in seq
fh = open('pc24.zip', 'w')
for i in range(1, len(seq), 2):
    xy = seq[i]
    r = P[xy[0]][xy[1]][0]
    fh.write(chr(r))
fh.close()
