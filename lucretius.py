import requests
import re

url = 'http://www.gutenberg.org/dirs/7/8/785/785.txt'
text = requests.get(url).text

begin = text.index('BOOK I')
end = text.rindex('\nEnd of the Project Gutenberg')

text = text[begin:end]
lines = text.splitlines()

book = None
line_count = 0
word = {}
word_count = 0
for idx, line in enumerate(lines):
    if not re.search(r'\w', line):
        continue
    book_found = re.match(r'BOOK ([A-Z]+)', line)
    if book_found:
        book = book_found.group(1)
        continue
    line_count += 1
    for x in re.findall(r'(\S+)', line):
        for y in x.split('--'):
            w = re.sub(r'\W+$', '', re.sub(r'^\W+', '', y)).lower()
            if len(w) == 0: continue
            word_count += 1
            if w in word:
                word[w].append((book, idx))
            else:
                word[w] = [(book, idx)]
print(line_count, 'lines', word_count, 'words')
words = sorted(word.keys(), key=lambda w: (len(word[w]), word[w][0][1]))
for w in words:
    if len(word[w]) < 100:
        print(w, len(word[w]))
