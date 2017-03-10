The program consists of a lzw-module, which has the algorithm implementation,
and serialization functions required by the algorithm. Bwt-module is written
in more procedural manner with only functions, without any classes. This is
because the bwt compression has minimal state. Datastructures module has
implementations of few used data structures. Compress module has mostly IO and
CLI functionality in it.

The data structures follow the python specific data model syntax, which is done
by implementing the special \_\_getitem\_\_ etc. methods. For example:
```python
data = HashTable()
data.put(key, value)
return data.get(key)
```

We can instead use this:

```python
data = HashTable()
data[key] = value
return data[key]
```

Python is the used project language. It was picked so the project could also be
as an opportunity for using python in more concrete project. C would have been
another interesting choice, but i only know the basics, so the project could
have been too slowed down by the lack of skill.

# LZW

The Lempel-Ziv-Welch compression works by substituting byte strings with an
12-bit integer value. The values are stored in hash table during compression,
and in dynamic array during uncompression.

Files used for testing were the MIT license file, first 10% lines from [a
book](http://www.gutenberg.org/ebooks/54063), and the full book.

|                      | file A      | file B      | file C      |
| -------------------- | ----------- | ----------- | ----------- |
| file size            | 1063 B      | 42 KB       | 417 KB      |
| final dict size      | 909         | 4096        | 4096        |
| compress time        | 15 ms       | 273 ms      | 2451 ms     |
| uncompress time      | 7 ms        | 96 ms       | 930 ms      |
| compression ratio    | 1.08        | 1.92        | 1.88        |
| compressed size %    | 92.3 %      | 52.1 %      | 53.3 %      |

LZW is running in linear O(n) time. The dictionary doesn't get full on the
small file test so the compression ratio is bad.

### Improvement ideas

The dictionary key size is static 12 bits. In unix program "compress"
(compression program which uses the same LZW algorithm), the key size grows
incrementally until all possible values are used at 16-bit size. The program
could also keep track of the compression ratio during the compression, and
remake the dictionary when it keeps getting worse. This would make the
compression work better for files, which have different beginning compared to
the rest of the file.

# BWT + RLE

Burrows-Wheeler transform works by rearranging text so that similiar runs of
characters appear more often in text. RLE then compresses the string by
substituting the run length with eight bit integer.

Tested files were MIT license file, and the same file repeated four times.
Third file is system log file with lots of repetitive data.

|                      | file A      | file B      | file C     |
| -------------------- | ----------- | ----------- | ---------- |
| file size            | 1063 B      | 4252 B      | 776 KB     |
| compress time        | 9 ms        | 42 ms       | 7504 ms    |
| uncompress time      | 2 ms        | 7 ms        | 885 ms     |
| compression ratio    | 0.72        | 2.88        | 2.05       |
| compressed size %    | 138.3 %     | 34.7 %      | 48.7 %     |


BWT and RLE are also running in linear O(n) time. The compression ratio is also
below 1.0 with the smaller file, because the BWT can't form runs of same
characters long enough. RLE stores the run count as a byte so it will take more
space, when there is multiple single character runs.

### BWT decoding pseudo code: The initial version and the optimised version

ETX control character is added to the transformed text during compression.

```
inverse-bwt(s)
    T = [s1, s2,...,sn]
    for i = 0 to s.length
        A = [s.length]
        for j = 0 to s.length
            A.prepend(s[j] + T[j])
        sort T
        table = T
    return row of T which ends to ETX
```

```
inverse-bwt2(s)
    R, I = create-LF-mapping(s)
    local-index = s.index(ETX-character)
    output = [s.length]
    for i in s.length:
        output[s.length - i - 1] = s[local-index]
        local-index = R[s[local-index]] + I[local-index]
    return output
```

The first inverse bwt algorithm was running in polynomial time, as prepending
is done n<sup>2</sup> times. The second version is using LF-mapping indice
lists, so that nested for-loops are not necessary and time complexity is now
O(n).

### Improvement ideas

BWT is an algorithm which has lots of possibilites for optimisation. The start
and end markers could be eliminated, which would make the output size slightly
smaller, and the compression would work on wider variety of files. This version
assumes that the input is text, and no ETX or STX control characters appear in
the input.

# Used resources

[https://www.cs.duke.edu/csed/curious/compression/lzw.html](https://www.cs.duke.edu/csed/curious/compression/lzw.html) - very good resource, this was used a lot

[https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform)

[http://www.cs.jhu.edu/~langmea/resources/bwt_fm.pdf](http://www.cs.jhu.edu/~langmea/resources/bwt_fm.pdf) - python examples

[https://wiki.python.org/moin/BitwiseOperators](https://wiki.python.org/moin/BitwiseOperators)

[https://www.cs.helsinki.fi/u/tpkarkka/opetus/12k/dct/lecture08.pdf](https://www.cs.helsinki.fi/u/tpkarkka/opetus/12k/dct/lecture08.pdf) - counting sort tip from last page
