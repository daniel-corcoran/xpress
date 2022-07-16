# xpress algorithm

The xpress algorithm uses base64 encoding chained with Huffman coding to compress files.

Description of algorithm [here](https://docs.google.com/document/d/1iS0BiSDSarbBey49KYhR_iHw1N2lZCUq3n6VcU5p98g/edit?usp=sharing).

## How-to 
### Compression
```
python3 compress.py source.file destination.file
```

### Decompression
```angular2html
python3 decompress.py source.file destination.file
```

## Benchmark results

Disclaimer: I know these results aren't that good. This was really just built for educational purposes and I wouldn't suggest anyone use it over 7Z, Bzip, etc. In some cases it is not efficient at all, but it seems to perform well on simple plain text. Although, it would be more efficient to just run a huffman coding on plain text without the base64 step, that was only added to support additional file formats.   
```
input  file:                     example files/homer_iliad.txt
output file:                     homer_iliad.txt.p
Original file size (bytes):      1161151
Compress file size (bytes):      1075403.0
Compression ratio:               1.08
Space savings:                   7.385 %
```


```
input  file:                     example files/testDocument.txt
output file:                     testDocument.txt.p
Original file size (bytes):      1801
Compress file size (bytes):      1733.625
Compression ratio:               1.04
Space savings:                   3.741 %
```

```
input  file:                     example files/smile.jpg
output file:                     smile.jpg.p
Original file size (bytes):      44734
Compress file size (bytes):      44697.125
Compression ratio:               1.0
Space savings:                   0.082 %
```

```
input  file:                     example files/wallpaper.png
output file:                     wallpaper.jpg.p
Original file size (bytes):      7899329
Compress file size (bytes):      7899447.5
Compression ratio:               1.0
Space savings:                   -0.002 %
```

```
input  file:                     example files/1kb.png
output file:                     1kb.png.p
Original file size (bytes):      1049
Compress file size (bytes):      1061.25
Compression ratio:               0.99
Space savings:                   -1.168 %
```