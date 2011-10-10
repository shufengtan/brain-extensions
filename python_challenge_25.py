import wave
'''<html>
<head>
  <title>imagine how they sound</title>
  <link rel="stylesheet" type="text/css" href="../style.css">
</head>
<body>
<center>
<br>
<br>
<img src="lake1.jpg"> <!-- can you see the waves? -->
</body>
</html>'''

waves = []
for i in range(1, 26):
    waves.append(wave.open('lake%d.wav' % i))

ints = []
for wav in waves:
    nchannels = wav.getnchannels()
    nframes = wav.getnframes()
    sampwidth = wav.getsampwidth()
    print nchannels, nframes, sampwidth
    ints.append([ord(x) for x in wav.readframes(nframes)])

for x in ints:
    print min(x), max(x)

import Image
im = Image.new('RGB', (300, 300), 0)
for p in range(25):
    for i in range(0, 10800, 180):
        for j in range(0, 180, 3):
            r = ints[p][i+j]
            g = ints[p][i+j+1]
            b = ints[p][i+j+2]
            y = p/5*60 + i/180
            x = p%5*60 + j/3
            print (x, y), (i+j, i+j+1, i+j+2),
            im.putpixel((x, y), (r, g, b))
        print

im.save('pc25.png')
