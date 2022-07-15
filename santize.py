import re

with open('wikipedia_compression.txt') as f:
    txt = f.read()

txt = txt.lower()

txt = re.sub(r'[^A-Za-z0-9 ]+', '', txt)

print(txt)

with open('wikipedia_compression_sanitized.txt', 'w') as f:
    f.write(txt)