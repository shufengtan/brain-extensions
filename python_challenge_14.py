import Image
# Python challenge Level 14
# >>>>>>>>>>
# ^>>>>>>>>v
# ^^>>>>>>vv
# ^^^>>>>vvv
# ^^^^>>vvvv
# ^^^^<<vvvv
# ^^^<<<vvvv
# ^^<<<<<vvv
# ^<<<<<<<vv
# <<<<<<<<<v

wire = Image.open('wire.png')
W, H = wire.size
assert W == 10000
assert H == 1

im = Image.new('RGB', (100, 100))

smin, smax = (0, 99)
w = 0
while w < W:
    for x in range(smin, smax+1):
        print 1, x, smin, w
        im.putpixel((x, smin), wire.getpixel((w, 0)))
        w += 1
    for y in range(smin+1, smax+1):
        print 2, smax, y, w
        im.putpixel((smax, y), wire.getpixel((w, 0)))
        w += 1
    for x in range(smax-1, smin-1, -1):
        print 3, x, smax, w
        im.putpixel((x, smax), wire.getpixel((w, 0)))
        w += 1
    for y in range(smax-1, smin, -1):
        print 4, smin, y, w
        im.putpixel((smin, y), wire.getpixel((w, 0)))
        w += 1
    smin += 1
    smax -= 1
im.save('14.png')
