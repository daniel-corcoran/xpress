import json
import struct
import math
import os
from bitarray import bitarray

with open('wikipedia_compression_sanitized.txt') as f:
    z = list(f.read())
#z = list("givaudan_daniel")
f_t = {}
for i in z:
    if i in f_t:
        f_t[i] += 1
    else:
        f_t[i] = 1
s_f_t = sorted(f_t.items(), key=lambda x:x[1], reverse=False)
h_l = [] # List of {freq, val} nodes which can contain nodes in the val

for i in s_f_t:
    print(i[0], i[1])
    h_l.append({"val": i[0], "freq": i[1]})

print(h_l)

k_d = {}

while(len(h_l) > 2):

    new_node = {"val": h_l[0:2], "freq": sum(i["freq"] for i in h_l[0:2])}
    print(new_node)
    h_l = h_l[2::]
    h_l.append(new_node)
    h_l = sorted(h_l, key=lambda x: x["freq"])
    print(h_l)

def assign(node, binary_value, header = ''):
    header += str(binary_value)

    print(header)
    node['binary'] = header


    if type(node['val']) == str: # If base case, assign value and return
        k_d[node['val']] = header
        return node

    else: # Else, assign value, append to header, and recursively call

        node['val'] = [
            assign(node['val'][0], 0, header),
            assign(node['val'][1], 1, header)
        ]
        return node


h_l = [assign(h_l[0], 0),
       assign(h_l[1], 1)]
print(h_l)
print(k_d)
# Compress string
c_s = ''
for x in z:
    c_s += k_d[x] + ''

total_len_hashtable = len(k_d)

hashtable_organized_by_length = {}
for x in k_d:
    if len(k_d[x]) in hashtable_organized_by_length:
        hashtable_organized_by_length[len(k_d[x])].append({'char': x,
                                                       'bin': k_d[x]})
    else:
        hashtable_organized_by_length[len(k_d[x])] = [{'char': x,
                                                       'bin': k_d[x]}]





buf = format(total_len_hashtable, '06b') # Cast total length of hash table to 6 binary bits

for i in hashtable_organized_by_length:
    buf +=  format(i, '04b') # Append length of hash
    buf += format(len(hashtable_organized_by_length[i]), '06b') # Append num hashes in table
    for c in hashtable_organized_by_length[i]:
        print(c)
        # Get byte of char
        bytes = bytearray(c['char'], 'utf8')
        bytes = [bin(z) for z in bytes][0][2:].zfill(8)
        print('~', c['char'], bytes )
        buf +=  bytes # Append original character utf-8
        buf += c['bin'] # Append hash value


print(buf)


print(c_s)
buf+=c_s
print(len(buf) / 8)
print(buf)
a = bitarray(buf)
with open('compressed.p', 'wb') as f:
    a.tofile(f)


