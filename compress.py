import json
import struct
import math
import os
from bitarray import bitarray
import base64
import sys

def compress(src, dst, debug=False):
    with open(src, 'rb') as f: # Load file into memory as base64 encode in UTF-8
        b_d = f.read()
        b64_enc = base64.b64encode(b_d)
        z = list(b64_enc.decode('utf-8'))
    if debug:
        if len(z) > 100:
            print("encoding message [", ''.join(z[:100]), "... (reduced for brevity)]")
        else:
            print("encoding message [", ''.join(z), "]")

    size_encoding = len(z)
    z = [i for i in z if i != '=']  # Remove = since they are padding - we will re-introduce them afterwards
    # Build frequency table of UTF-8 characters
    f_t = {}
    for i in z:
        if i in f_t:
            f_t[i] += 1
        else:
            f_t[i] = 1
    s_f_t = sorted(f_t.items(), key=lambda x:x[1], reverse=False)
    h_l = [] # List of {freq, val} nodes which can contain nodes in the val
    for i in s_f_t:
        h_l.append({"val": i[0], "freq": i[1]})

    if debug:
        print("[~~~freqtable constructed~~~]")
        for i in h_l:
            print(i['val'], '\t', i['freq'])
        print()

    k_d = {} # Hash table that will be built when assigning nodes in the binary tree
    while(len(h_l) > 2):

        new_node = {"val": h_l[0:2], "freq": sum(i["freq"] for i in h_l[0:2])}
        h_l = h_l[2::]
        h_l.append(new_node)
        h_l = sorted(h_l, key=lambda x: x["freq"])

    def assign(node, binary_value, header = ''):
        header += str(binary_value)
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

    # Compress string
    c_s = ''
    for x in z:
        c_s += k_d[x] + ''

    total_len_hashtable = len(k_d)

    if debug:
        print("[~~~Hashtable constructed~~~]")
        for i in k_d:
            print(i, '\t', k_d[i])
        print()

    hashtable_organized_by_length = {}
    for x in k_d:
        if len(k_d[x]) in hashtable_organized_by_length:
            hashtable_organized_by_length[len(k_d[x])].append({'char': x,
                                                           'bin': k_d[x]})
        else:
            hashtable_organized_by_length[len(k_d[x])] = [{'char': x,
                                                           'bin': k_d[x]}]

    print("[~~Writing to buffer~~]")

    buf = format(size_encoding, '032b') # Total number of b64 symbols that arre encoded
    if debug:
        print("1] encoding size: \t", size_encoding, '\t', format(size_encoding, '032b'))
    buf += format(total_len_hashtable, '07b') # Cast total length of hash table to 6 binary bits
    if debug:
        print("2] hashtable size: \t", total_len_hashtable, '\t', format(total_len_hashtable, '07b'))

    for i in hashtable_organized_by_length:
        buf +=  format(i, '04b') # Append length of hash
        if debug:
            print("\n3a] hash block size: \t", i, '\t', format(i, '04b'))

        buf += format(len(hashtable_organized_by_length[i]), '06b') # Append num hashes in table
        if debug:
            print("3b] no. hashes in block:",len(hashtable_organized_by_length[i]), '\t',format(len(hashtable_organized_by_length[i]), '06b'))

        for c in hashtable_organized_by_length[i]:
            #print(c)
            # Get byte of char
            cbytes = bytearray(c['char'], 'utf8')
            cbytes = [bin(z) for z in cbytes][0][2:].zfill(8)
            #print('~', c['char'], cbytes)
            buf += cbytes # Append original character utf-8
            buf += c['bin'] # Append hash value
            if debug:
                print('\t[~~~hb~~~]')
                print("\t3c] utf-8\t", c['char'], '\t', cbytes)
                print("\t3c] hash\t", c['bin'])



    buf+=c_s


    a = bitarray(buf)
    with open(dst, 'wb') as f:
        a.tofile(f)

    og_file_size = os.path.getsize(src)
    c_file_size = len(buf) / 8

    print("\n\n----------File has been compressed-----------------------------------------------")
    print("input  file:                \t", src)
    print("output file:                \t", dst)
    print("Original file size (bytes): \t", og_file_size)
    print("Compress file size (bytes): \t", c_file_size)
    print("Compression ratio:          \t", round(og_file_size / c_file_size, 2))
    print("Space savings:          \t", round(100 * (og_file_size  - c_file_size )/ og_file_size, 3), "%")


if __name__ == "__main__":
    print(sys.argv)
    i = sys.argv[1]
    o = sys.argv[2]
    assert os.path.exists(i) # Check if input file exists.
    #assert os.path.exists(o) # Check if output file exists.
    compress(i, o, debug=True)